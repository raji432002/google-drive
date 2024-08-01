# # # # from flask import Flask, render_template, request, redirect, url_for, send_file, jsonify
# # # # from google.oauth2.credentials import Credentials
# # # # from google_auth_oauthlib.flow import InstalledAppFlow
# # # # from google.auth.transport.requests import Request
# # # # from googleapiclient.discovery import build
# # # # from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
# # # # import os
# # # # import io

# # # # app = Flask(__name__)

# # # # SCOPES = ['https://www.googleapis.com/auth/drive.file']
# # # # CREDENTIALS_PATH = 'credentials.json'
# # # # TOKEN_PATH = 'token.json'
# # # # UPLOAD_FOLDER = 'uploads'

# # # # # Ensure the uploads directory exists
# # # # if not os.path.exists(UPLOAD_FOLDER):
# # # #     os.makedirs(UPLOAD_FOLDER)

# # # # class GoogleDriveManager:
# # # #     def __init__(self):
# # # #         self.creds = None
# # # #         self.service = None
# # # #         self.authenticate()

# # # #     def authenticate(self):
# # # #         if os.path.exists(TOKEN_PATH):
# # # #             self.creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)

# # # #         if not self.creds or not self.creds.valid:
# # # #             if self.creds and self.creds.expired and self.creds.refresh_token:
# # # #                 self.creds.refresh(Request())
# # # #             else:
# # # #                 flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
# # # #                 self.creds = flow.run_local_server(port=0)
# # # #             with open(TOKEN_PATH, 'w') as token:
# # # #                 token.write(self.creds.to_json())

# # # #         self.service = build('drive', 'v3', credentials=self.creds)

# # # #     def list_files(self):
# # # #         try:
# # # #             results = self.service.files().list(
# # # #                 pageSize=10, fields="nextPageToken, files(id, name, mimeType)").execute()
# # # #             items = results.get('files', [])
# # # #             return items
# # # #         except Exception as error:
# # # #             print(f'An error occurred while listing files from Google Drive: {error}')
# # # #             return []

# # # #     def upload_file(self, file_path, file_name, mimetype):
# # # #         file_metadata = {'name': file_name}
# # # #         media = MediaFileUpload(file_path, mimetype=mimetype)

# # # #         try:
# # # #             file = self.service.files().create(body=file_metadata, media_body=media, fields='id').execute()
# # # #             return file.get("id")
# # # #         except Exception as error:
# # # #             print(f'An error occurred while uploading file to Google Drive: {error}')
# # # #             return None

# # # #     def download_file(self, file_id):
# # # #         try:
# # # #             request = self.service.files().get_media(fileId=file_id)
# # # #             fh = io.BytesIO()
# # # #             downloader = MediaIoBaseDownload(fh, request)
# # # #             done = False
# # # #             while not done:
# # # #                 status, done = downloader.next_chunk()
# # # #                 print(f'Download {int(status.progress() * 100)}% complete.')
# # # #             fh.seek(0)
# # # #             return fh
# # # #         except Exception as error:
# # # #             print(f'An error occurred while downloading file from Google Drive: {error}')
# # # #             return None

# # # #     def delete_file(self, file_id):
# # # #         try:
# # # #             self.service.files().delete(fileId=file_id).execute()
# # # #             return True
# # # #         except Exception as error:
# # # #             print(f'An error occurred while deleting file from Google Drive: {error}')
# # # #             return False

# # # # drive_manager = GoogleDriveManager()

# # # # @app.route('/')
# # # # def index():
# # # # #    files = drive_manager.list_files()
# # # # #    local_files = [{'id': f, 'name': f, 'mimeType': 'local'} for f in os.listdir(UPLOAD_FOLDER)]
# # # # #    return render_template('index.html', files=files + local_files)
# # # #     google_files = drive_manager.list_files()
# # # #     local_files = [{'id': f, 'name': f, 'mimeType': 'local'} for f in os.listdir(UPLOAD_FOLDER)]
    
# # # #     # Ensure local files have unique IDs
# # # #     combined_files = google_files + [{'id': 'local-' + f['id'], 'name': f['name'], 'mimeType': f['mimeType']} for f in local_files]
    
# # # #     return render_template('index.html', files=combined_files)
# # # # @app.route('/upload', methods=['POST'])
# # # # def upload():
# # # #     if 'file' not in request.files:
# # # #         return redirect(url_for('index'))

