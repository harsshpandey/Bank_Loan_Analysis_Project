import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np

# Load the cleaned data
try:
    df = pd.read_csv('cleaned_financial_loan.csv')
    # Convert date columns back to datetime
    date_columns = ['issue_date', 'last_credit_pull_date', 'last_payment_date', 'next_payment_date']
    for col in date_columns:
        df[col] = pd.to_datetime(df[col], errors='coerce')
    print("Data loaded successfully!")
except Exception as e:
    print(f"Error loading data: {e}")
    print("Creating sample data for demonstration...")
    # Create sample data for demonstration
    np.random.seed(42)
    n = 1000
    df = pd.DataFrame({
        'id': range(1, n+1),
        'loan_amount': np.random.uniform(5000, 50000, n),
        'total_payment': np.random.uniform(6000, 60000, n),
        'int_rate': np.random.uniform(0.05, 0.25, n),
        'dti': np.random.uniform(0.1, 0.8, n),
        'issue_date': pd.date_range('2023-01-01', periods=n, freq='D'),
        'loan_status': np.random.choice(['Fully Paid', 'Current', 'Charged Off'], n, p=[0.6, 0.3, 0.1]),
        'address_state': np.random.choice(['CA', 'TX', 'NY', 'FL', 'IL'], n),
        'term': np.random.choice(['36 months', '60 months'], n),
        'emp_length': np.random.choice(['< 1 year', '1 year', '2 years', '3 years', '4 years', '5 years', '6 years', '7 years', '8 years', '9 years', '10+ years'], n),
        'purpose': np.random.choice(['debt_consolidation', 'credit_card', 'home_improvement', 'major_purchase', 'medical', 'car', 'vacation', 'wedding'], n),
        'home_ownership': np.random.choice(['RENT', 'OWN', 'MORTGAGE'], n)
    })

print(f"Dataset shape: {df.shape}")
print(f"Columns: {list(df.columns)}")

# 1. KPI Summary Chart
def create_kpi_summary():
    """Create a summary chart showing key KPIs"""
    kpis = {
        'Metric': ['Total Applications', 'Total Funded ($)', 'Total Received ($)', 'Good Loan %', 'Bad Loan %', 'Avg Interest Rate %', 'Avg DTI %'],
        'Value': [
            len(df),
            df['loan_amount'].sum(),
            df['total_payment'].sum(),
            (len(df[df['loan_status'].isin(['Fully Paid', 'Current'])] / len(df)) * 100,
            (len(df[df['loan_status'] == 'Charged Off']) / len(df)) * 100,
            df['int_rate'].mean() * 100,
            df['dti'].mean() * 100
        ]
    }
    
    kpi_df = pd.DataFrame(kpis)
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=kpi_df['Metric'],
        y=kpi_df['Value'],
        marker_color=['#1f77b4', '#2ca02c', '#ff7f0e', '#d62728', '#9467bd', '#8c564b', '#e377c2']
    ))
    
    fig.update_layout(
        title="Key Performance Indicators Summary",
        xaxis_title="Metrics",
        yaxis_title="Values",
        height=500,
        showlegend=False
    )
    
    fig.write_html("kpi_summary.html")
    print("✅ KPI Summary chart saved as 'kpi_summary.html'")
    return fig

# 2. Monthly Trends Chart
def create_monthly_trends():
    """Create monthly trends chart"""
    monthly_data = df.groupby(df['issue_date'].dt.to_period('M')).agg({
        'id': 'count',
        'loan_amount': 'sum',
        'total_payment': 'sum'
    }).reset_index()
    
    monthly_data['issue_date'] = monthly_data['issue_date'].astype(str)
    
    fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=('Monthly Loan Applications', 'Monthly Amounts ($)'),
        vertical_spacing=0.1
    )
    
    fig.add_trace(
        go.Bar(x=monthly_data['issue_date'], y=monthly_data['id'], 
               name='Applications', marker_color='skyblue'),
        row=1, col=1
    )
    
    fig.add_trace(
        go.Scatter(x=monthly_data['issue_date'], y=monthly_data['loan_amount'], 
                  name='Funded Amount', line=dict(color='green')),
        row=2, col=1
    )
    
    fig.add_trace(
        go.Scatter(x=monthly_data['issue_date'], y=monthly_data['total_payment'], 
                  name='Amount Received', line=dict(color='orange')),
        row=2, col=1
    )
    
    fig.update_layout(height=600, showlegend=True, title_text="Monthly Trends Analysis")
    fig.write_html("monthly_trends.html")
    print("✅ Monthly Trends chart saved as 'monthly_trends.html'")
    return fig

