import sublime, sublime_plugin
import os, subprocess

class RefreshCommand(sublime_plugin.TextCommand):
    """ Refresh the project """

    label = "REFRESH: "
    base_cmd = "source ~/.bash_profile && "
    status_msg = ""

    folder = None
    cmd = None
    callback = None

    # will only run if there is one (1) project folder in the window
    # runs asynchronously for real-time status updates (useful for
    # long running refreshes)

    # First runs `rebuild_jekyll`, then `remove_logs`, then `restart_rack`

    def run(self, edit):
        folders = self.view.window().folders()
        if len(folders) == 1:
            self.status_msg = ""
            self.set_status(self.label)
            self.folder = str(folders.pop())

            self.start_refresh()
        elif len(folders) == 0:
            self.set_status("no project folders to refresh, ")
            self.finish_refresh()
        else:
            self.set_status("can't refresh more than one project folder, ")
            self.finish_refresh()

    # action methods

    def start_refresh(self):
        self.rebuild_jekyll()

    def rebuild_jekyll(self):
        cmd = "bundle exec jekyll --no-auto --no-server"
        callback = self.remove_logs
        if os.path.exists(os.path.join(self.folder, '_config.yml')):
            self.setup_cmd(cmd, callback)
        else:
            callback()

    def remove_logs(self):
        cmd = "rm -f log/*.log"
        callback = self.restart_rack
        if os.path.exists(os.path.join(self.folder, 'log')):
            self.setup_cmd(cmd, callback)
        else:
            callback()

    def restart_rack(self):
        cmd = "mkdir -p tmp && touch tmp/restart.txt"
        callback = self.finish_refresh
        if os.path.exists(os.path.join(self.folder, 'config.ru')):
            self.setup_cmd(cmd, callback)
        else:
            callback()

    def finish_refresh(self):
        if self.status_msg == self.label:
            self.set_status("nothing needed.")
        else:
            self.set_status("done.")

    # private methods

    def setup_cmd(self, cmd, callback):
        self.set_status("`" + cmd + "`... ")
        self.cmd = cmd
        self.callback = callback
        sublime.set_timeout(self.run_cmd, 1)

    def run_cmd(self):
        try:
            p = subprocess.Popen(self.base_cmd+self.cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=self.folder, shell=True)
            result, err = p.communicate()
        except Exception as e:
            self.set_status(str(e))
        self.callback()

    def set_status(self, msg):
        self.status_msg += msg
        sublime.status_message(self.status_msg)