# # # #     file = request.files['file']
# # # #     if file and file.filename != '':
# # # #         file_path = os.path.join(UPLOAD_FOLDER, file.filename)
# # # #         file.save(file_path)

# # # #         file_id = drive_manager.upload_file(file_path, file.filename, file.mimetype)
# # # #         return redirect(url_for('index'))

# # # #     return redirect(url_for('index'))

# # # # @app.route('/download/<file_id>')
# # # # def download(file_id):
# # # #     local_file_path = os.path.join(UPLOAD_FOLDER, file_id)
# # # #     if os.path.exists(local_file_path):
# # # #         return send_file(local_file_path, as_attachment=True)

# # # #     file = drive_manager.download_file(file_id)
# # # #     if file:
# # # #         return send_file(file, as_attachment=True, download_name=file_id)

# # # #     return redirect(url_for('index'))

# # # # @app.route('/delete/<file_id>', methods=['POST'])
# # # # def delete(file_id):
# # # #     local_file_path = os.path.join(UPLOAD_FOLDER, file_id)
# # # #     if os.path.exists(local_file_path):
# # # #         os.remove(local_file_path)
# # # #         return jsonify({'success': True})

# # # #     success = drive_manager.delete_file(file_id)
# # # #     return jsonify({'success': success})

# # # # if __name__ == '__main__':
# # # #     app.run(debug=True)

# # # from flask import Flask, render_template, request, redirect, url_for, send_file, jsonify
# # # from google.oauth2.credentials import Credentials
# # # from google_auth_oauthlib.flow import InstalledAppFlow
# # # from google.auth.transport.requests import Request
# # # from googleapiclient.discovery import build
# # # from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
# # # import os
# # # import io

# # # app = Flask(__name__)

# # # SCOPES = ['https://www.googleapis.com/auth/drive.file']
# # # CREDENTIALS_PATH = 'credentials.json'
# # # TOKEN_PATH = 'token.json'
# # # UPLOAD_FOLDER = 'uploads'

# # # # Ensure the uploads directory exists
# # # if not os.path.exists(UPLOAD_FOLDER):
# # #     os.makedirs(UPLOAD_FOLDER)

# # # class GoogleDriveManager:
# # #     def __init__(self):
# # #         self.creds = None
# # #         self.service = None
# # #         self.authenticate()

# # #     def authenticate(self):
# # #         if os.path.exists(TOKEN_PATH):
# # #             self.creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)

# # #         if not self.creds or not self.creds.valid:
# # #             if self.creds and self.creds.expired and self.creds.refresh_token:
# # #                 self.creds.refresh(Request())
# # #             else:
# # #                 flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
# # #                 self.creds = flow.run_local_server(port=0)
# # #             with open(TOKEN_PATH, 'w') as token:
# # #                 token.write(self.creds.to_json())

# # #         self.service = build('drive', 'v3', credentials=self.creds)

# # #     # def list_files(self):
# # #     #     try:
# # #     #         query = "mimeType != 'application/vnd.google-apps.folder'"
# # #     #         results = self.service.files().list(
# # #     #             q=query,
# # #     #             pageSize=10,
# # #     #             fields="nextPageToken, files(id, name, mimeType)"
# # #     #         ).execute()
# # #     #         items = results.get('files', [])
# # #     #         return items
# # #     #     except Exception as error:
# # #     #         print(f'An error occurred while listing files from Google Drive: {error}')
# # #     #         return []
# # #     def list_files(self):
# # #         try:
# # #             results = self.service.files().list(
# # #                 pageSize=10,
# # #                 fields="nextPageToken, files(id, name, mimeType)"
# # #             ).execute()
# # #             items = results.get('files', [])
# # #             return items
# # #         except Exception as error:
# # #             print(f'An error occurred while listing files from Google Drive: {error}')
# # #             return []

# # #     def upload_file(self, file_path, file_name, mimetype):
# # #         file_metadata = {'name': file_name}
# # #         media = MediaFileUpload(file_path, mimetype=mimetype)

# # #         try:
# # #             file = self.service.files().create(body=file_metadata, media_body=media, fields='id').execute()
# # #             return file.get("id")
# # #         except Exception as error:
# # #             print(f'An error occurred while uploading file to Google Drive: {error}')
# # #             return None

