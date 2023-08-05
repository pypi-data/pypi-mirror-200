import cv2
import sys
import subprocess

from PyQt5.QtCore import Qt, QPoint, QRect, QTimer, QCoreApplication
from PyQt5.QtGui import QImage, QPixmap, QPainter,QColor, QPen, QKeyEvent
from PyQt5.QtWidgets import QSplitter, QHBoxLayout, QInputDialog, QApplication, QAction, QSizePolicy,QTextEdit, QFileDialog, QColorDialog, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton
import os
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = '/usr/lib/x86_64-linux-gnu/qt5/plugins/platforms/'

camera_index: int
count: int = 0
cap=record=None


class WebcamDrawingWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(2100, 1100)
        self.setAutoFillBackground(True)

        self.webcam_feed_widget = WebcamFeedWidget(self)
        self.drawing_overlay_widget = DrawingOverlayWidget(self.webcam_feed_widget, self)
        
        self.sticky_note_widget = StickyNoteWidget(" ",self)#"Double-click to edit", self)
        self.sticky_note_widget.hide()
        #self.drawing_overlay_widget = DrawingOverlayWidget(self)

        layout = QVBoxLayout()
        layout.addWidget(self.webcam_feed_widget)
        self.setLayout(layout)

        self.webcam_feed_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.drawing_overlay_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
     
    def resizeEvent(self, event):
        self.drawing_overlay_widget.move(self.webcam_feed_widget.pos())
        self.drawing_overlay_widget.resize(self.webcam_feed_widget.size())

    def mousePressEvent(self, event):
        self.drawing_overlay_widget.mousePressEvent(event)

    def mouseMoveEvent(self, event):
        self.drawing_overlay_widget.mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self.drawing_overlay_widget.mouseReleaseEvent(event)

class WebcamFeedWidget(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
       # global camera_index
        #camera_index=0
        global record
        self._current_image = None
        self._capture = None
        self.qimg = QImage()##
        self._recording = False
        self._video_writer = None
        self.zoom_level = 0
        self.rotation_angle = 0
        self.output_filename = None
        # self.stop_event = Event()
  
    def stop_recording(self):
        global record
        if record is not None:
            record.release()
            record = None
        self.start()
    
    def zoom_in(self):
        self.zoom_level += 2

    def zoom_out(self):
        self.zoom_level -= 2

    def rotate(self):
        self.rotation_angle += 90
        if self.rotation_angle >= 360:
            self.rotation_angle = 0

    def changeCam(self):
        cameras=None
        cameras = MainWindow.get_available_cameras(self)
        if not cameras:
            raise Exception("No USB cameras found.")

        camera, ok = QInputDialog.getItem(self, "Select camera", "Select a USB camera to use:", cameras, 0, False)
        if not ok:
            sys.exit(0)

        global camera_index
        camera_index = int(camera[-1])
        cap = cv2.VideoCapture(camera_index)
 
    #try to get a frame, if it returns nothing
        success, frame = cap.read()
        if not success:
            camera_index=0
            
            cap.release()
            del(cap)
            print("Webcam feed is not available")
        #     self.changeCam()
        # else:
        del(cameras)
        cap.release()
        self.start()
    
    def start(self):
        global camera_index
        # del(self._capture)
        self._capture = cv2.VideoCapture(camera_index)
        self._capture.set(cv2.CAP_PROP_AUTOFOCUS, 1)  # Enable autofocus

        self._capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self._capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        self.timer = QTimer(self)
        self.timer.start(int(1000/30))
        self.timer.timeout.connect(self.update_frame)
          # 30 fps

        # self.timer = QTimer(self)
        # self.timer.timeout.connect(self.update_frame)
        # self.timer.start(16)    

    def update_frame(self):
            global record    
            ret, frame = self._capture.read()
            
            if ret:
                # Apply the zoom level to the frame
                scale = 1 + self.zoom_level / 10
                resized = cv2.resize(frame, None, fx=scale, fy=scale)

                # Apply the rotation angle to the frame
                rows, cols, ch = resized.shape
                center = (cols / 2, rows / 2)
                rotation_matrix = cv2.getRotationMatrix2D(center, self.rotation_angle, 1)
                rotated = cv2.warpAffine(resized, rotation_matrix, (cols, rows))

                resized_frame = cv2.resize(rotated, (2100, 1100)) #frame, (2100, 1100)) -> before zoom and rotation frame is used
                self._current_image = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)
                height, width, _ = self._current_image.shape
                bytes_per_line = width * 3
                qimg = QImage(self._current_image.data, width, height, bytes_per_line, QImage.Format_RGB888)
                pixmap = QPixmap.fromImage(qimg)
                self.setPixmap(pixmap)
                if record is not None:                  
                  record.write(frame)
               
                # Write the frame to the video file
                    

    def stop(self):
        # self.stop_event.set()
        # self.process.join()
        if self._capture is not None:
            self._capture.release()
            self._capture = None

    def get_image(self):
        return self._current_image