# 3. Loan Status Analysis
def create_loan_status_analysis():
    """Create comprehensive loan status analysis"""
    status_data = df.groupby('loan_status').agg({
        'id': 'count',
        'loan_amount': 'sum',
        'total_payment': 'sum',
        'int_rate': 'mean',
        'dti': 'mean'
    }).reset_index()
    
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Loan Count by Status', 'Funded Amount by Status', 
                       'Interest Rate by Status', 'DTI by Status'),
        specs=[[{"type": "pie"}, {"type": "bar"}],
               [{"type": "bar"}, {"type": "bar"}]]
    )
    
    # Pie chart for loan count
    fig.add_trace(
        go.Pie(labels=status_data['loan_status'], values=status_data['id'],
               name="Loan Count"),
        row=1, col=1
    )
    
    # Bar chart for funded amount
    fig.add_trace(
        go.Bar(x=status_data['loan_status'], y=status_data['loan_amount'],
               name="Funded Amount", marker_color='lightgreen'),
        row=1, col=2
    )
    
    # Bar chart for interest rate
    fig.add_trace(
        go.Bar(x=status_data['loan_status'], y=status_data['int_rate']*100,
               name="Interest Rate (%)", marker_color='lightcoral'),
        row=2, col=1
    )
    
    # Bar chart for DTI
    fig.add_trace(
        go.Bar(x=status_data['loan_status'], y=status_data['dti']*100,
               name="DTI (%)", marker_color='lightblue'),
        row=2, col=2
    )
    
    fig.update_layout(height=700, showlegend=False, title_text="Loan Status Analysis")
    fig.write_html("loan_status_analysis.html")
    print("✅ Loan Status Analysis chart saved as 'loan_status_analysis.html'")
    return fig

# 4. Geographic Analysis
def create_geographic_analysis():
    """Create geographic analysis charts"""
    state_data = df.groupby('address_state').agg({
        'id': 'count',
        'loan_amount': 'sum',
        'total_payment': 'sum'
    }).reset_index()
    
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=('Loan Applications by State', 'Amounts by State'),
        specs=[[{"type": "bar"}, {"type": "bar"}]]
    )
    
    fig.add_trace(
        go.Bar(x=state_data['address_state'], y=state_data['id'],
               name="Applications", marker_color='lightseagreen'),
        row=1, col=1
    )
    
    fig.add_trace(
        go.Bar(x=state_data['address_state'], y=state_data['loan_amount'],
               name="Funded Amount", marker_color='gold'),
        row=1, col=2
    )
    
    fig.update_layout(height=500, showlegend=True, title_text="Geographic Analysis by State")
    fig.write_html("geographic_analysis.html")
    print("✅ Geographic Analysis chart saved as 'geographic_analysis.html'")
    return fig

# 5. Good vs Bad Loan Analysis
def create_good_vs_bad_analysis():
    """Create good vs bad loan comparison"""
    good_loans = df[df['loan_status'].isin(['Fully Paid', 'Current'])]
    bad_loans = df[df['loan_status'] == 'Charged Off']
    
    comparison_data = pd.DataFrame({
        'Category': ['Good Loans', 'Bad Loans'],
        'Count': [len(good_loans), len(bad_loans)],
        'Amount': [good_loans['loan_amount'].sum(), bad_loans['loan_amount'].sum()],
        'Percentage': [
            (len(good_loans) / len(df)) * 100,
            (len(bad_loans) / len(df)) * 100
        ]
    })
    
    fig = make_subplots(
        rows=1, cols=3,
        subplot_titles=('Loan Count Comparison', 'Amount Comparison', 'Percentage Distribution'),
        specs=[[{"type": "bar"}, {"type": "bar"}, {"type": "pie"}]]
    )
    
    # Count comparison
    fig.add_trace(
        go.Bar(x=comparison_data['Category'], y=comparison_data['Count'],
               marker_color=['lightgreen', 'lightcoral']),
        row=1, col=1
    )
    
    # Amount comparison
    fig.add_trace(
        go.Bar(x=comparison_data['Category'], y=comparison_data['Amount'],
               marker_color=['lightgreen', 'lightcoral']),
        row=1, col=2
    )
    
    # Percentage pie chart
    fig.add_trace(
        go.Pie(labels=comparison_data['Category'], values=comparison_data['Percentage'],
               marker_colors=['lightgreen', 'lightcoral']),
        row=1, col=3
    )
    
    fig.update_layout(height=500, showlegend=False, title_text="Good vs Bad Loan Analysis")
    fig.write_html("good_vs_bad_analysis.html")
    print("✅ Good vs Bad Loan Analysis chart saved as 'good_vs_bad_analysis.html'")
    return fig