# # #     def download_file(self, file_id):
# # #         try:
# # #             request = self.service.files().get_media(fileId=file_id)
# # #             fh = io.BytesIO()
# # #             downloader = MediaIoBaseDownload(fh, request)
# # #             done = False
# # #             while not done:
# # #                 status, done = downloader.next_chunk()
# # #                 print(f'Download {int(status.progress() * 100)}% complete.')
# # #             fh.seek(0)
# # #             return fh
# # #         except Exception as error:
# # #             print(f'An error occurred while downloading file from Google Drive: {error}')
# # #             return None

# # #     def delete_file(self, file_id):
# # #         try:
# # #             self.service.files().delete(fileId=file_id).execute()
# # #             return True
# # #         except Exception as error:
# # #             print(f'An error occurred while deleting file from Google Drive: {error}')
# # #             return False

# # # drive_manager = GoogleDriveManager()

# # # @app.route('/')
# # # def index():
# # #     files = drive_manager.list_files()
# # #     local_files = [{'id': f, 'name': f, 'mimeType': 'local'} for f in os.listdir(UPLOAD_FOLDER)]
# # #     return render_template('index.html', files=files + local_files)

# # # @app.route('/upload', methods=['POST'])
# # # def upload():
# # #     if 'file' not in request.files:
# # #         return redirect(url_for('index'))

# # #     file = request.files['file']
# # #     if file and file.filename != '':
# # #         file_path = os.path.join(UPLOAD_FOLDER, file.filename)
# # #         file.save(file_path)

# # #         file_id = drive_manager.upload_file(file_path, file.filename, file.mimetype)
# # #         return redirect(url_for('index'))

# # #     return redirect(url_for('index'))

# # # @app.route('/download/<file_id>')
# # # def download(file_id):
# # #     local_file_path = os.path.join(UPLOAD_FOLDER, file_id)
# # #     if os.path.exists(local_file_path):
# # #         return send_file(local_file_path, as_attachment=True)

# # #     file = drive_manager.download_file(file_id)
# # #     if file:
# # #         return send_file(file, as_attachment=True, download_name=file_id)

# # #     return redirect(url_for('index'))

# # # @app.route('/delete/<file_id>', methods=['POST'])
# # # def delete(file_id):
# # #     local_file_path = os.path.join(UPLOAD_FOLDER, file_id)
# # #     if os.path.exists(local_file_path):
# # #         os.remove(local_file_path)
# # #         return jsonify({'success': True})

# # #     success = drive_manager.delete_file(file_id)
# # #     return jsonify({'success': success})

# # # if __name__ == '__main__':
# # #     app.run(debug=True)


# # from flask import Flask, render_template, request, redirect, url_for, send_file, jsonify
# # from google.oauth2.credentials import Credentials
# # from google_auth_oauthlib.flow import InstalledAppFlow
# # from google.auth.transport.requests import Request
# # from googleapiclient.discovery import build
# # from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
# # import os
# # import io

# # app = Flask(__name__)

# # SCOPES = ['https://www.googleapis.com/auth/drive.file']
# # CREDENTIALS_PATH = 'credentials.json'
# # TOKEN_PATH = 'token.json'
# # UPLOAD_FOLDER = 'uploads'

# # # Ensure the uploads directory exists
# # if not os.path.exists(UPLOAD_FOLDER):
# #     os.makedirs(UPLOAD_FOLDER)

# # class GoogleDriveManager:
# #     def __init__(self):
# #         self.creds = None
# #         self.service = None
# #         self.authenticate()

# #     def authenticate(self):
# #         if os.path.exists(TOKEN_PATH):
# #             self.creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)

# #         if not self.creds or not self.creds.valid:
# #             if self.creds and self.creds.expired and self.creds.refresh_token:
# #                 self.creds.refresh(Request())
# #             else:
# #                 flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
# #                 self.creds = flow.run_local_server(port=0)
# #             with open(TOKEN_PATH, 'w') as token:
# #                 token.write(self.creds.to_json())

# #         self.service = build('drive', 'v3', credentials=self.creds)

# #     def list_files(self):
# #         try:
# #             results = self.service.files().list(
# #                 pageSize=10,
# #                 fields="nextPageToken, files(id, name, mimeType)"
# #             ).execute()
# #             items = results.get('files', [])
# #             return items
# #         except Exception as error:
# #             print(f'An error occurred while listing files from Google Drive: {error}')
# #             return []

# #     def upload_file(self, file_path, file_name, mimetype):
# #         file_metadata = {'name': file_name}
# #         media = MediaFileUpload(file_path, mimetype=mimetype)

