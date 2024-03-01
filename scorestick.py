import os, json, datetime, json2html, multiprocessing
from rich.text import Text
from http.server import HTTPServer, SimpleHTTPRequestHandler

from textual.app import App, Binding
from textual.widgets import *
from textual.containers import *

from src.rdp_c import rdp_check
from src.ssh_c import ssh_check
from src.winrm_c import winrm_check
from src.mysql_c import mysql_check
from src.http_c import http_check
from src.dns_c import dns_check
from src.ftp_c import ftp_check
from src.smb_c import smb_check

out_directory = 'out/'
def host_server(http_port):
    class web_server(SimpleHTTPRequestHandler):   
        def do_GET(self):
            if '.html' in self.path:
                self.path = './' + out_directory + self.path
            if out_directory not in self.path:
                self.path = './' + out_directory
            super().do_GET()
        def log_message(self, format, *args):
            pass
        def log_error(self, format, *args):
            pass
    HTTPServer(('0.0.0.0', http_port), web_server).serve_forever()

class scoreboard_app(App):
    BINDINGS = [
        Binding('ctrl+c', 'exit', 'Exit'),
        Binding('tab', 'focus_next', 'Focus Next'),
    ]

    def __init__(self, seconds=5, history=20, check_directory='checks/', http_port=1337, web=True, verbose=True, *args, **kwargs):
        self.results = []
        self.seconds = seconds
        self.history = history
        self.directory = check_directory
        self.out_directory = out_directory
        self.verbose = verbose
        if not os.path.exists(self.out_directory):
            os.mkdir(self.out_directory)
        if web:
            self.process = multiprocessing.Process(target=host_server, args=(http_port,))
            self.process.start()
        super().__init__(*args, **kwargs)

    def get_checks(self):
        checks = []
        for filename in os.listdir(self.directory):
            if '.json' in filename:
                with open(self.directory + filename, 'r') as f:
                    new_check = json.loads(f.read())
                    if ('display_name' in new_check) and ('service' in new_check) and ('host' in new_check):
                        checks.append(new_check)
                    f.close()
        return checks
    
    def get_check_filename(self, check):
        ip_split = check['host'].split('.')
        name = check['service']
        name += '_'
        name += ip_split[2] + '-' + ip_split[3]
        name += '_'
        for char in check['display_name']:
            if char.isalpha():
                name += char
        name += '.html'
        return name

    def compose(self):
        with Center():
            yield DataTable()

    def on_mount(self):
        t = self.query_one(DataTable)
        t.cursor_type = None
        self.update_table()
        self.set_interval(self.seconds, callback=self.update_table)

    def update_table(self):
        t = self.query_one(DataTable)
        t.clear(columns=True)
        names = [Text('Time', justify='center')]
        for check in self.get_checks():
            names.append(Text(check['display_name'], justify='center'))
        t.add_columns(*names)
        self.update_results()
        self.results.reverse()
        t.add_rows(self.results[:self.history])
        self.results.reverse()

    def update_results(self):
        if len(self.results) > self.history:
            self.results = self.results[-1 * self.history:] 
        values = [Text(datetime.datetime.now().strftime('%I:%M'), justify='center')]
        for check in self.get_checks():
            value = self.process_check(check)
            if value == 0:
                values.append(Text('pass', justify='center', style='#11ff11'))
                self.handle_success(check)
            elif value == 'check error':
                values.append(Text('err', justify='center', style='#1111ff'))
                self.handle_error(check)
            else:
                values.append(Text('fail', justify='center', style='#ff1111'))
                self.handle_failure(check, value)
        self.results.append(values)

    def handle_success(self, check):
        filename = self.out_directory + self.get_check_filename(check)
        if os.path.exists(filename):
            os.remove(filename)

    def handle_error(self, check):
        filename = self.out_directory + self.get_check_filename(check)
        with open(filename, 'w') as f:
            f.write('bozo set up the check wrong\n' + json2html.json2html.convert(json=json.dumps(check)))
            f.close()

    def handle_failure(self, check, result):
        filename = self.out_directory + self.get_check_filename(check)
        with open(filename, 'w') as f:
            if (self.verbose):
                f.write(str(result) + '\n' + json2html.json2html.convert(json=json.dumps(check)))
            else:
                sneaky = {
                    'display_name': check['display_name'],
                    'service': check['service'],
                    'host': check['host']
                }
                f.write(str(result) + '\n' + json2html.json2html.convert(json=json.dumps(sneaky)))
            f.close

    def process_check(self, check):
        check_type = check['service']
        if check_type == 'rdp':
            return rdp_check(check)
        elif check_type == 'ssh':
            return ssh_check(check)
        elif check_type == 'winrm':
            return winrm_check(check)
        elif check_type == 'mysql':
            return mysql_check(check)
        elif check_type == 'dns':
            return dns_check(check)
        elif check_type == 'http':
            return http_check(check)
        elif check_type == 'ftp':
            return ftp_check(check)
        elif check_type == 'smb':
            return smb_check(check)
        else:
            return 'check error'
    
    def action_exit(self):
        self.process.terminate()
        self.exit(result=0)

if __name__ == '__main__': 
    app = scoreboard_app()
    app.run()