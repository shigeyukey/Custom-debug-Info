# Copyright (C) Shigeyuki <http://patreon.com/Shigeyuki>
# License: GNU AGPL version 3 or later <http://www.gnu.org/licenses/agpl.html>｣

from aqt import QPushButton
from .shigeAPI import shigeAPI

def get_restart_button():
    restart_button = None
    if shigeAPI.restart_anki.check():
        restart_button = QPushButton("Restart Anki")
        restart_button.clicked.connect(shigeAPI.restart_anki.run)
    return restart_button