# #         try:
# #             file = self.service.files().create(body=file_metadata, media_body=media, fields='id').execute()
# #             return file.get("id")
# #         except Exception as error:
# #             print(f'An error occurred while uploading file to Google Drive: {error}')
# #             return None

# #     def download_file(self, file_id):
# #         try:
# #             request = self.service.files().get_media(fileId=file_id)
# #             fh = io.BytesIO()
# #             downloader = MediaIoBaseDownload(fh, request)
# #             done = False
# #             while not done:
# #                 status, done = downloader.next_chunk()
# #                 print(f'Download {int(status.progress() * 100)}% complete.')
# #             fh.seek(0)
# #             return fh
# #         except Exception as error:
# #             print(f'An error occurred while downloading file from Google Drive: {error}')
# #             return None

# #     def delete_file(self, file_id):
# #         try:
# #             self.service.files().delete(fileId=file_id).execute()
# #             return True
# #         except Exception as error:
# #             print(f'An error occurred while deleting file from Google Drive: {error}')
# #             return False

# # drive_manager = GoogleDriveManager()

# # @app.route('/')
# # def index():
# #     files = drive_manager.list_files()
# #     local_files = [{'id': f, 'name': f, 'mimeType': 'local'} for f in os.listdir(UPLOAD_FOLDER)]
# #     return render_template('index.html', files=files + local_files)

# # @app.route('/upload', methods=['POST'])
# # def upload():
# #     if 'file' not in request.files:
# #         return redirect(url_for('index'))

# #     file = request.files['file']
# #     if file and file.filename != '':
# #         file_path = os.path.join(UPLOAD_FOLDER, file.filename)
# #         file.save(file_path)

# #         file_id = drive_manager.upload_file(file_path, file.filename, file.mimetype)
# #         return redirect(url_for('index'))

# #     return redirect(url_for('index'))

# # @app.route('/download/<file_id>')
# # def download(file_id):
# #     local_file_path = os.path.join(UPLOAD_FOLDER, file_id)
# #     if os.path.exists(local_file_path):
# #         return send_file(local_file_path, as_attachment=True)

# #     file = drive_manager.download_file(file_id)
# #     if file:
# #         return send_file(file, as_attachment=True, download_name=file_id)

# #     return redirect(url_for('index'))

# # @app.route('/delete/<file_id>', methods=['POST'])
# # def delete(file_id):
# #     local_file_path = os.path.join(UPLOAD_FOLDER, file_id)
# #     if os.path.exists(local_file_path):
# #         os.remove(local_file_path)
# #         return jsonify({'success': True})

# #     success = drive_manager.delete_file(file_id)
# #     return jsonify({'success': success})

# # @app.route('/folder/<folder_id>')
# # def folder_contents(folder_id):
# #     try:
# #         query = f"'{folder_id}' in parents"
# #         results = drive_manager.service.files().list(
# #             q=query,
# #             pageSize=10,
# #             fields="nextPageToken, files(id, name, mimeType)"
# #         ).execute()
# #         items = results.get('files', [])
# #         return render_template('folder_contents.html', files=items)
# #     except Exception as error:
# #         print(f'An error occurred while retrieving folder contents: {error}')
# #         return redirect(url_for('index'))

# # if __name__ == '__main__':
# #     app.run(debug=True)


# from flask import Flask, render_template, request, redirect, url_for, send_file, jsonify
# from google.oauth2.credentials import Credentials
# from google_auth_oauthlib.flow import InstalledAppFlow
# from google.auth.transport.requests import Request
# from googleapiclient.discovery import build
# from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
# import os
# import io
# import logging

# logging.basicConfig(
#     level=logging.DEBUG,
#     format='%(asctime)s %(levelname)s %(name)s %(threadname)s : %(message)s',
#     handlers=[
#         logging.FileHandler('app.log'),
#         logging.StreamHandler
#     ]
# )

# app = Flask(__name__)

# SCOPES = ['https://www.googleapis.com/auth/drive.file']
# CREDENTIALS_PATH = 'credentials.json'
# TOKEN_PATH = 'token.json'
# UPLOAD_FOLDER = 'uploads'

# # Ensure the uploads directory exists
# if not os.path.exists(UPLOAD_FOLDER):
#     os.makedirs(UPLOAD_FOLDER)

