import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
from datetime import datetime
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

# Initialize the Dash app with custom CSS
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Custom CSS for beautiful styling
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
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
            .dashboard-container {
                background: rgba(255, 255, 255, 0.95);
                backdrop-filter: blur(10px);
                border-radius: 20px;
                margin: 20px;
                box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
                overflow: hidden;
            }
            .header-section {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 40px 0;
                text-align: center;
                position: relative;
                overflow: hidden;
            }
            .header-section::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grain" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="25" cy="25" r="1" fill="white" opacity="0.1"/><circle cx="75" cy="75" r="1" fill="white" opacity="0.1"/><circle cx="50" cy="10" r="0.5" fill="white" opacity="0.1"/></pattern></defs><rect width="100" height="100" fill="url(%23grain)"/></svg>');
                opacity: 0.3;
            }
            .header-title {
                font-size: 3.5rem;
                font-weight: 700;
                margin: 0;
                text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
                position: relative;
                z-index: 1;
            }
            .header-subtitle {
                font-size: 1.2rem;
                font-weight: 300;
                margin: 10px 0 0 0;
                opacity: 0.9;
                position: relative;
                z-index: 1;
            }
            .kpi-card {
                background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
                border: none;
                border-radius: 20px;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
                transition: all 0.3s ease;
                overflow: hidden;
                position: relative;
            }
            .kpi-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
            }
            .kpi-card::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                height: 4px;
                background: linear-gradient(90deg, #667eea, #764ba2);
            }
            .kpi-icon {
                font-size: 2.5rem;
                margin-bottom: 15px;
                display: block;
            }
            .kpi-value {
                font-size: 2.5rem;
                font-weight: 700;
                margin: 10px 0;
                background: linear-gradient(135deg, #667eea, #764ba2);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            }
            .kpi-label {
                font-size: 1rem;
                font-weight: 500;
                color: #6c757d;
                margin: 0;
            }
            .kpi-description {
                font-size: 0.9rem;
                color: #adb5bd;
                margin: 5px 0 0 0;
            }
            .chart-section {
                background: white;
                border-radius: 20px;
                padding: 30px;
                margin: 20px 0;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05);
                border: 1px solid #f1f3f4;
            }
            .section-title {
                font-size: 1.8rem;
                font-weight: 600;
                color: #2c3e50;
                margin-bottom: 20px;
                display: flex;
                align-items: center;
                gap: 10px;
            }
            .section-icon {
                font-size: 2rem;
                background: linear-gradient(135deg, #667eea, #764ba2);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            }
            .footer {
                background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
                color: white;
                text-align: center;
                padding: 30px;
                margin-top: 40px;
                border-radius: 0 0 20px 20px;
            }
            .metric-badge {
                display: inline-block;
                padding: 4px 12px;
                border-radius: 20px;
                font-size: 0.8rem;
                font-weight: 500;
                margin: 2px;
            }
            .metric-positive { background: linear-gradient(135deg, #28a745, #20c997); color: white; }
            .metric-warning { background: linear-gradient(135deg, #ffc107, #fd7e14); color: white; }
            .metric-danger { background: linear-gradient(135deg, #dc3545, #e83e8c); color: white; }
            .metric-info { background: linear-gradient(135deg, #17a2b8, #6f42c1); color: white; }
            .metric-primary { background: linear-gradient(135deg, #007bff, #6610f2); color: white; }
            .metric-secondary { background: linear-gradient(135deg, #6c757d, #495057); color: white; }
            .metric-dark { background: linear-gradient(135deg, #343a40, #212529); color: white; }
            
            @keyframes fadeInUp {
                from {
                    opacity: 0;
                    transform: translateY(30px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
            .animate-fade-in {
                animation: fadeInUp 0.6s ease-out;
            }
            
            .stats-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 20px;
                margin: 20px 0;
            }
            
            .quick-stats {
                background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
                border-radius: 15px;
                padding: 20px;
                text-align: center;
                border: 1px solid #dee2e6;
            }
            
            .quick-stats-value {
                font-size: 2rem;
                font-weight: 700;
                color: #495057;
                margin: 10px 0;
            }
            
            .quick-stats-label {
                font-size: 0.9rem;
                color: #6c757d;
                font-weight: 500;
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

# Calculate KPIs
def calculate_kpis():
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
    
    good_loan_amount = good_loans['loan_amount'].sum()
    bad_loan_amount = bad_loans['loan_amount'].sum()
    
    # MTD and PMTD calculations (assuming current month is December)
    current_month = 12
    previous_month = 11
    
    mtd_applications = len(df[df['issue_date'].dt.month == current_month])
    pmtd_applications = len(df[df['issue_date'].dt.month == previous_month])
    
    mtd_funded = df[df['issue_date'].dt.month == current_month]['loan_amount'].sum()
    pmtd_funded = df[df['issue_date'].dt.month == previous_month]['loan_amount'].sum()
    
    mtd_received = df[df['issue_date'].dt.month == current_month]['total_payment'].sum()
    pmtd_received = df[df['issue_date'].dt.month == previous_month]['total_payment'].sum()
    
    return {
        'total_applications': total_applications,
        'total_funded': total_funded,
        'total_received': total_received,
        'avg_interest_rate': avg_interest_rate,
        'avg_dti': avg_dti,
        'good_loan_percentage': good_loan_percentage,
        'bad_loan_percentage': bad_loan_percentage,
        'good_loan_amount': good_loan_amount,
        'bad_loan_amount': bad_loan_amount,
        'mtd_applications': mtd_applications,
        'pmtd_applications': pmtd_applications,
        'mtd_funded': mtd_funded,
        'pmtd_funded': pmtd_funded,
        'mtd_received': mtd_received,
        'pmtd_received': pmtd_received
    }

# Create enhanced visualizations with beautiful colors
def create_monthly_trend_chart():
    monthly_data = df.groupby(df['issue_date'].dt.to_period('M')).agg({
        'id': 'count',
        'loan_amount': 'sum',
        'total_payment': 'sum'
    }).reset_index()
    
    monthly_data['issue_date'] = monthly_data['issue_date'].astype(str)
    
    fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=('📊 Monthly Loan Applications', '💰 Monthly Amounts ($)'),
        vertical_spacing=0.15
    )
    
    fig.add_trace(
        go.Bar(x=monthly_data['issue_date'], y=monthly_data['id'], 
               name='Applications', marker_color='#667eea',
               marker_line_color='#764ba2', marker_line_width=2),
        row=1, col=1
    )
    
    fig.add_trace(
        go.Scatter(x=monthly_data['issue_date'], y=monthly_data['loan_amount'], 
                   name='Funded Amount', line=dict(color='#28a745', width=4),
                   mode='lines+markers', marker=dict(size=8, color='#28a745')),
        row=2, col=1
    )
    
    fig.add_trace(
        go.Scatter(x=monthly_data['issue_date'], y=monthly_data['total_payment'], 
                   name='Amount Received', line=dict(color='#fd7e14', width=4),
                   mode='lines+markers', marker=dict(size=8, color='#fd7e14')),
        row=2, col=1
    )
    
    fig.update_layout(
        height=600, 
        showlegend=True, 
        title_text="📈 Monthly Trends Analysis",
        title_font_size=20,
        title_font_color='#2c3e50',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Inter", size=12)
    )
    
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgba(0,0,0,0.1)')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(0,0,0,0.1)')
    
    return fig

def create_loan_status_chart():
    status_data = df.groupby('loan_status').agg({
        'id': 'count',
        'loan_amount': 'sum',
        'total_payment': 'sum',
        'int_rate': 'mean',
        'dti': 'mean'
    }).reset_index()
    
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('🏦 Loan Count by Status', '💵 Funded Amount by Status', 
                       '📊 Interest Rate by Status', '⚖️ DTI by Status'),
        specs=[[{"type": "pie"}, {"type": "bar"}],
               [{"type": "bar"}, {"type": "bar"}]],
        vertical_spacing=0.12,
        horizontal_spacing=0.1
    )
    
    # Beautiful color palette
    colors = ['#667eea', '#764ba2', '#f093fb', '#f5576c', '#4facfe', '#00f2fe']
    
    # Pie chart for loan count
    fig.add_trace(
        go.Pie(labels=status_data['loan_status'], values=status_data['id'],
               name="Loan Count", marker_colors=colors[:len(status_data)],
               textinfo='label+percent', textposition='inside'),
        row=1, col=1
    )
    
    # Bar chart for funded amount
    fig.add_trace(
        go.Bar(x=status_data['loan_status'], y=status_data['loan_amount'],
               name="Funded Amount", marker_color='#28a745',
               marker_line_color='#20c997', marker_line_width=2),
        row=1, col=2
    )
    
    # Bar chart for interest rate
    fig.add_trace(
        go.Bar(x=status_data['loan_status'], y=status_data['int_rate']*100,
               name="Interest Rate (%)", marker_color='#fd7e14',
               marker_line_color='#ffc107', marker_line_width=2),
        row=2, col=1
    )
    
    # Bar chart for DTI
    fig.add_trace(
        go.Bar(x=status_data['loan_status'], y=status_data['dti']*100,
               name="DTI (%)", marker_color='#6f42c1',
               marker_line_color='#e83e8c', marker_line_width=2),
        row=2, col=2
    )
    
    fig.update_layout(
        height=700, 
        showlegend=False, 
        title_text="🔍 Loan Status Analysis",
        title_font_size=20,
        title_font_color='#2c3e50',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Inter", size=12)
    )
    
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgba(0,0,0,0.1)')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(0,0,0,0.1)')
    
    return fig

def create_geographic_chart():
    state_data = df.groupby('address_state').agg({
        'id': 'count',
        'loan_amount': 'sum',
        'total_payment': 'sum'
    }).reset_index()
    
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=('🌍 Loan Applications by State', '💰 Amounts by State'),
        specs=[[{"type": "bar"}, {"type": "bar"}]],
        horizontal_spacing=0.1
    )
    
    fig.add_trace(
        go.Bar(x=state_data['address_state'], y=state_data['id'],
               name="Applications", marker_color='#20c997',
               marker_line_color='#28a745', marker_line_width=2),
        row=1, col=1
    )
    
    fig.add_trace(
        go.Bar(x=state_data['address_state'], y=state_data['loan_amount'],
               name="Funded Amount", marker_color='#ffc107',
               marker_line_color='#fd7e14', marker_line_width=2),
        row=1, col=2
    )
    
    fig.update_layout(
        height=500, 
        showlegend=True, 
        title_text="🌍 Geographic Analysis by State",
        title_font_size=20,
        title_font_color='#2c3e50',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Inter", size=12)
    )
    
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgba(0,0,0,0.1)')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(0,0,0,0.1)')
    
    return fig

def create_categorical_charts():
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
        subplot_titles=('🎯 Top 10 Loan Purposes', '⏰ Loan Distribution by Term',
                       '👔 Employee Length Analysis', '🏠 Home Ownership Analysis'),
        specs=[[{"type": "bar"}, {"type": "pie"}],
               [{"type": "bar"}, {"type": "bar"}]],
        vertical_spacing=0.12,
        horizontal_spacing=0.1
    )
    
    # Beautiful colors
    colors = ['#667eea', '#764ba2', '#f093fb', '#f5576c', '#4facfe', '#00f2fe', '#43e97b', '#38f9d7', '#fa709a', '#fee140']
    
    # Purpose bar chart
    fig.add_trace(
        go.Bar(x=purpose_data['purpose'], y=purpose_data['id'],
               name="Applications", marker_color=colors[:len(purpose_data)],
               marker_line_color='#495057', marker_line_width=1),
        row=1, col=1
    )
    
    # Term pie chart
    fig.add_trace(
        go.Pie(labels=term_data['term'], values=term_data['id'],
               name="Term Distribution", marker_colors=colors[:len(term_data)],
               textinfo='label+percent', textposition='inside'),
        row=1, col=2
    )
    
    # Employee length bar chart
    fig.add_trace(
        go.Bar(x=emp_data['emp_length'], y=emp_data['id'],
               name="Applications", marker_color='#28a745',
               marker_line_color='#20c997', marker_line_width=2),
        row=2, col=1
    )
    
    # Home ownership bar chart
    fig.add_trace(
        go.Bar(x=home_data['home_ownership'], y=home_data['id'],
               name="Applications", marker_color='#6f42c1',
               marker_line_color='#e83e8c', marker_line_width=2),
        row=2, col=2
    )
    
    fig.update_layout(
        height=800, 
        showlegend=False, 
        title_text="📊 Categorical Analysis",
        title_font_size=20,
        title_font_color='#2c3e50',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Inter", size=12)
    )
    
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgba(0,0,0,0.1)')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(0,0,0,0.1)')
    
    return fig

def create_good_vs_bad_loan_chart():
    good_loans = df[df['loan_status'].isin(['Fully Paid', 'Current'])]
    bad_loans = df[df['loan_status'] == 'Charged Off']
    
    # Create comparison data
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
        subplot_titles=('📊 Loan Count Comparison', '💰 Amount Comparison', '📈 Percentage Distribution'),
        specs=[[{"type": "bar"}, {"type": "bar"}, {"type": "pie"}]],
        horizontal_spacing=0.1
    )
    
    # Count comparison
    fig.add_trace(
        go.Bar(x=comparison_data['Category'], y=comparison_data['Count'],
               marker_color=['#28a745', '#dc3545'],
               marker_line_color=['#20c997', '#e83e8c'], marker_line_width=2),
        row=1, col=1
    )
    
    # Amount comparison
    fig.add_trace(
        go.Bar(x=comparison_data['Category'], y=comparison_data['Amount'],
               marker_color=['#28a745', '#dc3545'],
               marker_line_color=['#20c997', '#e83e8c'], marker_line_width=2),
        row=1, col=2
    )
    
    # Percentage pie chart
    fig.add_trace(
        go.Pie(labels=comparison_data['Category'], values=comparison_data['Percentage'],
               marker_colors=['#28a745', '#dc3545'],
               textinfo='label+percent', textposition='inside'),
        row=1, col=3
    )
    
    fig.update_layout(
        height=500, 
        showlegend=False, 
        title_text="✅ Good vs Bad Loan Analysis",
        title_font_size=20,
        title_font_color='#2c3e50',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Inter", size=12)
    )
    
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgba(0,0,0,0.1)')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(0,0,0,0.1)')
    
    return fig



# App layout with beautiful UI
app.layout = html.Div([
    # Header Section
    html.Div([
        html.H1("🏦 Bank Loan Analytics Dashboard", className="header-title"),
        html.P("Comprehensive Financial Analytics & Performance Insights", className="header-subtitle")
    ], className="header-section"),
    
    # Main Dashboard Container
    html.Div([
        # KPI Cards Row 1
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Span("📊", className="kpi-icon"),
                        html.H2(f"{calculate_kpis()['total_applications']:,}", className="kpi-value"),
                        html.H4("Total Applications", className="kpi-label"),
                        html.P("Total loan applications received", className="kpi-description")
                    ])
                ], className="kpi-card h-100")
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Span("💰", className="kpi-icon"),
                        html.H2(f"${calculate_kpis()['total_funded']:,.0f}", className="kpi-value"),
                        html.H4("Total Funded", className="kpi-label"),
                        html.P("Total amount funded across all loans", className="kpi-description")
                    ])
                ], className="kpi-card h-100")
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Span("💵", className="kpi-icon"),
                        html.H2(f"${calculate_kpis()['total_received']:,.0f}", className="kpi-value"),
                        html.H4("Total Received", className="kpi-label"),
                        html.P("Total amount received from borrowers", className="kpi-description")
                    ])
                ], className="kpi-card h-100")
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Span("📈", className="kpi-icon"),
                        html.H2(f"{calculate_kpis()['good_loan_percentage']:.1f}%", className="kpi-value"),
                        html.H4("Good Loan %", className="kpi-label"),
                        html.P("Percentage of performing loans", className="kpi-description")
                    ])
                ], className="kpi-card h-100")
            ], width=3)
        ], className="mb-4"),
        
        # KPI Cards Row 2
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Span("🎯", className="kpi-icon"),
                        html.H2(f"{calculate_kpis()['mtd_applications']:,}", className="kpi-value"),
                        html.H4("MTD Applications", className="kpi-label"),
                        html.P("Month-to-date applications", className="kpi-description")
                    ])
                ], className="kpi-card h-100")
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Span("📊", className="kpi-icon"),
                        html.H2(f"{calculate_kpis()['avg_interest_rate']:.2f}%", className="kpi-value"),
                        html.H4("Avg Interest Rate", className="kpi-label"),
                        html.P("Average interest rate across all loans", className="kpi-description")
                    ])
                ], className="kpi-card h-100")
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Span("⚖️", className="kpi-icon"),
                        html.H2(f"{calculate_kpis()['avg_dti']:.1f}%", className="kpi-value"),
                        html.H4("Avg DTI Ratio", className="kpi-label"),
                        html.P("Average debt-to-income ratio", className="kpi-description")
                    ])
                ], className="kpi-card h-100")
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Span("📉", className="kpi-icon"),
                        html.H2(f"{calculate_kpis()['bad_loan_percentage']:.1f}%", className="kpi-value"),
                        html.H4("Bad Loan %", className="kpi-label"),
                        html.P("Percentage of charged-off loans", className="kpi-description")
                    ])
                ], className="kpi-card h-100")
            ], width=3)
        ], className="mb-4"),
        
        # Quick Stats Section
        html.Div([
            html.H3("📊 Quick Statistics", className="section-title"),
            html.Div([
                html.Div([
                    html.Div(f"{calculate_kpis()['mtd_funded']:,.0f}", className="quick-stats-value"),
                    html.Div("MTD Funded ($)", className="quick-stats-label")
                ], className="quick-stats"),
                html.Div([
                    html.Div(f"{calculate_kpis()['mtd_received']:,.0f}", className="quick-stats-value"),
                    html.Div("MTD Received ($)", className="quick-stats-label")
                ], className="quick-stats"),
                html.Div([
                    html.Div(f"{calculate_kpis()['pmtd_applications']:,}", className="quick-stats-value"),
                    html.Div("PMTD Applications", className="quick-stats-label")
                ], className="quick-stats"),
                html.Div([
                    html.Div(f"{calculate_kpis()['good_loan_amount']:,.0f}", className="quick-stats-value"),
                    html.Div("Good Loan Amount ($)", className="quick-stats-label")
                ], className="quick-stats")
            ], className="stats-grid")
        ], className="chart-section"),
        
        # Charts Section
        html.Div([
            html.H3("📈 Monthly Trends Analysis", className="section-title"),
            dcc.Graph(id='monthly-trend-chart', figure=create_monthly_trend_chart())
        ], className="chart-section"),
        
        html.Div([
            html.H3("🔍 Loan Status Analysis", className="section-title"),
            dcc.Graph(id='loan-status-chart', figure=create_loan_status_chart())
        ], className="chart-section"),
        
        html.Div([
            html.H3("🌍 Geographic Analysis", className="section-title"),
            dcc.Graph(id='geographic-chart', figure=create_geographic_chart())
        ], className="chart-section"),
        
        html.Div([
            html.H3("✅ Good vs Bad Loan Analysis", className="section-title"),
            dcc.Graph(id='good-vs-bad-chart', figure=create_good_vs_bad_loan_chart())
        ], className="chart-section"),
        
        html.Div([
            html.H3("📊 Categorical Analysis", className="section-title"),
            dcc.Graph(id='categorical-chart', figure=create_categorical_charts())
        ], className="chart-section"),
        
        # Footer
        html.Div([
            html.Hr(style={'borderColor': 'rgba(255,255,255,0.2)'}),
            html.P("🏦 Dashboard created based on SQL KPI queries from Bank Loan Project", 
                   style={'margin': '0', 'fontSize': '1.1rem'}),
            html.P("📊 Interactive Analytics Dashboard with Beautiful UI", 
                   style={'margin': '10px 0 0 0', 'opacity': '0.8'})
        ], className="footer")
        
    ], className="dashboard-container")
    
], className="animate-fade-in")

if __name__ == '__main__':
    print("Starting Beautiful Bank Loan Dashboard...")
    print("Open your browser and go to: http://127.0.0.1:8050/")
    app.run(debug=True, host='127.0.0.1', port=8050)
