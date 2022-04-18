# ! /usr/bin/python3
from sys import exit as sysExit
import sys

from sympy import randprime
from random import randint
from hashlib import sha1

from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QStackedWidget, QFileDialog, QDialog
from PyQt5.QtCore import QTimer

# Generate Screen
class GenerateScreen(QtWidgets.QMainWindow):
    def __init__(self):
        super(GenerateScreen, self).__init__()
        loadUi(".\generate.ui", self)
    
        self.menu_1.setChecked(True)
        self.menu_2.clicked.connect(self.goToSign)
        self.menu_3.clicked.connect(self.goToVerify)
        
        self.generate_key.clicked.connect(self.generateKey)
        self.save_public.clicked.connect(self.savePublicKey)
        self.save_private.clicked.connect(self.savePrivateKey)
        
        self.save_public.setDisabled(True)
        self.save_private.setDisabled(True)
    
    def goToSign(self):
        signscreen = SignScreen()
        widget.addWidget(signscreen)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def goToVerify(self):
        verifyscreen = VerifyScreen()
        widget.addWidget(verifyscreen)
        widget.setCurrentIndex(widget.currentIndex()+1)
    
    def fpb(self, a, b):
        if(b == 0):
            return a
        else:
            return self.fpb(b, a % b)
    
    def setBlankAlert(self):
        self.alert.setText("")
            
    def generateKey(self):
        self.p = randprime(2**9, 2**10)
        self.display_p.setText(str(self.p))
        self.q = randprime(2**9, 2**10)
        self.display_q.setText(str(self.q))
        self.n = self.p * self.q
        self.display_n.setText(str(self.n))
        self.totient = (self.p-1) * (self.q-1)
        self.e = randint(3,2**16+1)
        while(self.fpb(self.totient, self.e) != 1):
            self.e = randint(3, 2**16+1)
        self.display_public.setText(str(self.e))
        k = 1
        self.d = 0.1
        while(self.d%1 != 0):
            self.d = (1 + k * self.totient)/self.e
            k += 1
        self.d = int(self.d)
        self.display_private.setText(str(self.d))

        self.save_public.setDisabled(False)
        self.save_private.setDisabled(False)

    def savePublicKey(self):
        name = QFileDialog.getSaveFileName(self, 'Save Public Key')
        file = open(name[0],'w')
        file.write(str(self.e) + "," + str(self.n))
        file.close()
        
        self.alert.setText("Public key saved successfully")

        timer = QTimer(self)
        timer.setSingleShot(True)
        timer.timeout.connect(self.setBlankAlert)
        timer.start(3000)

    def savePrivateKey(self):
        name = QFileDialog.getSaveFileName(self, 'Save Private Key')
        file = open(name[0],'w')
        file.write(str(self.d) + "," + str(self.n))
        file.close()

        self.alert.setText("Private key saved successfully")

        timer = QTimer(self)
        timer.setSingleShot(True)
        timer.timeout.connect(self.setBlankAlert)
        timer.start(3000)

