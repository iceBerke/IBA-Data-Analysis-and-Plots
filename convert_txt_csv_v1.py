# Description

# Developed with Claude.AI and ChatGPT v. 5.2
# Last updated: 17/12/2025

import pandas as pd
import re
from pathlib import Path

# -----------------------------
# HARD-CODED INPUT FILE PATH
# -----------------------------
INPUT_FILE = Path(r"C:\Users\berke\Desktop\IBA\data_analysis\2025-12-Poly-Lysine test\A0112000.txt")

def convert_txt_to_csv(input_file: Path):

    if not input_file.exists():
        print(f"Error: File not found: {input_file}")
        return

    # Output: same folder, same name, .csv extension
    output_file = input_file.with_suffix(".csv")

    # Try different encodings
    for encoding in ["latin-1", "cp1252", "iso-8859-1", "utf-8"]:
        try:
            with open(input_file, "r", encoding=encoding) as f:
                lines = f.readlines()
            print(f"✓ Successfully read with {encoding} encoding")
            break
        except Exception:
            continue
    else:
        print("Error: Could not read file with any encoding")
        return

    # Parse space-delimited data (2+ spaces)
    data = []
    for line in lines:
        fields = re.split(r"\s{2,}", line.strip())
        if fields and any(fields):
            data.append(fields)

    if len(data) < 2:
        print("Error: File must have at least a header row and one data row")
        return

    # Create DataFrame
    df = pd.DataFrame(data[1:], columns=data[0])
    df = df.replace(',', '.', regex=True)
    df['Time'] = '"' + df['Time'].astype(str) + '"'

    # Save as CSV
    df.to_csv(output_file, index=False, sep=';')  

    print(f"✓ CSV file created: {output_file}")
    print(f"  • Columns: {len(df.columns)}")
    print(f"  • Rows: {len(df)}")

if __name__ == "__main__":
    convert_txt_to_csv(INPUT_FILE)
