#!/usr/bin/env python

import sys, os
from PyQt4 import QtGui, QtCore

class Signer(QtCore.QThread):
  signing_done = QtCore.pyqtSignal()
  def __init__(self, text):
    QtCore.QThread.__init__(self)
    self.text = text
  def run(self):
    cmd = "cd /home/mquigley/sandia-hand-ws/src/sandia-hand/ros/sandia_hand_teleop/simple_grasp && bash -c \". /home/mquigley/sandia-hand-ws/devel/setup.bash && ./simple_grasp_asl.py only \\\"%s\\\" 4 1\"" % self.text
    print cmd
    os.system(cmd)
    self.signing_done.emit()

class GUI(QtGui.QWidget):
  def __init__(self):
    super(GUI, self).__init__()
    font = QtGui.QFont("Arial",200)
    self.qle = QtGui.QLineEdit(self)
    self.qle.setGeometry(10, 10, 1300, 300)
    self.qle.setFont(font)
    #self.qle.textChanged[str].connect(self.onChanged)
    self.qle.returnPressed.connect(self.onReturn)
    self.setGeometry(20, 20, 1320, 400)
    self.setWindowTitle("ASL demo")
    self.show()
  def onSigningDone(self):
    self.qle.clear()
    self.setBoxColor('white')
    self.qle.setEnabled(True)
    self.qle.setFocus()
  def onReturn(self):
    print self.qle.text()
    self.signing_thread = Signer(self.qle.text())
    self.signing_thread.signing_done.connect(self.onSigningDone)
    self.signing_thread.start()
    self.setBoxColor('green')
    self.qle.setEnabled(False)
  def setBoxColor(self, color):
    #pal = QtGui.QPalette(self.qle.palette())
    #pal.setColor(QtGui.QPalette.Base,QtGui.QColor(color))
    #self.qle.setPalette(pal)
    #self.qle.update()
    self.qle.setStyleSheet("QLineEdit {background: %s; }" % color)
    self.qle.show()
    self.qle.setAutoFillBackground(True)

if __name__ == '__main__':
  app = QtGui.QApplication(sys.argv)
  gui = GUI()
  sys.exit(app.exec_())
