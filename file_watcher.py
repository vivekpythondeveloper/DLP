import os
import time
import shutil  # Needed for moving files
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class Watcher:
    def __init__(self, directories_to_watch):
        self.observer = Observer()
        self.directories_to_watch = directories_to_watch

    def run(self):
        event_handler = Handler()
        for directory in self.directories_to_watch:
            self.observer.schedule(event_handler, directory, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print("Observer Stopped")
        self.observer.join()

class Handler(FileSystemEventHandler):
    @staticmethod
    def on_any_event(event):
        print(f"current event name is {event}")
        if event.is_directory:
            return None
        elif event.event_type == 'created':
            print(f"Detected {event.event_type} - {event.src_path}.")
            if should_intercept(event.src_path):
                delete_file(event.src_path)
                print("File operation intercepted and file deleted!")
                # Prompt user for confirmation or take other actions as needed
        elif event.event_type == 'moved':
            print(f"Detected {event.event_type} - from {event.src_path} to {event.dest_path}.")
            if should_intercept(event.src_path):
                move_file_back(event.dest_path, event.src_path)
                print("File operation intercepted and file moved back!")
                # Prompt user for confirmation or take other actions as needed
        # If user confirms or if interception is not required, proceed with scanning the file
        scan_file(event.src_path)

def delete_file(file_path):
    while True:
        try:
            os.remove(file_path)
            break  # Exit loop if deletion successful
        except PermissionError:
            print(f"PermissionError: Unable to delete file {file_path}. Retrying in 1 second...")
            time.sleep(1)

def move_file_back(src_path, dest_path):
    while True:
        try:
            os.rename(src_path, dest_path)
            break  # Exit loop if move successful
        except PermissionError:
            print(f"PermissionError: Unable to move file {src_path} back to {dest_path}. Retrying in 1 second...")
            time.sleep(1)



def should_intercept(file_path):
    print(f"this is intercept code {file_path}")
    # Implement logic to determine if the file operation should be intercepted
    # You can check file properties such as file type, destination directory, etc.
    # For demonstration purposes, intercept all file operations
    return True

def scan_file(file_path):
    print(f"Scanning {file_path}...")
    # Implement your file scanning logic here.

def get_important_directories():
    # Customize this list based on user configuration or common directories
    directories = [
        os.path.expanduser("~/Desktop"),
        os.path.expanduser("~/Documents"),
        os.path.expanduser("~/Downloads")
    ]
    return directories

if __name__ == '__main__':
    important_directories = get_important_directories()
    watcher = Watcher(important_directories)
    watcher.run()
