#!/usr/bin/env python3
"""
Directory Scanner for /home/saba
Scans specified directories and generates JSON metadata
"""

import os
import json
from datetime import datetime
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

class DirectoryScanner:
    def __init__(self):
        self.scan_results = []
        self.total_files = 0
        self.total_dirs = 0
        self.scanned_items = 0
        self.lock = threading.Lock()  # For thread-safe operations

        # Paths to scan - removed /home/saba root to avoid system folders
        self.paths_to_scan = [
            '/home/saba/VES',
            '/home/saba/Desktop',
            '/home/saba/cloud_constellation'
        ]

        # Patterns to ignore
        self.ignore_patterns = {
            'node_modules',
            '.git',
            '.venv',
            '__pycache__',
            '.cache',
            '.local',
            '.npm'
        }

        self.ignore_extensions = {'.pyc', '.log'}

    def should_ignore(self, path):
        """Check if a path should be ignored based on patterns"""
        path_parts = Path(path).parts
        for part in path_parts:
            if part in self.ignore_patterns:
                return True

        # Check if it's a file with ignored extension
        if os.path.isfile(path):
            _, ext = os.path.splitext(path)
            if ext in self.ignore_extensions:
                # Special case: allow .log files in key directories
                path_parts = Path(path).parts
                if len(path_parts) <= 3:  # Top level directories
                    return False
                return True

        # Additional system folders to ignore - these should be ignored throughout the scan
        system_folders = {'.bash_history', '.bash_logout', '.bash_profile', '.bashrc',
                         '.git', '.gitconfig', '.gitignore', '.profile', '.python_history',
                         '.cache', '.local', '.npm', '.ssh', '.config', '.Xauthority',
                         '.Xresources', '.bashrc.backup_20251123_001952', '.claude.json',
                         '.claude.json.backup', '.git-credentials', '.gtkrc-2.0', '.nanorc',
                         '.nvidia-settings-rc', '.nvidia-settings-rc.bak', '.orion-codex.log',
                         '.orionrc', '.sqlite_history', '.ves_cosmos_ultimate_config.json',
                         'Documents', 'Videos', 'Photos', 'Music', 'Templates', 'Public'}

        # If this is a system folder, ignore it
        if os.path.basename(path) in system_folders:
            return True

        return False
    
    def get_file_type(self, file_path):
        """Get the file extension without the dot"""
        _, ext = os.path.splitext(file_path)
        if ext.startswith('.'):
            return ext[1:]  # Remove the leading dot
        return ext
    
    def contains_key_files(self, directory):
        """Check if directory contains key files like README, config files, etc."""
        contents = os.listdir(directory)
        has_readme = False
        has_config = False
        
        for item in contents:
            item_lower = item.lower()
            if item_lower.startswith('readme'):
                has_readme = True
            if any(cfg in item_lower for cfg in ['config', 'settings', 'setup', '.env', 'requirements', 'package.json', 'pyproject.toml']):
                has_config = True
        
        return has_readme, has_config
    
    def scan_directory(self, root_path, depth=0):
        """Scan a directory and collect metadata"""
        try:
            # Calculate depth level from base scan directories
            base_depth = len(root_path.split(os.sep))
            for dirpath, dirnames, filenames in os.walk(root_path, followlinks=False):
                # Update total directories count in a thread-safe way
                with self.lock:
                    self.total_dirs += len(dirnames)

                # Check if any subdirectory should be ignored
                dirnames[:] = [d for d in dirnames if not self.should_ignore(os.path.join(dirpath, d))]

                # Calculate current depth level
                current_depth = len(dirpath.split(os.sep)) - base_depth

                # Process files in current directory
                project_files = []
                file_types = set()

                for filename in filenames:
                    file_path = os.path.join(dirpath, filename)

                    if not self.should_ignore(file_path):
                        # Update counters in a thread-safe way
                        with self.lock:
                            self.total_files += 1
                            self.scanned_items += 1

                        # Add to progress reporting
                        if self.scanned_items % 5000 == 0:
                            print(f"Progress: Scanned {self.scanned_items} items...")

                        # Skip binary files for content analysis
                        try:
                            # Try to read the first part of the file to check if it's binary
                            with open(file_path, 'rb') as test_file:
                                chunk = test_file.read(1024)
                                if b'\x00' not in chunk:  # Simple check for binary files
                                    project_files.append(filename)
                        except:
                            # If we can't read the file, skip it
                            pass

                        # Collect file types
                        file_ext = self.get_file_type(filename)
                        if file_ext:
                            file_types.add(file_ext)

                # Get directory metadata
                try:
                    stat_info = os.stat(dirpath)
                    # Calculate size for files that are not ignored
                    size_bytes = 0
                    for f in os.listdir(dirpath):
                        file_path = os.path.join(dirpath, f)
                        if os.path.isfile(file_path) and not self.should_ignore(file_path):
                            try:
                                size_bytes += os.path.getsize(file_path)
                            except:
                                pass  # Skip files we can't access
                    size_kb = size_bytes // 1024
                    mod_time = datetime.fromtimestamp(stat_info.st_mtime).isoformat()
                except:
                    size_kb = 0
                    mod_time = ""

                # Check for key files
                has_readme, has_config = self.contains_key_files(dirpath)

                # Create project data
                project_data = {
                    "path": dirpath,
                    "name": os.path.basename(dirpath),
                    "type": "directory",
                    "size_kb": size_kb,
                    "last_modified": mod_time,
                    "contains": project_files[:20],  # Limit to first 20 files to avoid huge arrays
                    "has_readme": has_readme,
                    "has_config": has_config,
                    "file_types": list(file_types),
                    "depth_level": current_depth
                }

                # Add to results in a thread-safe way
                with self.lock:
                    self.scan_results.append(project_data)

        except PermissionError:
            print(f"Permission denied: {root_path}")
        except Exception as e:
            print(f"Error scanning {root_path}: {str(e)}")
    
    def run_scan(self):
        """Run the directory scan using parallel processing"""
        print("Starting directory scan...")

        # Filter paths that exist
        existing_paths = [path for path in self.paths_to_scan if os.path.exists(path)]

        # Use ThreadPoolExecutor for parallel scanning
        with ThreadPoolExecutor(max_workers=4) as executor:
            # Submit scan jobs for each path
            futures = {executor.submit(self.scan_directory, path): path for path in existing_paths}

            # Wait for all tasks to complete
            for future in as_completed(futures):
                path = futures[future]
                try:
                    future.result()  # This will raise any exceptions from the thread
                    print(f"Completed scanning: {path}")
                except Exception as e:
                    print(f"Error scanning {path}: {str(e)}")

        # Generate final output
        output = {
            "scan_timestamp": datetime.now().isoformat(),
            "total_files": self.total_files,
            "total_dirs": self.total_dirs,
            "projects": self.scan_results
        }

        # Create output directory if it doesn't exist
        output_dir = "/home/saba/MASTER_NAVIGATOR"
        os.makedirs(output_dir, exist_ok=True)

        # Save to JSON file
        output_path = os.path.join(output_dir, "raw_scan_data.json")
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2)

        print(f"Scan complete! Found {self.total_files} files and {self.total_dirs} directories.")
        print(f"Results saved to: {output_path}")

        return output_path

if __name__ == "__main__":
    scanner = DirectoryScanner()
    output_path = scanner.run_scan()