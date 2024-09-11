# app-kasada


This application enables users to securely transfer .xlsm files from a Google Drive folder to Azure Blob Storage. The application includes user authentication, with login and password management. It also logs every user action such as login, file viewing and file transfer in a log file.

Features :
- User authentication: login, password change and account creation.
- Google Drive to Azure Blob Transfer: Transfer files from a specified Google Drive folder to Azure Blob Storage.
- File viewer: lists all files in a Google Drive folder.
- Logging: Records every user action, including login, file viewing and file transfers.

Prerequisites:
To run this application, you'll need :
- Python 3.x** installed.
- **Streamlit** installed (for the web interface).
- A **Google Cloud** account to generate OAuth 2.0 credentials to access Google Drive.
- An **Azure Storage** account and the **connection string** for Azure Blob Stora


Installation :

1. Clone the repository :
   git clone https://github.com/votre-repo/google-drive-to-azure-transfer.git
   cd google-drive-to-azure-transfer

2. Install the required Python packages:
   pip install -r requirements.txt

3. **Configure your Google OAuth credentials**:
   - Go to [Google Cloud Console](https://console.cloud.google.com/).
   - Create a new project and activate the **API Google Drive**.
   - Create **service account credentials** and download the `credentials.json` file.
   - In the project's root folder, create a folder called `creds` and place your `credentials.json` file in this folder:
     mkdir creds
     mv /path/to/your/credentials.json creds/

4. **Azure Blob Storage connection string** :
   - Retrieve your Azure Data Lake Storage (ADLS) connection string from the Azure portal.
   - Open the `fonc.py` file and insert your connection string in the `connect_str` variable:
     connect_str = “your-connection-string-azure-blob”


Project structure :
google-drive-to-azure-transfer/
│
├── app.py # Main application file
├── functions.py # User authentication, password management and logging functions
├── fonc.py # Contains functions for Google Drive and Azure Blob operations
├── users.json # Stores user credentials (generated at runtime)
├── log.txt # Records user actions (generated at runtime)
├── creds/ # Contains credentials.json for access to Google Drive API
│ └── credentials.json # service account credentials for the Google Drive API
└── requirements.txt # Python dependencies

Running the application:

1. To run the application, navigate to the project folder and use the following command:
   streamlit run app.py

2. Open the URL provided in your web browser (usually `http://localhost:8501`).

How to use :

Sidebar options:
- **Enter Google Drive folder URL**: Enter the link to the Google Drive folder from which you wish to transfer files.
- **View files**: Lists all files in the specified Google Drive folder.
- Transfer files to Azure**: Transfers `.xlsm` files to Azure Blob Storage.