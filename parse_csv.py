#!/usr/bin/env python3
"""
CSV Parser for Governors Dossier
Split CSV columns into individual text files
"""

import pandas as pd
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

def split_columns(csv_path: str, output_dir: str) -> None:
    """
    Read the CSV at csv_path and write one .txt file per column into output_dir.
    """
    logging.info(f"Reading CSV from {csv_path}")
    df = pd.read_csv(csv_path)
    outdir = Path(output_dir)
    outdir.mkdir(parents=True, exist_ok=True)
    
    logging.info(f"Found {len(df.columns)} columns: {list(df.columns)}")
    
    for col in df.columns:
        file_path = outdir / f"{col}.txt"
        logging.info(f"Writing column '{col}' to {file_path}")
        
        with file_path.open("w", encoding="utf-8") as f:
            for val in df[col].astype(str):
                f.write(val + "\n")
        
        logging.info(f"Finished writing {file_path} ({len(df)} lines)")

def parse_governors_csv():
    """Parse the governors CSV using the ultra-clean version"""
    
    # Use the ultra-clean CSV we just created
    csv_files = [
        "governors_ultra_clean.csv",
        "governors_final_clean.csv", 
        "governors_dossier.csv"
    ]
    
    # Find the first available CSV file
    csv_path = None
    for csv_file in csv_files:
        if Path(csv_file).exists():
            csv_path = csv_file
            break
    
    if csv_path is None:
        logging.error("No CSV file found!")
        return
    
    logging.info(f"Using CSV file: {csv_path}")
    
    # Create output directory
    output_dir = "csv_columns"
    
    # Split the columns
    split_columns(csv_path, output_dir)
    
    logging.info("CSV parsing complete!")

if __name__ == "__main__":
    parse_governors_csv()
