# FOH - Fragments of Hope Data Organization

Scripts and tools for organizing Fragments of Hope marine conservation data on Synology NAS.

## 📁 Folder Structure

This repository helps you create and maintain the following folder structure on your Synology NAS:

```
FOH Data/
└── MPAS/
    ├── Inner Cayes/
    │   ├── Salt Water Caye/
    │   │   ├── Temperature Data/
    │   │   │   ├── 2020/
    │   │   │   ├── 2021/
    │   │   │   └── ...
    │   │   ├── Growth Data/
    │   │   │   └── [years]
    │   │   ├── Water Quality Data/
    │   │   │   └── [years]
    │   │   ├── Survey Data/
    │   │   │   └── [years]
    │   │   ├── Photos/
    │   │   ├── Videos/
    │   │   ├── Reports/
    │   │   └── Field Notes/
    │   └── [Other Sites]/
    ├── North Cayes/
    │   └── [Sites with same structure]
    └── [Other MPA Areas]/
```

## 🛠️ Scripts

### 1. `create_folder_structure.py`
Creates the complete folder hierarchy on your NAS.

**Features:**
- Dry-run mode to preview before creating
- Configurable areas, sites, and data types
- Automatic year folder creation for time-series data

**Usage:**
```bash
python3 create_folder_structure.py
```

**Configuration:**
Edit the script to customize:
- `BASE_PATH` - Your NAS mount point
- `AREAS` - Dictionary of MPA areas and their sites
- `DATA_TYPES` - List of data categories
- `START_YEAR` / `END_YEAR` - Year range

### 2. `transfer_data.py`
Interactive tool to transfer data from USB drives to the correct NAS locations.

**Features:**
- Automatic metadata detection from filenames
- Interactive confirmation and correction
- Copy or move modes
- Creates destination folders automatically

**Usage:**
```bash
python3 transfer_data.py
```

**Configuration:**
- `BASE_PATH` - Your NAS MPAS folder
- `USB_MOUNT` - Your USB drive mount point

## 🚀 Getting Started

### 1. Clone this repository
```bash
git clone https://github.com/kylonnealbze/FOH.git
cd FOH
```

### 2. Customize the scripts
Edit both Python files to add your specific:
- MPA areas (Inner Cayes, North Cayes, etc.)
- Site names
- NAS mount paths

### 3. Create the folder structure
```bash
python3 create_folder_structure.py
```

### 4. Transfer data from USB
```bash
python3 transfer_data.py
```

## 📝 File Naming Conventions

For best automatic detection, name your files with:
- **Area**: Include "Inner Cayes", "North Cayes", etc.
- **Site**: Include site name like "Salt Water Caye"
- **Data Type**: Include keywords like "temperature", "growth", "survey"
- **Year**: Include 4-digit year (e.g., 2024)

**Example:** `InnerCayes_SaltWaterCaye_Temperature_2024-03-15.csv`

## 🔧 Customization

### Adding New Areas
Edit `create_folder_structure.py`:
```python
AREAS = {
    "Inner Cayes": ["Salt Water Caye", "Your Site Here"],
    "North Cayes": ["Another Site"],
    "Your New Area": ["Site 1", "Site 2"],
}
```

### Adding Data Types
Edit the `DATA_TYPES` list:
```python
DATA_TYPES = [
    "Temperature Data",
    "Your New Data Type",
]
```

## 📋 Requirements

- Python 3.6+
- Access to Synology NAS (via SSH or mounted drive)
- Standard library only (no external dependencies)

## 📚 Related Resources

- [Moving Worlds Experteering Guide](https://www.notion.so/boreal321/Moving-Worlds-Experteering-1ec9b0b409f680aa866dca991f0ed02c)
- Fragments of Hope Foundation

## 📄 License

MIT License - Feel free to use and modify for your organization.

## 🤝 Contributing

Issues and pull requests welcome! This is a tool for the conservation community.

---

**Maintained by:** @kylonnealbze  
**Organization:** Fragments of Hope Foundation
