# Google Forms + Databricks Real-Time Survey System

A complete solution for creating live, interactive surveys using Google Forms and Databricks Free Edition. Perfect for user group meetings, workshops, and presentations where you want to collect and visualize participant feedback in real-time!

## What This Does

This project enables you to:
- Create surveys using Google Forms (free, familiar, mobile-friendly)
- Automatically sync responses to Google Sheets
- Ingest data into Databricks for analysis
- Display live dashboards during your presentation
- Visualize results in real-time as participants respond

## Perfect For

- User group meetings
- Conference workshops
- Training sessions
- Team retrospectives
- Live polling during presentations
- Customer feedback collection
- Community surveys

## What's Included

### Documentation
- **QUICKSTART.md** - Get up and running in 30 minutes
- **GOOGLE_FORMS_DATABRICKS_GUIDE.md** - Comprehensive guide with architecture details
- **SAMPLE_FORM_QUESTIONS.md** - Ready-to-use survey questions

### Code
- **google_sheets_connector.py** - Python connector for Google Sheets API
- **databricks_survey_analysis.py** - Complete Databricks notebook with visualizations
- **config_template.py** - Configuration template for easy setup
- **requirements.txt** - All Python dependencies

### Examples
- Test data generation
- Multiple visualization types
- Auto-refresh functionality
- Real-time dashboard updates

## Quick Start

### 1. Create Google Form (5 min)
```
1. Go to forms.google.com
2. Create a new form with your questions
3. Link it to Google Sheets (Responses → Sheets icon)
```

### 2. Set Up Google Cloud (10 min)
```
1. Enable Google Sheets API
2. Create a service account
3. Download JSON credentials
4. Share your sheet with the service account email
```

### 3. Set Up Databricks (10 min)
```
1. Sign up at community.cloud.databricks.com (free!)
2. Create a cluster
3. Create a notebook
4. Upload credentials or use Databricks Secrets
```

### 4. Run Your Dashboard (5 min)
```
1. Copy databricks_survey_analysis.py to your notebook
2. Update configuration with your credentials
3. Run the cells
4. Watch your live dashboard!
```

See **QUICKSTART.md** for detailed step-by-step instructions.

## Architecture

```
┌─────────────────┐
│  Participants   │
│   (Fill Form)   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Google Form    │
└────────┬────────┘
         │ (Auto-sync)
         ▼
┌─────────────────┐
│ Google Sheets   │
└────────┬────────┘
         │ (API)
         ▼
┌─────────────────┐      ┌──────────────┐
│ Python Script   │─────▶│  Databricks  │
│  (Connector)    │      │  (Analysis)  │
└─────────────────┘      └──────┬───────┘
                                │
                                ▼
                         ┌──────────────┐
                         │  Dashboard   │
                         │ (Visualize)  │
                         └──────────────┘
```

## Features

### Data Collection
- ✅ Mobile-friendly forms (Google Forms)
- ✅ Automatic response collection
- ✅ Timestamp tracking
- ✅ Multiple question types supported

### Data Processing
- ✅ Real-time data sync
- ✅ Pandas DataFrame integration
- ✅ Spark DataFrame support (Databricks)
- ✅ Incremental loading options

### Visualizations
- ✅ Response timeline (line chart)
- ✅ Experience level distribution (bar chart)
- ✅ Technology interest (pie chart)
- ✅ Rating analysis (histogram)
- ✅ Comprehensive dashboard (multi-chart)
- ✅ Auto-refresh capability

### Security
- ✅ Service account authentication
- ✅ Databricks Secrets integration
- ✅ No credentials in code
- ✅ .gitignore protection

## Example Use Case

**User Group Meeting Flow:**

1. **Before meeting**: Share Google Form link
2. **Start of meeting**: Show empty dashboard
3. **During presentation**: Ask participants to fill form
4. **Mid-meeting**: Refresh dashboard, show results
5. **End of meeting**: Final dashboard update, discuss insights

## Technology Stack

