import pandas as pd
import os
import json
import sys

def analyze_je(file_path):
    print(f"Analyzing {file_path}...")
    try:
        df = pd.read_excel(file_path)
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)

    # Clean Debit column
    # Convert to numeric, coercing errors (like '.') to NaN
    df['Debit'] = pd.to_numeric(df['Debit'], errors='coerce')

    # Fill NaN with 0 for calculations if appropriate, or just ignore.
    # Usually in accounting, blank debit means 0.
    df['Debit'] = df['Debit'].fillna(0.0)
    df['Credit'] = df['Credit'].fillna(0.0)

    # Basic Statistics
    row_count = len(df)

    effective_date_min = df['EffectiveDate'].min()
    effective_date_max = df['EffectiveDate'].max()

    total_debit = df['Debit'].sum()
    total_credit = df['Credit'].sum()

    unique_gl_accounts = df['GLAccountNumber'].nunique()

    # Create summary dictionary
    summary = {
        "row_count": int(row_count),
        "effective_date_min": str(effective_date_min),
        "effective_date_max": str(effective_date_max),
        "total_debit": float(total_debit),
        "total_credit": float(total_credit),
        "unique_gl_accounts": int(unique_gl_accounts)
    }

    # Format output text
    report_text = f"""JE Analysis Report
==================
File: {file_path}
Row Count: {row_count}
Date Range: {effective_date_min} to {effective_date_max}
Total Debit: {total_debit:,.2f}
Total Credit: {total_credit:,.2f}
Unique GL Accounts: {unique_gl_accounts}
"""

    # Ensure output directory exists
    output_dir = "analysis_output"
    os.makedirs(output_dir, exist_ok=True)

    # Write text report
    with open(os.path.join(output_dir, "summary.txt"), "w") as f:
        f.write(report_text)

    # Write JSON report
    with open(os.path.join(output_dir, "summary.json"), "w") as f:
        json.dump(summary, f, indent=4)

    print("Analysis complete. Results saved to 'analysis_output'.")

if __name__ == "__main__":
    file_path = "je_samples.xlsx"
    if len(sys.argv) > 1:
        file_path = sys.argv[1]

    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        sys.exit(1)

    analyze_je(file_path)
