import sublime, sublime_plugin
import os, subprocess

class RefreshCommand(sublime_plugin.TextCommand):
    """ Refresh the project """

    status_msg = ""
    label = "REFRESH: "

    def run(self, edit):
        self.status_msg = ""
        self.set_status(self.label)
        sublime.set_timeout(self.run_folders, 1)

    def run_folders(self):
        for folder in self.view.window().folders():
            f = str(folder)
            c = "source ~/.bash_profile && "

            # jekyll rebuild: `bundle exec jekyll --no-auto --no-server`
            if os.path.exists(os.path.join(f, '_config.yml')):
                cmd = "bundle exec jekyll --no-auto --no-server"
                self.set_status("`" + cmd + "`, ")
                try:
                    p = subprocess.Popen(c+cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=f, shell=True)
                    result, err = p.communicate()
                except Exception as e:
                    self.set_status(str(e))

            # Rack restart: `touch tmp/restart.txt`
            if os.path.exists(os.path.join(f, 'config.ru')):
                cmd = "mkdir -p tmp && touch tmp/restart.txt"
                self.set_status("`" + cmd + "`, ")
                try:
                    p = subprocess.Popen(c+cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=f, shell=True)
                    result, err = p.communicate()
                except Exception as e:
                    self.set_status(str(e))

            # Summary message
            if self.status_msg == self.label:
                self.set_status("nothing needed.")
            else:
                self.set_status("done.")

    def set_status(self, msg):
        self.status_msg += msg
        sublime.status_message(self.status_msg)

