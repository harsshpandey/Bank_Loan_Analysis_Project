# clean_data.py

import pandas as pd

try:
    # --- Step 1: Load your original CSV file ---
    # This line reads your 'financial_loan.csv' file into a format
    # that Python can work with.
    print("Reading the original file: 'financial_loan.csv'...")
    df = pd.read_csv('financial_loan.csv')
    print("File loaded successfully!")

    # --- Step 2: Define the columns that need fixing ---
    # These are the columns that looked like text but should be dates.
    date_columns = [
        'issue_date',
        'last_credit_pull_date',
        'last_payment_date',
        'next_payment_date'
    ]

    # --- Step 3: Convert the columns to a proper date format ---
    # This loop goes through each column name in date_columns and converts it.
    # The 'errors='coerce'' part is important; it will mark any date
    # that can't be understood as invalid, preventing the script from crashing.
    print("Fixing date columns...")
    for col in date_columns:
        df[col] = pd.to_datetime(df[col], format='%d-%m-%Y', errors='coerce')
    print("Date formatting complete.")

    # --- Step 4: Save the cleaned data to a new file ---
    # This saves all the changes into a new CSV file, so your original
    # file remains untouched.
    cleaned_file_path = 'cleaned_financial_loan.csv'
    df.to_csv(cleaned_file_path, index=False)
    
    
    print("-" * 50)
    print(f"Success! A new file named '{cleaned_file_path}' has been created.")
    print("This new file contains the corrected date formats.")

except FileNotFoundError:
    print("Error: Could not find 'financial_loan.csv'.")
    print("Please make sure the script is in the same folder as your data file.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")