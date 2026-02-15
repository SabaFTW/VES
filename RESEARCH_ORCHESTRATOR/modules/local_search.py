"""
Local Search Module - Fast file system search using ripgrep

Features:
- Multi-file type search
- Context extraction
- Directory scanning
- File content preview
- Proper error handling
"""

import subprocess
import json
import os
from pathlib import Path
from typing import List, Dict, Any, Optional
import logging
import tempfile

logger = logging.getLogger(__name__)

class LocalSearchError(Exception):
    """Custom exception for local search errors"""
    pass

class LocalSearch:
    """
    Local file search using ripgrep (rg) for fast text searching
    """
    
    def __init__(self, root_path: str = "/home/saba", default_extensions: Optional[List[str]] = None):
        self.root_path = Path(root_path).expanduser()
        self.default_extensions = default_extensions or ['txt', 'md', 'py', 'json', 'pdf', 'doc', 'docx', 'csv', 'xml']
        self._validate_dependencies()
        self._validate_root_path()
    
    def _validate_dependencies(self):
        """Check if required tools are available"""
        try:
            result = subprocess.run(['rg', '--version'], capture_output=True, text=True, timeout=5)
            if result.returncode != 0:
                raise LocalSearchError("ripgrep (rg) not found. Please install with: sudo apt install ripgrep")
        except FileNotFoundError:
            raise LocalSearchError("ripgrep (rg) not found. Please install with: sudo apt install riprep")
        except subprocess.TimeoutExpired:
            raise LocalSearchError("Timeout while checking ripgrep. Installation may be corrupted.")
    
    def _validate_root_path(self):
        """Validate that the root path exists and is accessible"""
        if not self.root_path.exists():
            raise LocalSearchError(f"Root path does not exist: {self.root_path}")
        
        if not self.root_path.is_dir():
            raise LocalSearchError(f"Root path is not a directory: {self.root_path}")
        
        # Test if we can list the directory
        try:
            next(self.root_path.iterdir())  # Just test if we can iterate
        except PermissionError:
            raise LocalSearchError(f"Permission denied accessing root path: {self.root_path}")
        except StopIteration:
            # Empty directory, which is OK
            pass
    
    def search(self, terms: List[str], file_extensions: Optional[List[str]] = None, max_results: int = 100) -> List[Dict[str, Any]]:
        """
        Search for terms in local files using ripgrep with proper error handling
        """
        if file_extensions is None:
            file_extensions = self.default_extensions
        
        # Validate inputs
        if not terms:
            raise LocalSearchError("No search terms provided")
        
        # Validate terms and extensions
        validated_terms = [str(term) for term in terms if str(term).strip()]
        if not validated_terms:
            raise LocalSearchError("No valid search terms provided")
        
        if not file_extensions:
            raise LocalSearchError("No file extensions provided")
        
        validated_extensions = [ext for ext in file_extensions if str(ext).strip()]
        if not validated_extensions:
            raise LocalSearchError("No valid file extensions provided")
        
        all_results = []
        
        for term in validated_terms:
            try:
                # Sanitize term to prevent command injection
                if not self._is_safe_term(term):
                    logger.warning(f"Unsafe search term skipped: {term}")
                    continue
                
                # Build the rg command with JSON output for better parsing
                cmd = ["rg", "-F", "-n", "--json", "--color=never"]
                
                # Add file extension filters
                for ext in validated_extensions:
                    clean_ext = ext.replace('.', '').strip()
                    if clean_ext:  # Only add if not empty after cleaning
                        cmd.extend(["-g", f"*.{clean_ext}"])
                
                cmd.append(term)
                cmd.append(str(self.root_path))
                
                # Execute search with timeout
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
                
                if result.returncode == 0 and result.stdout:
                    lines = result.stdout.strip().split('\n')
                    for line in lines:
                        if line.strip():
                            try:
                                data = json.loads(line)
                                if data.get('type') == 'match':
                                    # Validate file path is within root directory
                                    file_path = data['data']['path']['text']
                                    try:
                                        resolved_path = Path(file_path).resolve()
                                        root_resolved = self.root_path.resolve()
                                        if not resolved_path.is_relative_to(root_resolved):
                                            logger.warning(f"File path outside root directory: {file_path}")
                                            continue
                                    except ValueError:
                                        # Paths are on different drives (Windows), skip
                                        continue
                                    
                                    all_results.append({
                                        'file_path': file_path,
                                        'line_number': data['data']['line_number'],
                                        'content': data['data']['lines']['text'].strip(),
                                        'term': term,
                                        'relative_path': str(Path(file_path).relative_to(self.root_path)),
                                        'type': 'local'
                                    })
                                    
                                    # Limit results to prevent overflow
                                    if len(all_results) >= max_results:
                                        break
                            except json.JSONDecodeError:
                                # Skip invalid JSON lines
                                continue
                            except KeyError:
                                # Skip incomplete JSON data
                                continue
                                
                    # Limit results per term
                    if len(all_results) >= max_results:
                        break
                elif result.returncode == 1:
                    # No matches found, continue to next term
                    continue
                else:
                    # Error occurred
                    logger.error(f"Error searching for term '{term}': {result.stderr}")
            except subprocess.TimeoutExpired:
                logger.warning(f"Search for term '{term}' timed out")
                continue
            except Exception as e:
                logger.error(f"Unexpected error searching for term '{term}': {str(e)}")
                continue
        
        return all_results
    
    def _is_safe_term(self, term: str) -> bool:
        """
        Check if the search term is safe to use in a command (basic injection prevention)
        """
        unsafe_chars = [';', '&', '|', '`', '$', '>', '<', '(', ')', '{', '}']
        return not any(char in term for char in unsafe_chars)
    
    def search_with_context(self, terms: List[str], context_lines: int = 2, file_extensions: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """
        Search with additional context lines around matches
        """
        if file_extensions is None:
            file_extensions = self.default_extensions
        
        # Validate inputs
        if not terms:
            raise LocalSearchError("No search terms provided")
        
        validated_terms = [str(term) for term in terms if str(term).strip()]
        if not validated_terms:
            raise LocalSearchError("No valid search terms provided")
        
        validated_extensions = [ext for ext in file_extensions if str(ext).strip()]
        if not validated_extensions:
            raise LocalSearchError("No valid file extensions provided")
        
        all_results = []
        
        for term in validated_terms:
            try:
                if not self._is_safe_term(term):
                    logger.warning(f"Unsafe context search term skipped: {term}")
                    continue
                
                # Build command with context, limiting context lines to prevent overflow
                context_lines = max(0, min(10, int(context_lines)))  # Clamp between 0 and 10
                
                cmd = ["rg", "-F", "-C", str(context_lines), "--json", "--color=never"]
                
                for ext in validated_extensions:
                    clean_ext = ext.replace('.', '').strip()
                    if clean_ext:
                        cmd.extend(["-g", f"*.{clean_ext}"])
                
                cmd.append(term)
                cmd.append(str(self.root_path))
                
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
                
                if result.returncode == 0 and result.stdout:
                    lines = result.stdout.strip().split('\n')
                    for line in lines:
                        if line.strip():
                            try:
                                data = json.loads(line)
                                result_type = data.get('type')
                                if result_type in ['context', 'match']:
                                    file_path = data['data']['path']['text']
                                    try:
                                        resolved_path = Path(file_path).resolve()
                                        root_resolved = self.root_path.resolve()
                                        if not resolved_path.is_relative_to(root_resolved):
                                            logger.warning(f"File path outside root directory: {file_path}")
                                            continue
                                    except ValueError:
                                        continue
                                    
                                    all_results.append({
                                        'file_path': file_path,
                                        'line_number': data['data']['line_number'],
                                        'content': data['data']['lines']['text'].strip(),
                                        'term': term,
                                        'relative_path': str(Path(file_path).relative_to(self.root_path)),
                                        'type': result_type
                                    })
                            except json.JSONDecodeError:
                                continue
                            except KeyError:
                                continue
            except subprocess.TimeoutExpired:
                logger.warning(f"Context search for term '{term}' timed out")
                continue
            except Exception as e:
                logger.error(f"Error in context search for term '{term}': {str(e)}")
                continue
        
        return all_results
    
    def scan_directory_structure(self, path: Optional[str] = None, max_depth: int = 3) -> Dict[str, Any]:
        """
        Scan directory structure to understand the file organization
        """
        scan_path = Path(path) if path else self.root_path
        
        # Validate path exists and is safe
        try:
            resolved_path = scan_path.resolve()
            root_resolved = self.root_path.resolve()
            if not resolved_path.is_relative_to(root_resolved):
                raise LocalSearchError(f"Scan path outside root directory: {scan_path}")
        except ValueError:
            raise LocalSearchError(f"Invalid scan path: {scan_path}")
        
        if not scan_path.exists():
            raise LocalSearchError(f"Scan path does not exist: {scan_path}")
        
        if not scan_path.is_dir():
            raise LocalSearchError(f"Scan path is not a directory: {scan_path}")
        
        result = {
            'path': str(scan_path),
            'directories': [],
            'files': [],
            'subdirs': {}
        }
        
        try:
            # Limit the number of items to prevent excessive scanning
            items = list(scan_path.iterdir())
            if len(items) > 1000:  # Arbitrary limit to prevent very large directories
                logger.warning(f"Directory {scan_path} has {len(items)} items, processing first 1000")
                items = items[:1000]
            
            for item in items:
                if item.is_dir():
                    result['directories'].append(item.name)
                    if max_depth > 0:
                        try:
                            result['subdirs'][item.name] = self.scan_directory_structure(item, max_depth - 1)
                        except PermissionError:
                            logger.warning(f"Permission denied accessing directory: {item}")
                            continue
                elif item.is_file():
                    result['files'].append(item.name)
        except PermissionError:
            logger.warning(f"Permission denied accessing directory: {scan_path}")
        except OSError as e:
            logger.error(f"OS error scanning directory {scan_path}: {e}")
        
        return result
    
    def get_file_preview(self, file_path: str, lines: int = 10) -> str:
        """
        Get a preview of file content (first N lines)
        """
        try:
            path = Path(file_path)
            
            # Validate path is within root directory
            resolved_path = path.resolve()
            root_resolved = self.root_path.resolve()
            if not resolved_path.is_relative_to(root_resolved):
                raise LocalSearchError(f"File path outside root directory: {file_path}")
            
            if not path.exists():
                raise LocalSearchError(f"File does not exist: {file_path}")
            
            if not path.is_file():
                raise LocalSearchError(f"Path is not a file: {file_path}")
            
            # Limit file size to prevent loading huge files
            file_size = path.stat().st_size
            if file_size > 10 * 1024 * 1024:  # 10MB limit
                raise LocalSearchError(f"File too large to preview ({file_size} bytes): {file_path}")
            
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                content_lines = []
                for i, line in enumerate(f):
                    if i >= lines:
                        break
                    content_lines.append(line)
                
            return ''.join(content_lines).strip()
        except UnicodeDecodeError:
            logger.warning(f"Could not decode file as text: {file_path}")
            return ""
        except Exception as e:
            logger.error(f"Error reading file preview for {file_path}: {str(e)}")
            return ""
    
    def get_file_info(self, file_path: str) -> Dict[str, Any]:
        """
        Get detailed info about a file
        """
        try:
            path = Path(file_path)
            
            # Validate path is within root directory
            resolved_path = path.resolve()
            root_resolved = self.root_path.resolve()
            if not resolved_path.is_relative_to(root_resolved):
                raise LocalSearchError(f"File path outside root directory: {file_path}")
            
            if not path.exists():
                raise LocalSearchError(f"File does not exist: {file_path}")
            
            stat = path.stat()
            return {
                'size_bytes': stat.st_size,
                'modified': stat.st_mtime,
                'created': stat.st_ctime,
                'path': str(path),
                'name': path.name,
                'extension': path.suffix,
                'relative_path': str(path.relative_to(self.root_path))
            }
        except Exception as e:
            logger.error(f"Error getting file info for {file_path}: {str(e)}")
            return {}
    
    def search_by_size(self, min_size: int = 0, max_size: int = 100000000) -> List[Dict[str, Any]]:
        """
        Search for files within size range (in bytes)
        """
        if min_size < 0 or max_size < 0:
            raise LocalSearchError("File sizes must be non-negative")
        
        if min_size > max_size:
            raise LocalSearchError("min_size cannot be greater than max_size")
        
        results = []
        files_processed = 0
        max_files = 10000  # Limit to prevent extremely long processing
        
        try:
            for root, dirs, files in os.walk(self.root_path):
                # Limit recursion depth if needed
                for file in files:
                    if files_processed >= max_files:
                        logger.warning(f"Stopped processing at {max_files} files to prevent long execution")
                        break
                    
                    filepath = Path(root) / file
                    try:
                        # Validate path is within root directory
                        resolved_path = filepath.resolve()
                        root_resolved = self.root_path.resolve()
                        if not resolved_path.is_relative_to(root_resolved):
                            continue  # Skip files outside root for security
                        
                        stat = filepath.stat()
                        if min_size <= stat.st_size <= max_size:
                            results.append(self.get_file_info(str(filepath)))
                        
                        files_processed += 1
                        if files_processed >= max_files:
                            break
                    except (PermissionError, OSError):
                        # Skip files we can't access
                        continue
                        
                if files_processed >= max_files:
                    break
        except Exception as e:
            logger.error(f"Error in search_by_size: {str(e)}")
        
        return results

# Example usage:
# search = LocalSearch("/home/saba/VES")
# results = search.search(["research", "AI"], file_extensions=["md", "txt"])