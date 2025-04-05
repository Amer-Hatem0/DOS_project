import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

 
class WatcherHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith('.py'):   
            print(f'Change detected in {event.src_path}. Rebuilding containers...')
            subprocess.run(['docker-compose', 'down'], check=True)
            subprocess.run(['docker-compose', 'up', '--build'], check=True)

 
if __name__ == "__main__":
    event_handler = WatcherHandler()
    observer = Observer()
    observer.schedule(event_handler, path='./', recursive=True)   

    print("Watching for file changes...")
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
