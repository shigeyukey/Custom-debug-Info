
from aqt import mw, QPushButton, QMenu

def get_restart_button():
    restart_button = None
    for action in mw.form.menuTools.actions():
        if action.text() == "Anki Restart":
            submenu = action.menu() # type: QMenu
            for subaction in submenu.actions():
                if subaction.text() == "Restart Anki now":
                    restart_button = QPushButton("Restart Anki")
                    restart_button.clicked.connect(subaction.trigger)
                    break
    return restart_button