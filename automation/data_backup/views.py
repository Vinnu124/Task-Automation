from django.shortcuts import render,redirect
import shutil
import os
from google_auth_oauthlib.flow import InstalledAppFlow  
from google.auth.transport.requests import Request 
from django.contrib import messages
from .forms import backup
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError



def home_view(request):
    username=request.session.get('username')
    context={
        'username':username
    }
    return render(request,'home.html',context)
def backup_view(request):
    form = backup()
    logs=[]
    if request.method == 'POST':
        source = request.POST['source']
        destination = request.POST['destination']
        if os.path.isdir(source):
            for filename in os.listdir(source):
                source_file = os.path.join(source, filename)
                destination_file = os.path.join(destination, filename)
                if os.path.isfile(source_file):
                    if not os.path.exists(destination_file):
                        try:
                            shutil.copy2(source_file, destination)
                            logs.append(f'File {filename} copied successfully')
                        except Exception as e:
                            logs.append(str(e))
                    else:
                        logs.append(f'File {filename} already backed up')
            messages.success(request, 'ALL FILES BACKED UP SUCCESSFULLY')           
        else:
            logs.append(f'Invalid source path: {source}')
        
        form = backup()
    context={
        'form':form,
        'logs':logs
    }
    return render(request,'backup.html',context)

def backup_drive(request):
    form=backup()
    if request.method=='POST':
        source=request.POST['source']
        SOURCE=["https://www.googleapis.com/auth/drive"]
        creds=None
        if os.path.exists("token.json"):
            creds=Credentials.from_authorized_user_file('token.json',SOURCE)
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow=InstalledAppFlow.from_client_secrets_file("credentials.json",SOURCE)
                creds=flow.run_local_server(port=0)
            with open("token.json",'w') as token:
                token.write(creds.to_json())
        try:
            service=build("drive","v3", credentials=creds)
            response=service.files.list(
                q="name='Backup_Folder' and mimeType='application/vnd.google-apps.folder'",
                space='drive' 
            ).execute()

            if not response['files']:
                file_metadata={
                    "name":"Backup_Folder",
                    "mimeType":"application/vnd.google-apps.folder"
                }

                file=service.files.create(body=file_metadata,fields="id").execute()

                folder_id=file.get('id')
            else:
                folder_id=response['files'][0]['id']
            for file in os.listdir(source):  # Use the source variable here
                file_metadata={
                    "name":file,
                    "parents":[folder_id]
                }
                media=MediaFileUpload(f"{source}/{file}")  # And here
                upload_file=service.files().create(body=file_metadata,media_body=media,fields="id").execute()
                print("Backed up file " + file)
        except HttpError as e:
            print("Error"+str(e))
            form=backup()
    context={
        "form":form
    }
    return render(request,'drive.html',context)

