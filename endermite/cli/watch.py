import os
import time
from typing import NamedTuple


class Change(NamedTuple):
    """Represents a change being made to a watched directory"""

    action: str
    path: str

    def format(self, base_dir):
        """Return a string describing the change relative to a base directory."""
        path = self.path[len(str(base_dir)):]
        return f'{self.action.capitalize()} "{path}"'


def watch_directory(path, interval=0.4):
    """Indefinitely yield the changes being made to a given directory."""
    watcher = DirectoryWatcher(path)
    while True:
        changes = watcher.check_directory()
        if changes:
            yield changes
        time.sleep(interval)


class DirectoryWatcher:
    """Holds state and implements methods for watching a directory."""

    def __init__(self, path):
        self.path = path
        self.files = {}

    def check_directory(self):
        """Return the list of changes made to the directory."""
        changes = []
        new_files = {}
        self.traverse(str(self.path), changes, new_files)

        deleted = self.files.keys() - new_files.keys()
        changes.extend(Change('removed', path) for path in deleted)

        self.files = new_files
        return changes

    def traverse(self, path, changes, new_files):
        """Check for created and edited files by traversing the directory."""
        for entry in os.scandir(path):
            if entry.is_dir():
                if entry.name != '__pycache__':
                    self.traverse(entry.path, changes, new_files)
            else:
                mtime = entry.stat().st_mtime
                new_files[entry.path] = mtime
                previous = self.files.get(entry.path)
                if not previous:
                    changes.append(Change('created', entry.path))
                elif previous != mtime:
                    changes.append(Change('edited', entry.path))
