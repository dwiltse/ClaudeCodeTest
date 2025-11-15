# Quick Start Guide: Real-Time Survey with Google Forms + Databricks

This guide will get you up and running in 30 minutes!

## Prerequisites

- Google account
- Databricks Community Edition account (free)
- 30 minutes of setup time

## Step-by-Step Setup

### Part 1: Google Forms Setup (5 minutes)

1. **Create your form**
   - Go to https://forms.google.com
   - Click "+ Blank" to create a new form
   - Title it "User Group Survey" (or your preferred name)

2. **Add questions** (example questions provided):
   ```
   1. Name (Short answer)
   2. Experience Level (Multiple choice)
      - Beginner
      - Intermediate
      - Advanced
      - Expert
   3. Primary Technology Interest (Checkboxes)
      - Python
      - SQL
      - Machine Learning
      - Data Engineering
      - Cloud Computing
      - Other
   4. How did you hear about us? (Dropdown)
      - Colleague
      - Social Media
      - Search Engine
      - Event
      - Other
   5. Session Rating (Linear scale 1-5)
   6. Comments (Paragraph)
   ```

3. **Link to Google Sheets**
   - Click "Responses" tab
   - Click the green Sheets icon
   - Click "Create" to make a new spreadsheet
   - Note the spreadsheet ID from the URL:
     `https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/edit`

### Part 2: Google Cloud Setup (10 minutes)

1. **Create Google Cloud Project**
   - Go to https://console.cloud.google.com
   - Create new project (top left dropdown)
   - Name it "Survey Analytics" or similar

2. **Enable Google Sheets API**
   ```
   Navigation: APIs & Services → Library → Search "Google Sheets API" → Enable
   ```

3. **Create Service Account**
   ```
   Navigation: APIs & Services → Credentials → Create Credentials → Service Account
   ```
   - Name: `survey-reader`
   - Role: `Viewer` (or `Editor` if you need write access)
   - Click "Done"

4. **Generate JSON Key**
   - Click on the service account you just created
   - Go to "Keys" tab
   - "Add Key" → "Create New Key" → JSON
   - Download the file (keep it secure!)
   - Rename it to `service-account.json`