# 6. Categorical Analysis
def create_categorical_analysis():
    """Create categorical analysis charts"""
    # Purpose analysis
    purpose_data = df.groupby('purpose').agg({
        'id': 'count',
        'loan_amount': 'sum'
    }).reset_index().sort_values('id', ascending=False).head(10)
    
    # Term analysis
    term_data = df.groupby('term').agg({
        'id': 'count',
        'loan_amount': 'sum'
    }).reset_index()
    
    # Employee length analysis
    emp_data = df.groupby('emp_length').agg({
        'id': 'count',
        'loan_amount': 'sum'
    }).reset_index()
    
    # Home ownership analysis
    home_data = df.groupby('home_ownership').agg({
        'id': 'count',
        'loan_amount': 'sum'
    }).reset_index()
    
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Top 10 Loan Purposes', 'Loan Distribution by Term',
                       'Employee Length Analysis', 'Home Ownership Analysis'),
        specs=[[{"type": "bar"}, {"type": "pie"}],
               [{"type": "bar"}, {"type": "bar"}]]
    )
    
    # Purpose bar chart
    fig.add_trace(
        go.Bar(x=purpose_data['purpose'], y=purpose_data['id'],
               name="Applications", marker_color='lightcoral'),
        row=1, col=1
    )
    
    # Term pie chart
    fig.add_trace(
        go.Pie(labels=term_data['term'], values=term_data['id'],
               name="Term Distribution"),
        row=1, col=2
    )
    
    # Employee length bar chart
    fig.add_trace(
        go.Bar(x=emp_data['emp_length'], y=emp_data['id'],
               name="Applications", marker_color='lightgreen'),
        row=2, col=1
    )
    
    # Home ownership bar chart
    fig.add_trace(
        go.Bar(x=home_data['home_ownership'], y=home_data['id'],
               name="Applications", marker_color='lightblue'),
        row=2, col=2
    )
    
    fig.update_layout(height=800, showlegend=False, title_text="Categorical Analysis")
    fig.write_html("categorical_analysis.html")
    print("✅ Categorical Analysis chart saved as 'categorical_analysis.html'")
    return fig

# 7. Risk Analysis Dashboard
def create_risk_analysis():
    """Create risk analysis dashboard"""
    # Interest rate distribution
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Interest Rate Distribution', 'DTI Distribution', 
                       'Loan Amount vs Interest Rate', 'Risk Matrix'),
        specs=[[{"type": "histogram"}, {"type": "histogram"}],
               [{"type": "scatter"}, {"type": "scatter"}]]
    )
    
    # Interest rate histogram
    fig.add_trace(
        go.Histogram(x=df['int_rate']*100, nbinsx=30, name="Interest Rate %",
                    marker_color='lightcoral'),
        row=1, col=1
    )
    
    # DTI histogram
    fig.add_trace(
        go.Histogram(x=df['dti']*100, nbinsx=30, name="DTI %",
                    marker_color='lightblue'),
        row=1, col=2
    )
    
    # Scatter plot: Loan Amount vs Interest Rate
    fig.add_trace(
        go.Scatter(x=df['loan_amount'], y=df['int_rate']*100, mode='markers',
                  name="Amount vs Rate", marker=dict(color='green', size=3, opacity=0.6)),
        row=2, col=1
    )
    
    # Risk matrix: DTI vs Interest Rate
    fig.add_trace(
        go.Scatter(x=df['dti']*100, y=df['int_rate']*100, mode='markers',
                  name="DTI vs Rate", marker=dict(color='red', size=3, opacity=0.6)),
        row=2, col=2
    )
    
    fig.update_layout(height=700, showlegend=False, title_text="Risk Analysis Dashboard")
    fig.write_html("risk_analysis.html")
    print("✅ Risk Analysis Dashboard saved as 'risk_analysis.html'")
    return fig

# Main execution
if __name__ == "__main__":
    print("🚀 Generating Bank Loan Analytics Charts...")
    print("=" * 50)
    
    # Generate all charts
    create_kpi_summary()
    create_monthly_trends()
    create_loan_status_analysis()
    create_geographic_analysis()
    create_good_vs_bad_analysis()
    create_categorical_analysis()
    create_risk_analysis()
    
    print("=" * 50)
    print("🎉 All charts generated successfully!")
    print("📁 Check your current directory for the HTML files")
    print("🌐 Open any HTML file in your web browser to view the interactive charts")
    print("\n📊 Generated Charts:")
    print("  • kpi_summary.html - Key Performance Indicators")
    print("  • monthly_trends.html - Monthly Trends Analysis")
    print("  • loan_status_analysis.html - Loan Status Analysis")
    print("  • geographic_analysis.html - Geographic Analysis")
    print("  • good_vs_bad_analysis.html - Good vs Bad Loan Analysis")
    print("  • categorical_analysis.html - Categorical Analysis")
    print("  • risk_analysis.html - Risk Analysis Dashboard")
