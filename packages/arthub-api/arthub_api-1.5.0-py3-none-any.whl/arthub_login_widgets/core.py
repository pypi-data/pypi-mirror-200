# -*- coding: utf-8 -*-
"""A Qt Widget for login ArtHub."""

# Import future modules
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# Import built-in modules
import logging
import webbrowser
import os

# Import third-party modules
from Qt import QtCore
from Qt import QtGui
from Qt import QtWidgets

# Import local modules
from arthub_login_widgets.constants import ARTHUB_RESET_PASSWORD_WEB_URL
from arthub_login_widgets.constants import UI_TEXT_MAP
from arthub_login_widgets.filesystem import get_login_account
from arthub_login_widgets.filesystem import get_resource_file
from arthub_login_widgets.filesystem import save_login_account


def _load_style_sheet(style_file):
    try:
        from lightbox_ui.style import load_style_sheet
        return load_style_sheet(style_file)
    except ImportError:
        with open(style_file, "r") as css_file:
            css_string = css_file.read().strip("\n")
            data = os.path.expandvars(css_string)
            return data


class LoginWindow(QtWidgets.QMainWindow):
    def __init__(
            self,
            api,
            api_callback=None,
            parent_window=None,
            language_cn=True,
    ):
        """Initialize an instance.

        Args:
            api(arthub_api.OpenAPI): The instance of the arthub_api.OpenAPI.
            api_callback (Function, optional): Called when the login is successful, the login status will be saved
                                                     in arthub_open_api.
            parent_window (QtWidgets.QWidget, optional): The Qt main window instance.
            language_cn (Boolean, optional): The text is displayed in Chinese, otherwise in English.

        """
        super(LoginWindow, self).__init__(parent=parent_window)
        self.language_cn = language_cn
        self.arthub_open_api = api
        self._api_callback = api_callback
        self.logged = False

        # init ui
        self.setFixedSize(280, 290)
        self.central_widget = QtWidgets.QWidget(self)
        self.central_widget.setObjectName("central_widget")
        self.setCentralWidget(self.central_widget)

        # icon
        self.icon_label = QtWidgets.QLabel(self)
        self.icon_label.setFixedSize(QtCore.QSize(167, 40))
        self.icon_label.setPixmap(QtGui.QPixmap(get_resource_file("arthub_white.png")))
        self.icon_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.icon_label.setScaledContents(True)

        # line edit
        def _create_line_edit():
            _line_edit_font = QtGui.QFont()
            _line_edit_font.setPixelSize(13)
            _line_edit = QtWidgets.QLineEdit(self)
            _line_edit.setFont(_line_edit_font)
            _line_edit.setFixedSize(228, 31)
            _line_edit.setTextMargins(5, 0, 5, 0)
            return _line_edit

        self.line_edit_account = _create_line_edit()
        self.line_edit_password = _create_line_edit()
        self.line_edit_password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)

        # login status prompt
        _label_prompt_font = QtGui.QFont()
        _label_prompt_font.setPixelSize(11)
        self.label_prompt = QtWidgets.QLabel("", self)
        self.label_prompt.setObjectName("label_prompt")
        self.label_prompt.setFont(_label_prompt_font)
        self.label_prompt.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        # login button
        self.pushButton_login = QtWidgets.QPushButton(self.central_widget)
        self.pushButton_login.setObjectName("pushButton_login")
        self.pushButton_login.setText("")
        self.pushButton_login.setFixedSize(228, 34)
        self.pushButton_login.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self.pushButton_login.clicked.connect(self.on_login)

        # reset password button
        _label_forgot_password_font = QtGui.QFont()
        _label_forgot_password_font.setPixelSize(11)
        self.label_forgot_password = QtWidgets.QPushButton("", self)
        self.label_forgot_password.setObjectName("label_forgot_password")
        self.label_forgot_password.setFont(_label_forgot_password_font)
        self.label_forgot_password.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self.label_forgot_password.clicked.connect(self.on_forgot_password)

        main_layout = QtWidgets.QVBoxLayout(self.central_widget)
        main_layout.addSpacing(31)
        main_layout.setSpacing(5)
        main_layout.addWidget(self.icon_label)
        main_layout.addSpacing(15)
        main_layout.setAlignment(self.icon_label, QtCore.Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.line_edit_account)
        main_layout.setAlignment(self.line_edit_account, QtCore.Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.line_edit_password)
        main_layout.setAlignment(self.line_edit_password, QtCore.Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.label_prompt)
        main_layout.setAlignment(self.label_prompt, QtCore.Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.pushButton_login)
        main_layout.setAlignment(self.pushButton_login, QtCore.Qt.AlignmentFlag.AlignCenter)
        main_layout.addSpacing(1)
        main_layout.addWidget(self.label_forgot_password)
        main_layout.setAlignment(self.label_forgot_password, QtCore.Qt.AlignmentFlag.AlignCenter)
        main_layout.addSpacing(23)
        self.central_widget.setLayout(main_layout)
        self.translate_ui()

        # init model
        last_account = get_login_account()
        if last_account is not None:
            self.line_edit_account.setText(last_account)

        # set style
        qss_file = get_resource_file("style.qss")
        style_sheet = _load_style_sheet(qss_file)
        self.setStyleSheet(style_sheet)

    def set_callback(self, callback):
        self._api_callback = callback

    def _get_ui_text_by_language(self, key):
        v = UI_TEXT_MAP.get(key)
        if v is None:
            return ""
        return v[1 if self.language_cn else 0]

    def translate_ui(self):
        self.setWindowTitle(self._get_ui_text_by_language("window_title"))
        self.line_edit_account.setPlaceholderText(self._get_ui_text_by_language("account_placeholder"))
        self.line_edit_password.setPlaceholderText(self._get_ui_text_by_language("password_placeholder"))
        self.pushButton_login.setText(self._get_ui_text_by_language("login_button"))
        self.label_forgot_password.setText(self._get_ui_text_by_language("forgot_password_button"))

    def set_prompt(self, text):
        self.label_prompt.setText(text)

    def _on_login_succeeded(self, account):
        save_login_account(account)
        if self._api_callback:
            self._api_callback(self)
        self.logged = True
        self.close()

    def login(self):
        self.set_prompt("")
        account = self.line_edit_account.text()
        password = self.line_edit_password.text()
        if account == "":
            self.set_prompt("Email/Phone cannot be empty")
            return
        if password == "":
            self.set_prompt("Password cannot be empty")
            return

        res = self.arthub_open_api.login(account, password)
        if not res.is_succeeded():
            error_msg = res.error_message()
            logging.warning("Log in ArtHub failed: %s", error_msg)
            self.set_prompt(error_msg)
            return

        self._on_login_succeeded(account)

    def on_login(self):
        self.login()

    @staticmethod
    def on_forgot_password():
        webbrowser.open(ARTHUB_RESET_PASSWORD_WEB_URL)