5. **Share your Google Sheet**
   - Open your survey responses spreadsheet
   - Click "Share" button
   - Paste the service account email (from the JSON file: `client_email`)
   - Give it "Viewer" or "Editor" permission
   - Uncheck "Notify people" (it's a robot, not a person!)
   - Click "Share"

### Part 3: Databricks Setup (10 minutes)

1. **Sign up for Databricks Community Edition**
   - Go to https://community.cloud.databricks.com/
   - Sign up (it's free!)
   - Verify your email

2. **Create a cluster**
   - Go to "Compute" in the left sidebar
   - Click "Create Cluster"
   - Name: `survey-cluster`
   - Leave defaults (smallest size is fine)
   - Click "Create Cluster"
   - Wait ~5 minutes for it to start

3. **Create a notebook**
   - Go to "Workspace" in the left sidebar
   - Click your username → "Create" → "Notebook"
   - Name: `Survey Dashboard`
   - Default language: `Python`
   - Cluster: Select the cluster you just created
   - Click "Create"

4. **Upload credentials (SECURE METHOD)**

   **Option A: Using Databricks Secrets (Recommended)**
   - Install Databricks CLI on your computer:
     ```bash
     pip install databricks-cli
     ```
   - Configure it:
     ```bash
     databricks configure --token
     ```
     - Host: `https://community.cloud.databricks.com`
     - Token: Generate from User Settings → Access Tokens
   - Create secret scope:
     ```bash
     databricks secrets create-scope --scope google-api
     ```
   - Store credentials:
     ```bash
     databricks secrets put --scope google-api --key credentials --string-value "$(cat service-account.json)"
     databricks secrets put --scope google-api --key spreadsheet-id --string-value "YOUR_SPREADSHEET_ID"
     ```

   **Option B: Manual upload (Less secure, OK for demos)**
   - In Databricks, go to "Data" → "Add Data"
   - Upload `service-account.json`
   - Note the path: `/dbfs/FileStore/...`

### Part 4: Run Your Dashboard (5 minutes)

1. **Copy code to Databricks**
   - Open the `databricks_survey_analysis.py` file from this repo
   - Copy each section into separate cells in your Databricks notebook
   - OR import the entire file as a notebook

2. **Update configuration** (CELL 3)
   - If using secrets: Code is already set!
   - If using manual upload: Update the file path

3. **Run the cells in order**
   - Click "Run All" or run each cell individually
   - Watch your dashboard come to life!

## Testing Your Setup

1. **Test the form**
   - Open your Google Form
   - Fill it out 3-4 times with test data
   - Check that data appears in the Google Sheet

2. **Test data connection**
   - Run CELL 5 in Databricks
   - You should see your test responses

3. **Test visualizations**
   - Run CELL 7-11
   - You should see charts and graphs

## During Your Meeting

### Before the meeting:

1. Start your Databricks cluster (takes ~5 minutes)
2. Open your notebook
3. Run cells 1-5 to ensure everything works
4. Share your Google Form link with participants
   - Get the link: Open form → Send → Link icon → Copy
   - Shorten it with bit.ly for easier sharing

### During the meeting:

1. **Present your screen** showing Databricks dashboard
2. **Share the form link** via:
   - QR code (use qr-code-generator.com)
   - Chat message
   - Slide with the link

3. **Enable auto-refresh**:
   ```python
   auto_refresh_dashboard(interval_seconds=30, duration_minutes=60)
   ```

4. **Watch responses come in live!**

### Tips for success:

- Test with 5-10 responses before the meeting
- Have the form open on your phone to demo
- Mention when you're refreshing the data
- Explain what patterns you're seeing
- Ask follow-up questions based on results

## Troubleshooting

### "Insufficient permissions" error
```
Solution: Make sure you shared the Google Sheet with the service account email
Check: Open sheet → Share → Verify service account email is listed
```

### "Spreadsheet not found" error
```
Solution: Double-check the spreadsheet ID in your configuration
The ID is in the URL: docs.google.com/spreadsheets/d/{THIS_PART}/edit
```

### "No module named gspread" error
```
Solution: Run CELL 1 to install dependencies
%pip install gspread google-auth pandas plotly
```

### Databricks cluster keeps stopping
```
Solution: Community Edition clusters auto-stop after 2 hours of inactivity
Just restart it before your meeting (takes ~5 minutes)
```

### Form responses not showing up
```
Solution: Check these:
1. Data is in Google Sheets? (Open the sheet to verify)
2. Service account has access? (Check sharing settings)
3. Correct spreadsheet ID? (Double-check the ID)
4. API enabled? (Check Google Cloud Console)
```

## Cost Breakdown

Everything is FREE! 🎉

- Google Forms: Free
- Google Sheets: Free (up to 10M cells)
- Google Sheets API: Free (100 requests per 100 seconds)
- Databricks Community Edition: Free (1 cluster, limited compute)

## Next Steps

Once you're comfortable with the basics:

1. **Customize visualizations** - Add your own charts
2. **Add more questions** - Expand your form
3. **Schedule automated reports** - Use Databricks Jobs
4. **Export to CSV/PDF** - Share results with stakeholders
5. **Connect to other tools** - Slack notifications, email alerts, etc.

## Example Timeline

For a 60-minute user group meeting:

```
0:00 - Welcome & intro
0:05 - Share form link, ask people to fill it out
0:10 - Start presentation (while responses come in)
0:30 - First dashboard reveal
0:35 - Continue presentation
0:50 - Final dashboard update
0:55 - Discuss insights from the data
1:00 - Wrap up
```

## Support

- Google Sheets API docs: https://developers.google.com/sheets/api
- Databricks docs: https://docs.databricks.com/
- This repo: Check the main GOOGLE_FORMS_DATABRICKS_GUIDE.md

## Security Reminder

🔒 **NEVER commit your service-account.json file to Git!**

Already in .gitignore:
- `*.json` (all JSON files)
- `service-account.json` (explicit)
- `.env` (environment variables)

Good luck with your presentation! 🚀
