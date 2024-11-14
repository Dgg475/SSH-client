import paramiko

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
            # Create SSH client instance
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            # If password is provided, use it for the connection
            if self.password:
                self.client.connect(self.host, port=self.port, username=self.username, password=self.password)
            else:
                self.client.connect(self.host, port=self.port, username=self.username)

            # Create SFTP session for file transfers
            self.sftp = self.client.open_sftp()
            print(f"Connected to {self.host}:{self.port}")
        except Exception as e:
            print(f"Failed to connect: {e}")
            self.client = None

    def execute_command(self, command):
        """Execute arbitrary command on remote server and return output."""
        if not self.client:
            print("No active SSH connection.")
            return
        try:
            stdin, stdout, stderr = self.client.exec_command(command)
            return stdout.read().decode()  # Read command output
        except Exception as e:
            return f"Error executing command: {e}"

    def upload_file(self, local_path, remote_path):
        if not self.sftp:
            print("No active SSH connection.")
            return
        try:
            self.sftp.put(local_path, remote_path)
            print(f"Uploaded {local_path} to {remote_path}")
        except Exception as e:
            print(f"Error uploading file: {e}")

    def download_file(self, remote_path, local_path):
        if not self.sftp:
            print("No active SSH connection.")
            return
        try:
            self.sftp.get(remote_path, local_path)
            print(f"Downloaded {remote_path} to {local_path}")
        except Exception as e:
            print(f"Error downloading file: {e}")

    def list_remote_files(self, remote_path="."):
        """List files in a remote directory."""
        if not self.sftp:
            print("No active SSH connection.")
            return
        try:
            return self.sftp.listdir(remote_path)
        except Exception as e:
            return f"Error listing files: {e}"

    def close(self):
        if self.client:
            self.sftp.close()
            self.client.close()
            print("Connection closed.")
