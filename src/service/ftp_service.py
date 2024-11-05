import os
import ftplib
from dotenv import load_dotenv
load_dotenv()

def download_image(filename: str) -> None:
  ftp_server: str = os.getenv("FTP_SERVER")
  ftp_user: str = os.getenv("FTP_USER")
  ftp_password: str = os.getenv("FTP_PASSWORD")
  ftp_folder: str = os.getenv("FTP_FOLDER")
  
  with ftplib.FTP(ftp_server) as ftp:
    try:
      ftp.login(ftp_user, ftp_password)
      print(f"Connected to {ftp_server} as {ftp_user}")
      
      ftp.cwd(ftp_folder)
      
      local_file_path = os.path.join(os.path.dirname(__file__), "../data", filename)
      os.makedirs(os.path.dirname(local_file_path), exist_ok=True)
      
      with open(local_file_path, "wb") as local_file:
        ftp.retrbinary(f"RETR {filename}", local_file.write)
        
      print(f"Downloaded {filename} from {ftp_server}")
    except ftplib.all_errors as e:
      print(f"Ftp error: {e}")
      
def upload_image(filename: str) -> None:
  ftp_server: str = os.getenv("FTP_SERVER")
  ftp_user: str = os.getenv("FTP_USER")
  ftp_password: str = os.getenv("FTP_PASSWORD")
  ftp_folder_output: str = os.getenv("FTP_FOLDER_OUTPUT")
  
  with ftplib.FTP(ftp_server) as ftp:
    try:
      ftp.login(ftp_user, ftp_password)
      print(f"Connected to {ftp_server} as {ftp_user}")
      
      ftp.cwd(ftp_folder_output)
      
      local_file_path = os.path.join(os.path.dirname(__file__), "../../output", filename)
      
      with open(local_file_path, "rb") as local_file:
        ftp.storbinary(f"STOR {filename}", local_file)
        
      print(f"Uploaded {filename} to {ftp_server}")
      
      os.remove(local_file_path)
    except ftplib.all_errors as e:
      print(f"Ftp error: {e}")