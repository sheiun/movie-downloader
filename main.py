import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *

import crawler


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = '小程式'
        self.width = 1024
        self.height = 768
        self.status_message = '準備就緒'
        self.initUi()

        self.table_widget = MyTableWidget(self)
        self.setCentralWidget(self.table_widget)

    def initUi(self):
        self.setWindowTitle(self.title)
        self.resize(self.width, self.height)
        self.statusBar().showMessage(self.status_message)
        self.show()


class MyTableWidget(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)

        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = MyTabWidget(self, "影片搜尋")
        self.tab2 = QWidget()

        # Add tabs
        self.tabs.addTab(self.tab1, self.tab1.name)
        self.tabs.addTab(self.tab2, "下載清單")

        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)


class MyTabWidget(QWidget):
    def __init__(self, parent, name):
        super(QWidget, self).__init__(parent)
        self.name = name
        self.layout = QVBoxLayout(self)
        # Create search block
        self.search_block = QHBoxLayout(self)
        # search bar
        self.search_bar = QLineEdit(self)
        self.search_block.addWidget(self.search_bar)
        # search button
        self.search_button = QPushButton("搜尋")
        self.search_button.clicked.connect(self.search)
        self.search_block.addWidget(self.search_button)
        # add search block
        self.layout.addLayout(self.search_block)
        # list view
        self.search_list = QListWidget(self)
        self.layout.addWidget(self.search_list)
        # layout
        self.layout.setAlignment(Qt.AlignTop)
        self.setLayout(self.layout)

    @pyqtSlot()
    def search(self):
        list_fetch_thread = ListFetchThread(self.search_bar.text())
        list_fetch_thread.list_fetched.connect(self.get_movie_list)
        print('test1')
        list_fetch_thread.start()
        print('test2')

    def get_movie_list(self, data):
        movie_list = data
        self.search_list.clear()
        for movie in movie_list:
            movie_item = QListWidgetItem()
            movie_item.setText(movie[0])
            movie_item.setToolTip(movie[1])
            self.search_list.addItem(movie_item)
        self.search_list.itemDoubleClicked.connect(self.ask)

    def ask(self, item):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("通知")
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setText("是否要下載: \n" + item.text())
        msg_box.addButton(QPushButton('是'), QMessageBox.YesRole)
        msg_box.addButton(QPushButton('否'), QMessageBox.NoRole)
        ret = msg_box.exec_()  # return 0: yes return 1:no
        if ret == 0:
            print(item.toolTip())  # crawler.crawl_page()


class ListFetchThread(QThread):

    list_fetched = pyqtSignal(object)

    def __init__(self, text, page=1, parent=None):
        super().__init__(parent)
        self.text = text
        self.page = page

    def run(self):
        movie_list = crawler.crawl(self.text, self.page)
        self.list_fetched.emit(movie_list)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
