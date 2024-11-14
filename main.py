from ssh_connection import SSHConnection

def main():
    print("Welcome to SSH Client!")
    
    # Collecting user input for SSH connection details
    host = input("Enter the host: ")
    port = input("Enter the port (default 22): ") or 22
    username = input("Enter the username: ")
    password = input("Enter the password (leave blank if none): ") or None

    # Create an instance of SSHConnection
    ssh = SSHConnection(host, int(port), username, password)

    # Connect to the server
    ssh.connect()

    if ssh.client:
        # Display options after successful connection
        while True:
            print("\nAvailable Commands:")
            print("1. List Remote Files")
            print("2. Upload File")
            print("3. Download File")
            print("4. Execute Command")
            print("5. Exit")

            choice = input("Enter command number: ")

            if choice == '1':
                remote_path = input("Enter remote path (default .): ") or "."
                files = ssh.list_remote_files(remote_path)
                if isinstance(files, list):
                    print("\nRemote Files:")
                    for file in files:
                        print(file)
                else:
                    print(files)

            elif choice == '2':
                local_file = input("Enter local file path to upload: ")
                remote_path = input("Enter remote directory to upload to: ")
                ssh.upload_file(local_file, remote_path)

            elif choice == '3':
                remote_file = input("Enter remote file path to download: ")
                local_path = input("Enter local path to save the file: ")
                ssh.download_file(remote_file, local_path)

            elif choice == '4':
                command = input("Enter command to execute on remote server: ")
                output = ssh.execute_command(command)
                print(f"\nCommand Output:\n{output}")

            elif choice == '5':
                ssh.close()
                print("Exiting...")
                break
            else:
                print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()
