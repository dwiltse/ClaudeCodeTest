"""
Google Sheets Connector for Survey Data
Connects to Google Sheets and fetches survey responses for Databricks analysis
"""

import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import json
from datetime import datetime
from typing import Optional, List


class GoogleSheetsConnector:
    """
    Connects to Google Sheets and retrieves survey response data.

    Usage:
        # Using service account
        connector = GoogleSheetsConnector(
            credentials_path='path/to/service-account.json',
            spreadsheet_id='your-spreadsheet-id'
        )
        df = connector.get_responses()

        # Or in Databricks with secrets
        connector = GoogleSheetsConnector(
            credentials_json=dbutils.secrets.get(scope="google-api", key="credentials"),
            spreadsheet_id='your-spreadsheet-id'
        )
    """

    def __init__(
        self,
        credentials_path: Optional[str] = None,
        credentials_json: Optional[str] = None,
        spreadsheet_id: Optional[str] = None,
        spreadsheet_url: Optional[str] = None
    ):
        """
        Initialize the connector.

        Args:
            credentials_path: Path to service account JSON file
            credentials_json: JSON string of service account credentials
            spreadsheet_id: Google Sheets ID (from URL)
            spreadsheet_url: Full Google Sheets URL
        """
        self.client = self._authenticate(credentials_path, credentials_json)
        self.spreadsheet = self._open_spreadsheet(spreadsheet_id, spreadsheet_url)

    def _authenticate(
        self,
        credentials_path: Optional[str],
        credentials_json: Optional[str]
    ) -> gspread.Client:
        """Authenticate with Google Sheets API."""
        scopes = [
            'https://www.googleapis.com/auth/spreadsheets.readonly',
            'https://www.googleapis.com/auth/drive.readonly'
        ]

        if credentials_path:
            creds = Credentials.from_service_account_file(
                credentials_path,
                scopes=scopes
            )
        elif credentials_json:
            creds_dict = json.loads(credentials_json)
            creds = Credentials.from_service_account_info(
                creds_dict,
                scopes=scopes
            )
        else:
            raise ValueError("Must provide either credentials_path or credentials_json")

        return gspread.authorize(creds)

    def _open_spreadsheet(
        self,
        spreadsheet_id: Optional[str],
        spreadsheet_url: Optional[str]
    ) -> gspread.Spreadsheet:
        """Open the Google Spreadsheet."""
        if spreadsheet_id:
            return self.client.open_by_key(spreadsheet_id)
        elif spreadsheet_url:
            return self.client.open_by_url(spreadsheet_url)
        else:
            raise ValueError("Must provide either spreadsheet_id or spreadsheet_url")

    def get_responses(
        self,
        worksheet_name: str = "Form Responses 1",
        include_timestamp: bool = True
    ) -> pd.DataFrame:
        """
        Fetch all survey responses as a pandas DataFrame.

        Args:
            worksheet_name: Name of the worksheet (default is Google Forms default)
            include_timestamp: Whether to include the timestamp column

        Returns:
            DataFrame with survey responses
        """
        worksheet = self.spreadsheet.worksheet(worksheet_name)
        data = worksheet.get_all_records()
        df = pd.DataFrame(data)

        # Parse timestamp if present
        if include_timestamp and 'Timestamp' in df.columns:
            df['Timestamp'] = pd.to_datetime(df['Timestamp'])

        return df

    def get_responses_since(
        self,
        since: datetime,
        worksheet_name: str = "Form Responses 1"
    ) -> pd.DataFrame:
        """
        Fetch only new responses since a given timestamp.

        Args:
            since: DateTime to filter from
            worksheet_name: Name of the worksheet

        Returns:
            DataFrame with new responses only
        """
        df = self.get_responses(worksheet_name)

        if 'Timestamp' in df.columns:
            df['Timestamp'] = pd.to_datetime(df['Timestamp'])
            df = df[df['Timestamp'] > since]

        return df

    def get_response_count(self, worksheet_name: str = "Form Responses 1") -> int:
        """
        Get the total number of responses (excluding header).

        Args:
            worksheet_name: Name of the worksheet

        Returns:
            Number of responses
        """
        worksheet = self.spreadsheet.worksheet(worksheet_name)
        return len(worksheet.get_all_values()) - 1  # Subtract header row

    def get_latest_responses(
        self,
        n: int = 10,
        worksheet_name: str = "Form Responses 1"
    ) -> pd.DataFrame:
        """
        Get the N most recent responses.

        Args:
            n: Number of recent responses to fetch
            worksheet_name: Name of the worksheet

        Returns:
            DataFrame with N most recent responses
        """
        df = self.get_responses(worksheet_name)
        return df.tail(n)

    def get_column_names(self, worksheet_name: str = "Form Responses 1") -> List[str]:
        """
        Get all column names (survey questions).

        Args:
            worksheet_name: Name of the worksheet

        Returns:
            List of column names
        """
        worksheet = self.spreadsheet.worksheet(worksheet_name)
        return worksheet.row_values(1)


# Example usage functions

def example_basic_usage():
    """Example: Basic usage with service account."""
    # Initialize connector
    connector = GoogleSheetsConnector(
        credentials_path='service-account.json',
        spreadsheet_id='your-spreadsheet-id-here'
    )

    # Get all responses
    df = connector.get_responses()
    print(f"Total responses: {len(df)}")
    print(df.head())

    # Get recent responses
    latest = connector.get_latest_responses(n=5)
    print("\nLatest 5 responses:")
    print(latest)


def example_databricks_usage():
    """
    Example: Usage in Databricks notebook.

    This assumes you've set up Databricks Secrets.
    """
    # Uncomment when running in Databricks:
    # credentials_json = dbutils.secrets.get(scope="google-api", key="credentials")
    # spreadsheet_id = dbutils.secrets.get(scope="google-api", key="spreadsheet-id")

    # For demo purposes:
    credentials_json = '{"type": "service_account", ...}'  # Your JSON here
    spreadsheet_id = 'your-spreadsheet-id'

    connector = GoogleSheetsConnector(
        credentials_json=credentials_json,
        spreadsheet_id=spreadsheet_id
    )

    # Get data and create Spark DataFrame
    pandas_df = connector.get_responses()

    # Convert to Spark DataFrame (in Databricks)
    # spark_df = spark.createDataFrame(pandas_df)
    # display(spark_df)

    return pandas_df


def example_incremental_load():
    """Example: Only fetch new responses since last check."""
    connector = GoogleSheetsConnector(
        credentials_path='service-account.json',
        spreadsheet_id='your-spreadsheet-id'
    )

    # Store this timestamp between runs
    last_check = datetime(2025, 11, 15, 10, 0, 0)

    # Get only new responses
    new_responses = connector.get_responses_since(last_check)
    print(f"New responses since {last_check}: {len(new_responses)}")

    return new_responses


if __name__ == "__main__":
    # Run example
    print("Google Sheets Connector - Example Usage")
    print("=" * 50)
    print("\nUpdate the credentials_path and spreadsheet_id before running!")
    print("\nAvailable methods:")
    print("- get_responses(): Get all survey data")
    print("- get_response_count(): Get total number of responses")
    print("- get_latest_responses(n): Get N most recent responses")
    print("- get_responses_since(datetime): Get responses after a timestamp")
    print("- get_column_names(): Get survey question headers")
