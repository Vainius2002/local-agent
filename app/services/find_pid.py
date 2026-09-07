import subprocess

def find_pid(port):

    process = subprocess.run(["lsof", "-i", f":{port}"], capture_output=True, text=True)
    if process.returncode == 0:
        return f"Port running on pid {process.stdout},"

    process = subprocess.run(["cmd.exe", "/c", f"netstat -ano | findstr :{port}"], capture_output=True, text=True)
    if process.returncode == 0:
        return f"Port running on pid {process.stdout},"

    else:
        return f"Failed to find pid of port {port}."