# Sign Screen
class SignScreen(QtWidgets.QMainWindow):
    def __init__(self):
        super(SignScreen, self).__init__()
        loadUi("sign.ui", self)
    
        self.menu_2.setChecked(True)
        self.menu_1.clicked.connect(self.goToGenerate)
        self.menu_3.clicked.connect(self.goToVerify)
        
        self.browse_message.clicked.connect(self.browseMessage)
        self.browse_private.clicked.connect(self.browsePrivateKey)
        self.sign_message.clicked.connect(self.signMessage)
        
        self.method_1.setChecked(True)
        self.sign_message.setDisabled(True)
        self.is_message_browsed = False
        self.is_private_key_browsed = False

    def goToGenerate(self):
        generatescreen = GenerateScreen()
        widget.addWidget(generatescreen)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def goToVerify(self):
        verifyscreen = VerifyScreen()
        widget.addWidget(verifyscreen)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def browseMessage(self):
        name = QFileDialog.getOpenFileName(self, 'Open Message')
        file = open(name[0],'r')
        self.message = file.read()
        self.message_name = name[0]
        file.close()
        
        self.is_message_browsed = True
        self.display_message.setText(self.message)

        if (self.is_private_key_browsed):
            self.sign_message.setDisabled(False)
    
    def browsePrivateKey(self):
        name = QFileDialog.getOpenFileName(self, 'Open Private Key')
        file = open(name[0],'r')
        file_pkey = file.read()
        self.private_key = int(file_pkey.split(",")[0])
        self.private_n = int(file_pkey.split(",")[1])
        file.close()

        self.is_private_key_browsed = True
        self.display_private.setText(str(self.private_key))

        if (self.is_message_browsed):
            self.sign_message.setDisabled(False)
    
    def DecToHex(self, x):
        i = 0
        while ((x // 16**i) != 0):
            i += 1
            
        ArrSize = i
        temp1 = x
        temp2 = x
        Arr = [" " for i in range(ArrSize)]
        
        for i in range(ArrSize-1,-1,-1):
            temp1 = temp1 // 16
            sisa = temp2 % 16
            temp2 = temp1
            if (sisa == 0):
                Arr[i] = "0"
            elif (sisa == 1):
                Arr[i] = "1"
            elif (sisa == 2):
                Arr[i] = "2"
            elif (sisa == 3):
                Arr[i] = "3"
            elif (sisa == 4):
                Arr[i] = "4"
            elif (sisa == 5):
                Arr[i] = "5"
            elif (sisa == 6):
                Arr[i] = "6"
            elif (sisa == 7):
                Arr[i] = "7"
            elif (sisa == 8):
                Arr[i] = "8"
            elif (sisa == 9):
                Arr[i] = "9"
            elif (sisa == 10):
                Arr[i] = 'a'
            elif (sisa == 11):
                Arr[i] = 'b'
            elif (sisa == 12):
                Arr[i] = 'c'
            elif (sisa == 13):
                Arr[i] = 'd'
            elif (sisa == 14):
                Arr[i] = 'e'
            elif (sisa == 15):
                Arr[i] = 'f'

        return "".join(Arr)

    def HexToDec(self, x):
        sum = 0
        for i in range(len(x)):
            if (x[i] == '0'):
                sum = sum + (0 * (16**(len(x)-1-i)))
            elif (x[i] == '1'):
                sum = sum + (1 * (16**(len(x)-1-i)))
            elif (x[i] == '2'):
                sum = sum + (2 * (16**(len(x)-1-i)))
            elif (x[i] == '3'):
                sum = sum + (3 * (16**(len(x)-1-i)))
            elif (x[i] == '4'):
                sum = sum + (4 * (16**(len(x)-1-i)))
            elif (x[i] == '5'):
                sum = sum + (5 * (16**(len(x)-1-i)))
            elif (x[i] == '6'):
                sum = sum + (6 * (16**(len(x)-1-i)))
            elif (x[i] == '7'):
                sum = sum + (7 * (16**(len(x)-1-i)))
            elif (x[i] == '8'):
                sum = sum + (8 * (16**(len(x)-1-i)))
            elif (x[i] == '9'):
                sum = sum + (9 * (16**(len(x)-1-i)))
            elif (x[i] == 'A') or (x[i] == 'a'):
                sum = sum + (10 * (16**(len(x)-1-i)))
            elif (x[i] == 'B') or (x[i] == 'b'):
                sum = sum + (11 * (16**(len(x)-1-i)))
            elif (x[i] == 'C') or (x[i] == 'c'):
                sum = sum + (12 * (16**(len(x)-1-i)))
            elif (x[i] == 'D') or (x[i] == 'd'):
                sum = sum + (13 * (16**(len(x)-1-i)))
            elif (x[i] == 'E') or (x[i] == 'e'):
                sum = sum + (14 * (16**(len(x)-1-i)))
            elif (x[i] == 'F') or (x[i] == 'f'):
                sum = sum + (15 * (16**(len(x)-1-i)))
        
        return (sum)
    
    def setBlankAlert(self):
        self.alert.setText("")

    def signMessage(self):
        self.alert.setText("Signing Message..")

        # Menghitung hash dari pesan awal
        hash = sha1(self.message.encode('utf-8'))
        digest = hash.hexdigest()

        # Menghitung sign dari hash
        s = self.HexToDec(digest)**self.private_key % self.private_n
        s_hex = self.DecToHex(s)
        
        if(self.method_1.isChecked()):
            name = QFileDialog.getSaveFileName(self, 'Save Signature')
            file = open(name[0],'w')
            text = str(s_hex)
        else:
            file = open(self.message_name, "a")
            text = "\n<ds>" + str(s_hex) + "</ds>"
        file.write(text)
        file.close()

        self.alert.setText("Message signed successfully")

        timer = QTimer(self)
        timer.setSingleShot(True)
        timer.timeout.connect(self.setBlankAlert)
        timer.start(3000)

# Verify Screen
class VerifyScreen(QtWidgets.QMainWindow):
    def __init__(self):
        super(VerifyScreen, self).__init__()
        loadUi("verify.ui", self)
    
        self.menu_3.setChecked(True)
        self.menu_1.clicked.connect(self.goToGenerate)
        self.menu_2.clicked.connect(self.goToSign)

        self.browse_message.clicked.connect(self.browseMessage)
        self.browse_public.clicked.connect(self.browsePublicKey)
        self.browse_sign.clicked.connect(self.browseSign)
        self.verify_sign.clicked.connect(self.verifySign)

        self.location_1.clicked.connect(self.changeLocation)
        self.location_2.clicked.connect(self.changeLocation)
        
        self.location_1.setChecked(True)
        self.verify_sign.setDisabled(True)

        self.is_message_browsed = False
        self.is_public_key_browsed = False
        self.is_sign_browsed = False

    def changeLocation(self):
        if(self.location_1.isChecked()):
            self.browse_sign.setDisabled(False)
            if (self.is_public_key_browsed and self.is_message_browsed and self.is_sign_browsed):
                self.verify_sign.setDisabled(False)
            else:
                self.verify_sign.setDisabled(True)
        else:
            self.browse_sign.setDisabled(True)
            if (self.is_public_key_browsed and self.is_message_browsed):
                self.verify_sign.setDisabled(False)
            else:
                self.verify_sign.setDisabled(True)
        
    def goToGenerate(self):
        generatescreen = GenerateScreen()
        widget.addWidget(generatescreen)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def goToSign(self):
        signscreen = SignScreen()
        widget.addWidget(signscreen)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def browseMessage(self):
        name = QFileDialog.getOpenFileName(self, 'Open Message')
        file = open(name[0],'r')
        self.message = file.read()
        file.close()
        
        self.is_message_browsed = True
        self.display_message.setText(self.message)

        if(self.location_1.isChecked()):
            if (self.is_public_key_browsed and self.is_sign_browsed):
                self.verify_sign.setDisabled(False)
        else:
            if (self.is_public_key_browsed):
                self.verify_sign.setDisabled(False)

    def browsePublicKey(self):
        name = QFileDialog.getOpenFileName(self, 'Open Public Key')
        file = open(name[0],'r')
        file_pkey = file.read()
        self.public_key = int(file_pkey.split(",")[0])
        self.public_n = int(file_pkey.split(",")[1])
        file.close()

        self.is_public_key_browsed = True
        self.display_public.setText(str(self.public_key))

        if(self.location_1.isChecked()):
            if (self.is_message_browsed and self.is_sign_browsed):
                self.verify_sign.setDisabled(False)
        else:
            if (self.is_message_browsed):
                self.verify_sign.setDisabled(False)
    
    def browseSign(self):
        name = QFileDialog.getOpenFileName(self, 'Open Signature')
        file = open(name[0],'r')
        self.sign = file.read()
        file.close()

        self.is_sign_browsed = True
        if (self.is_public_key_browsed and self.is_message_browsed):
            self.verify_sign.setDisabled(False)
    
    def HexToDec(self, x):
        sum = 0
        for i in range(len(x)):
            if (x[i] == '0'):
                sum = sum + (0 * (16**(len(x)-1-i)))
            elif (x[i] == '1'):
                sum = sum + (1 * (16**(len(x)-1-i)))
            elif (x[i] == '2'):
                sum = sum + (2 * (16**(len(x)-1-i)))
            elif (x[i] == '3'):
                sum = sum + (3 * (16**(len(x)-1-i)))
            elif (x[i] == '4'):
                sum = sum + (4 * (16**(len(x)-1-i)))
            elif (x[i] == '5'):
                sum = sum + (5 * (16**(len(x)-1-i)))
            elif (x[i] == '6'):
                sum = sum + (6 * (16**(len(x)-1-i)))
            elif (x[i] == '7'):
                sum = sum + (7 * (16**(len(x)-1-i)))
            elif (x[i] == '8'):
                sum = sum + (8 * (16**(len(x)-1-i)))
            elif (x[i] == '9'):
                sum = sum + (9 * (16**(len(x)-1-i)))
            elif (x[i] == 'A') or (x[i] == 'a'):
                sum = sum + (10 * (16**(len(x)-1-i)))
            elif (x[i] == 'B') or (x[i] == 'b'):
                sum = sum + (11 * (16**(len(x)-1-i)))
            elif (x[i] == 'C') or (x[i] == 'c'):
                sum = sum + (12 * (16**(len(x)-1-i)))
            elif (x[i] == 'D') or (x[i] == 'd'):
                sum = sum + (13 * (16**(len(x)-1-i)))
            elif (x[i] == 'E') or (x[i] == 'e'):
                sum = sum + (14 * (16**(len(x)-1-i)))
            elif (x[i] == 'F') or (x[i] == 'f'):
                sum = sum + (15 * (16**(len(x)-1-i)))
        
        return (sum)

    def setBlankAlert(self):
        self.alert.setText("")

    def verifySign(self):
        if(self.location_2.isChecked()):
            arr_message = self.message.split("\n<ds>")
            if (len(arr_message) == 1):
                self.alert.setText("No signature detected")
            else:
                self.message = arr_message[0]
                self.sign = arr_message[1].split("</ds>")[0]
         
        hash_message = self.HexToDec(sha1(self.message.encode('utf-8')).hexdigest()) % self.public_n
        hash_sign = self.HexToDec(self.sign)**self.public_key % self.public_n

        if(hash_sign == 0):
            self.alert.setText("No signature detected")
        else:
            if hash_message == hash_sign:
                self.alert.setText("Signature Valid")
            else:
                self.alert.setText("Signature Invalid")
        
        timer = QTimer(self)
        timer.setSingleShot(True)
        timer.timeout.connect(self.setBlankAlert)
        timer.start(3000)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName("Digital Signature RSA-SHA1")

    main = GenerateScreen()
    
    widget = QStackedWidget()
    widget.addWidget(main)
    widget.setMinimumHeight(500)
    widget.setMinimumWidth(480)

    widget.show()
    
    sys.exit(app.exec_())