import os, json, datetime
from rich.text import Text
from textual.app import App, Binding
from textual.widgets import *
from textual.containers import *

from src.rdp_c import rdp_check
from src.ssh_c import ssh_check
from src.winrm_c import winrm_check
from src.mysql_c import mysql_check
from src.http_c import http_check
from src.dns_c import dns_check

class scoreboard_app(App):
    BINDINGS = [
        Binding('ctrl+c', 'exit', 'Exit'),
        Binding('tab', 'focus_next', 'Focus Next'),
    ]

    def __init__(self, seconds=5, history=20, directory='checks/', *args, **kwargs):
        self.seconds = seconds
        self.history = history
        self.directory = directory
        self.results = []
        super().__init__(*args, **kwargs)

    def get_checks(self):
        checks = []
        for filename in os.listdir(self.directory):
            if '.json' in filename:
                with open(self.directory + filename, 'r') as f:
                    checks.append(json.loads(f.read()))
        return checks

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
        names = []
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
        values = []
        for check in self.get_checks():
            value = self.process_check(check)
            if value == 0:
                values.append(Text('pass', justify='center', style='#11ff11'))
            else:
                values.append(Text('fail', justify='center', style='#ff1111'))
                self.handle_error(check, value)
        self.results.append(values)

    def handle_error(self, check, result):
        pass

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
    
    def action_exit(self):
        self.exit(result=0)

if __name__ == '__main__': 
    app = scoreboard_app()
    app.run()