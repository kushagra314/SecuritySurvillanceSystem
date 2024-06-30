import sys
import cv2
from AnamolyDetect import Prg
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QApplication, QLabel, QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QLineEdit, QLabel
from twilio.rest import Client
import os
from dotenv import load_dotenv

load_dotenv()

detect = Prg()

account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')

RESOLUTION=(800, 600)

class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Security Surviellance System")
        self.setGeometry(100, 100, 800, 600)
        self.msgnotsent = True

        # Create a central widget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Create a QVBoxLayout for the central widget
        main_layout = QVBoxLayout(central_widget)

        label=QLabel("Enter Phone Number: ")
        self.line_edit=QLineEdit()
        self.line_edit.setMaxLength(13)
        self.line_edit.setPlaceholderText("Phone Number")
        self.line_edit.returnPressed.connect(self.phno_entered)
        submit_button=QPushButton("Submit")
        submit_button.clicked.connect(self.phno_entered)

        h_layout = QHBoxLayout()
        h_layout.addWidget(label)
        h_layout.addWidget(self.line_edit)
        h_layout.addWidget(submit_button)

        # Create a QHBoxLayout for the buttons
        button_layout = QHBoxLayout()

        # Create and add buttons to the button_layout

        button_cam1=QPushButton("Camera 1")
        button_cam1.clicked.connect(self.cam1)

        button_cam2=QPushButton("Camera 2")
        button_cam2.clicked.connect(self.cam2)

        button_layout.addWidget(button_cam1)
        button_layout.addWidget(button_cam2)

        # Create a QLabel to display the webcam feed
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)

        # Add the button layout and label to the main layout
        main_layout.addLayout(button_layout)
        main_layout.addLayout(h_layout)
        main_layout.addWidget(self.label)
        
        # Initialize the webcam
        self.cap = cv2.VideoCapture(0)

        # Set up a timer to update the frame regularly
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(60)  # Update every 30 ms

    def cam1(self): self.cap = cv2.VideoCapture(0)
    def cam2(self): self.cap = cv2.VideoCapture(1)

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            frame=cv2.resize(frame, RESOLUTION)
            frame, count, weapon_present = detect.CountHeadDetectWeapon(frame)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            if self.msgnotsent and (count > 15 or weapon_present): 
                self.SendMessage()
                self.msgnotsent = False
            # Convert the frame to QImage
            h, w, ch = frame.shape
            bytes_per_line = ch * w
            qimg = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)

            # Set the QImage to the QLabel
            self.label.setPixmap(QPixmap.fromImage(qimg))

    def closeEvent(self, event):
        # Release the webcam when closing the window
        self.cap.release()
        super().closeEvent(event)

    def phno_entered(self):
        self.phno = self.line_edit.text()
    
    def SendMessage(self):
        client = Client(account_sid, auth_token)
        message = client.messages.create(
        from_='+12088587843',
        body='Alert! Something is wrong in the monitored area.',
        to=self.phno
        )
        print(message.sid)
       
if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = Window()
    window.show()

    sys.exit(app.exec())
