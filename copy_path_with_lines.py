import sublime
import sublime_plugin
import os

class CopyPathWithLinesCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        view = self.view
        fully_qualified_path = view.file_name()

        if not fully_qualified_path:
            sublime.status_message("No file path (unsaved file).")
            return

        # Make path fully qualified for clarity sake.
        file_path = fully_qualified_path

        # Make path relative to project if possible (I ended up not using this)
        # window = view.window()
        # folders = window.folders() if window else []
        # relative_path = fully_qualified_path
        # for folder in folders:
        #     if fully_qualified_path.startswith(folder):
        #         relative_path = os.path.relpath(fully_qualified_path, folder)
        #         break
        # file_path = relative_path

        # Handle selections
        parts = []
        for sel in view.sel():
            start_line = view.rowcol(sel.begin())[0] + 1
            end_line = view.rowcol(sel.end())[0] + 1
            if start_line == end_line:
                parts.append(f"{file_path}:{start_line}")
            else:
                parts.append(f"{file_path}:{start_line}-{end_line}")

        result = ", ".join(parts)
        sublime.set_clipboard(result)
        sublime.status_message(f"Copied: {result}")
