#!/usr/bin/env python3
"""
File Integrity Verifier for PALANTIR_CODEX_v2.0_DUAL_MODE
Checks SHA256 checksums and verifies archive integrity
"""

import hashlib
import os
import json
from pathlib import Path

def calculate_sha256(file_path):
    """Calculate SHA256 checksum of a file"""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def verify_archive_integrity(archive_root):
    """Verify the integrity of the entire archive"""
    root_path = Path(archive_root)
    checksum_file = root_path / "METADATA" / "INTEGRITY_CHECKS" / "SHA256_CHECKSUMS.txt"
    
    if not checksum_file.exists():
        print("ERROR: Checksum file not found!")
        return False
        
    with open(checksum_file, 'r') as f:
        expected_checksums = {}
        for line in f:
            if line.strip():
                parts = line.split()
                if len(parts) >= 2:
                    expected_checksums[parts[1]] = parts[0]
    
    verified_files = 0
    failed_files = []
    
    for file_path in root_path.rglob('*'):
        if file_path.is_file():
            relative_path = str(file_path.relative_to(root_path))
            if relative_path in expected_checksums:
                actual_checksum = calculate_sha256(file_path)
                expected_checksum = expected_checksums[relative_path]
                
                if actual_checksum == expected_checksum:
                    print(f"✓ {relative_path}")
                    verified_files += 1
                else:
                    print(f"✗ {relative_path} - CHECKSUM MISMATCH!")
                    failed_files.append(relative_path)
    
    print(f"\nVerification complete: {verified_files} files verified, {len(failed_files)} failed")
    return len(failed_files) == 0

def generate_checksums(archive_root):
    """Generate SHA256 checksums for all files in the archive"""
    root_path = Path(archive_root)
    checksums = []
    
    for file_path in root_path.rglob('*'):
        if file_path.is_file():
            relative_path = str(file_path.relative_to(root_path))
            checksum = calculate_sha256(file_path)
            checksums.append(f"{checksum}  {relative_path}")
    
    checksum_file = root_path / "METADATA" / "INTEGRITY_CHECKS" / "SHA256_CHECKSUMS.txt"
    with open(checksum_file, 'w') as f:
        f.write('\n'.join(checksums))
        
    print(f"Generated checksums for {len(checksums)} files")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage: python file_verifier.py [verify|generate] [archive_path]")
        sys.exit(1)
        
    command = sys.argv[1]
    archive_path = sys.argv[2]
    
    if command == "verify":
        success = verify_archive_integrity(archive_path)
        sys.exit(0 if success else 1)
    elif command == "generate":
        generate_checksums(archive_path)
    else:
        print("Invalid command. Use 'verify' or 'generate'")
        sys.exit(1)