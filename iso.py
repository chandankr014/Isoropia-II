import os
import pandas as pd
import subprocess
import re

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
        result = float(numeric_value) * 1000 #convert to mg
        return result
    else:
        return 0


def main():

    data = pd.read_excel('alwc_sheet.xlsx')
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
        rh = df['RH ']
        temp = df['Temp']

        chemicals = ['\n', str(1), str(1),
                    str(float(na)/1000), str(float(so42)/1000), 
                    str(float(nh4)/1000), str(float(no3)/1000), 
                    str(float(cl)/1000), str(float(ca)/1000), 
                    str(float(k)/1000), str(float(mg)/1000), 
                    str(float(rh)/100), str(float(temp))]

        result = run_calculation(chemicals)
        print(result)

        screen_txt = 'SCREEN.txt'
        screen_dat = 'SCREEN.dat'
        line_74 = None
        with open(screen_txt, 'r') as file:
            lines = file.readlines()
            if len(lines) >= 74:
                line_74 = lines[73].strip()
                print(line_74)
                RESULT = extract_value(line_74)
                print(RESULT)
                # open datafram and write result
                data.at[index, 'RESULT'] = RESULT
            else:
                print("The file has less than 74 lines.")

        if os.path.exists(screen_txt):
            os.remove(screen_txt)
            print(f"Deleted: {screen_txt}")
        if os.path.exists(screen_dat):
            os.remove(screen_dat)
            print(f"Deleted: {screen_dat}")
    
    data.to_csv("DATAFRAME.csv")

# calling
main()