# class GoogleDriveManager:
#     def __init__(self):
#         self.creds = None
#         self.service = None
#         self.authenticate()

#     def authenticate(self):
#         logging.info('Authenticating with Google Drive API')
#         if os.path.exists(TOKEN_PATH):
#             self.creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)

#         if not self.creds or not self.creds.valid:
#             if self.creds and self.creds.expired and self.creds.refresh_token:
#                 logging.info('Refreshing expired Google Drive credentials')
#                 self.creds.refresh(Request())
#             else:
#                 logging.info('Starting new authentication flow for Google Drive')
#                 flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
#                 self.creds = flow.run_local_server(port=0)
#             with open(TOKEN_PATH, 'w') as token:
#                 token.write(self.creds.to_json())

#         self.service = build('drive', 'v3', credentials=self.creds)
#         logging.info('Google Drive API authentication successful')

#     def list_files(self):
#         logging.info('Listing files from Google Drive')
#         try:
#             #logging.info
#             #q="mimeType='application/vnd.google-apps.folder' or mimeType!='application/vnd.google-apps.folder'",

#             results = self.service.files().list(
#                 q="",
#                 pageSize=100,
#                 fields="nextPageToken, files(id, name, mimeType)"
#             ).execute()
#             items = results.get('files', [])
#             logging.debug(f'Files listed from Google Drive : {items}')
#             return items
#         except Exception as error:
#             logging.error(f'An error occurred while listing files from Google Drive: {error}')
#             return []

#     def upload_file(self, file_path, file_name, mimetype, parent_id=None):
#         file_metadata = {'name': file_name}
#         if parent_id:
#             file_metadata['parents'] = [parent_id]
#         media = MediaFileUpload(file_path, mimetype=mimetype)

#         try:
#             file = self.service.files().create(body=file_metadata, media_body=media, fields='id').execute()
#             return file.get("id")
#         except Exception as error:
#             print(f'An error occurred while uploading file to Google Drive: {error}')
#             return None

#     def create_folder(self, folder_name, parent_id=None):
#         file_metadata = {
#             'name': folder_name,
#             'mimeType': 'application/vnd.google-apps.folder'
#         }
#         if parent_id:
#             file_metadata['parents'] = [parent_id]

#         try:
#             folder = self.service.files().create(body=file_metadata, fields='id').execute()
#             return folder.get('id')
#         except Exception as error:
#             print(f'An error occurred while creating folder in Google Drive: {error}')
#             return None

#     def download_file(self, file_id):
#         try:
#             request = self.service.files().get_media(fileId=file_id)
#             fh = io.BytesIO()
#             downloader = MediaIoBaseDownload(fh, request)
#             done = False
#             while not done:
#                 status, done = downloader.next_chunk()
#                 print(f'Download {int(status.progress() * 100)}% complete.')
#             fh.seek(0)
#             return fh
#         except Exception as error:
#             print(f'An error occurred while downloading file from Google Drive: {error}')
#             return None

#     def delete_file(self, file_id):
#         try:
#             self.service.files().delete(fileId=file_id).execute()
#             return True
#         except Exception as error:
#             print(f'An error occurred while deleting file from Google Drive: {error}')
#             return False

# drive_manager = GoogleDriveManager()

# @app.route('/')
# def index():
#     files = drive_manager.list_files()
#    # local_files = [{'id': f, 'name': f, 'mimeType': 'local'} for f in os.listdir(UPLOAD_FOLDER)]
#     return render_template('index.html', files=files)

# @app.route('/upload', methods=['POST'])
# def upload():
#     if 'file' not in request.files:
#         return redirect(url_for('index'))

#     file = request.files['file']
#     if file and file.filename != '':
#         file_path = os.path.join(UPLOAD_FOLDER, file.filename)
#         file.save(file_path)

#         file_id = drive_manager.upload_file(file_path, file.filename, file.mimetype)
#         return redirect(url_for('index'))

#     return redirect(url_for('index'))

# @app.route('/upload_folder', methods=['POST'])
# def upload_folder():
#     folder_name = request.form['folder_name']
#     parent_folder_id = request.form.get('parent_folder_id')  # Optional parent folder ID

#     folder_id = drive_manager.create_folder(folder_name, parent_folder_id)
#     if not folder_id:
#         return jsonify({'success': False, 'message': 'Failed to create folder'})

