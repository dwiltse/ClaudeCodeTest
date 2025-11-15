"""
Databricks Survey Analysis Notebook
Real-time survey data analysis and visualization

This file is designed to be imported into Databricks as a notebook.
Each section can be run as a separate cell.
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import json

# For Databricks
try:
    import pyspark  # noqa: F401
    IN_DATABRICKS = True
except ImportError:
    IN_DATABRICKS = False


# CELL 1: Install Required Libraries
# ==================================
# Run this first in Databricks
"""
%pip install gspread google-auth pandas plotly
"""


# CELL 2: Configuration
# ====================
# Update these with your actual values

# Option 1: Using Databricks Secrets (Recommended)
if IN_DATABRICKS:
    CREDENTIALS_JSON = dbutils.secrets.get(scope="google-api", key="credentials")  # noqa: F821
    SPREADSHEET_ID = dbutils.secrets.get(scope="google-api", key="spreadsheet-id")  # noqa: F821
else:
    # Option 2: For local testing (NOT for production)
    CREDENTIALS_JSON = """
    {
        "type": "service_account",
        "project_id": "your-project-id",
        "private_key_id": "your-key-id",
        "private_key": "your-private-key",
        "client_email": "your-service-account@project.iam.gserviceaccount.com",
        "client_id": "your-client-id",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token"
    }
    """
    SPREADSHEET_ID = "your-spreadsheet-id-here"


# CELL 4: Data Ingestion Function
# ===============================
def fetch_survey_data():
    """Fetch survey data from Google Sheets."""
    import gspread
    from google.oauth2.service_account import Credentials

    # Authenticate
    scopes = [
        'https://www.googleapis.com/auth/spreadsheets.readonly',
        'https://www.googleapis.com/auth/drive.readonly'
    ]

    creds_dict = json.loads(CREDENTIALS_JSON)
    creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)
    client = gspread.authorize(creds)

    # Open spreadsheet and get data
    spreadsheet = client.open_by_key(SPREADSHEET_ID)
    worksheet = spreadsheet.worksheet("Form Responses 1")
    data = worksheet.get_all_records()

    # Convert to DataFrame
    df = pd.DataFrame(data)

    # Parse timestamp if exists
    if 'Timestamp' in df.columns:
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])

    return df


# CELL 5: Fetch Data
# ==================
print("Fetching survey data from Google Sheets...")
df = fetch_survey_data()

print(f"Total responses: {len(df)}")
print(f"Columns: {list(df.columns)}")
print("\nFirst few responses:")
display(df.head())  # noqa: F821

# Convert to Spark DataFrame if in Databricks
if IN_DATABRICKS:
    spark_df = spark.createDataFrame(df)  # noqa: F821
    spark_df.createOrReplaceTempView("survey_responses")
    print("\nCreated temporary view: survey_responses")


# CELL 6: Basic Statistics
# ========================
print("=== Survey Statistics ===")
print(f"Total Responses: {len(df)}")

if 'Timestamp' in df.columns:
    print(f"First Response: {df['Timestamp'].min()}")
    print(f"Latest Response: {df['Timestamp'].max()}")
    print(f"Time Range: {df['Timestamp'].max() - df['Timestamp'].min()}")

    # Responses in last 5 minutes
    recent = df[df['Timestamp'] > (datetime.now() - timedelta(minutes=5))]
    print(f"Responses in last 5 minutes: {len(recent)}")

print("\nResponse rate over time:")
if 'Timestamp' in df.columns:
    df['Hour'] = df['Timestamp'].dt.floor('H')
    hourly_counts = df.groupby('Hour').size()
    print(hourly_counts)


# CELL 7: Visualization - Response Timeline
# =========================================
def plot_response_timeline(df):
    """Plot responses over time."""
    if 'Timestamp' not in df.columns:
        print("No timestamp column found")
        return

    # Create cumulative count
    df_sorted = df.sort_values('Timestamp')
    df_sorted['Cumulative_Count'] = range(1, len(df_sorted) + 1)

    fig = px.line(
        df_sorted,
        x='Timestamp',
        y='Cumulative_Count',
        title='Survey Responses Over Time',
        labels={'Cumulative_Count': 'Total Responses', 'Timestamp': 'Time'}
    )

    fig.update_layout(
        hovermode='x unified',
        height=400
    )

    return fig


# Display the plot
fig_timeline = plot_response_timeline(df)
if fig_timeline:
    fig_timeline.show()


# CELL 8: Visualization - Experience Level Distribution
# ====================================================
# Adjust column name to match your actual form question
EXPERIENCE_COLUMN = 'Experience Level'  # Change this to your actual column name


def plot_experience_distribution(df, column_name):
    """Plot distribution of experience levels."""
    if column_name not in df.columns:
        print(f"Column '{column_name}' not found. Available columns: {list(df.columns)}")
        return

    counts = df[column_name].value_counts()

    fig = px.bar(
        x=counts.index,
        y=counts.values,
        title=f'Distribution of {column_name}',
        labels={'x': column_name, 'y': 'Number of Responses'},
        color=counts.values,
        color_continuous_scale='viridis'
    )

    fig.update_layout(showlegend=False, height=400)
    return fig


# Display the plot
if EXPERIENCE_COLUMN in df.columns:
    fig_exp = plot_experience_distribution(df, EXPERIENCE_COLUMN)
    if fig_exp:
        fig_exp.show()


# CELL 9: Visualization - Technology Interest
# ===========================================
# Adjust to your actual column name
TECH_INTEREST_COLUMN = 'Primary Technology Interest'


def plot_technology_interest(df, column_name):
    """Plot technology interest as a pie chart."""
    if column_name not in df.columns:
        print(f"Column '{column_name}' not found.")
        return

    # Handle multiple selections (if checkboxes were used)
    # This splits comma-separated values
    all_interests = []
    for response in df[column_name].dropna():
        if isinstance(response, str):
            interests = [x.strip() for x in response.split(',')]
            all_interests.extend(interests)

    interest_counts = pd.Series(all_interests).value_counts()

    fig = px.pie(
        values=interest_counts.values,
        names=interest_counts.index,
        title=f'{column_name} Distribution',
        hole=0.3  # Donut chart
    )

    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(height=500)
    return fig


# Display the plot
if TECH_INTEREST_COLUMN in df.columns:
    fig_tech = plot_technology_interest(df, TECH_INTEREST_COLUMN)
    if fig_tech:
        fig_tech.show()


# CELL 10: Visualization - Rating Analysis
# ========================================
RATING_COLUMN = 'Session Rating'  # Adjust to your actual column name


def plot_rating_distribution(df, column_name):
    """Plot rating distribution as a histogram."""
    if column_name not in df.columns:
        print(f"Column '{column_name}' not found.")
        return

    # Convert to numeric if needed
    ratings = pd.to_numeric(df[column_name], errors='coerce').dropna()

    fig = go.Figure()

    # Histogram
    fig.add_trace(go.Histogram(
        x=ratings,
        nbinsx=5,
        name='Distribution',
        marker_color='skyblue'
    ))

    # Add average line
    avg_rating = ratings.mean()
    fig.add_vline(
        x=avg_rating,
        line_dash="dash",
        line_color="red",
        annotation_text=f"Average: {avg_rating:.2f}",
        annotation_position="top"
    )

    fig.update_layout(
        title=f'{column_name} Distribution',
        xaxis_title='Rating',
        yaxis_title='Count',
        height=400
    )

    return fig, avg_rating


# Display the plot
if RATING_COLUMN in df.columns:
    result = plot_rating_distribution(df, RATING_COLUMN)
    if result:
        fig_rating, avg = result
        fig_rating.show()
        print(f"\nAverage Rating: {avg:.2f}")


# CELL 11: Real-Time Dashboard
# ============================
def create_dashboard(df):
    """Create a comprehensive dashboard with multiple visualizations."""

    # Create subplots
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Responses Over Time', 'Experience Level',
                        'Technology Interest', 'Session Ratings'),
        specs=[[{'type': 'scatter'}, {'type': 'bar'}],
               [{'type': 'pie'}, {'type': 'histogram'}]]
    )

    # 1. Timeline (if timestamp exists)
    if 'Timestamp' in df.columns:
        df_sorted = df.sort_values('Timestamp')
        df_sorted['Count'] = range(1, len(df_sorted) + 1)
        fig.add_trace(
            go.Scatter(x=df_sorted['Timestamp'], y=df_sorted['Count'],
                       mode='lines', name='Cumulative'),
            row=1, col=1
        )

    # 2. Experience Level (adjust column name as needed)
    exp_col = next((col for col in df.columns if 'experience' in col.lower()), None)
    if exp_col:
        exp_counts = df[exp_col].value_counts()
        fig.add_trace(
            go.Bar(x=exp_counts.index, y=exp_counts.values, name='Experience'),
            row=1, col=2
        )

    # 3. Technology Interest
    tech_col = next(
        (col for col in df.columns
         if 'technology' in col.lower() or 'interest' in col.lower()),
        None
    )
    if tech_col:
        # Handle multi-select
        all_tech = []
        for resp in df[tech_col].dropna():
            if isinstance(resp, str):
                all_tech.extend([x.strip() for x in resp.split(',')])
        tech_counts = pd.Series(all_tech).value_counts()
        fig.add_trace(
            go.Pie(labels=tech_counts.index, values=tech_counts.values, name='Tech'),
            row=2, col=1
        )

    # 4. Ratings
    rating_col = next((col for col in df.columns if 'rating' in col.lower()), None)
    if rating_col:
        ratings = pd.to_numeric(df[rating_col], errors='coerce').dropna()
        fig.add_trace(
            go.Histogram(x=ratings, nbinsx=5, name='Ratings'),
            row=2, col=2
        )

    # Update layout
    fig.update_layout(
        height=800,
        showlegend=False,
        title_text=f"Survey Dashboard - {len(df)} Responses"
    )

    return fig


# Create and display dashboard
print("Creating comprehensive dashboard...")
dashboard = create_dashboard(df)
dashboard.show()


# CELL 12: Auto-Refresh Function (for live demos)
# ==============================================
def auto_refresh_dashboard(interval_seconds=30, duration_minutes=60):
    """
    Automatically refresh dashboard at regular intervals.

    Args:
        interval_seconds: How often to refresh
        duration_minutes: How long to keep refreshing
    """
    import time

    start_time = time.time()
    end_time = start_time + (duration_minutes * 60)

    iteration = 0
    while time.time() < end_time:
        iteration += 1
        print(f"\n{'=' * 60}")
        print(f"Refresh #{iteration} at {datetime.now().strftime('%H:%M:%S')}")
        print(f"{'=' * 60}")

        try:
            # Fetch fresh data
            df_fresh = fetch_survey_data()
            print(f"Total responses: {len(df_fresh)}")

            # Create dashboard
            dashboard = create_dashboard(df_fresh)
            dashboard.show()

            # Wait before next refresh
            if time.time() < end_time:
                print(f"\nNext refresh in {interval_seconds} seconds...")
                time.sleep(interval_seconds)

        except Exception as e:
            print(f"Error during refresh: {e}")
            time.sleep(interval_seconds)

    print("\nAuto-refresh completed!")

# Uncomment to enable auto-refresh during your meeting
# auto_refresh_dashboard(interval_seconds=30, duration_minutes=60)


# CELL 13: Export Results (Optional)
# ==================================
def export_results(df, output_path="/dbfs/FileStore/survey_results.csv"):
    """Export results to CSV for further analysis."""
    df.to_csv(output_path, index=False)
    print(f"Results exported to: {output_path}")

# Uncomment to export
# export_results(df)


# CELL 14: SQL Analysis (Databricks)
# ==================================
"""
If you created the temporary view in CELL 5, you can use SQL:

