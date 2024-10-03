import subprocess


def shutdown_system():
    try:
        subprocess.Popen(['shutdown', '/s', '/t', '1'])
        return {"text": "Shutting down the system."}
    except Exception as e:
        return {"text": f"Error shutting down the system: {e}"}

def restart_system():
    try:
        subprocess.Popen(['shutdown', '/r', '/t', '1'])
        return {"text": "Restarting the system."}
    except Exception as e:
        return {"text": f"Error restarting the system: {e}"}
