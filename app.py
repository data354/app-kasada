import streamlit as st
from googleapiclient.discovery import build
from fonctions import check_credentials, update_password, create_user, user_exists, log_action
from fonc import authenticate_google_drive, authenticate_azure_blob, list_files_in_drive_folder, get_folder_name, download_file_from_drive, upload_file_to_azure_blob, connect_str


st.set_page_config(
        page_title="usali loading app ",
)

# Login page
def login():
    st.title("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if check_credentials(username, password):
            st.success(f"Welcome, {username}!")
            st.session_state['logged_in'] = True
            st.session_state['username'] = username
        else:
            st.warning("Incorrect username or password.")

# Change password page
def change_password():
    st.title("Change Password")

    username = st.text_input("Username")
    old_password = st.text_input("Old Password", type="password")
    new_password = st.text_input("New Password", type="password")
    confirm_password = st.text_input("Confirm New Password", type="password")

    if st.button("Change Password"):
        if new_password != confirm_password:
            st.warning("Passwords do not match.")
        elif not check_credentials(username, old_password):
            st.warning("Incorrect old password.")
        else:
            update_password(username, new_password)
            st.success("Password successfully changed.")

# Create new account page
def create_account():
    st.title("Create New Account")

    new_username = st.text_input("New Username")
    new_password = st.text_input("New Password", type="password")
    confirm_new_password = st.text_input("Confirm New Password", type="password")

    if st.button("Create Account"):
        if new_password != confirm_new_password:
            st.warning("Passwords do not match.")
        elif user_exists(new_username):
            st.warning("Username already exists.")
        else:
            create_user(new_username, new_password)
            st.success(f"Account for {new_username} created successfully!")

# Transfer application
def transfer_app():

    # Sidebar
    st.sidebar.header("Parameters")

    # Input for Google Drive folder link
    url = st.sidebar.text_input("Enter the URL of the Google Drive folder")
    folder_id = url.split("/")[-1]

    # Button to list files
    list_files_button = st.sidebar.button("View files")

    # Button to transfer files
    transfer_files_button = st.sidebar.button("Transfer files to Azure")

    # Authenticate Google Drive with feedback
    def authenticate_google_with_feedback():
        try:
            creds = authenticate_google_drive()
            st.success("✅ Authentication successful! 😊")
            return creds
        except Exception as e:
            st.error("❌ Authentication failed! Please check your credentials.")
            st.error(f"Error: {str(e)}")
            return None

    # If "View files" button is clicked
    if list_files_button:
        creds = authenticate_google_with_feedback()
        
        if creds:
            drive_service = build('drive', 'v3', credentials=creds)
            
            # Get folder name
            folder_name = get_folder_name(drive_service, folder_id)
            
            # List files in the Google Drive folder
            files = list_files_in_drive_folder(drive_service, folder_id)
            
            if files:
                st.write(f"Files in folder '{folder_name}':")
                for file in files:
                    st.write(f"- {file['name']}")
            else:
                st.write("No files found in the folder.")
        
        # Log the action
        log_action(st.session_state['username'], "Viewed files in Google Drive")

    # If "Transfer files to Azure" button is clicked
    if transfer_files_button:
        creds = authenticate_google_with_feedback()
        
        if creds:
            drive_service = build('drive', 'v3', credentials=creds)
            blob_service_client = authenticate_azure_blob(connect_str)
            
            # List files in the Google Drive folder
            files = list_files_in_drive_folder(drive_service, folder_id)
            folder_name = get_folder_name(drive_service, folder_id)
            
            # Transfer .xlsm files to Azure
            for file in files:
                if file['name'].endswith('.xlsm'):
                    st.write(f"Downloading {file['name']}...")
                    file_stream = download_file_from_drive(drive_service, file['id'])
                    success = upload_file_to_azure_blob(blob_service_client, 'bronze', folder_name, file['name'], file_stream)
                    if success:
                        st.success(f"{file['name']} has been uploaded successfully 😊")
                    else:
                        st.error(f"Upload failed for {file['name']}.")
        
        # Log the action
        log_action(st.session_state['username'], "Transferred files to Azure")

# Main application interface after login
def main_page():
    st.title(f"Welcome {st.session_state['username']} to the Transfer Application!")
    transfer_app()
    if st.button("Logout"):
        st.session_state['logged_in'] = False
        log_action(st.session_state['username'], "Logged out")

# Main function with login and navigation logic
def main():
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

    # Show sidebar menu only if user is not logged in
    if not st.session_state['logged_in']:
        # Sidebar menu with options
        menu = ["Login", "Change Password", "Create Account"]
        choice = st.sidebar.selectbox("Menu", menu)

        # Display the selected page
        if choice == "Login":
            login()
        elif choice == "Change Password":
            change_password()
        elif choice == "Create Account":
            create_account()
    else:
        # If user is logged in, display the main application
        main_page()

if __name__ == "__main__":
    main()
