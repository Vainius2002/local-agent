def write_file(path, content):
    try:
        with open(path, "w") as f:
            f.write(content)
            return f"File {path} has been updated!"

    except FileNotFoundError:
        return f"File not found: {path}"

    except PermissionError:
        return f"Permission denied: {path}"
        
    except Exception as e:
        return f"Failed to read file: {e}"

