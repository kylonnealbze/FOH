#!/usr/bin/env python3
"""
FOH Data Transfer Tool
Helps organize and transfer data from USB drives to the FOH Data structure
"""

import os
import shutil
from pathlib import Path
from datetime import datetime

# Configuration
NAS_BASE_PATH = "/volume1/FOH Data/MPAS"  # Update to your NAS mount point
USB_SOURCE_PATH = "/path/to/usb/drive"     # Update to your USB mount point

def list_files_recursive(source_path):
    """List all files in source directory recursively"""
    source = Path(source_path)
    files = []
    
    for item in source.rglob('*'):
        if item.is_file():
            files.append(item)
    
    return files

def infer_destination(file_path, nas_base):
    """
    Attempt to infer the correct destination based on file name/path
    Returns suggested destination path or None
    """
    file_name = file_path.name.lower()
    parent_dir = file_path.parent.name.lower()
    
    # Example inference logic - customize based on your file naming conventions
    area = None
    site = None
    data_type = None
    year = None
    
    # Try to extract year from filename or path
    for y in range(2020, 2027):
        if str(y) in str(file_path):
            year = str(y)
            break
    
    # Infer data type from keywords
    if any(keyword in file_name for keyword in ['temp', 'temperature']):
        data_type = "Temperature Data"
    elif any(keyword in file_name for keyword in ['growth', 'coral']):
        data_type = "Growth Data"
    elif any(keyword in file_name for keyword in ['water', 'quality', 'wq']):
        data_type = "Water Quality Data"
    elif any(keyword in file_name for keyword in ['survey']):
        data_type = "Survey Data"
    elif file_path.suffix.lower() in ['.jpg', '.jpeg', '.png', '.raw']:
        data_type = "Photos"
    elif file_path.suffix.lower() in ['.mp4', '.mov', '.avi']:
        data_type = "Videos"
    elif file_path.suffix.lower() in ['.pdf', '.doc', '.docx']:
        data_type = "Reports"
    
    # Try to infer site from path or filename
    if 'salt' in str(file_path).lower() or 'swc' in str(file_path).lower():
        area = "Inner Cayes"
        site = "Salt Water Caye"
    
    # Build destination path if we have enough info
    if area and site and data_type:
        dest = Path(nas_base) / area / site / data_type
        if year and data_type in ["Temperature Data", "Growth Data", "Water Quality Data", "Survey Data"]:
            dest = dest / year
        return dest
    
    return None

def transfer_file(source_file, destination_dir, mode='copy'):
    """
    Transfer a file to destination
    
    Args:
        source_file: Source file path
        destination_dir: Destination directory
        mode: 'copy' or 'move'
    """
    dest_dir = Path(destination_dir)
    dest_dir.mkdir(parents=True, exist_ok=True)
    
    dest_file = dest_dir / source_file.name
    
    # Handle filename conflicts
    if dest_file.exists():
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        stem = dest_file.stem
        suffix = dest_file.suffix
        dest_file = dest_dir / f"{stem}_{timestamp}{suffix}"
    
    if mode == 'copy':
        shutil.copy2(source_file, dest_file)
        print(f"✓ Copied: {source_file.name} -> {dest_file}")
    elif mode == 'move':
        shutil.move(str(source_file), str(dest_file))
        print(f"✓ Moved: {source_file.name} -> {dest_file}")
    
    return dest_file

def interactive_transfer():
    """Interactive mode for transferring files"""
    print("=" * 60)
    print("FOH Data Transfer Tool")
    print("=" * 60)
    
    source = input(f"\nSource path [{USB_SOURCE_PATH}]: ").strip() or USB_SOURCE_PATH
    
    if not Path(source).exists():
        print(f"Error: Source path does not exist: {source}")
        return
    
    files = list_files_recursive(source)
    print(f"\nFound {len(files)} files to process\n")
    
    mode = input("Transfer mode - (c)opy or (m)ove? [c]: ").strip().lower() or 'c'
    transfer_mode = 'copy' if mode == 'c' else 'move'
    
    transferred = 0
    skipped = 0
    
    for file_path in files:
        print(f"\n{'=' * 60}")
        print(f"File: {file_path.relative_to(source)}")
        
        suggested_dest = infer_destination(file_path, NAS_BASE_PATH)
        
        if suggested_dest:
            print(f"Suggested: {suggested_dest}")
            choice = input("(a)ccept, (m)anual, or (s)kip? [a]: ").strip().lower() or 'a'
        else:
            print("Could not infer destination")
            choice = input("(m)anual entry or (s)kip? [s]: ").strip().lower() or 's'
        
        if choice == 's':
            skipped += 1
            continue
        elif choice == 'm':
            dest = input("Enter destination path: ").strip()
            if dest:
                transfer_file(file_path, dest, transfer_mode)
                transferred += 1
        elif choice == 'a' and suggested_dest:
            transfer_file(file_path, suggested_dest, transfer_mode)
            transferred += 1
    
    print(f"\n{'=' * 60}")
    print(f"Transfer complete!")
    print(f"  Transferred: {transferred}")
    print(f"  Skipped: {skipped}")
    print(f"{'=' * 60}")

def main():
    """Main function"""
    try:
        interactive_transfer()
    except KeyboardInterrupt:
        print("\n\nTransfer cancelled by user")
    except Exception as e:
        print(f"\nError: {e}")

if __name__ == "__main__":
    main()