import sublime, sublime_plugin
import os, subprocess

class RefreshCommand(sublime_plugin.TextCommand):
    """ Refresh the project """

    def run(self, edit):
        for folder in self.view.window().folders():
            label = "REFRESH: "
            status_msg = label

            f = str(folder)
            c = "source ~/.bash_profile && "

            # jekyll rebuild: `bundle exec jekyll --no-auto --no-server`
            if os.path.exists(os.path.join(f, '_config.yml')):
                cmd = "bundle exec jekyll --no-auto --no-server"
                status_msg += "`" + cmd + "`, "
                try:
                    p = subprocess.Popen(c+cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=f, shell=True)
                    result, err = p.communicate()
                    # status_msg += err
                except Exception as e:
                    status_msg += str(e)

            # Rack restart: `touch tmp/restart.txt`
            if os.path.exists(os.path.join(f, 'config.ru')):
                cmd = "mkdir -p tmp && touch tmp/restart.txt"
                status_msg += "`" + cmd + "`, "
                try:
                    p = subprocess.Popen(c+cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=f, shell=True)
                    result, err = p.communicate()
                    # status_msg += err
                except Exception as e:
                    status_msg += str(e)

            # Summary message
            if status_msg == label:
                status_msg += "nothing needed."
            else:
                status_msg += "done."

            sublime.status_message(status_msg)
