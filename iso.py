import os
import pandas as pd
import subprocess
import re
import time

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
pH
H+ concentration
"""


def main():

    # data = pd.read_excel('sheet.xlsx')
    data = pd.read_csv('sheet.csv')
    print(data.columns)

    # INPUTS PARAMETERS
    for index, df in data.iterrows():
        na = df['Na']
        so42 = df['SO42-']
        nh4 = df['NH4+']
        no3 = df['NO3-']
        cl = df['Cl-']
        ca = df['Ca']
        k = df['K+']
        mg = df['Mg']
        rh = df['RH']
        temp = df['Temp']

        chemicals = ['\n', str(1), str(1),
                    str(float(na)), str(float(so42)), 
                    str(float(nh4)), str(float(no3)), 
                    str(float(cl)), str(float(ca)), 
                    str(float(k)), str(float(mg)), 
                    str(float(rh)), str(float(temp))]

        result = run_calculation(chemicals)
        print(result)

        screen_txt = 'SCREEN.txt'
        screen_dat = 'SCREEN.dat'
        line_74 = None
        with open(screen_txt, 'r') as file:
            lines = file.readlines()
            if len(lines) >= 74:
                # AWLC
                line_74 = lines[73].strip()
                print(line_74)
                awlc = extract_value(line_74)
                print(awlc)

                # H+ concentration
                line_75 = lines[74].strip()
                print(line_75)
                hydrogen_conc = extract_value(line_75)
                print(hydrogen_conc)

                # pH concentration
                line_88 = lines[87].strip()
                print(line_88)
                ph_conc = extract_value(line_88)
                print(ph_conc)

                # open datafram and write result
                data.at[index, 'AWLC'] = awlc
                data.at[index, 'Hydrogen'] = hydrogen_conc
                data.at[index, 'PH'] = ph_conc

            else:
                print("Error reading lines")

        artifacts_folder = 'artifacts'
        # os.makedirs(artifacts_folder, exist_ok=True)
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
        
    data.to_csv("DATAFRAME.csv")

# calling
main()
