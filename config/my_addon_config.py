# Copyright (C) Shigeyuki <http://patreon.com/Shigeyuki>
# License: GNU AGPL version 3 or later <http://www.gnu.org/licenses/agpl.html>｣

import random
from os.path import join, dirname

from aqt import (QAction, QBrush, QButtonGroup, QColor, QColorDialog, QDialog, QFrame, QGroupBox, QHBoxLayout, QMenu, QMessageBox, QPainter, QPalette, QRadioButton, QRectF, QResizeEvent,
                QTabWidget, QWidget, Qt, qconnect, gui_hooks, QVBoxLayout, QLabel, QPushButton, QDoubleSpinBox, mw, QIcon, QPainterPath,
                QPixmap, QCheckBox)
from aqt.utils import openLink,tooltip

from .button_manager import mini_button
from .shige_addons import add_shige_addons_tab
from .endroll.endroll import add_credit_tab

from .._version import ADDON_NAME, __version__

set_window_title = ADDON_NAME
addon_banner_image = ""
patreon_banner_jpg = "Patreon_banner.jpg"

dialog_icon = "ladybug.png"
patreon_link_url = "http://patreon.com/Shigeyuki"
set_scaledToWidth = 450
set_scaledToWidth = 500


# PATREON_LABEL_WIDTH = 500

WIDGET_WIDTH = 524
WIDGET_HEIGHT = 478
# Width: 524, Height: 478