#     for file in request.files.getlist('files'):
#         if file and file.filename != '':
#             file_path = os.path.join(UPLOAD_FOLDER, file.filename)
#             file.save(file_path)
#             drive_manager.upload_file(file_path, file.filename, file.mimetype, folder_id)

#     return redirect(url_for('index'))

# @app.route('/download/<file_id>')
# def download(file_id):
#     local_file_path = os.path.join(UPLOAD_FOLDER, file_id)
#     if os.path.exists(local_file_path):
#         return send_file(local_file_path, as_attachment=True)

#     file = drive_manager.download_file(file_id)
#     if file:
#         return send_file(file, as_attachment=True, download_name=file_id)

#     return redirect(url_for('index'))

# @app.route('/delete/<file_id>', methods=['POST'])
# def delete(file_id):
#     local_file_path = os.path.join(UPLOAD_FOLDER, file_id)
#     if os.path.exists(local_file_path):
#         os.remove(local_file_path)
#         return jsonify({'success': True})

#     success = drive_manager.delete_file(file_id)
#     return jsonify({'success': success})

# @app.route('/folder/<folder_id>')
# def folder_contents(folder_id):
#     try:
#         query = f"'{folder_id}' in parents"
#         results = drive_manager.service.files().list(
#             q=query,
#             pageSize=10,
#             fields="nextPageToken, files(id, name, mimeType)"
#         ).execute()
#         items = results.get('files', [])
#         return render_template('folder_contents.html', files=items)
#     except Exception as error:
#         print(f'An error occurred while retrieving folder contents: {error}')
#         return redirect(url_for('index'))
# @app.route('/folder/<folder_id>')

# def view_folder(folder_id):
#     try:
#         results = drive_manager.service.files().list(
#             q=f"'{folder_id}' in parents",
#             pageSize=100,
#             fields="nextPageToken, files(id, name, mimeType)").execute()
#         items = results.get('files', [])
#         return render_template('index.html', files=items)
#     except Exception as error:
#         print(f'An error occurred while listing folder contents: {error}')
#         return redirect(url_for('index'))


# if __name__ == '__main__':
#     app.run(debug=True)
# logging file

# from flask import Flask, render_template, request, redirect, url_for, send_file, jsonify
# from google.oauth2.credentials import Credentials
# from google_auth_oauthlib.flow import InstalledAppFlow
# from google.auth.transport.requests import Request
# from googleapiclient.discovery import build
# from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
# import os
# import io
# import logging

# # Configure logging
# logging.basicConfig(
#     level=logging.DEBUG,
#     format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s',
#     handlers=[
#         logging.FileHandler("app.log"),
#         logging.StreamHandler()
#     ]
# )

# app = Flask(__name__)

# SCOPES = ['https://www.googleapis.com/auth/drive.file']
# CREDENTIALS_PATH = 'credentials.json'
# TOKEN_PATH = 'token.json'
# UPLOAD_FOLDER = 'uploads'

# # Ensure the uploads directory exists
# if not os.path.exists(UPLOAD_FOLDER):
#     os.makedirs(UPLOAD_FOLDER)

# class GoogleDriveManager:
#     def __init__(self):
#         self.creds = None
#         self.service = None
#         self.authenticate()

#     def authenticate(self):
#         logging.info("Authenticating with Google Drive API")
#         if os.path.exists(TOKEN_PATH):
#             self.creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)

#         if not self.creds or not self.creds.valid:
#             if self.creds and self.creds.expired and self.creds.refresh_token:
#                 logging.info("Refreshing expired Google Drive credentials")
#                 self.creds.refresh(Request())
#             else:
#                 logging.info("Starting new authentication flow for Google Drive")
#                 flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
#                 self.creds = flow.run_local_server(port=0)
#             with open(TOKEN_PATH, 'w') as token:
#                 token.write(self.creds.to_json())

#         self.service = build('drive', 'v3', credentials=self.creds)
#         logging.info("Google Drive API authentication successful")

#     def list_files(self):
#         logging.info("Listing files from Google Drive")
#         try:
#             results = self.service.files().list(
#                 q="mimeType='application/vnd.google-apps.folder' or mimeType!='application/vnd.google-apps.folder'",
#                 pageSize=100,
#                 fields="nextPageToken, files(id, name, mimeType)").execute()
#             items = results.get('files', [])
#             logging.debug(f"Files listed from Google Drive")
#             return items
#         except Exception as error:
#             logging.error(f"An error occurred while listing files from Google Drive: {error}")
#             return []

