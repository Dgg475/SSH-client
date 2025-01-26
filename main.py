from ssh_connection import SSHConnection

def main():
    print("Welcome to the Enhanced SSH Client!")

    host = input("Enter the host: ")
    port = input("Enter the port (default 22): ") or 22
    username = input("Enter the username: ")
    password = input("Enter the password (leave blank if none): ") or None

    ssh = SSHConnection(host, int(port), username, password)

    ssh.connect()

    if ssh.client:
        print("\nConnected to remote server.")
        print("You can execute normal SSH commands or use custom commands:")
        print("Custom Commands:")
        print("- `viewfl <remote_path>`: List remote files in a specific directory.")
        print("- `upload <local_file> <remote_path>`: Upload a local file to a remote path.")
        print("- `download <remote_file> <local_path>`: Download a remote file to a local path.")
        print("- `exit`: Disconnect and exit the program.")

        while True:
            command = input(f"{username}@{host}> ")

            
            if command.startswith("viewfl"):
                try:
                    _, remote_path = command.split(" ", 1)
                except ValueError:
                    remote_path = "."
                files = ssh.list_remote_files(remote_path)
                if isinstance(files, list):
                    print("\nRemote Files:")
                    for file in files:
                        print(file)
                else:
                    print(files)

            elif command.startswith("upload"):
                try:
                    _, local_file, remote_path = command.split(" ", 2)
                except ValueError:
                    print("Usage: upload <local_file> <remote_path>")
                    continue
                ssh.upload_file(local_file, remote_path)

            elif command.startswith("download"):
                try:
                    _, remote_file, local_path = command.split(" ", 2)
                except ValueError:
                    print("Usage: download <remote_file> <local_path>")
                    continue
                ssh.download_file(remote_file, local_path)

            elif command == "exit":
                ssh.close()
                print("Disconnected from the server. Exiting...")
                break

            else:
            
                output = ssh.execute_command(command)
                print(output)

if __name__ == "__main__":
    main()
