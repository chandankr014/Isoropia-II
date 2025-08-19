from csv import excel
import os
import pandas as pd
import subprocess
import re
import time
from glob import glob


##### ------- CONFIGURATION ------- #####
exe_path = r"isrpia2.exe"
DATA_DIR = "data_jayaraju2"

# 0 - FORWARD, 
# 1 - REVERSE
MODE = "1" 
# 0 - GAS (SOLID + LIQUID POSSIBLE)
# 1 - AEROSOL (LIQUID ONLY (METASTABLE), 
AEROSOL_STATE = "1" 

MODE_NAMES = {"0": "FORWARD", "1": "REVERSE"}
AEROSOL_STATE_NAMES = {"0": "GAS_SOLID_LIQUID", "1": "AEROSOL_METASTABLE"}


def get_output_folder():
    """Generate output folder path based on MODE and AEROSOL_STATE"""
    mode_name = MODE_NAMES.get(MODE, f"MODE_{MODE}")
    state_name = AEROSOL_STATE_NAMES.get(AEROSOL_STATE, f"STATE_{AEROSOL_STATE}")
    return os.path.join("Output", DATA_DIR, f"{mode_name}_{state_name}")

def get_artifacts_folder():
    """Generate artifacts folder path based on MODE and AEROSOL_STATE"""
    mode_name = MODE_NAMES.get(MODE, f"MODE_{MODE}")
    state_name = AEROSOL_STATE_NAMES.get(AEROSOL_STATE, f"STATE_{AEROSOL_STATE}")
    return f"artifacts_{DATA_DIR}_{mode_name}_{state_name}"

def validate_configuration():
    """Validate the current configuration settings"""
    issues = []
    
    # Check if executable exists
    if not os.path.exists(exe_path):
        issues.append(f"ISOROPIA executable not found: {exe_path}")
    
    # Check if data directory exists
    if not os.path.exists(DATA_DIR):
        issues.append(f"Data directory not found: {DATA_DIR}")
    
    # Validate MODE
    if MODE not in MODE_NAMES:
        issues.append(f"Invalid MODE: {MODE}. Valid values: {list(MODE_NAMES.keys())}")
    
    # Validate AEROSOL_STATE
    if AEROSOL_STATE not in AEROSOL_STATE_NAMES:
        issues.append(f"Invalid AEROSOL_STATE: {AEROSOL_STATE}. Valid values: {list(AEROSOL_STATE_NAMES.keys())}")
    
    return issues

