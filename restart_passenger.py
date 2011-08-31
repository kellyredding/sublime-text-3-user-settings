import sublime, sublime_plugin
import os, time

class RestartPassengerCommand(sublime_plugin.TextCommand):
    """Touch tmp/restart.txt file in the rails project to restart pasenger"""

    def run(self, edit):
        for folder in self.view.window().folders():
            fname = os.path.join(str(folder), 'tmp', 'restart.txt')
            if os.path.exists(os.path.dirname(fname)):
                with file(fname, 'a'):
                    os.utime(fname, None)
                    sublime.status_message('Successfully restarted Passenger')
