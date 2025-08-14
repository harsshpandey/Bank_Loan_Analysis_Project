# 🏦 Bank Loan Analytics Dashboard

<div align="center">

![Dashboard Preview](https://img.shields.io/badge/Dashboard-Interactive-blue?style=for-the-badge&logo=plotly)
![Python](https://img.shields.io/badge/Python-3.8+-green?style=for-the-badge&logo=python)
![Dash](https://img.shields.io/badge/Dash-2.10+-purple?style=for-the-badge&logo=plotly)
![MySQL](https://img.shields.io/badge/MySQL-8.0+-orange?style=for-the-badge&logo=mysql)

**Comprehensive Financial Analytics Dashboard with Beautiful UI & Interactive Visualizations**

[🚀 Quick Start](#-quick-start) • [📊 Features](#-features) • [🔧 Setup](#-setup) • [📈 Process](#-process)

</div>

---

## 🌟 **Project Overview**

This project transforms raw bank loan data into a **stunning, interactive analytics dashboard** using Python, MySQL, and modern web technologies. The dashboard provides comprehensive insights into loan performance, risk assessment, and financial metrics through beautiful visualizations and real-time KPI tracking.

### 🎯 **What You'll Get**
- **Beautiful Glass Morphism UI** with gradient backgrounds and smooth animations
- **Interactive Charts** powered by Plotly and Dash
- **Real-time KPI Calculations** from MySQL database
- **Responsive Design** that works on all devices
- **Professional Analytics** ready for business presentations

---

## 🚀 **Quick Start**

### **Option 1: Run Dashboard (Recommended)**
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the beautiful dashboard
python bank_loan_dashboard.py

# 3. Open browser: http://127.0.0.1:8050/
```

### **Option 2: Generate Standalone Charts**
```bash
# Generate HTML chart files
python simple_charts.py
```

### **Option 3: Windows Users**
```bash
# Use batch file
run_dashboard.bat

# Or PowerShell script
.\run_dashboard.ps1
```

---

## 📊 **Dashboard Features**

### 🎨 **Beautiful UI Elements**
- **Gradient Backgrounds** - Blue to purple gradients
- **Glass Morphism Cards** - Semi-transparent KPI cards
- **Hover Effects** - Smooth animations and transformations
- **Modern Typography** - Inter font family
- **Responsive Layout** - Works on all screen sizes

### 📈 **Interactive Visualizations**
- **KPI Summary Cards** - Key metrics at a glance
- **Monthly Trends Analysis** - Loan patterns over time
- **Loan Status Breakdown** - Comprehensive status analysis
- **Geographic Distribution** - State-wise loan analysis
- **Good vs Bad Loan Analysis** - Risk assessment
- **Categorical Analysis** - Purpose, term, employment insights

### 🔍 **KPI Categories**
- **Total Applications & Amounts** - Overall portfolio metrics
- **Performance Metrics** - Good vs bad loan percentages
- **Geographic Insights** - Regional loan distribution
- **Risk Indicators** - Interest rates, DTI ratios
- **Temporal Analysis** - Month-to-date trends

---

## 🔧 **Setup & Installation**

### **Prerequisites**
- Python 3.8+
- MySQL 8.0+
- Modern web browser

### **Installation Steps**
```bash
# 1. Clone or download the project
cd "Bank Loan Project"

# 2. Create virtual environment (recommended)
python -m venv .venv

# 3. Activate virtual environment
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Prepare your data (see Data Preparation section)
```

### **Dependencies**
```
pandas>=1.5.0          # Data manipulation
plotly>=5.15.0          # Interactive charts
dash>=2.10.0            # Web dashboard framework
dash-bootstrap-components>=1.4.0  # UI components
numpy>=1.24.0           # Numerical operations
```

---

## 📈 **Complete Process Workflow**

### **Phase 1: Data Preparation & Cleaning** 🔧

#### **Step 1: Initial Data Assessment**
```python
# Load raw data
import pandas as pd
df = pd.read_csv('financial_loan.csv')

# Check data structure
print(f"Dataset shape: {df.shape}")
print(f"Columns: {list(df.columns)}")
print(f"Data types:\n{df.dtypes}")
print(f"Missing values:\n{df.isnull().sum()}")
```

#### **Step 2: Data Cleaning Process**
```python
# clean_data.py - Complete cleaning workflow
import pandas as pd

def clean_financial_data():
    # 1. Load raw data
    df = pd.read_csv('financial_loan.csv')
    
    # 2. Fix date columns (convert from DD-MM-YYYY format)
    date_columns = [
        'issue_date',
        'last_credit_pull_date', 
        'last_payment_date',
        'next_payment_date'
    ]
    
    for col in date_columns:
        df[col] = pd.to_datetime(df[col], format='%d-%m-%Y', errors='coerce')
    
    # 3. Handle missing values
    df['emp_length'].fillna('Unknown', inplace=True)
    df['home_ownership'].fillna('Unknown', inplace=True)
    
    # 4. Clean categorical data
    df['purpose'] = df['purpose'].str.replace('_', ' ').str.title()
    
    # 5. Save cleaned data
    df.to_csv('cleaned_financial_loan.csv', index=False)
    
    return df

# Execute cleaning
cleaned_df = clean_financial_data()
print("✅ Data cleaning completed!")
```

#### **Step 3: Data Quality Check**
```python
# Verify cleaning results
print("=== Data Quality Report ===")
print(f"Original records: {len(pd.read_csv('financial_loan.csv'))}")
print(f"Cleaned records: {len(cleaned_df)}")
print(f"Date columns converted: {cleaned_df['issue_date'].dtype}")
print(f"Missing values remaining: {cleaned_df.isnull().sum().sum()}")
```

### **Phase 2: MySQL KPI Development** 🗄️

#### **Step 1: Database Setup**
```sql
-- Create database and table
CREATE DATABASE bank_loan_analytics;
USE bank_loan_analytics;

-- Import cleaned data (using your preferred method)
-- LOAD DATA INFILE 'cleaned_financial_loan.csv' INTO TABLE bank_loan_data;
```

#### **Step 2: Core KPI Queries**
```sql
-- Query MySql File.sql - Key Performance Indicators

-- 1. Total Applications & Amounts
SELECT 
    COUNT(*) as Total_Applications,
    SUM(loan_amount) as Total_Funded_Amount,
    SUM(total_payment) as Total_Amount_Received,
    AVG(int_rate) * 100 as Average_Interest_Rate,
    AVG(dti) * 100 as Average_DTI_Ratio
FROM bank_loan_data;

-- 2. Good vs Bad Loan Analysis
SELECT 
    loan_status,
    COUNT(*) as Loan_Count,
    SUM(loan_amount) as Total_Amount,
    (COUNT(*) / (SELECT COUNT(*) FROM bank_loan_data)) * 100 as Percentage
FROM bank_loan_data 
GROUP BY loan_status;

-- 3. Monthly Trends
SELECT 
    DATE_FORMAT(issue_date, '%Y-%m') as Month,
    COUNT(*) as Applications,
    SUM(loan_amount) as Funded_Amount,
    SUM(total_payment) as Received_Amount
FROM bank_loan_data 
GROUP BY DATE_FORMAT(issue_date, '%Y-%m')
ORDER BY Month;

-- 4. Geographic Analysis
SELECT 
    address_state,
    COUNT(*) as Applications,
    SUM(loan_amount) as Funded_Amount,
    AVG(int_rate) * 100 as Avg_Interest_Rate
FROM bank_loan_data 
GROUP BY address_state
ORDER BY Applications DESC;

-- 5. Purpose Analysis
SELECT 
    purpose,
    COUNT(*) as Applications,
    SUM(loan_amount) as Total_Amount,
    AVG(int_rate) * 100 as Avg_Interest_Rate
FROM bank_loan_data 
GROUP BY purpose
ORDER BY Applications DESC
LIMIT 10;
```

#### **Step 3: Advanced Analytics Queries**
```sql
-- Risk Assessment KPIs
SELECT 
    CASE 
        WHEN dti <= 0.3 THEN 'Low Risk'
        WHEN dti <= 0.5 THEN 'Medium Risk'
        ELSE 'High Risk'
    END as Risk_Category,
    COUNT(*) as Loan_Count,
    AVG(int_rate) * 100 as Avg_Interest_Rate,
    SUM(loan_amount) as Total_Amount
FROM bank_loan_data 
GROUP BY Risk_Category;

-- Employee Length Analysis
SELECT 
    emp_length,
    COUNT(*) as Applications,
    AVG(loan_amount) as Avg_Loan_Amount,
    AVG(int_rate) * 100 as Avg_Interest_Rate
FROM bank_loan_data 
GROUP BY emp_length
ORDER BY 
    CASE emp_length
        WHEN '< 1 year' THEN 1
        WHEN '1 year' THEN 2
        WHEN '2 years' THEN 3
        -- ... continue for all years
        WHEN '10+ years' THEN 11
    END;
```

### **Phase 3: Python Dashboard Development** 🐍

#### **Step 1: Data Loading & Processing**
```python
# Load cleaned data into dashboard
try:
    df = pd.read_csv('cleaned_financial_loan.csv')
    # Convert date columns back to datetime
    date_columns = ['issue_date', 'last_credit_pull_date', 'last_payment_date', 'next_payment_date']
    for col in date_columns:
        df[col] = pd.to_datetime(df[col], errors='coerce')
    print("✅ Data loaded successfully!")
except Exception as e:
    print(f"❌ Error loading data: {e}")
    # Fallback to sample data for demonstration
```

#### **Step 2: KPI Calculation Functions**
```python
def calculate_kpis():
    """Calculate all key performance indicators"""
    # Total KPIs
    total_applications = len(df)
    total_funded = df['loan_amount'].sum()
    total_received = df['total_payment'].sum()
    avg_interest_rate = df['int_rate'].mean() * 100
    avg_dti = df['dti'].mean() * 100
    
    # Good vs Bad Loans
    good_loans = df[df['loan_status'].isin(['Fully Paid', 'Current'])]
    bad_loans = df[df['loan_status'] == 'Charged Off']
    
    good_loan_percentage = (len(good_loans) / total_applications) * 100
    bad_loan_percentage = (len(bad_loans) / total_applications) * 100
    
    return {
        'total_applications': total_applications,
        'total_funded': total_funded,
        'total_received': total_received,
        'avg_interest_rate': avg_interest_rate,
        'avg_dti': avg_dti,
        'good_loan_percentage': good_loan_percentage,
        'bad_loan_percentage': bad_loan_percentage
    }
```

#### **Step 3: Visualization Functions**
```python
def create_monthly_trend_chart():
    """Create beautiful monthly trends visualization"""
    monthly_data = df.groupby(df['issue_date'].dt.to_period('M')).agg({
        'id': 'count',
        'loan_amount': 'sum',
        'total_payment': 'sum'
    }).reset_index()
    
    fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=('📊 Monthly Loan Applications', '💰 Monthly Amounts ($)'),
        vertical_spacing=0.15
    )
    
    # Add beautiful charts with custom styling
    fig.add_trace(
        go.Bar(x=monthly_data['issue_date'], y=monthly_data['id'], 
               name='Applications', marker_color='#667eea',
               marker_line_color='#764ba2', marker_line_width=2),
        row=1, col=1
    )
    
    # Apply beautiful styling
    fig.update_layout(
        height=600, 
        title_text="📈 Monthly Trends Analysis",
        title_font_size=20,
        title_font_color='#2c3e50',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Inter", size=12)
    )
    
    return fig
```

#### **Step 4: Dashboard Layout & Styling**
```python
# Beautiful UI with custom CSS
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        <title>🏦 Bank Loan Analytics Dashboard</title>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
        <style>
            body {
                font-family: 'Inter', sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                margin: 0;
                padding: 0;
                min-height: 100vh;
            }
            .kpi-card {
                background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
                border-radius: 20px;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
                transition: all 0.3s ease;
            }
            .kpi-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        {%config%}
        {%scripts%}
        {%renderer%}
    </body>
</html>
'''
```

---

## 📱 **Dashboard Screenshots & Visual Guide**

### **Main Dashboard View**
```
┌─────────────────────────────────────────────────────────────┐
│                    🏦 Bank Loan Analytics Dashboard         │
│              Comprehensive Financial Analytics & Insights    │
├─────────────────────────────────────────────────────────────┤
│  📊 1,000    💰 $25,000,000    💵 $30,000,000    📈 90.0% │
│ Applications  Total Funded     Total Received    Good Loan% │
├─────────────────────────────────────────────────────────────┤
│  🎯 150       📊 12.5%         ⚖️ 45.2%         📉 10.0%  │
│ MTD Apps      Avg Interest     Avg DTI Ratio    Bad Loan%  │
├─────────────────────────────────────────────────────────────┤
│                    📈 Monthly Trends Analysis               │
│  [Interactive Bar Chart - Applications over Time]          │
│  [Interactive Line Chart - Amounts over Time]              │
├─────────────────────────────────────────────────────────────┤
│                    🔍 Loan Status Analysis                 │
│  [Pie Chart - Loan Count by Status]                       │
│  [Bar Charts - Amounts, Interest Rates, DTI by Status]    │
├─────────────────────────────────────────────────────────────┤
│                    🌍 Geographic Analysis                   │
│  [Bar Charts - Applications & Amounts by State]            │
├─────────────────────────────────────────────────────────────┤
│                    ✅ Good vs Bad Loan Analysis            │
│  [Comparison Charts - Count, Amount, Percentage]           │
├─────────────────────────────────────────────────────────────┤
│                    📊 Categorical Analysis                 │
│  [Multi-panel Charts - Purpose, Term, Employment, Home]   │
└─────────────────────────────────────────────────────────────┘
```

### **KPI Cards Design**
```
┌─────────────────────────────────────┐
│ ████████████████████████████████████ │ ← Gradient top border
│                                     │
│              📊                     │ ← Large icon
│                                     │
│           1,000                     │ ← Large value (gradient text)
│                                     │
│      Total Applications             │ ← Label
│                                     │
│  Total loan applications received   │ ← Description
│                                     │
└─────────────────────────────────────┘
```

### **Chart Styling Features**
- **Color Palette**: Modern gradients (#667eea, #764ba2, #28a745, #fd7e14)
- **Typography**: Inter font family for professional appearance
- **Animations**: Smooth fade-in effects and hover transformations
- **Responsiveness**: Adapts to all screen sizes
- **Interactive Elements**: Zoom, pan, hover tooltips

---
<img width="1804" height="886" alt="Image" src="https://github.com/user-attachments/assets/1a2beb31-8828-437f-b43a-8010b9eaab53" />
<img width="1845" height="785" alt="Image" src="https://github.com/user-attachments/assets/a80394c2-92b6-40b4-8ed4-d2606250647d" />
<img width="1846" height="807" alt="Image" src="https://github.com/user-attachments/assets/beb4e483-99e8-49a4-930b-591c9380b704" />
<img width="1856" height="856" alt="Image" src="https://github.com/user-attachments/assets/17ec1158-04d9-40e3-97aa-380aa867dbd6" />
<img width="1850" height="860" alt="Image" src="https://github.com/user-attachments/assets/7b6b6466-5cca-4338-8cf0-30a9e0a4b5a0" />
<img width="1859" height="599" alt="Image" src="https://github.com/user-attachments/assets/a610e46d-9a63-4b64-a8e7-75c83484acc7" />
<img width="1863" height="837" alt="Image" src="https://github.com/user-attachments/assets/63f21824-8769-47dd-81de-9a966190a7d0" />
<img width="1875" height="897" alt="Image" src="https://github.com/user-attachments/assets/71cbb6c5-f29e-4dc0-87c6-3c8e8c514412" />

## 🚀 **Running the Dashboard**

### **Method 1: Direct Python Execution**
```bash
# Navigate to project directory
cd "Bank Loan Project"

# Activate virtual environment
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # macOS/Linux

# Run dashboard
python bank_loan_dashboard.py

# Open browser: http://127.0.0.1:8050/
```

### **Method 2: Windows Batch File**
```bash
# Double-click or run from command line
run_dashboard.bat
```

### **Method 3: PowerShell Script**
```powershell
# Run with execution policy
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\run_dashboard.ps1
```

### **Method 4: Interactive Setup**
```bash
# Guided installation and setup
python install_and_run.py
```

---

## 🔧 **Customization Options**

### **Modifying KPIs**
```python
# Add new KPI in calculate_kpis() function
def calculate_kpis():
    # ... existing KPIs ...
    
    # New KPI: Average loan amount
    avg_loan_amount = df['loan_amount'].mean()
    
    # New KPI: Portfolio growth rate
    current_month = df['issue_date'].dt.month.max()
    previous_month = current_month - 1 if current_month > 1 else 12
    
    current_month_amount = df[df['issue_date'].dt.month == current_month]['loan_amount'].sum()
    previous_month_amount = df[df['issue_date'].dt.month == previous_month]['loan_amount'].sum()
    
    growth_rate = ((current_month_amount - previous_month_amount) / previous_month_amount) * 100
    
    return {
        # ... existing KPIs ...
        'avg_loan_amount': avg_loan_amount,
        'growth_rate': growth_rate
    }
```

### **Adding New Charts**
```python
def create_custom_chart():
    """Create custom visualization"""
    # Your custom chart logic here
    fig = go.Figure()
    
    # Add traces, styling, etc.
    
    return fig

# Add to dashboard layout
html.Div([
    html.H3("🎯 Custom Analysis", className="section-title"),
    dcc.Graph(id='custom-chart', figure=create_custom_chart())
], className="chart-section")
```

### **Modifying UI Styles**
```css
/* Custom CSS in app.index_string */
.custom-card {
    background: linear-gradient(135deg, #ff6b6b, #ee5a24);
    border-radius: 25px;
    box-shadow: 0 15px 35px rgba(255, 107, 107, 0.3);
}

.custom-button {
    background: linear-gradient(135deg, #667eea, #764ba2);
    border: none;
    border-radius: 50px;
    padding: 15px 30px;
    color: white;
    font-weight: 600;
    transition: all 0.3s ease;
}
```

---

## 📊 **Business Intelligence Applications**

### **Risk Management**
- **Portfolio Risk Assessment**: Identify high-risk loan segments
- **Geographic Risk Mapping**: Regional risk concentration analysis
- **Industry Risk Monitoring**: Sector-specific risk trends

### **Performance Optimization**
- **Loan Approval Optimization**: Data-driven approval criteria
- **Interest Rate Optimization**: Market-competitive pricing
- **Collection Strategy**: Targeted collection approaches

### **Strategic Planning**
- **Market Expansion**: Geographic opportunity identification
- **Product Development**: Customer segment analysis
- **Resource Allocation**: Performance-based resource distribution

---

## 🐛 **Troubleshooting**

### **Common Issues & Solutions**

#### **Issue 1: Dashboard Won't Start**
```bash
# Error: ModuleNotFoundError: No module named 'plotly'
pip install -r requirements.txt

# Error: Port already in use
# Change port in bank_loan_dashboard.py
app.run(debug=True, host='127.0.0.1', port=8051)  # Use different port
```

#### **Issue 2: Data Loading Errors**
```python
# Check if data file exists
import os
if not os.path.exists('cleaned_financial_loan.csv'):
    print("❌ Data file not found. Run clean_data.py first.")
    
# Check data format
df = pd.read_csv('cleaned_financial_loan.csv')
print(f"Data shape: {df.shape}")
print(f"Columns: {list(df.columns)}")
```

#### **Issue 3: Chart Display Issues**
```python
# Ensure all required columns exist
required_columns = ['id', 'loan_amount', 'total_payment', 'int_rate', 'dti', 'issue_date', 'loan_status']
missing_columns = [col for col in required_columns if col not in df.columns]
if missing_columns:
    print(f"❌ Missing columns: {missing_columns}")
```

### **Performance Optimization**
```python
# For large datasets, add data sampling
if len(df) > 10000:
    df = df.sample(n=10000, random_state=42)
    print("📊 Using sample data for performance")

# Cache expensive calculations
from functools import lru_cache

@lru_cache(maxsize=128)
def calculate_kpis():
    # ... KPI calculation logic
    pass
```

---

## 🚀 **Future Enhancements**

### **Planned Features**
- **Real-time Data Updates**: Live data streaming
- **Advanced Filtering**: Interactive filters and drill-downs
- **Export Functionality**: PDF reports and data exports
- **User Authentication**: Multi-user access control
- **Mobile App**: Native mobile dashboard

### **Advanced Analytics**
- **Machine Learning**: Predictive loan default models
- **Time Series Analysis**: Advanced trend forecasting
- **Geospatial Analysis**: Interactive maps and location insights
- **Customer Segmentation**: Advanced customer profiling

---

## 🤝 **Contributing**

We welcome contributions! Here's how you can help:

### **Development Setup**
```bash
# 1. Fork the repository
# 2. Create feature branch
git checkout -b feature/amazing-feature

# 3. Make changes and test
python bank_loan_dashboard.py

# 4. Commit changes
git commit -m "Add amazing feature"

# 5. Push and create pull request
git push origin feature/amazing-feature
```

### **Contribution Areas**
- **New Visualizations**: Add innovative chart types
- **UI Improvements**: Enhance user experience
- **Performance**: Optimize data processing
- **Documentation**: Improve guides and examples
- **Testing**: Add comprehensive test coverage

---

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 **Acknowledgments**

- **Plotly**: For amazing interactive visualizations
- **Dash**: For the web dashboard framework
- **Bootstrap**: For responsive UI components
- **Inter Font**: For beautiful typography

---

## 📞 **Support & Contact**

- **Issues**: [GitHub Issues](https://github.com/yourusername/bank-loan-dashboard/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/bank-loan-dashboard/discussions)
- **Email**: your.email@example.com

---

<div align="center">

**Made with ❤️ for Data Analytics & Business Intelligence**

[⬆️ Back to Top](#-bank-loan-analytics-dashboard)

</div>
