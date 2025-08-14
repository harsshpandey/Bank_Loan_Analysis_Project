#!/usr/bin/env python3
"""
Bank Loan Analytics - Installation and Setup Script
This script helps you install dependencies and run the visualization tools.
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    print("📦 Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ All packages installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing packages: {e}")
        return False

def check_data_file():
    """Check if the cleaned data file exists"""
    if os.path.exists("cleaned_financial_loan.csv"):
        print("✅ Found cleaned_financial_loan.csv")
        return True
    else:
        print("⚠️  Warning: cleaned_financial_loan.csv not found")
        print("   The scripts will use sample data for demonstration")
        return False

def run_dashboard():
    """Run the interactive dashboard"""
    print("\n🚀 Starting Interactive Dashboard...")
    print("   This will open a web browser window")
    print("   If it doesn't open automatically, go to: http://127.0.0.1:8050/")
    print("   Press Ctrl+C to stop the dashboard")
    
    try:
        subprocess.run([sys.executable, "bank_loan_dashboard.py"])
    except KeyboardInterrupt:
        print("\n🛑 Dashboard stopped by user")
    except Exception as e:
        print(f"❌ Error running dashboard: {e}")

def generate_charts():
    """Generate standalone charts"""
    print("\n📊 Generating Standalone Charts...")
    try:
        subprocess.run([sys.executable, "simple_charts.py"])
        print("\n🎉 Charts generated successfully!")
        print("   Open any of the generated HTML files in your web browser")
    except Exception as e:
        print(f"❌ Error generating charts: {e}")

def main():
    """Main function"""
    print("🏦 Bank Loan Analytics - Setup and Installation")
    print("=" * 50)
    
    # Check Python version
    if sys.version_info < (3, 7):
        print("❌ Python 3.7 or higher is required")
        print(f"   Current version: {sys.version}")
        return
    
    print(f"✅ Python version: {sys.version.split()[0]}")
    
    # Install requirements
    if not install_requirements():
        print("❌ Failed to install requirements. Please check your internet connection and try again.")
        return
    
    # Check data file
    check_data_file()
    
    # Show menu
    while True:
        print("\n" + "=" * 50)
        print("🎯 What would you like to do?")
        print("1. 🚀 Run Interactive Dashboard")
        print("2. 📊 Generate Standalone Charts")
        print("3. 🔄 Install Requirements Again")
        print("4. ❌ Exit")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == "1":
            run_dashboard()
        elif choice == "2":
            generate_charts()
        elif choice == "3":
            install_requirements()
        elif choice == "4":
            print("👋 Goodbye! Happy analyzing!")
            break
        else:
            print("❌ Invalid choice. Please enter 1, 2, 3, or 4.")

if __name__ == "__main__":
    main()
