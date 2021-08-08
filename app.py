import sys
import asyncio
import platform

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5 import QtGui, QtCore
import qasync


from gui.MainWindow import Ui_MainWindow
from proxy import ProxyServer
from settings import Settings, GAMEHOSTS

from plugins import outfit
from plugins import shield


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        loop = asyncio.get_event_loop()


        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon('gui/thumbnail.png'))


        self.set_hosts()
        self.proxy = ProxyServer()
        self.proxy_task = loop.create_task(self.proxy.start())

        self.outfit_plugin = outfit.Plugin(self.proxy)
        self.initUi()


    def initUi(self):
        self.gamehostSelectBox.addItems(GAMEHOSTS.keys())
        self.gamehostSelectBox.currentTextChanged.connect(
                lambda x:self.proxy.switch_gamehost(str(x)))


        self.outfitSaveBtn.clicked.connect(self.on_save_outfit)

        self.outfitDeleteBtn.clicked.connect(self.on_delete_outfit)

        self.outfitSelectBox.setDuplicatesEnabled(False)
        self.outfitSelectBox.addItem("Wishlist")
        self.outfitSelectBox.addItems\
                                (outfit.OutfitManager.outfits.keys())
        self.outfitSelectBox.currentIndexChanged.\
                                    connect(self.on_load_outfit)

        self.forceUpdateBtn.clicked.\
                                connect(self.outfit_plugin.force_update)
        self.outfitActivateBtn.toggled.connect(self.on_outfit_activate)
        self.outfitActivateBtn.setChecked(True)

        self.shieldActivateBtn.toggled.connect(self.on_shield_activate)
        self.shieldActivateBtn.setChecked(True)





    def set_hosts(self):
        try:
            Settings.hosts_config.add_host_overrides()
        except PermissionError:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Hosts file could not be written.\n"
                        "The app might not work properly.  "
                        "Try running as admin")
            msg.setWindowTitle("Warning")
            msg.show()

    def closeEvent(self, event):
        try:
            Settings.hosts_config.rem_host_overrides()
            self.proxy_task.cancel()

        except: pass
        event.accept()

    def on_save_outfit(self):
        name = str(self.outfitSelectBox.currentText())
        if name == "Wishlist":
            return
        old_keys = list(outfit.OutfitManager.outfits.keys())

        outfit.OutfitManager.save_outfit(name)

        if name not in old_keys:
            items_len = self.outfitSelectBox.count()
            self.outfitSelectBox.addItem(name)
            self.outfitSelectBox.setCurrentIndex(items_len)

    def on_delete_outfit(self):
        name = str(self.outfitSelectBox.currentText())
        if name == "Wishlist":
            return
        index = self.outfitSelectBox.currentIndex()
        outfit.OutfitManager.delete_outfit(name)
        self.outfitSelectBox.removeItem(index)

    def on_load_outfit(self):
        name = str(self.outfitSelectBox.currentText())
        if name == "Wishlist":
            outfit.OutfitManager.activate_wl(True)
        else:
            outfit.OutfitManager.select_current_outfit(name)
            outfit.OutfitManager.activate_wl(False)
        if outfit.OutfitManager.is_active:
            self.outfit_plugin.force_update()


    def on_outfit_activate(self, activate):
        outfit.OutfitManager.is_active = activate
        self.on_load_outfit()
        if activate:
            self.outfitActivateBtn.setText("Deactivate")
        else:
            self.outfitActivateBtn.setText("Activate")

    def on_shield_activate(self, activate):
        shield.Plugin.is_active = activate
        if activate:
            self.shieldActivateBtn.setText("Deactivate")
        else:
            self.shieldActivateBtn.setText("Activate")


def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')


    loop = qasync.QEventLoop(app)
    asyncio.set_event_loop(loop)

    window = MainWindow()
    window.show()
    with loop:
        loop.run_forever()

    sys.exit()



if __name__ == "__main__":
    if platform.system() == "Windows":
        import pyuac
        if not pyuac.isUserAdmin():
            pyuac.runAsAdmin()
        else:
            main()
    else:        
        main()