# ---- ﾌｫﾝﾄの設定画面を作成するｸﾗｽ --------
class MyAddonConfig(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        config = mw.addonManager.getConfig(__name__)

        self.font_size = config.get("font_size", 16)
        self.background_color = config.get("background_color", "#1f1f1f")
        self.text_color = config.get("text_color", "#68cefe")
        self.color_traceback = config.get("color_traceback", "#ff5500")
        self.color_file = config.get("color_file", "#50fa7b")
        self.color_line = config.get("color_line", "#0effa7")
        self.color_error = config.get("color_error", "#ff5555")
        self.color_in = config.get("color_in", "#bd93f9")
        self.color_string = config.get("color_string", "#c57d47")



        # Set window icon
        addon_path = dirname(__file__)
        self.icon_path = join(addon_path, dialog_icon)
        self.logo_icon = QIcon(self.icon_path)
        self.setWindowIcon(self.logo_icon)


        # Patreonﾗﾍﾞﾙ-----------------------------------
        self.patreon_label = QLabel()
        self.addon_banner_image = join(addon_path, addon_banner_image)

        patreon_banner_path = join(addon_path, self.addon_banner_image)
        pixmap = QPixmap(patreon_banner_path)
        pixmap = pixmap.scaledToWidth(set_scaledToWidth, Qt.TransformationMode.SmoothTransformation)

        path = QPainterPath()
        path.addRoundedRect(QRectF(pixmap.rect()), 10, 10)
        rounded_pixmap = QPixmap(pixmap.size())
        rounded_pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter(rounded_pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setClipPath(path)
        painter.drawPixmap(0, 0, pixmap)
        painter.end()
        pixmap = rounded_pixmap

        self.patreon_label.setPixmap(pixmap)
        self.patreon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.patreon_label.setFixedSize(pixmap.width(), pixmap.height())
        self.patreon_label.mousePressEvent = self.open_patreon_Link
        self.patreon_label.setCursor(Qt.CursorShape.PointingHandCursor)
        self.patreon_label.enterEvent = self.patreon_label_enterEvent
        self.patreon_label.leaveEvent = self.patreon_label_leaveEvent

        # Patreonﾗﾍﾞﾙ-----------------------------------

        self.setWindowTitle(f"{set_window_title}  (Created by Shigeඞ)")

        # QPushButtonを作成して､ﾌｫﾝﾄ名をprintする
        button = QPushButton('OK')
        # button.clicked.connect(self.handle_button_clicked)
        button.clicked.connect(self.close)
        button.setFixedWidth(100)

        # button2 = QPushButton('Cancel')
        # button2.clicked.connect(self.cancelSelect)
        # button2.clicked.connect(self.hide)
        # button2.setFixedWidth(100)

        def get_default_conf():
            reply = QMessageBox.question(self, 'Custom Debug info', 'Do you want to restore the default settings?', QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                addon = mw.addonManager.addonFromModule(__name__)
                defaultConf = mw.addonManager.addonConfigDefaults(addon)
                mw.addonManager.writeConfig(__name__, defaultConf)
                tooltip("Restore Default")
                self.close()
                setMyAddonConfig()

        restore_button = QPushButton('RestoreDefault')
        restore_button.clicked.connect(get_default_conf)
        # button.clicked.connect(self.hide)
        mini_button(restore_button)


        button3 = QPushButton('👍️RateThis')
        button3.clicked.connect(lambda:openLink("https://ankiweb.net/shared/info/1594977234") )
        mini_button(button3)

        button4 = QPushButton('💖Become a Patron')
        button4.clicked.connect(lambda:openLink("https://www.patreon.com/Shigeyuki") )
        mini_button(button4)

        button5 = QPushButton("📖Wiki")
        button5.clicked.connect(lambda: openLink(
            "https://shigeyukey.github.io/shige-addons-wiki/debug_info.html"))
        mini_button(button5)

        report_button = QPushButton("🚨Report")
        report_button.clicked.connect(lambda: openLink(
            "https://shigeyukey.github.io/shige-addons-wiki/debug_info.html#report-problems-or-requests"))
        mini_button(report_button)


        # self.test
        # self.test_lavel = self.create_checkbox("test text","test")


        self.font_size
        self.font_size_label, self.font_size_spinbox =self.create_spinbox(
            "[ Font Size ] 1-30  ", 1, 30, self.font_size, 100, 0, 1, "font_size")
        
        self.font_size_spinbox.valueChanged.connect(self.handle_button_clicked)



        ### tab ###
        tab_widget = QTabWidget(self)


        # tab2_widget===========================================
        tab2_widget = QWidget()
        tab2_layout = QVBoxLayout()

        font_hbox = QHBoxLayout()
        font_hbox.addWidget(self.font_size_label)
        font_hbox.addWidget(self.font_size_spinbox)
        font_hbox.addStretch()
        tab2_layout.addLayout(font_hbox)

        tab2_layout.addWidget(self.create_separator())#-------------

        tab2_layout.addWidget(QLabel("<b>[ Colors ]</b>"))

        self.create_color_button("background_color", "Background Color", tab2_layout)
        self.create_color_button("text_color", "Text Color", tab2_layout)
        self.create_color_button("color_traceback", "Traceback Color", tab2_layout)
        self.create_color_button("color_file", "File Color", tab2_layout)
        self.create_color_button("color_line", "Line and Numbers Color", tab2_layout)
        self.create_color_button("color_error", "Error Color", tab2_layout)
        self.create_color_button("color_in", "In Color", tab2_layout)
        self.create_color_button("color_string", "String Color", tab2_layout)

        tab2_layout.addWidget(self.create_separator())#-------------
        # tab2_layout.addWidget(QLabel("[ ]"))
        # tab2_layout.addWidget()

        def debug_test_01():
            raise Exception("Intentional Error in debug_test_01")

        def debug_test_02():
            errors = [ValueError, TypeError, KeyError, IndexError, AttributeError]
            raise random.choice(errors)("Intentional Error in debug_test_02")

        debug_button_01 = QPushButton("Debug Test 01")
        debug_button_01.clicked.connect(debug_test_01)
        debug_button_01.setFixedWidth(150)

        debug_button_02 = QPushButton("Debug Test 02")
        debug_button_02.clicked.connect(debug_test_02)
        debug_button_02.setFixedWidth(150)


        debug_hbox = QHBoxLayout()
        debug_hbox.addWidget(debug_button_01)
        debug_hbox.addWidget(debug_button_02)
        debug_hbox.addStretch()
        tab2_layout.addLayout(debug_hbox)


        tab2_layout.addStretch(1)
        tab2_widget.setLayout(tab2_layout)


        # # tab 3 =================================================

        # tab3_widget = QWidget()
        # tab3_layout = QVBoxLayout()


        # # tab3_layout.addWidget()


        # tab3_layout.addWidget(self.create_separator())#-------------



        # tab3_layout.addStretch(1)
        # tab3_widget.setLayout(tab3_layout)



        ### tabs ###

        tab_widget.addTab(tab2_widget,"design")
        # tab_widget.addTab(tab3_widget,"design")
        # tab_widget.addTab(scroll_area, "Credit" )
        add_credit_tab(self, tab_widget)
        add_shige_addons_tab(self, tab_widget)


        main_layout = QVBoxLayout()
        main_layout.addWidget(self.patreon_label)
        main_layout.addWidget(tab_widget)

        button_layout = QHBoxLayout()
        button_layout.addWidget(button)
        button_layout.addWidget(restore_button)
        # button_layout.addWidget(button2)
        button_layout.addStretch()

        button_layout.addWidget(button5)
        button_layout.addWidget(button3)
        button_layout.addWidget(button4)
        # button_layout.addStretch(1)

        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

        self.resize(WIDGET_WIDTH, WIDGET_HEIGHT)


    def resizeEvent(self, event:"QResizeEvent"):
        size = event.size()
        print(f"Width: {size.width()}, Height: {size.height()}")
        super().resizeEvent(event)


    def create_color_button(self, color_attr, label_text, layout:QHBoxLayout):
        color_button = QPushButton()
        color_button.setFixedWidth(70)

        def choose_colors():
            get_color = self.get_color(getattr(self, color_attr))
            if get_color is not None:
                setattr(self, color_attr, get_color)
                color_button.setStyleSheet(f"background-color: {get_color}")
                
                self.handle_button_clicked()


        color_button.clicked.connect(choose_colors)

        color = getattr(self, color_attr)
        if color is not None:
            color_button.setStyleSheet(f"background-color: {color}")
        color_label = QLabel(label_text)
        color_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        h_layout = QHBoxLayout()
        h_layout.addWidget(color_button)
        h_layout.addWidget(color_label)
        layout.addLayout(h_layout)

    def get_color(self, current_color=None):
        dialog = QColorDialog()
        dialog.setOption(QColorDialog.ColorDialogOption.ShowAlphaChannel, on=True)
        if current_color == "rgba(0, 0, 0, 0)":
            current_color = "#00000000"
        if current_color is not None:
            dialog.setCurrentColor(QColor(current_color))
        if dialog.exec() == QDialog.DialogCode.Accepted:
            color = dialog.selectedColor()
            if color.isValid():
                return color.name(QColor.NameFormat.HexArgb)
            return None


    # ﾗｼﾞｵﾎﾞﾀﾝ ---------------------------
    def update_count_each_deck(self, checked):
        self.count_each_deck = checked

    def update_count_all_decks(self, checked):
        self.count_all_decks = checked

    def update_progress_bar_v1(self, checked):
        self.progress_bar_v1 = checked
    #---------------------------------------



    def create_group_box(self):
        group_box = QGroupBox("Advanced")
        group_box.setObjectName("myGroupBox")
        group_box.setStyleSheet("""
            QGroupBox#myGroupBox { font-weight: normal; }
            QGroupBox#myGroupBox::title { color: gray; }
        """)
        group_box.setCheckable(True)
        group_box.setChecked(False)
        card_layout2 = QVBoxLayout()
        group_box.setLayout(card_layout2)
        return group_box, card_layout2


    # --- cancel -------------
    def cancelSelect(self):
        emoticons = [":-/", ":-O", ":-|"]
        selected_emoticon = random.choice(emoticons)
        tooltip("Canceled " + selected_emoticon)
        self.close()

    # 画像を追加
    def set_wallpaper(tab: QWidget, wallpaper_path: str):
        palette = QPalette()
        pixmap = QPixmap(wallpaper_path)
        brush = QBrush(pixmap)
        palette.setBrush(QPalette.ColorRole.Window, brush)
        tab.setPalette(palette)
        tab.setAutoFillBackground(True)


    # ﾚｲｱｳﾄにｽﾍﾟｰｽを追加する関数=======================
    def add_widget_with_spacing(self,layout:QVBoxLayout, widget):
        hbox = QHBoxLayout()
        hbox.addSpacing(15)
        hbox.addWidget(widget)
        hbox.addStretch(1)
        layout.addLayout(hbox)

    # ﾁｪｯｸﾎﾞｯｸｽを生成する関数=======================
    def create_checkbox(self, label, attribute_name):
        checkbox = QCheckBox(label, self)
        checkbox.setChecked(getattr(self, attribute_name))

        def handler(state):
            if state == 2:
                setattr(self, attribute_name, True)
            else:
                setattr(self, attribute_name, False)

        checkbox.stateChanged.connect(handler)
        return checkbox
    #=================================================

    # ｽﾋﾟﾝﾎﾞｯｸｽを作成する関数=========================
    def create_spinbox(self, label_text, min_value,
                                max_value, initial_value, width,
                                decimals, step, attribute_name):
        def spinbox_handler(value):
            value = round(value, 1)
            if decimals == 0:
                setattr(self, attribute_name, int(value))
            else:
                setattr(self, attribute_name, value)

        label = QLabel(label_text, self)
        spinbox = QDoubleSpinBox(self)
        spinbox.setMinimum(min_value)
        spinbox.setMaximum(max_value)
        spinbox.setValue(initial_value)
        spinbox.setFixedWidth(width)
        spinbox.setDecimals(decimals)
        spinbox.setSingleStep(step)
        spinbox.valueChanged.connect(spinbox_handler)
        return label, spinbox
    #=================================================


    # ｾﾊﾟﾚｰﾀを作成する関数=========================
    def create_separator(self):
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        separator.setStyleSheet("border: 1px solid gray")
        return separator
    # =================================================

    # ﾗｼﾞｵﾎﾞﾀﾝを作成する関数===============
    def create_radio_buttons(self, button_dict:dict, radio_attr):
        layout = QVBoxLayout()
        button_group = QButtonGroup(layout)
        for button_name, button_value in button_dict.items():
            radio_button = QRadioButton(button_name)
            radio_button.setChecked(getattr(self, radio_attr) == button_value)
            radio_button.toggled.connect(
                lambda checked,
                button_value=button_value: self.update_radio_buttons(checked, button_value, radio_attr))
            layout.addWidget(radio_button)
            button_group.addButton(radio_button)
        return layout

    def update_radio_buttons(self, checked, button_value, radio_attr):
        if checked:
            setattr(self, radio_attr, button_value)
    #============================================

    # ------------ patreon label----------------------
    def load_and_process_image(self, image_path):
        self.pixmap = QPixmap(image_path)
        self.pixmap = self.pixmap.scaledToWidth(set_scaledToWidth, Qt.TransformationMode.SmoothTransformation)

        path = QPainterPath()
        path.addRoundedRect(QRectF(self.pixmap.rect()), 10, 10)  # 10は角の丸みの大きさ
        rounded_pixmap = QPixmap(self.pixmap.size())
        rounded_pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter(rounded_pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setClipPath(path)
        painter.drawPixmap(0, 0, self.pixmap)
        painter.end()
        self.pixmap = rounded_pixmap

    def patreon_label_enterEvent(self, event):
        addon_path = dirname(__file__)
        patreon_banner_hover_path = join(addon_path, patreon_banner_jpg)
        self.load_and_process_image(patreon_banner_hover_path)
        self.patreon_label.setPixmap(self.pixmap)

    def patreon_label_leaveEvent(self, event):
        self.load_and_process_image(self.addon_banner_image)
        self.patreon_label.setPixmap(self.pixmap)
    # ------------ patreon label----------------------

    #-- open patreon link-----
    def open_patreon_Link(self,url):
        openLink(patreon_link_url)


    #------------spinbox: font size-----------------
    def handle_popup_card_number(self, value):
        value = round(value, 1)
        self.anki_popup_card_number = int(value)
    #------------spinbox-----------------


    def handle_button_clicked(self):
        self.save_config_data()

        emoticons = [":-)", ":-D", ";-)"]
        selected_emoticon = random.choice(emoticons)
        tooltip("Changed setting " + selected_emoticon)


    def save_config_data(self):
        config = mw.addonManager.getConfig(__name__)

        config["font_size"] = self.font_size
        config["background_color"] = self.background_color
        config["text_color"] = self.text_color
        config["color_traceback"] = self.color_traceback
        config["color_file"] = self.color_file
        config["color_line"] = self.color_line
        config["color_error"] = self.color_error
        config["color_in"] = self.color_in
        config["color_string"] = self.color_string

        mw.addonManager.writeConfig(__name__, config)

def setMyAddonConfig():
    myAddonConfing = MyAddonConfig(mw)
    myAddonConfing.show()

def setMyAddonConfigModal():
    myAddonConfig = MyAddonConfig(mw)
    if hasattr(myAddonConfig, "exec"):
        myAddonConfig.exec()
    elif hasattr(myAddonConfig, "exec_"):
        myAddonConfig.exec_()
    else:
        myAddonConfig.setModal(True)
        myAddonConfig.show()



def add_my_addon_config_button():
    mw.addonManager.setConfigAction(__name__, setMyAddonConfigModal)

    myAddonAction = QAction(f"🐞{ADDON_NAME} (Created by Shigeඞ)", mw)
    qconnect(myAddonAction.triggered, setMyAddonConfig)
    mw.form.menuTools.addAction(myAddonAction)

def add_my_config_guihooks():
    gui_hooks.main_window_did_init.append(add_my_addon_config_button)

