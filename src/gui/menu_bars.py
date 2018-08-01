from PyQt5.QtWidgets import QAction, QDialog, QLabel, QVBoxLayout, QTextEdit, QMenuBar
import webbrowser
from src.gui.modal_dialogs import show_feature_in_development_dialog


class MenuBars:
    def __init__(self, bar):
        super(MenuBars, self).__init__()
        self.bar = bar
        self.file_menu = bar.addMenu('&File')
        self.edit_menu = bar.addMenu('&Edit')
        self.view_menu = bar.addMenu('&View')
        self.tshoot_menu = bar.addMenu('&Troubleshoot')
        self.help_menu = bar.addMenu('&Help')

    def generate_menu_bars(self):
        # File options
        file_open = QAction('&Open', self.bar)
        file_open.setShortcut('Ctrl+O')
        file_save = QAction('&Save', self.bar)
        file_save.setShortcut('Ctrl+S')
        file_quit = QAction('&Quit', self.bar)
        file_quit.setShortcut('Ctrl+Q')

        # Edit options
        edit_preferences = QAction('&Prefrences', self.bar)
        edit_preferences.setShortcut('Ctrl+P')

        # View options
        view_interfaces = QAction('&Interfaces', self.bar)
        view_interfaces.setShortcut('Ctrl+I')
        view_routing = QAction('&Routing', self.bar)
        view_routing.setShortcut('Ctrl+R')
        view_connection_data = QAction('Connection &Data', self.bar)
        view_connection_data.setShortcut('Ctrl+D')

        # Tshoot options
        tshoot_errors = QAction('Tshoot &Errors', self.bar)
        tshoot_errors.setShortcut('Ctrl+E')
        tshoot_pcap = QAction('Tshoot &with Pcaps', self.bar)
        tshoot_pcap.setShortcut('Ctrl+W')

        # Help options
        help_support = QAction('Get S&upport', self.bar)
        help_support.setShortcut('Ctrl+U')
        help_about = QAction('A&bout', self.bar)
        help_about.setShortcut('Ctrl+B')

        self.file_menu.addAction(file_open)
        self.file_menu.addAction(file_save)
        self.file_menu.addAction(file_quit)
        self.edit_menu.addAction(edit_preferences)
        self.view_menu.addAction(view_interfaces)
        self.view_menu.addAction(view_routing)
        self.view_menu.addAction(view_connection_data)
        self.tshoot_menu.addAction(tshoot_errors)
        self.tshoot_menu.addAction(tshoot_pcap)
        self.help_menu.addAction(help_support)
        self.help_menu.addAction(help_about)

        file_open.triggered.connect(self.file_open_action)
        file_save.triggered.connect(self.file_save_action)
        file_quit.triggered.connect(self.file_quit_action)
        edit_preferences.triggered.connect(self.edit_prefs_action)
        view_interfaces.triggered.connect(self.view_interfaces_action)
        view_routing.triggered.connect(self.view_routing_action)
        view_connection_data.triggered.connect(self.view_data_action)
        tshoot_errors.triggered.connect(self.tshoot_error_action)
        tshoot_pcap.triggered.connect(self.tshoot_pcap_action)
        help_support.triggered.connect(self.help_support_action)
        help_about.triggered.connect(self.help_about_action)

    def file_open_action(self):
        # Might use this to open a saved vpn config
        show_feature_in_development_dialog()
        pass

    def file_save_action(self):
        # Might use this to save a vpn config
        show_feature_in_development_dialog()
        pass

    def file_quit_action(self):
        exit()

    def edit_prefs_action(self):
        # Preferences should go here.
        # How many settings are here will depend on the feature set
        self.prefs = QDialog()
        layout = QVBoxLayout()
        self.prefs_heading = QLabel('<h1>Preferences</h1>')
        layout.addWidget(self.prefs_heading)
        self.prefs.setLayout(layout)
        self.prefs.show()

    def view_interfaces_action(self):
        # If linux/macos > ifconfig
        # If Windows > ipconfig /all
        show_feature_in_development_dialog()
        pass

    def view_routing_action(self):
        # If linux/macos > netstat -rn
        # If Windows > route print
        show_feature_in_development_dialog()
        pass

    def view_data_action(self):
        show_feature_in_development_dialog()
        pass

    def tshoot_error_action(self):
        # In Windows, use powershell: get-eventlog
        show_feature_in_development_dialog()
        pass

    def tshoot_pcap_action(self):
        show_feature_in_development_dialog()
        pass

    @staticmethod
    def help_support_action():
        # Redirect to Meraki's support website
        webbrowser.open('https://meraki.cisco.com/support')

    @staticmethod
    def help_about_action():
        about_popup = QDialog()
        about_popup.setWindowTitle("Meraki Client VPN: About")
        about_program = QLabel()
        about_program.setText("<h1>Meraki VPN Client 0.5.1</h1>\n"
                              "Developed by Ross Jacobs<br><br><br>"
                              "This project is licensed with the "
                              "Apache License, which can be viewed below:")
        license_text = open("LICENSE", 'r').read()
        licenses = QTextEdit()
        licenses.setText(license_text)
        licenses.setReadOnly(True)  # People shouldn't be able to edit licenses!
        popup_layout = QVBoxLayout()
        popup_layout.addWidget(about_program)
        popup_layout.addWidget(licenses)
        about_popup.setLayout(popup_layout)
        about_popup.setMinimumSize(600, 200)
        about_popup.exec_()
