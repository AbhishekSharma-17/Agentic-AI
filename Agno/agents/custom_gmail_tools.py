"""
Custom extension of GmailTools with fixed port OAuth flow
"""

import os
from pathlib import Path
from typing import Optional, List

from agno.tools.gmail import GmailTools
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow


class FixedPortGmailTools(GmailTools):
    """GmailTools subclass that uses a fixed port for OAuth flow."""
    
    def __init__(
        self,
        port: int = 8000,
        use_oauth_callback: bool = False,
        *args,
        **kwargs
    ):
        """Initialize with a fixed port."""
        self.port = port
        self.use_oauth_callback = use_oauth_callback
        super().__init__(*args, **kwargs)
        
    def _auth(self) -> None:
        """Override authentication to use a fixed port."""
        token_file = Path(self.token_path or "token.json")
        creds_file = Path(self.credentials_path or "credentials.json")

        if token_file.exists():
            self.creds = Credentials.from_authorized_user_file(str(token_file), self.scopes)

        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                client_config = {
                    "installed": {
                        "client_id": os.getenv("GOOGLE_CLIENT_ID"),
                        "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
                        "project_id": os.getenv("GOOGLE_PROJECT_ID"),
                        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                        "token_uri": "https://oauth2.googleapis.com/token",
                        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                        # Include both URI formats that are registered in Google Cloud Console
                        "redirect_uris": [
                            "http://localhost:8000/", 
                            "http://localhost:8000/oauth2callback"
                        ],
                    }
                }
                
                # Use the credentials file if it exists, otherwise use the config from environment variables
                if creds_file.exists():
                    flow = InstalledAppFlow.from_client_secrets_file(str(creds_file), self.scopes)
                else:
                    flow = InstalledAppFlow.from_client_config(client_config, self.scopes)
                
                # Use a fixed port and specify redirect_uri_path if requested
                if self.use_oauth_callback:
                    self.creds = flow.run_local_server(port=self.port, redirect_uri_path="/oauth2callback")
                else:
                    # Default to root path with trailing slash which seems to be what Google expects
                    self.creds = flow.run_local_server(port=self.port, redirect_uri_path="/")

            # Save the credentials for future use
            if self.creds and self.creds.valid:
                token_file.write_text(self.creds.to_json())
