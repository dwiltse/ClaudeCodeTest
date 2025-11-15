# Google Forms to Databricks Real-Time Survey Guide

This guide will walk you through creating a real-time survey system using Google Forms and Databricks Free Edition.

## Architecture Overview

```
Participants → Google Form → Google Sheets → Python Script → Databricks → Dashboard
```

## Step 1: Create Google Form

1. Go to [Google Forms](https://forms.google.com)
2. Click "Blank" to create a new form
3. Add your survey questions (example questions for a user group):
   - Name (Short answer)
   - Experience Level (Multiple choice: Beginner, Intermediate, Advanced)
   - Primary Technology Interest (Checkboxes: Python, SQL, Machine Learning, Data Engineering, etc.)
   - How did you hear about us? (Dropdown)
   - Session Rating (Linear scale 1-5)
   - Comments/Feedback (Paragraph)

4. Click the "Responses" tab
5. Click the Google Sheets icon to "Create Spreadsheet"
6. This will create a linked Google Sheet that auto-updates with responses

## Step 2: Set Up Google Sheets API Access

### Option A: Using Google Service Account (Recommended for Production)

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable Google Sheets API:
   - Go to "APIs & Services" → "Library"
   - Search for "Google Sheets API"
   - Click "Enable"
4. Create Service Account:
   - Go to "APIs & Services" → "Credentials"
   - Click "Create Credentials" → "Service Account"
   - Fill in details and click "Create"
   - Grant role "Editor" (or more restrictive if preferred)
   - Click "Done"
5. Create Key:
   - Click on the service account you just created
   - Go to "Keys" tab
   - Click "Add Key" → "Create New Key"
   - Select "JSON" and click "Create"
   - Save the downloaded JSON file securely
6. Share your Google Sheet:
   - Open your Google Sheet
   - Click "Share"
   - Add the service account email (found in the JSON file)
   - Give "Editor" permissions

### Option B: Using OAuth (Simpler for Demo/Personal Use)

For quick demos, you can use OAuth with your personal Google account (see code examples).

## Step 3: Set Up Databricks Community Edition

1. Sign up at [Databricks Community Edition](https://community.cloud.databricks.com/)
2. Create a new cluster:
   - Go to "Compute" → "Create Cluster"
   - Select the smallest configuration (free tier)
   - Wait for cluster to start (~5 minutes)

## Step 4: Install Required Libraries in Databricks

In a Databricks notebook cell, run:

```python
%pip install gspread oauth2client pandas
```

Or for service account method:
```python
%pip install gspread google-auth pandas
```

## Step 5: Upload Credentials to Databricks

1. In Databricks, go to "Data" → "Add Data"
2. Upload your service account JSON file (or store credentials securely using Databricks Secrets)

For production, use Databricks Secrets:
```bash
# Install Databricks CLI locally
pip install databricks-cli

# Configure
databricks configure --token

# Create secret scope
databricks secrets create-scope --scope google-api

# Store the entire JSON file content
databricks secrets put --scope google-api --key credentials --string-value "$(cat path/to/credentials.json)"
```

## Step 6: Real-Time Data Ingestion Options

### Option A: Scheduled Refresh
- Set up a Databricks job to run every 1-5 minutes
- Good for: Most real-time needs, cost-effective

### Option B: Continuous Streaming
- Use Databricks Auto Loader with file upload triggers
- Good for: True real-time requirements

### Option C: Manual Refresh
- Add a "Refresh Data" button in your dashboard
- Good for: Demos where you control timing

## Step 7: Create Visualization Dashboard

Use Databricks SQL or Notebooks to create:
- Bar charts showing response distributions
- Pie charts for categorical data
- Word clouds for text responses
- Real-time participant count
- Time-series of response submissions

## Security Best Practices

1. **Never commit credentials to Git**: Add `*.json` to `.gitignore`
2. **Use Databricks Secrets** for production
3. **Limit API permissions** to minimum required
4. **Share spreadsheet** only with service account, not publicly
5. **Consider form response limits** for large audiences

## Troubleshooting

### "Insufficient permissions" error
- Verify service account email is shared on the spreadsheet
- Check that Google Sheets API is enabled

### "Quota exceeded" error
- Google Sheets API has rate limits (100 requests per 100 seconds per user)
- Add retry logic and caching

### Databricks cluster issues
- Community Edition clusters auto-terminate after 2 hours of inactivity
- Restart cluster if needed

## Cost Considerations

- **Google Forms**: Free
- **Google Sheets**: Free (up to 10 million cells)
- **Google Sheets API**: Free (with rate limits)
- **Databricks Community Edition**: Free (limited to 1 small cluster)

## Example Use Case Flow

1. **Before meeting**: Share Google Form link with participants
2. **During meeting**:
   - Show Databricks dashboard on screen
   - Ask participants to fill form
   - Refresh dashboard every 30-60 seconds
   - Discuss results live
3. **After meeting**: Export data for further analysis

## Next Steps

See the included Python scripts and Databricks notebook examples in this repository:
- `google_sheets_connector.py` - Connects to Google Sheets and fetches data
- `databricks_survey_analysis.py` - Example analysis code for Databricks
- `requirements.txt` - Required Python packages
