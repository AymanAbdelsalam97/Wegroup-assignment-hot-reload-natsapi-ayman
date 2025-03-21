import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Define the command to run your NATS application
command = ["python", "examples/minimal.py"]  # Update the path to your file

# Define the directory to watch
watch_directory = "examples"  # Watch the `examples` directory

# Define the file extensions to watch (optional)
watch_extensions = {".py"}

class ReloadHandler(FileSystemEventHandler):
    def __init__(self, process):
        self.process = process

    def on_modified(self, event):
        if any(event.src_path.endswith(ext) for ext in watch_extensions):
            print(f"File changed: {event.src_path}. Restarting application...")
            self.process.terminate()  # Terminate the current process
            self.process = subprocess.Popen(command)  # Restart the process

if __name__ == "__main__":
    # Start the NATS application
    process = subprocess.Popen(command)

    # Set up the file watcher
    event_handler = ReloadHandler(process)
    observer = Observer()
    observer.schedule(event_handler, path=watch_directory, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()