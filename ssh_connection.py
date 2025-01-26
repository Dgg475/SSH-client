import paramiko
import os

class SSHConnection:
    def __init__(self, host, port, username, password=None):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.client = None
        self.sftp = None

    def connect(self):
        try:
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.client.connect(
                self.host,
                port=self.port,
                username=self.username,
                password=self.password
            )
            self.sftp = self.client.open_sftp()
            print("Connection successful!")
        except Exception as e:
            print(f"Failed to connect: {e}")
            self.client = None

    def list_remote_files(self, remote_path="."):
        try:
            files = self.sftp.listdir(remote_path)
            return files
        except Exception as e:
            return f"Failed to list remote files: {e}"

    def upload_file(self, local_file, remote_path):
        try:
            if not os.path.exists(local_file):
                print(f"Local file '{local_file}' does not exist.")
                return
            remote_file_path = os.path.join(remote_path, os.path.basename(local_file))
            self.sftp.put(local_file, remote_file_path)
            print(f"File '{local_file}' successfully uploaded to '{remote_file_path}'.")
        except Exception as e:
            print(f"Failed to upload file: {e}")

    def download_file(self, remote_file, local_path):
        try:
            if not os.path.exists(local_path):
                print(f"Local path '{local_path}' does not exist. Creating it.")
                os.makedirs(local_path, exist_ok=True)
            local_file_path = os.path.join(local_path, os.path.basename(remote_file))
            self.sftp.get(remote_file, local_file_path)
            print(f"File '{remote_file}' successfully downloaded to '{local_file_path}'.")
        except Exception as e:
            print(f"Failed to download file: {e}")

    def execute_command(self, command):
        try:
            stdin, stdout, stderr = self.client.exec_command(command)
            return stdout.read().decode() + stderr.read().decode()
        except Exception as e:
            return f"Failed to execute command: {e}"

    def close(self):
        try:
            if self.sftp:
                self.sftp.close()
            if self.client:
                self.client.close()
            print("Connection closed.")
        except Exception as e:
            print(f"Failed to close connection: {e}")
