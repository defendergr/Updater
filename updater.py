from urllib.request import urlopen
from urllib import error
import sys
import json
from cryptography.fernet import Fernet
import PySimpleGUIQt as sg
from shutil import rmtree
import patoolib
import os

from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QThread, Signal, QFile, Qt
from PySide6.QtWidgets import QApplication



class Downloader(QThread):

    # Signal for the window to establish the maximum value
    # of the progress bar.
    setTotalProgress = Signal(int)
    # Signal to increase the progress.
    setCurrentProgress = Signal(int)
    # Signal to be emitted when the file has been downloaded successfully.
    succeeded = Signal()

    def __init__(self, url, filename):
        super().__init__()
        self._url = url
        self._filename = filename
        key = 'xFJwWVWsL2gZlbGqqi2N_7A8xNDpdXlw9A3EbW4cetQ='
        fn = 'data'
        self.path = Encrypted_data_dict.decrypt(fn, key)

    def run(self):
        url = self.path['update']
        filename = self.path['fn']
        readBytes = 0
        chunkSize = 1024
        # Open the URL address.
        with urlopen(url) as r:
            # Tell the window the amount of bytes to be downloaded.
            self.setTotalProgress.emit(int(r.info()["Content-Length"]))
            with open(filename, "ab") as f:
                while True:
                    # Read a piece of the file we are downloading.
                    chunk = r.read(chunkSize)
                    # If the result is `None`, that means data is not
                    # downloaded yet. Just keep waiting.
                    if chunk is None:
                        continue
                    # If the result is an empty `bytes` instance, then
                    # the file is complete.
                    elif chunk == b"":
                        break
                    # Write into the local file the downloaded chunk.
                    f.write(chunk)
                    readBytes += chunkSize
                    # Tell the window how many bytes we have received.
                    self.setCurrentProgress.emit(readBytes)
        # If this line is reached then no exception has ocurred in
        # the previous lines.
        self.succeeded.emit()


class MainWindow():

    def __init__(self):
        super(MainWindow, self).__init__()
        app = QApplication(sys.argv)
        app.setStyleSheet('QMainWindow{background-color: darkgray;} '
                          'QProgressBar{border-radius: 5px; background-color: gray;} '
                          'QProgressBar::chunk {border-radius: 5px; background-color: #F433FF;}'
                          'QProgressBar{text-align:center; font:bold} '
                          'QPushButton{border-radius: 5px; background-color: lightgray;}'
                          )
        ui_file_name = "form.ui"
        ui_file = QFile(ui_file_name)
        # if not ui_file.open(QIODevice.ReadOnly):
        #     print(f"Cannot open {ui_file_name}: {ui_file.errorString()}")
        #     sys.exit(-1)
        loader = QUiLoader()
        window = loader.load(ui_file)
        ui_file.close()
        # if not window:
        #     print(loader.errorString())
        #     sys.exit(-1)

        # TODO window icon

        # this keep window top
        window.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)

        # this will hide the title bar
        window.setWindowFlag(Qt.FramelessWindowHint)

        # window.onomaStixiou.entoles
        window.pushButton.clicked.connect(self.about)
        self.progressBar = window.progressBar

        window.show()

        key = 'xFJwWVWsL2gZlbGqqi2N_7A8xNDpdXlw9A3EbW4cetQ='
        fn = 'data'
        self.path = Encrypted_data_dict.decrypt(fn, key)

        if self.version_check():
            self.initDownload()


        app.exec()


    def initDownload(self):
        # Run the download in a new thread.
        self.downloader = Downloader(self.path['update'],self.path['fn'])
        print(self.path['update'])
        print(self.path['fn'])
        # Connect the signals which send information about the download
        # progress with the proper methods of the progress bar.
        self.downloader.setTotalProgress.connect(self.progressBar.setMaximum)
        self.downloader.setCurrentProgress.connect(self.progressBar.setValue)
        # Qt will invoke the `succeeded()` method when the file has been
        # downloaded successfully and `downloadFinished()` when the
        # child thread finishes.
        self.downloader.succeeded.connect(self.downloadSucceeded)
        self.downloader.finished.connect(self.downloadFinished)
        self.downloader.start()

    def downloadSucceeded(self):
        # Set the progress at 100%.
        self.progressBar.setValue(self.progressBar.maximum())


    def downloadFinished(self):
        # Delete the thread when no longer needed.
        del self.downloader
        print('setup starting')
        self.setup()

    def setup(self):
        if self.path['fn'].split(".")[-1] == 'rar' or self.path['fn'].split(".")[-1] == 'zip':
            if os.path.exists(self.path['fn'].split(".")[-2]):
                rmtree(self.path['fn'].split(".")[-2])
            patoolib.extract_archive(self.path['fn'], outdir="./")
        elif self.path['fn'].split(".")[-1] == 'exe':
            os.startfile(self.path['fn'])
        else:
            print(f"o typos arxioy {self.path['fn'].split('.')[-1]} den upostirizete pros to paron")
        os.remove(self.path['fn'])
        print('setup finished')
        sys.exit()


    def version_check(self):
        try:
            local_file = self.path['local']
            print(local_file)
            dl_file = self.path['remote']
            print(dl_file)
            ver_check = self.path['check']
            print(ver_check)
            version_remote = float(urlopen(ver_check).read().decode('utf8'))
            version_local = float(open(local_file, 'r').read().strip())
            print(f"Remote version {version_remote}")
            print(f"Local version {version_local}")
            if version_remote > version_local:
                return True
            else:
                print('updated')
                sys.exit()



        except error.HTTPError:
            print('Den vrethike to URL')
            sys.exit()

        except  FileNotFoundError:
            print('den vrethike to arxeio')
            sys.exit()

    def about(self):
        sg.Popup(' Πληροφορίες',
                 ' Updater Έκδοση 1.0 \n\n Ευχαριστώ που χρησιμοποιείτε την εφαρμογή. \n Η εφαρμογή αναπτύχθηκε από τον \n Κωνσταντίνο Καρακασίδη. \n\n Επικοινωνία: defendergr@gmail.com \n',
                 icon='icon.ico', keep_on_top=True)


class Encrypted_data_dict():
    def decrypt(filename, key):
        """
        Given a filename (str) and key (bytes), it encrypts the file and write it
        """
        f = Fernet(key)

        with open(filename, "rb") as file:
            # read all file data
            file_data = file.read()
            # encrypt data
            encrypted_data = f.decrypt(file_data)
            # reconstructing the data as a dictionary
            js = json.loads(encrypted_data)

            return js


if __name__ == "__main__":
    MainWindow()