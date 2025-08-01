import pandas as pd
import os

def excel_sheets_to_csvs(excel_path, output_dir="data_sathish"):
    os.makedirs(output_dir, exist_ok=True)
    # Load the Excel file
    xls = pd.ExcelFile(excel_path)
    # Set output directory to current if not specified
    if output_dir is None:
        output_dir = os.getcwd()
    # For each sheet, save as CSV
    for sheet_name in xls.sheet_names:
        df = pd.read_excel(xls, sheet_name)
        # Clean the sheet name for use as a filename
        safe_sheet_name = "".join([c if c.isalnum() or c in (' ', '.', '_') else '_' for c in sheet_name])
        csv_filename = os.path.join(output_dir, f"{safe_sheet_name}.csv")
        df.to_csv(csv_filename, index=False)
        print(f"Saved {csv_filename}")

if __name__ == "__main__":
    excel_path = "Raw ALW_Code data  (1).xlsx" 
    excel_sheets_to_csvs(excel_path)
