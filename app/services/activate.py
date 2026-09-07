import subprocess
from pathlib import Path

opened_app = []

def start_app(path, file_name, port):
    just_path = Path(path)

    path_bin = just_path / "venv" / "bin" / "python3"

    command = [
        str(path_bin),
        "-m",
        "uvicorn",
        file_name,
        "--host",
        "0.0.0.0",
        "--port",
        port,
        "--reload"
    ]


    try:
        run_cmd = subprocess.Popen(command, cwd=just_path)

        opened_app.append({
        "Path": str(just_path),
        "Pids": run_cmd.pid,
        "File name": file_name,
        "Port": port
        })

        return f"Project started at {just_path} with port as {port}"

    except Exception as e:
        return f"Process couldnt start: {e}"

