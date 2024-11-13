
import re
import os
from aqt import mw, QApplication, QDialog, QTextBrowser, QPushButton, QVBoxLayout, Qt, QHBoxLayout, QResizeEvent, QIcon
from aqt.utils import tooltip
from anki.hooks import wrap
from .rate_limit_timer import rate_limit
from .config.button_manager import mini_button
from .config.my_addon_config import setMyAddonConfig
from .restart_anki import get_restart_button

try:
    from aqt.errors import ErrorHandler
except Exception as e:
    print(e)
    ErrorHandler = None

try:
    from aqt.errors import is_chromium_cert_error
except Exception as e:
    print(e)
    is_chromium_cert_error = None

try:
    from aqt.errors import supportText
except Exception as e:
    print(e)
    supportText = None

previous_debug_text = ""
debug_text_count = 0
active_dialogs = []

class DebugInfoDialog(QDialog):
    def __init__(self, parent, debug_text):
        super().__init__(parent)
        self.debug_text = debug_text

        config = mw.addonManager.getConfig(__name__)

        self.widget_width = config.get("widget_width", 1200)
        self.widget_height = config.get("widget_height", 550)
        self.font_size = config.get("font_size", 16)
        self.background_color = config.get("background_color", "#1f1f1f")
        self.text_color = config.get("text_color", "#68cefe")
        self.color_traceback = config.get("color_traceback", "#ff5500")
        self.color_file = config.get("color_file", "#50fa7b")
        self.color_line = config.get("color_line", "#0effa7")
        self.color_error = config.get("color_error", "#ff5555")
        self.color_in = config.get("color_in", "#bd93f9")
        self.color_string = config.get("color_string", "#c57d47")

        self.setWindowTitle("Custom Debug Info by Shige")
        self.resize(self.widget_width, self.widget_height)
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowMinMaxButtonsHint)
        addon_path = os.path.dirname(__file__)
        self.setWindowIcon(QIcon(os.path.join(addon_path, "config", "ladybug.png")))

        self.text_browser = QTextBrowser(self)

        debug_text = self.format_log_text(debug_text)

        self.text_browser.setText(debug_text)
        self.text_browser.setStyleSheet(
            f"background-color: {self.background_color}; color: {self.text_color}; font-size: {self.font_size}px;")

        self.close_button = QPushButton("Close", self)
        self.close_button.clicked.connect(self.close)

        def copy_debug_info():
            QApplication.clipboard().setText(self.debug_text)
            tooltip("Copied to clipboard.", parent=self)

        self.copy_button = QPushButton("📋Copy", self)
        self.copy_button.clicked.connect(copy_debug_info)

        self.option_button = QPushButton("⚙️Option", self)
        self.option_button.clicked.connect(setMyAddonConfig)


        layout = QVBoxLayout()
        layout.addWidget(self.text_browser)
        hLayout = QHBoxLayout()
        hLayout.addWidget(self.close_button)
        hLayout.addWidget(self.copy_button)

        restart_button = get_restart_button()
        if isinstance(restart_button, QPushButton):
            hLayout.addWidget(restart_button)

        hLayout.addStretch()
        hLayout.addWidget(self.option_button)
        
        layout.addLayout(hLayout)

        self.setLayout(layout)

    def resizeEvent(self, event:"QResizeEvent"):
        size = event.size()
        config = mw.addonManager.getConfig(__name__)
        config["widget_width"] = size.width()
        config["widget_height"] = size.height()
        mw.addonManager.writeConfig(__name__, config)
        super().resizeEvent(event)

    def format_log_text(self, debug_text: str):
        debug_text = debug_text.replace("\n", "<br>")
        debug_text = debug_text.replace(" ", "&nbsp;")
        debug_text = debug_text.replace("Traceback", f"<span style='color: {self.color_traceback};'>Traceback</span>")
        debug_text = debug_text.replace("File", f"<span style='color: {self.color_file};'>File</span>")
        debug_text = debug_text.replace("line", f"<span style='color: {self.color_line};'>line</span>")
        debug_text = re.sub(r'(\b[A-Za-z]+Error\b)', rf"<span style='color: {self.color_error};'>\1</span>", debug_text)
        debug_text = re.sub(r'(\b\d+\b)', rf"<span style='color: {self.color_line};'>\1</span>", debug_text)
        debug_text = debug_text.replace("&nbsp;in&nbsp;", f" <span style='color: {self.color_in};'>&nbsp;in&nbsp;</span>")
        debug_text = re.sub(r'"([^"]*)"', rf'<span style="color: {self.color_string};">"\1"</span>', debug_text)
        return debug_text


def show_addon_debug_info_wrapper(self:"ErrorHandler", _old):
    try:
        global previous_debug_text, debug_text_count, active_dialogs

        error = self.pool
        self.pool = ""
        self.mw.progress.clear()

        if "AbortSchemaModification" in error:
            return
        if "DeprecationWarning" in error:
            return
        if "10013" in error:
            return
        if "invalidTempFolder" in error:
            return
        if "Beautiful Soup is not an HTTP client" in error:
            return
        if "database or disk is full" in error or "Errno 28" in error:
            return
        if "disk I/O error" in error:
            return
        if not is_chromium_cert_error == None:
            if is_chromium_cert_error(error):
                return


        if not supportText == None:
            debug_text = supportText() + "\n" + error
        else:
            debug_text = error

        # debug_text += addon_debug_info()

        if debug_text == previous_debug_text:
            debug_text_count += 1
        else:
            debug_text_count = 1
            previous_debug_text = debug_text

        if debug_text_count < 3 and len(active_dialogs) < 3:
            dialog = DebugInfoDialog(mw, debug_text)
            dialog.show()
            active_dialogs.append(dialog)
            dialog.finished.connect(lambda: active_dialogs.remove(dialog))
        else:
            if rate_limit.limit("debug_info_wrapper", 2):
                pass
            else:
                tooltip(f"🚨Same error is occurring in succession: {debug_text_count}")

        # dialog = DebugInfoDialog(mw, debug_text)
        # dialog.show()

    except Exception as e:
        print(e)
        _old(self)

if not ErrorHandler == None:
    if hasattr(ErrorHandler, "onTimeout"):
        ErrorHandler.onTimeout = wrap(ErrorHandler.onTimeout, show_addon_debug_info_wrapper, "around")



# def show_addon_debug_info_wrapper(self:ErrorHandler):
#     try:
#         error = self.pool

#         if "AbortSchemaModification" in error:
#             return
#         if "DeprecationWarning" in error:
#             return
#         if "10013" in error:
#             return
#         if "invalidTempFolder" in error:
#             return
#         if "Beautiful Soup is not an HTTP client" in error:
#             return
#         if "database or disk is full" in error or "Errno 28" in error:
#             return
#         if "disk I/O error" in error:
#             return
#         if is_chromium_cert_error(error):
#             return

#         debug_text = supportText() + "\n" + error
#         # debug_text += addon_debug_info()

#         dialog = DebugInfoDialog(mw, debug_text)
#         dialog.show()
#     except:
#         pass
#         # _old(self)

# if hasattr(ErrorHandler, "onTimeout"):
#     ErrorHandler.onTimeout = wrap(ErrorHandler.onTimeout, show_addon_debug_info_wrapper, "before")