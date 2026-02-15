#!/usr/bin/env python3
"""
Uploader Module for Ghostcore Evidence OS
"""

import zipfile
import os

class Uploader:
    def pack(self, files, zip_path):
        os.makedirs(os.path.dirname(zip_path), exist_ok=True)
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for file_path in files:
                if os.path.exists(file_path):
                    zipf.write(file_path, os.path.basename(file_path))
        return zip_path
