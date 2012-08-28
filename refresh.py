import sublime, sublime_plugin
import os, subprocess

class RefreshCommand(sublime_plugin.TextCommand):
    """ Refresh the project """

    status_msg = ""
    label = "REFRESH: "
    base_cmd = "source ~/.bash_profile && "

    def run(self, edit):
        self.status_msg = ""
        self.set_status(self.label)
        sublime.set_timeout(self.start_refresh, 1)

    def start_refresh(self):
        for folder in self.view.window().folders():
            f = str(folder)

            # jekyll rebuild: `bundle exec jekyll --no-auto --no-server`
            if os.path.exists(os.path.join(f, '_config.yml')):
                self.run_cmd(f, "bundle exec jekyll --no-auto --no-server")

            # Rack restart: `touch tmp/restart.txt`
            if os.path.exists(os.path.join(f, 'config.ru')):
                self.run_cmd(f, "mkdir -p tmp && touch tmp/restart.txt")

            # Summary message
            if self.status_msg == self.label:
                self.set_status("nothing needed.")
            else:
                self.set_status("done.")

    def run_cmd(self, folder, cmd):
        self.set_status("`" + cmd + "`, ")
        try:
            p = subprocess.Popen(self.base_cmd+cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=folder, shell=True)
            result, err = p.communicate()
        except Exception as e:
            self.set_status(str(e))

    def set_status(self, msg):
        self.status_msg += msg
        sublime.status_message(self.status_msg)

