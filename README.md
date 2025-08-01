# 🌟 Isoropia-II Automation Tool

> **A beginner-friendly Python tool to automate atmospheric chemistry calculations using Isoropia II software**

## 📖 What is This?

This tool helps atmospheric scientists and researchers automatically process large amounts of chemical data using the **Isoropia II** thermodynamic model. Instead of manually entering data point by point, this program:

- 📊 Reads your data from Excel or CSV files
- 🔄 Automatically runs Isoropia II calculations for each data row
- 💾 Saves all results in organized folders
- 📈 Calculates important atmospheric properties like pH, aerosol water content, and ion concentrations

## 🚀 Quick Start Guide

### Step 1: Download the Project

**Option A: Using Git (Recommended)**
```bash
git clone https://github.com/chandankr014/Isoropia-II.git
cd Isoropia-II
```

**Option B: Download ZIP**
1. Click the green "Code" button on GitHub
2. Select "Download ZIP"
3. Extract the ZIP file to your computer
4. Open the extracted folder

### Step 2: Install Python Requirements

Make sure you have Python installed on your computer. Then install the required packages:

```bash
pip install pandas openpyxl
```

### Step 3: Prepare Your Files

You need two things in your project folder:

1. **📁 Your data files** (CSV format) in a folder called `data_sathish` (or change the folder name in the script)
2. **⚙️ Isoropia II executable** (`isrpia2.exe`) in the main project folder

### Step 4: Configure the Settings

Open `iso.py` and modify these settings at the top:

```python
##### ------- CONFIGURATION ------- #####
DATA_DIR = "your_data_folder"    # Change this to your data folder name
MODE = "0"                       # 0=FORWARD, 1=REVERSE
AEROSOL_STATE = "0"             # 0=GAS_SOLID_LIQUID, 1=AEROSOL_METASTABLE
```

### Step 5: Run the Program

Open a terminal/command prompt **as Administrator** and run:

```bash
python iso.py
```

## 📊 Data Format Requirements

### Required Columns in Your CSV Files:

| Column Name | Description | Unit | Example |
|------------|-------------|------|---------|
| `Na` | Sodium | µg/m³ | 2.5 |
| `SO42-` | Sulfate | µg/m³ | 15.3 |
| `NH4+` | Ammonium | µg/m³ | 8.2 |
| `NO3-` | Nitrate | µg/m³ | 12.1 |
| `Cl-` | Chloride | µg/m³ | 3.7 |
| `Ca` | Calcium | µg/m³ | 1.2 |
| `K+` | Potassium | µg/m³ | 0.8 |
| `Mg` | Magnesium | µg/m³ | 0.5 |
| `RH` | Relative Humidity | 0-1 | 0.75 (for 75%) |
| `Temp` | Temperature | Kelvin | 298.15 |

### ⚠️ Important Notes:
- **RH must be decimal**: Use 0.75 for 75% humidity, NOT 75
- **Temperature in Kelvin**: Add 273.15 to Celsius (e.g., 25°C = 298.15 K)
- **No missing values**: All cells must contain numbers
- **Exact column names**: Use the exact column names shown above

## 🎛️ Configuration Options

### Processing Modes:

| MODE | Description | When to Use |
|------|-------------|-------------|
| `"0"` | **FORWARD** | You have gas-phase concentrations and want aerosol properties |
| `"1"` | **REVERSE** | You have aerosol concentrations and want gas-phase properties |

### Aerosol States:

| AEROSOL_STATE | Description | When to Use |
|---------------|-------------|-------------|
| `"0"` | **GAS + SOLID + LIQUID** | For dry conditions or when solids can form |
| `"1"` | **LIQUID ONLY (Metastable)** | For humid conditions, liquid aerosols only |

## 📁 Output Structure

The program creates organized folders based on your settings:

```
📦 Your Project Folder
├── 📂 Output/
│   └── 📂 data_sathish/
│       └── 📂 REVERSE_AEROSOL_METASTABLE/
│           ├── 📄 file1_REVERSE_AEROSOL_METASTABLE_processed.csv
│           └── 📄 file2_REVERSE_AEROSOL_METASTABLE_processed.csv
├── 📂 artifacts_data_sathish_REVERSE_AEROSOL_METASTABLE/
│   ├── 📄 20250801_143021_SCREEN.txt
│   └── 📄 20250801_143022_SCREEN.txt
└── 📄 iso.py
```

## 📈 What You Get Back

The processed CSV files will contain your original data plus these calculated columns:

- **AWLC**: Aerosol Water Liquid Content (µg/m³)
- **Hydrogen**: H⁺ ion concentration (mol/L)
- **PH**: pH value

## 🛠️ Troubleshooting

### Common Issues:

**❌ "ISOROPIA executable not found"**
- Make sure `isrpia2.exe` is in the same folder as `iso.py`

**❌ "Data directory not found"**
- Check that your data folder exists and the `DATA_DIR` setting is correct

**❌ "Missing required columns"**
- Verify your CSV has all the required column names (case-sensitive)

**❌ "Permission denied"**
- Run your terminal/command prompt as Administrator

**❌ "No CSV files found"**
- Make sure your data files are in CSV format in the correct folder

### Getting Help:

1. Check the terminal output - it shows detailed progress and error messages
2. Look in the artifacts folder for `SCREEN.txt` files to debug Isoropia issues
3. Verify your data format matches the requirements exactly

## 📊 Example Data File

Here's what your CSV file should look like:

```csv
Na,SO42-,NH4+,NO3-,Cl-,Ca,K+,Mg,RH,Temp
2.5,15.3,8.2,12.1,3.7,1.2,0.8,0.5,0.75,298.15
3.1,18.7,9.5,14.2,4.1,1.5,1.0,0.6,0.68,301.20
1.8,12.4,6.8,9.7,2.9,0.9,0.6,0.4,0.82,295.50
```

## 🌟 Features

- ✅ **Batch Processing**: Process hundreds of data points automatically
- ✅ **Smart Organization**: Results organized by processing mode and state
- ✅ **Error Handling**: Continues processing even if some calculations fail
- ✅ **Progress Tracking**: See real-time progress and success rates
- ✅ **Debugging Support**: Keeps calculation files for troubleshooting
- ✅ **Flexible Configuration**: Easy to change settings for different analyses

## 🤝 Need Help?

- 📧 **Email**: chandankr014@gmail.com
- 🐛 **Bug Reports**: Open an issue on GitHub
- 💡 **Feature Requests**: Let us know what you need!

## 📚 Learn More

- [Isoropia II Documentation](http://nenes.eas.gatech.edu/ISORROPIA/)
- [Atmospheric Chemistry Basics](https://www.epa.gov/air-research/atmospheric-chemistry)

---

*Made with ❤️ for the atmospheric science community*