def run_calculation(chemicals):
    try:
        # Start the process
        process = subprocess.Popen([exe_path], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Prepare input: feed each chemical one by one
        input_data = "\n".join(chemicals) + "\n"

        # Communicate the inputs and capture the output
        output, error = process.communicate(input=input_data)

        # Check if there's an error
        if process.returncode != 0:
            print(f"Error: {error}")
            return None

        return output
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def extract_value(data_string):
    match = re.search(r'([-+]?\d*\.\d+E[+-]?\d+)', data_string)
    if match:
        numeric_value = match.group(0)
        result = float(numeric_value)
        return result
    else:
        return 0
    
""" 
pH
H+ concentration
AWLC
"""

def isoropia_processor(FP):
    """
    Process a single CSV file through ISOROPIA calculations
    
    Args:
        FP (str): File path to the CSV file to process
    """
    try:
        if FP.endswith('.csv'):
            data = pd.read_csv(FP)
            print(f"Processing file: {FP}")
            print(f"Data shape: {data.shape}")
    
        if FP.endswith('.xlsx'):
            data = pd.read_excel(FP)
            print(f"Processing file: {FP}")
            print(f"Data shape: {data.shape}")

        # Validate required columns
        required_columns = ['Na+', 'SO42-', 'NH4+', 'NO3-', 'Cl-', 'Ca2+', 'K+', 'Mg2+', 'Relative Humidity (%)', 'Temperature (°C)']
        missing_columns = [col for col in required_columns if col not in data.columns]
        if missing_columns:
            print(f"Error: Missing required columns: {missing_columns}")
            return False
    except Exception as e:
        print(f"Error reading file {FP}: {e}")
        return False

    # INPUTS PARAMETERS
    successful_calculations = 0
    failed_calculations = 0
    
    for index, df in data.iterrows():
        try:
            na = df['Na+'] 
            so42 = df['SO42-'] 
            nh4 = df['NH4+'] 
            no3 = df['NO3-'] 
            cl = df['Cl-'] 
            ca = df['Ca2+'] 
            k = df['K+'] 
            mg = df['Mg2+'] 
            rh = df['Relative Humidity (%)'] / 100  # Convert RH to fraction
            temp = df['Temperature (°C)'] + 273.15  # Convert Temp to Kelvin

            chemicals = ['\n', f'{MODE}', f'{AEROSOL_STATE},0',
                        str(float(na)), str(float(so42)), 
                        str(float(nh4)), str(float(no3)), 
                        str(float(cl)), str(float(ca)), 
                        str(float(k)), str(float(mg)), 
                        str(float(rh)), str(float(temp))]

            result = run_calculation(chemicals)
            if result is None:
                print(f"Failed calculation for row {index}")
                failed_calculations += 1
                continue

            screen_txt = 'SCREEN.txt'
            screen_dat = 'SCREEN.dat'
            
            # Only process if SCREEN.txt exists and has sufficient lines
            if not os.path.exists(screen_txt):
                print(f"Warning: {screen_txt} not found for row {index}")
                failed_calculations += 1
                continue
                
            with open(screen_txt, 'r') as file:
                lines = file.readlines()
                if len(lines) >= 74:  # Ensure we have enough lines
                    # AWLC (line 74)
                    line_74 = lines[73].strip()
                    awlc = extract_value(line_74)
                    print(f"Row {index}: AWLC = {awlc}")

                    # H+ concentration (line 75)
                    line_75 = lines[74].strip()
                    hydrogen_conc = extract_value(line_75)
                    print(f"Row {index}: Hydrogen = {hydrogen_conc}")

                    # pH concentration (line 88)
                    line_88 = lines[87].strip()
                    ph_conc = extract_value(line_88)
                    print(f"Row {index}: pH = {ph_conc}")

                    # Update dataframe with results
                    data.at[index, 'AWLC'] = awlc
                    data.at[index, 'Hydrogen'] = hydrogen_conc
                    data.at[index, 'PH'] = ph_conc
                    
                    successful_calculations += 1

                else:
                    print(f"Error: Insufficient lines in SCREEN.txt for row {index} (found {len(lines)} lines)")
                    failed_calculations += 1

            # Archive SCREEN.txt only (not .dat files)
            artifacts_folder = get_artifacts_folder()
            os.makedirs(artifacts_folder, exist_ok=True)
            
            try:
                if os.path.exists(screen_txt):
                    timestamp = pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')
                    new_screen_txt = f"{timestamp}_{screen_txt}"
                    new_path = os.path.join(artifacts_folder, new_screen_txt)
                    os.rename(screen_txt, new_path)
                    print(f"Moved: {screen_txt} to {new_path}")
                if os.path.exists(screen_dat):
                    new_screen_dat = f"{timestamp}_{screen_dat}"
                    new_path = os.path.join(artifacts_folder, new_screen_dat)
                    os.rename(screen_dat, new_path)
                    print(f"Moved: {screen_dat} to {new_path}")
                if os.path.exists(screen_txt):
                    os.remove(screen_txt)
                    print(f"Deleted: {screen_txt}")
                if os.path.exists(screen_dat):
                    os.remove(screen_dat)
                    print(f"Deleted: {screen_dat}")
                time.sleep(1)
            except Exception as e:
                pass

        except Exception as e:
            print(f"Error processing row {index}: {e}")
            failed_calculations += 1
            continue
    
    print(f"Processing complete: {successful_calculations} successful, {failed_calculations} failed")
    
    # Save output with structured folder path
    output_folder = get_output_folder()
    os.makedirs(output_folder, exist_ok=True)
    
    # Generate output filename
    base_filename = os.path.basename(FP)
    name, ext = os.path.splitext(base_filename)
    mode_name = MODE_NAMES.get(MODE, f"MODE_{MODE}")
    state_name = AEROSOL_STATE_NAMES.get(AEROSOL_STATE, f"STATE_{AEROSOL_STATE}")
    output_filename = f"{name}_{mode_name}_{state_name}_processed.csv"
    output_path = os.path.join(output_folder, output_filename)
    
    data.to_csv(output_path, index=False)
    print(f"Results saved to: {output_path}")
    return True

# CALLING
if __name__ == "__main__":
    print("="*60)
    print("ISOROPIA BATCH PROCESSOR")
    print("="*60)
    
    print(f"Configuration:")
    print(f"  Data Directory: {DATA_DIR}")
    print(f"  Mode: {MODE} ({MODE_NAMES.get(MODE, 'Unknown')})")
    print(f"  Aerosol State: {AEROSOL_STATE} ({AEROSOL_STATE_NAMES.get(AEROSOL_STATE, 'Unknown')})")
    print(f"  Output Folder: {get_output_folder()}")
    print(f"  Artifacts Folder: {get_artifacts_folder()}")
    print("="*60)
    
    # Check if data directory exists
    csv_files = glob(os.path.join(DATA_DIR, "*.csv"))
    print(f"Total CSV files found: {len(csv_files)}")
    
    if not csv_files:
        print(f"No CSV files found in '{DATA_DIR}' directory!")
        exit(1)
    
    # List all files to be processed
    for i, csv_file in enumerate(csv_files, 1):
        print(f"  {i}. {csv_file}")
    
    print("\nStarting processing...")
    print("="*60)
    
    successful_files = 0
    failed_files = 0
    
    for i, csv_file in enumerate(csv_files, 1):
        print(f"\n[{i}/{len(csv_files)}] PROCESSING >>> {csv_file}")
        print("-" * 50)
        
        try:
            if isoropia_processor(csv_file):
                successful_files += 1
                print(f"✓ Successfully processed: {csv_file}")
            else:
                failed_files += 1
                print(f"✗ Failed to process: {csv_file}")
        except Exception as e:
            failed_files += 1
            print(f"✗ Error processing {csv_file}: {e}")
    
    print("\n" + "="*60)
    print("PROCESSING SUMMARY")
    print("="*60)
    print(f"Total files: {len(csv_files)}")
    print(f"Successful: {successful_files}")
    print(f"Failed: {failed_files}")
    print(f"Success rate: {(successful_files/len(csv_files)*100):.1f}%")
    print("="*60)
