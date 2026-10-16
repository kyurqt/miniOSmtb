
import os


class FileSystem:
    def __init__(self, root="minios_root"):
        # Sandbox root: MiniOS can never go above this folder.
        self.root = os.path.abspath(root)
        os.makedirs(self.root, exist_ok=True)
        self.cwd = self.root  # current working directory

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def _resolve(self, name):
        """Turn a user-typed name into a safe absolute path.
        Returns None if the path would escape the sandbox root."""
        name = name.strip().strip('"')
        path = os.path.abspath(os.path.join(self.cwd, name))
        try:
            if os.path.commonpath([path, self.root]) != self.root:
                return None
        except ValueError:
            return None
        return path

    def current_path(self):
        """Virtual path for display, e.g. '/Documents'."""
        rel = os.path.relpath(self.cwd, self.root)
        return "/" if rel == "." else "/" + rel.replace(os.sep, "/")

    # ------------------------------------------------------------------
    # Required commands
    # ------------------------------------------------------------------
    def dir(self, target=None):
        """dir [folder] - list the contents of a directory."""
        path = self._resolve(target) if target else self.cwd
        if path is None:
            return "Error: Access denied. Path is outside MiniOS."
        if not os.path.exists(path):
            return "Error: Directory does not exist."
        if not os.path.isdir(path):
            return "Error: That is a file, not a directory."

        try:
            entries = sorted(os.listdir(path), key=str.lower)
        except OSError as e:
            return f"Error: {e.strerror}"

        shown = "/" if path == self.root else "/" + \
            os.path.relpath(path, self.root).replace(os.sep, "/")
        lines = [f"Directory of {shown}", ""]
        files = folders = 0
        for entry in entries:
            full = os.path.join(path, entry)
            if os.path.isdir(full):
                lines.append(f"{'<DIR>':<10}{entry}")
                folders += 1
            else:
                lines.append(f"{os.path.getsize(full):<10}{entry}")
                files += 1
        if not entries:
            lines.append("(empty)")
        lines += ["", f"{files} file(s), {folders} folder(s)"]
        return "\n".join(lines)

    def mkdir(self, name):
        """mkdir <folder> - create a new directory."""
        if not name:
            return "Usage: mkdir <folder>"
        path = self._resolve(name)
        if path is None:
            return "Error: Access denied. Path is outside MiniOS."
        if os.path.exists(path):
            return "Error: A file or directory with that name already exists."
        try:
            os.makedirs(path)
        except OSError as e:
            return f"Error: Could not create directory ({e.strerror})."
        return "Directory created."

    def create(self, name, content=""):
        """create <file> [text] - create a new file (optionally with text)."""
        if not name:
            return "Usage: create <file>"
        path = self._resolve(name)
        if path is None:
            return "Error: Access denied. Path is outside MiniOS."
        if os.path.exists(path):
            return "Error: File already exists."
        if not os.path.isdir(os.path.dirname(path)):
            return "Error: Parent directory does not exist."
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
        except OSError as e:
            return f"Error: Could not create file ({e.strerror})."
        return "File created."

    def read(self, name):
        """read <file> - display the contents of a file."""
        if not name:
            return "Usage: read <file>"
        path = self._resolve(name)
        if path is None:
            return "Error: Access denied. Path is outside MiniOS."
        if not os.path.exists(path):
            return "Error: File does not exist."
        if os.path.isdir(path):
            return "Error: That is a directory, not a file."
        try:
            with open(path, "r", encoding="utf-8", errors="replace") as f:
                data = f.read()
        except OSError as e:
            return f"Error: Could not read file ({e.strerror})."
        return data if data else "(file is empty)"

    def delete(self, name):
        """delete <file|folder> - delete a file or an EMPTY directory."""
        if not name:
            return "Usage: delete <file or folder>"
        path = self._resolve(name)
        if path is None:
            return "Error: Access denied. Path is outside MiniOS."
        if path == self.root:
            return "Error: Cannot delete the root directory."
        if not os.path.exists(path):
            return "Error: File or directory does not exist."
        try:
            if os.path.isdir(path):
                if os.listdir(path):
                    return "Error: Directory is not empty."
                if path == self.cwd:
                    return "Error: Cannot delete the current directory."
                os.rmdir(path)
                return "Directory deleted."
            os.remove(path)
            return "File deleted."
        except OSError as e:
            return f"Error: Could not delete ({e.strerror})."

    # ------------------------------------------------------------------
    # Optional extras
    # ------------------------------------------------------------------
    def write(self, name, text, append=False):
        """write <file> <text> - write text to a file (creates it if needed)."""
        if not name:
            return "Usage: write <file> <text>"
        path = self._resolve(name)
        if path is None:
            return "Error: Access denied. Path is outside MiniOS."
        if os.path.isdir(path):
            return "Error: That is a directory, not a file."
        if not os.path.isdir(os.path.dirname(path)):
            return "Error: Parent directory does not exist."
        try:
            with open(path, "a" if append else "w", encoding="utf-8") as f:
                f.write(text + "\n")
        except OSError as e:
            return f"Error: Could not write file ({e.strerror})."
        return "Text written to file."

    def rename(self, old, new):
        """rename <old> <new> - rename a file or directory."""
        if not old or not new:
            return "Usage: rename <old> <new>"
        src, dst = self._resolve(old), self._resolve(new)
        if src is None or dst is None:
            return "Error: Access denied. Path is outside MiniOS."
        if not os.path.exists(src):
            return "Error: File or directory does not exist."
        if os.path.exists(dst):
            return "Error: Destination name already exists."
        try:
            os.rename(src, dst)
        except OSError as e:
            return f"Error: Could not rename ({e.strerror})."
        return "Renamed successfully."

    def cd(self, target=None):
        """cd <folder> - change directory ('cd ..' goes up, 'cd /' goes to root)."""
        if not target:
            return self.current_path()
        if target.strip() == "/":
            self.cwd = self.root
            return ""
        path = self._resolve(target)
        if path is None:
            return "Error: Access denied. Path is outside MiniOS."
        if not os.path.exists(path):
            return "Error: Directory does not exist."
        if not os.path.isdir(path):
            return "Error: That is a file, not a directory."
        self.cwd = path
        return ""

    def pwd(self):
        """pwd - show the current directory."""
        return self.current_path()