- **Google Forms** - Survey creation (free)
- **Google Sheets** - Data storage (free)
- **Google Sheets API** - Data access (free, with limits)
- **Python** - Data processing
- **Databricks Community Edition** - Analysis platform (free)
- **Plotly** - Interactive visualizations
- **Pandas** - Data manipulation

## Requirements

- Google account
- Databricks Community Edition account (free signup)
- Python 3.8+ (included in Databricks)
- See requirements.txt for Python packages

## Installation

### Local Testing
```bash
# Clone the repository
git clone https://github.com/yourusername/ClaudeCodeTest.git
cd ClaudeCodeTest

# Install dependencies
pip install -r requirements.txt

# Copy and configure
cp config_template.py config.py
# Edit config.py with your credentials
```

### Databricks Setup
```bash
# Install Databricks CLI
pip install databricks-cli

# Configure
databricks configure --token

# Create secrets
databricks secrets create-scope --scope google-api
databricks secrets put --scope google-api --key credentials --string-value "$(cat service-account.json)"
databricks secrets put --scope google-api --key spreadsheet-id --string-value "YOUR_SPREADSHEET_ID"
```

## Usage

### Basic Usage
```python
from google_sheets_connector import GoogleSheetsConnector

# Initialize
connector = GoogleSheetsConnector(
    credentials_path='service-account.json',
    spreadsheet_id='your-spreadsheet-id'
)

# Get all responses
df = connector.get_responses()
print(f"Total responses: {len(df)}")

# Get latest 10 responses
latest = connector.get_latest_responses(n=10)
```

### Databricks Auto-Refresh
```python
# In Databricks notebook
auto_refresh_dashboard(interval_seconds=30, duration_minutes=60)
```

This will:
- Refresh data every 30 seconds
- Update visualizations automatically
- Run for 60 minutes (duration of your meeting)

## Sample Questions

The repository includes **SAMPLE_FORM_QUESTIONS.md** with ready-to-use questions for:
- User group feedback
- Technical workshop evaluation
- Community building
- Product/service feedback

Copy and paste directly into Google Forms!

## Security Best Practices

🔒 **Important**: Never commit credentials to Git!

- ✅ Use `.gitignore` (included)
- ✅ Use Databricks Secrets for production
- ✅ Use service accounts (not personal credentials)
- ✅ Share sheets only with service account email
- ✅ Limit API permissions to read-only

## Troubleshooting

### Common Issues

**"Insufficient permissions"**
- Make sure you shared the Google Sheet with the service account email

**"Spreadsheet not found"**
- Double-check the spreadsheet ID in your configuration

**"No module named gspread"**
- Run `%pip install gspread google-auth pandas plotly` in Databricks

**Cluster keeps stopping**
- Community Edition auto-stops after 2 hours - just restart it

See the **GOOGLE_FORMS_DATABRICKS_GUIDE.md** for more troubleshooting tips.

## Cost

Everything is FREE! 🎉

- Google Forms: Free
- Google Sheets: Free (up to 10M cells)
- Google Sheets API: Free (100 req/100 sec)
- Databricks Community Edition: Free (1 cluster)

## Limitations

- Databricks Community Edition: 1 cluster, auto-stops after 2 hours
- Google Sheets API: Rate limits apply (usually not an issue)
- Real-time updates: Manual refresh or scheduled (not push-based)

## Contributing

Contributions welcome! Feel free to:
- Add new visualizations
- Improve error handling
- Add example questions
- Enhance documentation

## License

MIT License - Use freely for your user groups and presentations!

## Support

- Check the documentation files in this repo
- Google Sheets API: https://developers.google.com/sheets/api
- Databricks docs: https://docs.databricks.com/

## Acknowledgments

Built for data enthusiasts who want to make their user group meetings more interactive and data-driven!

---

**Ready to get started?** Check out **QUICKSTART.md** for a 30-minute setup guide!

**Questions?** Review **GOOGLE_FORMS_DATABRICKS_GUIDE.md** for comprehensive documentation.

**Need survey questions?** See **SAMPLE_FORM_QUESTIONS.md** for ready-to-use templates.

Happy surveying! 📊
