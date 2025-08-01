import os
import pandas as pd
import subprocess
import re
import time
import glob

# isoropia software location
exe_path = r"isrpia2.exe"

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
Aerosol liquid water content
"""


def isoropia_processor(FP):
    data = pd.read_csv(f'{FP}')

    # INPUTS PARAMETERS
    for index, df in data.iterrows():
        so42 = df['HRSO4']
        nh4 = df['HRNH4']
        no3 = df['HRNO3']
        cl = df['HRChl']
        ca = 0
        na = 0
        k = 0
        mg = 0
        rh = df['Relative Humidity (%)'] / 100
        temp = df['Temperature (°C)'] + 273.15

        chemicals = ['\n', str(1), '1,1',
                    str(float(na)), str(float(so42)), 
                    str(float(nh4)), str(float(no3)), 
                    str(float(cl)), str(float(ca)), 
                    str(float(k)), str(float(mg)), 
                    str(float(rh)), str(float(temp))]

        result = run_calculation(chemicals)
        print(result)

        screen_txt = 'SCREEN.txt'
        screen_dat = 'SCREEN.dat'
        line_54 = None
        with open(screen_txt, 'r') as file:
            lines = file.readlines()
            if len(lines) >= 54:
                # # ALWC
                # line_54 = lines[53].strip()
                # print(line_54)
                # alwc = extract_value(line_54)
                # print(alwc)
                # data.at[index, 'ALWC'] = alwc
                # pH
                line_68 = lines[67].strip()
                print(line_68)
                ph = extract_value(line_68)
                print(ph)
                data.at[index, 'pH'] = ph
            else:
                print("Error reading lines")

        artifacts_folder = 'artifacts'
        os.makedirs(artifacts_folder, exist_ok=True)
        try:
            if os.path.exists(screen_txt):
                os.remove(screen_txt)
                print(f"Deleted: {screen_txt}")
            if os.path.exists(screen_dat):
                os.remove(screen_dat)
                print(f"Deleted: {screen_dat}")
            time.sleep(0.1)
        except Exception as e:
            pass

    data.to_csv(f"output/{FP}", index=False)

# CALLING
if __name__=="__main__":
    data_folder = "data"
    csv_files = glob.glob(os.path.join(data_folder, "*.csv"))
    print("Total csv files found: ", len(csv_files))
    for csv_file in csv_files:
        print("  PROCESSING >>> ", csv_file)
        isoropia_processor(csv_file)
