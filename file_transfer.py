import os
from ssh_connection import SSHConnection

class FileTransfer:
    def _init_(self, ssh_connection):
        self.ssh_connection = ssh_connection

    def upload(self, local_file, remote_path):
        """Upload a file to the remote server."""
        if os.path.exists(local_file):
            self.ssh_connection.upload_file(local_file, remote_path)
        else:
            print(f"Local file {local_file} does not exist.")

    def download(self, remote_file, local_path):
        """Download a file from the remote server."""
        self.ssh_connection.download_file(remote_file, local_path)
