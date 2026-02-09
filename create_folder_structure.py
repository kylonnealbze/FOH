#!/usr/bin/env python3
"""
FOH Data Folder Structure Creator
Creates the standardized folder hierarchy for Fragments of Hope data on Synology NAS
"""

import os
from pathlib import Path

# Configuration
BASE_PATH = "/volume1/FOH Data"  # Update this to your NAS mount point

# Define the structure
AREAS = {
    "Inner Cayes": [
        "Salt Water Caye",
        # Add more sites here
    ],
    "North Cayes": [
        # Add sites here
    ],
    # Add more areas here
}

DATA_TYPES = [
    "Temperature Data",
    "Growth Data",
    "Water Quality Data",
    "Survey Data",
    "Photos",
    "Videos",
    "Reports",
    "Field Notes",
]

# Year range
START_YEAR = 2020
END_YEAR = 2026

def create_folder_structure(base_path, dry_run=True):
    """
    Create the complete folder structure
    
    Args:
        base_path: Root path for FOH Data
        dry_run: If True, only print what would be created without creating folders
    """
    base = Path(base_path)
    mpas_path = base / "MPAS"
    
    folders_created = []
    
    for area_name, sites in AREAS.items():
        area_path = mpas_path / area_name
        
        for site_name in sites:
            site_path = area_path / site_name
            
            for data_type in DATA_TYPES:
                data_type_path = site_path / data_type
                
                # Create year folders for time-series data
                if data_type in ["Temperature Data", "Growth Data", "Water Quality Data", "Survey Data"]:
                    for year in range(START_YEAR, END_YEAR + 1):
                        year_path = data_type_path / str(year)
                        folders_created.append(year_path)
                else:
                    # For other data types, don't create year subfolders
                    folders_created.append(data_type_path)
    
    # Create folders
    if dry_run:
        print("DRY RUN - The following folders would be created:\n")
        for folder in sorted(folders_created):
            print(f"  {folder}")
        print(f"\nTotal folders: {len(folders_created)}")
        print("\nTo actually create these folders, run with dry_run=False")
    else:
        print("Creating folder structure...\n")
        for folder in folders_created:
            folder.mkdir(parents=True, exist_ok=True)
            print(f"Created: {folder}")
        print(f"\n✓ Successfully created {len(folders_created)} folders")

def main():
    """Main function"""
    print("=" * 60)
    print("FOH Data Folder Structure Creator")
    print("=" * 60)
    print(f"\nBase path: {BASE_PATH}")
    print(f"Areas configured: {len(AREAS)}")
    print(f"Data types: {len(DATA_TYPES)}")
    print(f"Year range: {START_YEAR}-{END_YEAR}\n")
    
    # First run as dry run
    response = input("Run in DRY RUN mode first? (Y/n): ").strip().lower()
    
    if response != 'n':
        create_folder_structure(BASE_PATH, dry_run=True)
        
        proceed = input("\nProceed with actual folder creation? (y/N): ").strip().lower()
        if proceed == 'y':
            create_folder_structure(BASE_PATH, dry_run=False)
        else:
            print("Cancelled.")
    else:
        confirm = input("Create folders immediately? (y/N): ").strip().lower()
        if confirm == 'y':
            create_folder_structure(BASE_PATH, dry_run=False)
        else:
            print("Cancelled.")

if __name__ == "__main__":
    main()