#     def upload_file(self, file_path, file_name, mimetype):
#         logging.info(f"Uploading file to Google Drive: {file_name}")
#         file_metadata = {'name': file_name}
#         media = MediaFileUpload(file_path, mimetype=mimetype)

#         try:
#             file = self.service.files().create(body=file_metadata, media_body=media, fields='id').execute()
#             logging.info(f"File uploaded successfully to Google Drive: {file.get('id')}")
#             return file.get("id")
#         except Exception as error:
#             logging.error(f"An error occurred while uploading file to Google Drive: {error}")
#             return None

#     def download_file(self, file_id):
#         logging.info(f"Downloading file from Google Drive: {file_id}")
#         try:
#             request = self.service.files().get_media(fileId=file_id)
#             fh = io.BytesIO()
#             downloader = MediaIoBaseDownload(fh, request)
#             done = False
#             while not done:
#                 status, done = downloader.next_chunk()
#                 logging.debug(f"Download {int(status.progress() * 100)}% complete.")
#             fh.seek(0)
#             logging.info("File downloaded successfully from Google Drive")
#             return fh
#         except Exception as error:
#             logging.error(f"An error occurred while downloading file from Google Drive: {error}")
#             return None

#     def delete_file(self, file_id):
#         logging.info(f"Deleting file from Google Drive: {file_id}")
#         try:
#             self.service.files().delete(fileId=file_id).execute()
#             logging.info("File deleted successfully from Google Drive")
#             return True
#         except Exception as error:
#             logging.error(f"An error occurred while deleting file from Google Drive: {error}")
#             return False

# drive_manager = GoogleDriveManager()

# @app.route('/')
# def index():
#     logging.info("Fetching list of files for index page")
#     files = drive_manager.list_files()
#     local_files = [{'id': f, 'name': f} for f in os.listdir(UPLOAD_FOLDER)]
#     logging.debug(f"Local files: {local_files}")
#     return render_template('index.html', files=files + local_files)

# @app.route('/upload', methods=['POST'])
# def upload():
#     logging.info("Handling file upload request")
#     if 'file' not in request.files:
#         logging.warning("No file part in the request")
#         return redirect(url_for('index'))

#     file = request.files['file']
#     if file and file.filename != '':
#         file_path = os.path.join(UPLOAD_FOLDER, file.filename)
#         file.save(file_path)
#         logging.info(f"File saved locally: {file_path}")

#         file_id = drive_manager.upload_file(file_path, file.filename, file.mimetype)
#         return redirect(url_for('index'))

#     logging.warning("No file selected for upload")
#     return redirect(url_for('index'))

# @app.route('/download/<file_id>')
# def download(file_id):
#     logging.info(f"Handling file download request: {file_id}")
#     local_file_path = os.path.join(UPLOAD_FOLDER, file_id)
#     if os.path.exists(local_file_path):
#         logging.info(f"Serving local file: {local_file_path}")
#         return send_file(local_file_path, as_attachment=True)

#     file = drive_manager.download_file(file_id)
#     if file:
#         logging.info("Serving downloaded file from Google Drive")
#         return send_file(file, as_attachment=True, download_name=file_id)

#     logging.error("File not found for download")
#     return redirect(url_for('index'))

# @app.route('/delete/<file_id>', methods=['POST'])
# def delete(file_id):
#     logging.info(f"Handling file deletion request: {file_id}")
#     local_file_path = os.path.join(UPLOAD_FOLDER, file_id)
#     if os.path.exists(local_file_path):
#         os.remove(local_file_path)
#         logging.info("Local file deleted successfully")
#         return jsonify({'success': True})

#     success = drive_manager.delete_file(file_id)
#     return jsonify({'success': success})

# @app.route('/folder/<folder_id>')
# def view_folder(folder_id):
#     logging.info(f"Viewing contents of folder: {folder_id}")
#     try:
#         results = drive_manager.service.files().list(
#             q=f"'{folder_id}' in parents",
#             pageSize=100,
#             fields="nextPageToken, files(id, name, mimeType)").execute()
#         items = results.get('files', [])
#         logging.debug(f"Contents of folder {folder_id}: {items}")
#         return render_template('index.html', files=items)
#     except Exception as error:
#         logging.error(f"An error occurred while listing folder contents: {error}")
#         return redirect(url_for('index'))

# if __name__ == '__main__':
#     app.run(debug=True)
