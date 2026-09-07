import subprocess


def kill_task(pid):
  
    process = subprocess.run(["cmd.exe", "/c", "taskkill", "/PID", str(pid), "/F" ], capture_output=True, text=True)
    if process.returncode == 0:


        return f"PID {pid} successfully killed on windows cmd!"
    windows_error = process.stderr.strip() or process.stdout.strip()



    process = subprocess.run(["kill", str(pid)], capture_output=True, text=True)
    if process.returncode == 0:
        return f"PID {pid} successfully killed on linux wsl!"

    linux_error = process.stderr.strip() or process.stdout.strip()
    return f"Failed to kill either on cmd and wsl: {windows_error}, {linux_error}"
