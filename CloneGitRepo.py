import json
import os
import sys
import logging
import traceback

from subprocess import call
from PySide import QtGui
from PySide import QtCore
from PySide.QtGui import QMessageBox

jsonFile = "config.json"

get_icon_path = lambda x: os.path.join(
    os.path.dirname(__file__),
    'materials',
    x
)

class ImageButton(QtGui.QPushButton):
    '''
    The implementation of button with image icon.
    '''

    def __init__(self, parent, icon, iconsize=(10, 10)):
        super(ImageButton, self).__init__('', parent)
        self.setIcon(QtGui.QIcon(icon))
        self.setIconSize(QtCore.QSize(*iconsize))


class AppWindow(QtGui.QMainWindow):
    '''
    The implementation of main window of application.
    '''
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setWindowTitle('Set Up')
        self.setCentralWidget(InstallerWidget())

		
class InstallerWidget(QtGui.QWidget):
## Main window class

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.pack()


    def pack(self):
	## Window settings
        self.readParams()
        layout = QtGui.QVBoxLayout()
        self.label = QtGui.QLabel(
            '<font color=blue size=50>'
            + 'Welcome to the Walker Set Up'
            + '</font>'
        )
        self.lbPath = QtGui.QLabel('Path : ')
        self.lePath = QtGui.QLineEdit()
        self.lePath.setText(params["path"])

        self.lbUsr = QtGui.QLabel('User : ')
        self.leUsr = QtGui.QLineEdit()
        self.leUsr.setText(params["usr"])
        
        self.lbUrl = QtGui.QLabel('Url : ')
        self.leUrl = QtGui.QLineEdit()
        self.leUrl.setText(params["url"])

        self.lbFiles = QtGui.QLabel('File Type : ')
        self.leFiles = QtGui.QLineEdit()
        self.leFiles.setText(params["files"])

        self.lbSch = QtGui.QLabel('Run every : ')
        self.leTime = QtGui.QLineEdit()
        self.leTime.setText(params["time"])
        
        self.cbSch = QtGui.QComboBox()
        self.cbSch.addItem("MINUTE")
        self.cbSch.addItem("HOURLY")
        self.cbSch.addItem("DAILY")
        self.cbSch.addItem("WEEKLY")
        self.cbSch.addItem("MONTHLY")
        self.cbSch.setCurrentIndex(self.cbSch.findText(params["schedule"]))

        self.lbExe = QtGui.QLabel('Path to task : ')
        self.leExe = QtGui.QLineEdit()
        self.leExe.setText(params["exePath"])

        self.lbTask = QtGui.QLabel('Task name: ')
        self.lbTaskName =QtGui.QLabel(params["taskName"])

        self.btSave = ImageButton(self, get_icon_path('install.png'), (30, 30))
        self.btSave.clicked.connect(self.save)
        
        layout.addWidget(self.label)

        layout.addWidget(self.lbPath)
        layout.addWidget(self.lePath)

        layout.addWidget(self.lbUsr)
        layout.addWidget(self.leUsr)

        layout.addWidget(self.lbUrl)
        layout.addWidget(self.leUrl)

        layout.addWidget(self.lbFiles)
        layout.addWidget(self.leFiles)

        layout.addWidget(self.lbSch)
        layout.addWidget(self.leTime)
        layout.addWidget(self.cbSch)

        layout.addWidget(self.lbExe)
        layout.addWidget(self.leExe)

        layout.addWidget(self.lbTask)
        layout.addWidget(self.lbTaskName)

        layout.addWidget(self.btSave)
        self.setLayout(layout)
        
    def readParams(self):
	## Read parameters form JsonFile
        global params
        try:
            params = json.loads(open(jsonFile).read())
        except:
            logging.error(traceback.format_exc())

    def save(self):
	## Save data to file, clone repository and create windows task
         self.setEnabled(False)
         params["path"] = self.lePath.text()
         params["usr"] = self.leUsr.text()
         params["url"] = self.leUrl.text()
         params["files"] = self.leFiles.text()
         params["schedule"] = self.cbSch.currentText()
         params["time"] = self.leTime.text()
         params["exePath"] = self.leExe.text()
         params["taskName"] = self.lbTaskName.text()
         self.writeJson()
         msgBox = QMessageBox()
         messageText = "<font color=blue size=5>Saving Configuration ... OK <br>"
         if(cloneRepo(params["url"], params["path"])):
             messageText += "Creating repository ... OK <br>"
         else:
             messageText += "Creating repository ... <br> <font color= red>Already created or connection problem <br>"
             messageText += "Please check if <b>" + params["path"] +"</b> exists</font><br>"
         if((checkTask(params["taskName"])) == 0):
              deleteTask(params["taskName"])
         createTask(params["schedule"], params["time"], params["exePath"], params["taskName"])
         messageText +=  "Creating task ... OK </font>"
         msgBox.setText(messageText)         
         msgBox.exec_()
         self.setEnabled(True)

    def writeJson(self):
	## Write changes to json file
        with open(jsonFile,'w') as outfile:
            json.dump(params, outfile)


def cloneRepo(url, path):
##Clone repository (url - Repo's URL) (path - Repo's path)
	resp = call(["git","clone", url, path])
	if (resp == 128):
		return False
	print "Repository created at " + path
	return True

def createTask(sc, mo, tr, tn):
##Create windows task (SC - MINUTE, HOURLY, DAILY, WEEKLY) (MO - Number of minutes, hours...) 
##(TR - Path to exe) (TN - Task name)

	call(["schtasks", "/CREATE", "/SC", sc, "/MO", mo, "/TN", tn, "/TR", tr])
	print "Task " + tn + " created"
		
def deleteTask(tn):
##Delete windows task (TN - Task name)
	call(["schtasks", "/DELETE", "/TN", tn, "/F"])
	print "Task " + tn + " deleted"

def checkTask(tn):
##Check if Task exists (TN - Task name)
	return call(["schtasks", "/QUERY", "/TN", tn])
	
if __name__ == '__main__':
## Main
    try:
        app = QtGui.QApplication.instance()
        if app is None:
            app = QtGui.QApplication(sys.argv)
        window = AppWindow()
        window.show()
        app.exec_()
    except:
        logging.error(traceback.format_exc())
        raw_input()