%sql
SELECT
    DATE(Timestamp) as date,
    COUNT(*) as response_count,
    AVG(CAST(`Session Rating` AS DOUBLE)) as avg_rating
FROM survey_responses
GROUP BY DATE(Timestamp)
ORDER BY date DESC

-- Or for experience level distribution:
%sql
SELECT
    `Experience Level`,
    COUNT(*) as count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) as percentage
FROM survey_responses
GROUP BY `Experience Level`
ORDER BY count DESC
"""


# CELL 15: Helper Functions
# =========================
def print_survey_summary(df):
    """Print a text summary of survey results."""
    print("\n" + "=" * 60)
    print("SURVEY SUMMARY")
    print("=" * 60)
    print(f"Total Responses: {len(df)}")

    if 'Timestamp' in df.columns:
        print(f"Latest Response: {df['Timestamp'].max()}")

    print("\nBreakdown by Column:")
    for col in df.columns:
        if col != 'Timestamp':
            print(f"\n{col}:")
            counts = df[col].value_counts().head(5)
            for val, count in counts.items():
                pct = (count / len(df)) * 100
                print(f"  {val}: {count} ({pct:.1f}%)")


# Call summary
print_survey_summary(df)


print("\n" + "=" * 60)
print("Setup Complete! Dashboard is ready.")
print("=" * 60)
print("\nFor live demo during your meeting:")
print("1. Share the Google Form link with participants")
print("2. Run the auto_refresh_dashboard() function (CELL 12)")
print("3. The dashboard will update every 30 seconds")
print("4. Present the live results on screen!")
