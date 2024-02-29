import os, json
from rich.text import Text
from textual.app import App, Binding
from textual.widgets import *
from textual.containers import *

from src.rdp import rdp_check
from src.ssh import ssh_check
from src.winrm import winrm_check
from src.mysql import mysql_check
# from src.http import http_check
# from src.dns import dns_check

def get_checks():
    checks = []
    directory = 'checks/'
    for filename in os.listdir(directory):
        if '.json' in filename:
            with open(directory + filename, 'r') as f:
                checks.append(json.loads(f.read()))
    return checks

class scoreboard_app(App):
    BINDINGS = [
        Binding('ctrl+c', 'exit', 'Exit'),
        Binding('tab', 'focus_next', 'Focus Next'),
    ]

    seconds = 30

    def compose(self):
        with TabbedContent():
            with TabPane('scoreboard'):
                yield DataTable()
            with TabPane('failures'), ScrollableContainer():
                yield Label('fortnite')

    def on_mount(self):
        t = self.query_one(DataTable)
        t.cursor_type = None
        self.update_table()
        self.set_interval(self.seconds, callback=self.update_table)

    def update_table(self):
        t = self.query_one(DataTable)
        t.clear(columns=True)
        names = []
        for check in get_checks():
            names.append(Text(check['display_name'], justify='center'))
        t.add_columns(*names)
        values = []
        for check in get_checks():
            value = self.process_check(check)
            if value == 0:
                values.append(Text('pass', justify='center', style='#00ff00'))
            else:
                values.append(Text('fail', justify='center', style='#ff0000'))
        t.add_row(*values)

    def process_check(self, check):
        check_type = check['service']
        if check_type == 'rdp':
            return rdp_check(check)
        elif check_type == 'ssh':
            return ssh_check(check)
        elif check_type == 'winrm':
            return winrm_check(check)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def action_exit(self):
        self.exit(result=0)

if __name__ == '__main__': 
    app = scoreboard_app()
    app.run()