class StickyNoteWidget(QTextEdit):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setFixedSize(100, 100)
        self.setAutoFillBackground(True)
        self.setStyleSheet("background-color: yellow; border: 1px solid black;")
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.resizing = False
        self.resize_threshold = 10

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.offset = event.pos()
            if self.rect().bottomRight().x() - self.resize_threshold < event.pos().x() < self.rect().bottomRight().x() + self.resize_threshold and \
                self.rect().bottomRight().y() - self.resize_threshold < event.pos().y() < self.rect().bottomRight().y() + self.resize_threshold:
                self.resizing = True

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            if self.resizing:
                new_width = max(event.pos().x(), 50)
                new_height = max(event.pos().y(), 50)
                self.setFixedSize(new_width, new_height)
            else:
                self.move(self.mapToParent(event.pos() - self.offset))

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.resizing = False

class DrawingOverlayWidget(QWidget):
    def __init__(self, webcam_widget,parent=None):
        super().__init__(parent)   
        self._webcam_widget = webcam_widget  
        self._drawing_pixmap = None
        self.setFixedSize(2100,1100)
        self.drawing = False
        self.points = []
        self.pen_color = QColor(255, 0, 0)
        self.eraser_mode = False
        self.eraser_size = 30
        self.image = QImage(self.size(), QImage.Format_ARGB32)
        self.image.fill(Qt.transparent)

    def paintEvent(self, event):
        try:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing)
            # Draw webcam image for the eraser
            #webcam_image = self.parent().webcam_feed_widget.get_image()
            webcam_image = self._webcam_widget._current_image
            if webcam_image is not None:
                webcam_qimage = QImage(webcam_image.data, webcam_image.shape[1], webcam_image.shape[0], QImage.Format_RGB888)
                painter.drawImage(QRect(0, 0, self.width(), self.height()), webcam_qimage)
            # Draw on the transparent image
            for i in range(len(self.points) - 1):
                if self.points[i] is None or self.points[i + 1] is None:
                    continue
                pen = QPen(self.points[i].color, self.points[i].size, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
                image_painter = QPainter(self.image)
                image_painter.setRenderHint(QPainter.Antialiasing)
                image_painter.setPen(pen)

                if self.points[i].color.alpha() == 0:
                    image_painter.setCompositionMode(QPainter.CompositionMode_Clear)
                else:
                    image_painter.setCompositionMode(QPainter.CompositionMode_SourceOver)

                image_painter.drawLine(self.points[i].point, self.points[i + 1].point)
                image_painter.end()

            # Draw the transparent image with drawings on top of the webcam image
            painter.drawImage(QRect(0, 0, self.width(), self.height()), self.image)    
        
        except Exception as e:
            print("Exception in paintEvent:", e)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = True
            if not self.eraser_mode:
                self.points.append(PointColor(event.pos(), self.pen_color, 3))
            else:
                self.points.append(PointColor(event.pos(), self.pen_color, self.eraser_size))                    

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton and self.drawing:
            if not self.eraser_mode:
                self.points.append(PointColor(event.pos(), self.pen_color, 3))
            else:
                self.points.append(PointColor(event.pos(), self.pen_color, self.eraser_size))
            self.update()
            
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = False
            self.points.append(None)

    def set_pen_color(self, color):
        self.pen_color = color
        self.eraser_mode = False

    def set_eraser_mode(self, enabled=True):
        self.eraser_mode = enabled
        if enabled:
            self.pen_color = QColor(0, 0, 0, 0)
        else:
            self.pen_color = QColor(255, 0, 0)
            # self.pen_color = QColor(255, 255, 255)

    def set_eraser_size(self, size):
        self.eraser_size = size

class PointColor:
    def __init__(self, point, color, size):
        self.point = point
        self.color = color
        self.size = size

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        cameras = self.get_available_cameras()
        if not cameras:
            raise Exception("No USB cameras found.")

        camera, ok = QInputDialog.getItem(self, "Select camera", "Select a USB camera to use:", cameras, 0, False)
        if not ok:
            sys.exit(0)

        global camera_index
        camera_index = int(camera[-1])

        central_widget = QWidget(self)
        layout = QVBoxLayout(central_widget)
        
        self.webcam_feed_widget = WebcamFeedWidget(self)
        self.webcam_feed_widget.start()
        layout.addWidget(self.webcam_feed_widget)

        self.webcam_drawing_widget = DrawingOverlayWidget(self.webcam_feed_widget, self.webcam_feed_widget)
        self.webcam_drawing_widget.setGeometry(0, 0, self.webcam_feed_widget.width(), self.webcam_feed_widget.height())


        # self.initUI()
        self.setWindowTitle("Webcam Drawing")
        self.setWindowState(Qt.WindowFullScreen)
      
        self.setCentralWidget(central_widget)

        self.output_filename = None

        # Create a variable to hold the video writer object
        self.video_writer = None
        self.initUI()
    def initUI(self):
        # self.webcam_drawing_widget = WebcamDrawingWidget(self)
        # self.sticky_note_button = QPushButton("Add Sticky Note", self)
        # self.sticky_note_button.clicked.connect(self.add_sticky_note)
        # self.color_picker_button = QPushButton("Change Pen Color", self)
        # self.color_picker_button.clicked.connect(self.change_pen_color)
        # self.eraser_button = QPushButton("Eraser", self)
        # self.eraser_button.clicked.connect(self.toggle_eraser)
        # self.capture_button = QPushButton("Capture", self)
        # self.capture_button.clicked.connect(self.capture_image)
        # self.record_button = QPushButton("Record", self)
        # self.record_button.clicked.connect(self.toggle_recording)
        # self.rotate_button = QPushButton("Rotate", self)
        # self.rotate_button.clicked.connect(self.webcam_feed_widget.rotate)        
        # self.cam_change_button = QPushButton("Change Cam", self)
        # self.cam_change_button.clicked.connect(self.webcam_feed_widget.changeCam)      
        # self.Window_Close_button = QPushButton("Exit Window", self)
        # self.Window_Close_button.clicked.connect(self.Window_Close)

        # # Create a horizontal layout for the buttons
        # button_layout = QHBoxLayout()
        # button_layout.addWidget(self.sticky_note_button)
        # button_layout.addWidget(self.color_picker_button)
        # button_layout.addWidget(self.eraser_button)
        # button_layout.addWidget(self.capture_button)
        # button_layout.addWidget(self.record_button)
        # button_layout.addWidget(self.rotate_button)
        # button_layout.addWidget(self.cam_change_button)
        # button_layout.addWidget(self.Window_Close_button)

        # # Create a layout for the webcam feed and drawing widgets
        # webcam_layout = QVBoxLayout()
        # webcam_layout.addWidget(self.webcam_feed_widget)
        # webcam_layout.addWidget(self.webcam_drawing_widget)

        # # Create a vertical layout for the main content
        # main_layout = QVBoxLayout()
        # main_layout.addLayout(webcam_layout)
        # main_layout.addLayout(button_layout)

        # # Set the main layout as the central widget
        # central_widget = QWidget()
        # central_widget.setLayout(main_layout)
        # self.setCentralWidget(central_widget)
        # self.webcam_drawing_widget = WebcamDrawingWidget(self)
        self.sticky_note_button = QPushButton("Add Sticky Note", self)
        self.sticky_note_button.clicked.connect(self.add_sticky_note)
        self.sticky_note_button.setGeometry(QRect(10, 10, 120, 30))

        self.color_picker_button = QPushButton("Change Pen Color", self)
        self.color_picker_button.clicked.connect(self.change_pen_color)
        self.color_picker_button.setGeometry(QRect(150, 10, 120, 30))

        self.eraser_button = QPushButton("Eraser", self)
        self.eraser_button.clicked.connect(self.toggle_eraser)
        self.eraser_button.setGeometry(QRect(290, 10, 120, 30))

        capture_button = QPushButton("Capture", self)
        capture_button.setGeometry(QRect(430, 10, 120, 30))
        capture_button.clicked.connect(self.capture_image)

        self.record_button = QPushButton("Record", self)
        self.record_button.setGeometry(QRect(570, 10, 120, 30))
        self.record_button.clicked.connect(self.toggle_recording)

        self.rotate_button = QPushButton("Rotate", self)
        self.rotate_button.setGeometry(QRect(710, 10, 120, 30))
        self.rotate_button.clicked.connect(self.webcam_feed_widget.rotate)
        
        self.cam_change_button = QPushButton("Change Cam", self)
        self.cam_change_button.setGeometry(QRect(850, 10, 120, 30))
        self.cam_change_button.clicked.connect(self.webcam_feed_widget.changeCam)
        # self.stop_button = QPushButton("Stop Recording", self)
        # self.stop_button.setGeometry(QRect(980, 10, 120, 30))
        # self.stop_button.clicked.connect(self.webcam_feed_widget.stop_recording)
        # self.record_button.clicked.connect(self.toggle_recording)

        self.Window_Close_button = QPushButton("Exit Window", self)
        self.Window_Close_button.setGeometry(QRect(990, 10, 120, 30))
        self.Window_Close_button.clicked.connect(self.Window_Close)

    def get_available_cameras(self):
        devices = []
        for i in range(10):  # Increase this range if you expect more than 10 cameras
            cap = cv2.VideoCapture(i, cv2.CAP_ANY)
            if cap.isOpened():
                devices.append(f'/dev/video{i}')
                cap.release()
        return devices
        # output = subprocess.check_output("v4l2-ctl --list-devices", shell=True).decode("utf-8")
        # devices = [line.split(':')[0] for line in output.split('\n') if '/dev/video' in line]
        # return devices   

    def Window_Close(self):
        # quit_action = QAction('Quit', self)
        # quit_action.triggered.connect(QCoreApplication.quit)
        quit()
        # cv2.destroyAllWindows()

    def toggle_recording(self):
        global camera_index
        global record
        if self.output_filename is None:
            ret, frame = self.webcam_feed_widget._capture.read() 
            # print(ret)
            # capture  = cv2.VideoCapture(camera_index)            
            self.output_filename, _ = QFileDialog.getSaveFileName(self, 'Save Video', '', 'Video Files (*.avi *.mp4)')
            if self.output_filename:
                # fps = int(round(capture.get(cv2.CAP_PROP_FPS)))
                # width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
                # height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
                fourcc = cv2.VideoWriter_fourcc(*'mp4v')                
                # record = cv2.VideoWriter(self.output_filename, fourcc, 30.0, (width, height))
                record = cv2.VideoWriter(self.output_filename, fourcc, 20, (640,480))#(width, height))
                self.record_button.setStyleSheet("background-color: red")                        
                self.record_button.setText('Stop Recording')                    
        else:
            if record is not None:
                record.release()
                record = None
            self.video_writer = None
            self.webcam_feed_widget.stop_recording()            
            self.output_filename = None
            self.record_button.setStyleSheet("")                  
            self.record_button.setText('Record')
            
                

    def closeEvent(self, event):
        # Release the video writer object if it is still open
        if self.video_writer is not None:
             self.video_writer.release()
        event.accept()
                
    def capture_image(self):
        global camera_index
        webcam_image = self.webcam_feed_widget._current_image
        cap = cv2.VideoCapture(camera_index)
        ret, frame = cap.read()
        if ret:
            print("ret working")
        if webcam_image is None:
            print("Failed to capture image. Webcam feed is not available.")
            return
        self.output_filename, _ = QFileDialog.getSaveFileName(self, 'Save Image', '', 'Image Files (*.jpg *.jpeg *.png)')
        if self.output_filename:
            qimg = QImage(webcam_image.data, webcam_image.shape[1], webcam_image.shape[0], QImage.Format_RGB888)
            drawing_image = self.webcam_drawing_widget.drawing_overlay_widget.image
            sticky_note_image = self.webcam_drawing_widget.sticky_note_widget.grab().toImage()
            # self.sticky_note = StickyNoteWidget(self)
            # sticky_note_image_origin = self.sticky_note 
            
            if not qimg.isNull() and not drawing_image.isNull():
                combined_image = QImage(qimg.size(), QImage.Format_ARGB32)
                combined_image.fill(Qt.transparent)
                painter = QPainter(combined_image)
                painter.drawImage(0, 0, qimg)
                painter.drawImage(0, 0, drawing_image)
                # if sticky_note_image_origin.toPlainText() != '':
               
                # for sticky_note in self.sticky_note:
                #     sticky_note_image_origin = sticky_note.get_image_origin()
                #     if not sticky_note.isHidden():
                #         if not sticky_note_image_origin.isNull():
                #             painter.drawImage(sticky_note_image_origin.rect(), sticky_note_image_origin.toImage())
                #         else:
                #             sticky_note_image_origin.render(QPixmap(sticky_note_image_origin.size()).toImage())


                # if not sticky_note_image.isNull() and sticky_note_image.text().__str__() != "":
                #     painter.drawImage(self.webcam_drawing_widget.sticky_note_widget.pos(), sticky_note_image)
                painter.end()
                combined_image.save(self.output_filename)
                print("Image captured and saved as '{0}'".format(self.output_filename))
            else:
                print("Failed to capture image. Drawing overlay is not available.")

        # webcam_image = self.webcam_feed_widget._current_image
        # if webcam_image is None:
        #     print("Failed to capture image. Webcam feed is not available.")
        #     return
        # self.output_filename, _ = QFileDialog.getSaveFileName(self, 'Save Image', '', 'Image Files (*.jpg *.jpeg *.png)')
        # if self.output_filename:
        #     qimg = QImage(webcam_image.data, webcam_image.shape[1], webcam_image.shape[0], QImage.Format_RGB888)
        #     drawing_image = self.webcam_drawing_widget.drawing_overlay_widget.image
        #     sticky_note_image = self.webcam_drawing_widget.sticky_note_widget.grab().toImage()

        #     if not qimg.isNull() and not drawing_image.isNull():
                
        #         combined_image = QImage(qimg.size(), QImage.Format_ARGB32)
        #         combined_image.fill(Qt.transparent)

        #         painter = QPainter(combined_image)
        #         painter.drawImage(0, 0, qimg)
        #         painter.drawImage(0, 0, drawing_image)
        #         if sticky_note_image.text.__str__ !="":
        #             painter.drawImage(0, 0, sticky_note_image)
        #         painter.end()
        #         combined_image.save(self.output_filename)
        #         print("Image captured and saved as 'captured_image.png'")

        #     else:
        #         print("Failed to capture image. Drawing overlay is not available.")

    def add_sticky_note(self):
        sticky_note = StickyNoteWidget("Double-click to edit", self)
        sticky_note.show()
        sticky_note.move(QPoint(50, 50))

    def change_pen_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.webcam_drawing_widget.drawing_overlay_widget.set_pen_color(color)

    def toggle_eraser(self):
        if not self.webcam_drawing_widget.drawing_overlay_widget.eraser_mode:
            self.webcam_drawing_widget.drawing_overlay_widget.set_eraser_mode()
            self.eraser_button.setStyleSheet("background-color: red")
        else:
            self.webcam_drawing_widget.drawing_overlay_widget.set_eraser_mode(False)
            self.eraser_button.setStyleSheet("")        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec_())
