"""
Configuration Template for Google Forms + Databricks Survey System

INSTRUCTIONS:
1. Copy this file to 'config.py'
2. Fill in your actual values
3. NEVER commit config.py to Git (it's in .gitignore)
4. Use this in your Databricks notebook or local testing

For Databricks production use, prefer Databricks Secrets instead.
"""

# =============================================================================
# GOOGLE SHEETS CONFIGURATION
# =============================================================================

# Option 1: Path to service account JSON file (for local testing)
# Download this from Google Cloud Console
SERVICE_ACCOUNT_PATH = "path/to/your/service-account.json"

# Option 2: Service account JSON as a string (for Databricks without Secrets)
# Copy the entire contents of your service-account.json file
SERVICE_ACCOUNT_JSON = """
{
  "type": "service_account",
  "project_id": "your-project-id",
  "private_key_id": "your-private-key-id",
  "private_key": "-----BEGIN PRIVATE KEY-----\\n"
                 "YOUR_PRIVATE_KEY_HERE\\n"
                 "-----END PRIVATE KEY-----\\n",
  "client_email": "your-service-account@your-project.iam.gserviceaccount.com",
  "client_id": "your-client-id",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/"
                          "your-service-account%40your-project.iam.gserviceaccount.com"
}
"""

# =============================================================================
# SPREADSHEET CONFIGURATION
# =============================================================================

# Your Google Sheets ID (from the URL)
# URL format: https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/edit
SPREADSHEET_ID = "your-spreadsheet-id-here"

# Or use the full URL
SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/your-spreadsheet-id-here/edit"

# Worksheet name (default for Google Forms is "Form Responses 1")
WORKSHEET_NAME = "Form Responses 1"

# =============================================================================
# DATABRICKS CONFIGURATION (if using Databricks Secrets)
# =============================================================================

# Databricks Secret Scope name
DATABRICKS_SECRET_SCOPE = "google-api"

# Secret keys
DATABRICKS_CREDENTIALS_KEY = "credentials"
DATABRICKS_SPREADSHEET_ID_KEY = "spreadsheet-id"

# =============================================================================
# COLUMN MAPPING
# =============================================================================
# Map your Google Form questions to shorter variable names for easier coding
# Update these to match your actual form questions

COLUMN_NAMES = {
    'timestamp': 'Timestamp',
    'name': 'Name',
    'email': 'Email',
    'experience': 'What is your experience level with data analytics?',
    'technologies': 'What technologies are you most interested in? (Select all that apply)',
    'role': 'What is your primary role?',
    'heard_about': 'How did you hear about this user group?',
    'first_time': 'Is this your first time attending?',
    'session_rating': 'How would you rate today\'s session?',
    'future_topics': ('What topics would you like to see in future sessions? '
                      '(Select all that apply)'),
    'recommend_score': ('How likely are you to recommend this user group to '
                        'a colleague?'),
    'comments': 'Additional Comments or Suggestions'
}

# =============================================================================
# DASHBOARD CONFIGURATION
# =============================================================================

# Refresh interval for auto-refresh (seconds)
REFRESH_INTERVAL = 30

# Auto-refresh duration (minutes)
REFRESH_DURATION = 60

# Chart color scheme
COLOR_SCHEME = 'viridis'  # Options: viridis, plasma, inferno, magma, cividis

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================


def get_credentials_for_databricks():
    """
    Get credentials using Databricks Secrets.
    Use this function in your Databricks notebook.
    """
    try:
        credentials_json = dbutils.secrets.get(  # noqa: F821
            scope=DATABRICKS_SECRET_SCOPE,
            key=DATABRICKS_CREDENTIALS_KEY
        )
        spreadsheet_id = dbutils.secrets.get(  # noqa: F821
            scope=DATABRICKS_SECRET_SCOPE,
            key=DATABRICKS_SPREADSHEET_ID_KEY
        )
        return credentials_json, spreadsheet_id
    except Exception as e:
        print(f"Error accessing Databricks Secrets: {e}")
        print("Falling back to config values...")
        return SERVICE_ACCOUNT_JSON, SPREADSHEET_ID


def get_credentials_local():
    """
    Get credentials for local testing.
    Use this when running outside Databricks.
    """
    return SERVICE_ACCOUNT_PATH, SPREADSHEET_ID


def get_column(df, short_name):
    """
    Helper function to get a column by its short name.

    Usage:
        df_renamed = df.rename(columns={v: k for k, v in COLUMN_NAMES.items()})
        experience_col = get_column(df_renamed, 'experience')
    """
    return COLUMN_NAMES.get(short_name, short_name)


# =============================================================================
# VALIDATION
# =============================================================================

def validate_config():
    """Validate that configuration is set up correctly."""
    issues = []

    # Check if using default placeholder values
    if SPREADSHEET_ID == "your-spreadsheet-id-here":
        issues.append("SPREADSHEET_ID not set")

    if "your-project-id" in SERVICE_ACCOUNT_JSON:
        issues.append("SERVICE_ACCOUNT_JSON contains placeholder values")

    if issues:
        print("⚠️  Configuration Issues Found:")
        for issue in issues:
            print(f"   - {issue}")
        print("\nPlease update config_template.py with your actual values.")
        return False
    else:
        print("✅ Configuration looks good!")
        return True


if __name__ == "__main__":
    print("Configuration Template")
    print("=" * 60)
    print("\nThis is a template file. To use it:")
    print("1. Copy this file to 'config.py'")
    print("2. Update the values with your actual credentials")
    print("3. Run validate_config() to check your setup")
    print("\n" + "=" * 60)
    print("\nValidating current configuration...")
    validate_config()
