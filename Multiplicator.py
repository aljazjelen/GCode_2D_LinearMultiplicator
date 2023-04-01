"""
Created on Fri Dec  2 21:00:29 2022

@author: Aljaz Jelen
"""


import sys
from PyQt5.QtWidgets import ( 
    QApplication, 
    QWidget, 
    QInputDialog, 
    QLineEdit, 
    QFileDialog, 
    QPushButton, 
    QSpinBox, 
    QHBoxLayout,
    QVBoxLayout,
    QCheckBox,
    QLabel,
    QGridLayout,
    QRadioButton,
    QGroupBox
    )

from PyQt5.QtGui import QIcon, QPixmap



class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'GCode linear multiplicator'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.setFixedSize(480, 480)
        self.initUI()
        
        self.file = None
        self.gCode_single = None
        
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        
        
        # TOP
        main_top_layout = QHBoxLayout()
        self.loadGcodeButton = QPushButton("Load Gcode")
        self.loadGcodeButton.clicked.connect(self.openFileNameDialog)
        
        self.loadedFile = QLineEdit()
        self.loadedFile.setDisabled(True)
        
        self.saveGcodeButton = QPushButton("Save Gcode")
        self.saveGcodeButton.clicked.connect(self.saveFileDialog)
        
        main_top_layout.addWidget(self.loadGcodeButton)
        main_top_layout.addWidget(self.loadedFile)
        main_top_layout.addWidget(self.saveGcodeButton)
        
        # BOTTOM
        main_bot_layout = QHBoxLayout()
        
        settings_vlayout = QVBoxLayout()
        display_vlayout = QVBoxLayout()
        
        grid_Xsettings = QGridLayout()
        grid_Ysettings = QGridLayout()
        grid_genSettings = QGridLayout()
        grid_display = QGridLayout()
        #self.grid.addWidget(self.label,1,1)
        
        self.xRadio = QCheckBox("Multiply in X direction")
        self.xRadio.setChecked(True)
        self.xMultiplySp = QSpinBox()
		#self.sp.valueChanged.connect(self.valuechange)
        self.xOffset = QLineEdit()
        self.xRadio.toggled.connect(self.radioXYcontrol)
        
        
        self.yRadio = QCheckBox("Multiply in Y direction")
        self.yMultiplySp = QSpinBox()
        self.yOffset = QLineEdit()
        self.yMultiplySp.setDisabled(True)
        self.yOffset.setDisabled(True)
        self.yRadio.toggled.connect(self.radioXYcontrol)
        
        self.safeZ = QLineEdit()
        self.backHomeCheck = QCheckBox("Back Home")
        
        
        self.xFrame = QGroupBox(checkable=False)    
        self.xFrame.setTitle("X pattern settings")
        self.xFrame.setCheckable(False)
        
        yFrame = QGroupBox(checkable=False)    
        yFrame.setTitle("Y pattern settings")
        yFrame.setCheckable(False)
        
        genFrame = QGroupBox(checkable=False)    
        genFrame.setTitle("General settings")
        
        
        grid_Xsettings.addWidget(self.xRadio,0,0)
        grid_Xsettings.addWidget(QLabel("X Instances:"),1,0)
        grid_Xsettings.addWidget(self.xMultiplySp,1,1)
        grid_Xsettings.addWidget(QLabel("X Offset:"),2,0)
        grid_Xsettings.addWidget(self.xOffset,2,1)
        
        grid_Ysettings.addWidget(self.yRadio,3,0)
        grid_Ysettings.addWidget(QLabel("Y Instances:"),4,0)
        grid_Ysettings.addWidget(self.yMultiplySp,4,1)
        grid_Ysettings.addWidget(QLabel("Y Offset:"),5,0)
        grid_Ysettings.addWidget(self.yOffset,5,1)

        grid_genSettings.addWidget(QLabel("Safe Z moves:"),7,0)
        grid_genSettings.addWidget(self.safeZ,7,1)
        grid_genSettings.addWidget(QLabel("Return home:"),8,0)
        grid_genSettings.addWidget(self.backHomeCheck,8,1)
        
        
        self.xFrame.setLayout(grid_Xsettings)
        yFrame.setLayout(grid_Ysettings)
        genFrame.setLayout(grid_genSettings)
        
        self.M3line = QLineEdit()
        self.M3line.setDisabled(True)
        self.M4line = QLineEdit()
        self.M4line.setDisabled(True)
        self.M5line = QLineEdit()
        self.M5line.setDisabled(True)
        
        self.totalLines = QLineEdit()
        #self.totalLines.setReadOnly(True)
        self.totalLines.setDisabled(True)
        
        self.im = QPixmap("F:/Projects/Laser/multiplicator/description.jpg")
        self.label = QLabel()
        self.label.setPixmap(self.im)
        
        
        grid_display.addWidget(QLabel("M3 command on line:"),1,0)
        grid_display.addWidget(self.M3line,1,1)
        grid_display.addWidget(QLabel("M4 command on line:"),2,0)
        grid_display.addWidget(self.M4line,2,1)
        grid_display.addWidget(QLabel("M5 command on line:"),4,0)
        grid_display.addWidget(self.M5line,4,1)
        grid_display.addWidget(QLabel("Total number of lines:"),5,0)
        grid_display.addWidget(self.totalLines,5,1)  
        
        display_vlayout.addLayout(grid_display)
        display_vlayout.addWidget(self.label)

        settings_vlayout.addWidget(self.xFrame)
        settings_vlayout.addWidget(yFrame)
        settings_vlayout.addWidget(genFrame)      
        
        main_bot_layout.addLayout(settings_vlayout)
        main_bot_layout.addLayout(display_vlayout)
        
        # MAIN
        main_vbox_layout = QVBoxLayout()
        main_vbox_layout.addLayout(main_top_layout)
        main_vbox_layout.addLayout(main_bot_layout)
        
        self.setLayout(main_vbox_layout)

        self.show()
        
    def radioXYcontrol(self):
        if self.xRadio.isChecked():
            self.xMultiplySp.setDisabled(False)
            self.xOffset.setDisabled(False)
        else:
            self.xMultiplySp.setDisabled(True)
            self.xOffset.setDisabled(True)
            
        if self.yRadio.isChecked():
            self.yMultiplySp.setDisabled(False)
            self.yOffset.setDisabled(False)
        else:
            self.yMultiplySp.setDisabled(True)
            self.yOffset.setDisabled(True)
    
    
    def read_inputs(self):
        
        if self.gCode_single != None:
            x_offset = float(self.xOffset.text()) if self.xOffset.text() != '' else 0
            x_multi = int(self.xMultiplySp.value()) if self.xMultiplySp.value() != '' else 0
            y_offset = float(self.yOffset.text()) if self.yOffset.text() != '' else 0
            y_multi = int(self.yMultiplySp.value()) if self.yMultiplySp.value() != '' else 0
            safeZ = float(self.safeZ.text()) if self.safeZ.text() != '' else 10
            goHome =  (self.backHomeCheck.isChecked()) if self.backHomeCheck.isChecked() != '' else 1
            
            print("X offset: ",x_offset)
            print("X instances: ",x_multi)
            print("y offset: ",y_offset)
            print("Y instances: ",y_multi)
            
            print("Safe Z: ",safeZ)
            print("Go Home: ",goHome)
            
            sec_begin = int(self.M4line.text()) if self.M4line.text() != '' else 0
            sec_end = int(self.M5line.text()) if self.M5line.text() != '' else 0
            
            g_zero = "G0 X0 Y0\n"
            g_G0 = "G0"
            g_92 = "G92"
            g_X = "X"
            g_Y = "Y"
            g_Z = "Z"
    
            g_safeZup = g_G0 + " " + g_Z + str(safeZ) + "\n"
            g_safeZdown = g_G0 + " " + g_Z + "-" + str(safeZ) + "\n"
    
            g_safeZero = [g_safeZup,g_zero,g_safeZdown]
            
            print(type(self.gCode_single))
            GcodeSection = self.gCode_single[sec_begin:sec_end-1]
            newGcode = self.gCode_single[0:sec_begin]

            for i in range(x_multi+1):
                for j in range(y_multi+1):
                    # G92 command for next 
                    g_setOrigin = g_92 + " " + g_X + str(x_offset) + " " + g_Y + str(y_offset) + "\n"
                    # Safe up, zero, go to next origin, safe down
                    g_safeSetOrigin = [g_safeZup,g_zero,g_setOrigin,g_safeZdown]
                    
                    if (i == 0) & (j == 0):
                        pass
                    else:
                        newGcode.extend(g_safeSetOrigin)
                        
                    newGcode.extend(GcodeSection)
                    
                    
            
            g_returnOriginalHome = g_92 + " " + g_X + str(-x_offset*x_multi) + " " + g_Y + str(-y_offset*y_multi) + "\n"
            g_safeReturnOriginalHome = [g_safeZup,g_zero,g_returnOriginalHome,g_safeZdown]
            
            if (goHome == 1):
                newGcode.extend(g_safeReturnOriginalHome)
               
            newGcode.extend(self.gCode_single[sec_end-1:])
            print(newGcode)
        
        return newGcode
        
        
    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            print(fileName)
            
        
        if fileName != None:
            self.readfromfile(fileName)
            self.loadedFile.setText(fileName)
            
    def saveFileDialog(self):
        toSave = self.read_inputs()
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()","","All Files (*);;Text Files (*.txt)", options=options)
        if fileName:
            print(fileName)
            file = open(fileName,'w')
            #text = toSave.toPlainText()
            for i in toSave:
                file.write(i)
            file.close()
       
    def saveGcodeToFile(self):
        print("saving to file")
        
        
    def readfromfile(self,name):
        f = open(name, "r")
        self.gCode_single = f.readlines()

        for i,line in enumerate(self.gCode_single):
            if (line.find("M4")) > -1:
                print("M4 found at line:",i+1)
                self.M4line.setText(str(i+1))
            if (line.find("M5")) > -1:
                print("M5 found at line:",i+1)
                self.M5line.setText(str(i+1))
        print("Total number of lines:",i+1)
        f.close() 
        self.totalLines.setText(str(i+1))
            


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(True) 
    ex = App()
    sys.exit(app.exec_())
