from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMainWindow, QMessageBox
import os
import filters
from PIL import ImageQt


class SimpleImageEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.sourceImage = None # There is no source image initially
        self.targetImage = None # There is no target image initially
        self.lastTargetImage = None # There is no last target image initially
        self.lastSourceImage = None # There is no last source image initially
        self.setGeometry(0, 0, 1366, 768) #xpos, ypos, width, height
        self.centerWindow()
        self.setWindowTitle('Simple Image Editor') # Name the title of window
        self.setStyleSheet("background-color: rgb(210, 210, 210);") # Change the background color of the
        self.setupUi()
      

    def centerWindow (self):
        """
        This method centers the window on the screen.
        """
        resolution = QtWidgets.QDesktopWidget().screenGeometry()
        self.move((resolution.width() // 2) - (self.frameSize().width() // 2),
                (resolution.height() // 2) - (self.frameSize().height() // 2))

    def setupUi(self):
        
        self.centralWidget = QtWidgets.QWidget(self)
        self.centralWidget.setObjectName("centralWidget")

        # Setup source image label
        self.sourceImageBox = QtWidgets.QLabel(self.centralWidget)
        self.sourceImageBox.setGeometry(QtCore.QRect(0, 0, 550, 620))
        self.sourceImageBox.move(50, 74)
        self.sourceImageBox.setObjectName("sourceImageLabel")
        self.sourceImageBox.setStyleSheet("background-color: rgb(64, 64, 64);")

        # Setup source target label
        self.targetImageBox = QtWidgets.QLabel(self.centralWidget)
        self.targetImageBox.setGeometry(QtCore.QRect(0, 0, 550, 620))
        self.targetImageBox.move(766, 74)
        self.targetImageBox.setObjectName("targetImageLabel")
        self.targetImageBox.setStyleSheet("background-color: rgb(64, 64, 64);")
        self.targetImageBox.setAlignment(QtCore.Qt.AlignCenter)

        # Setup source image label
        self.sourceImageLabel = QtWidgets.QLabel(self.centralWidget)
        self.sourceImageLabel.setGeometry(QtCore.QRect(0, 0, 550, 620))
        self.sourceImageLabel.move(50, 74)
        self.sourceImageLabel.setObjectName("sourceImageLabel")
        self.sourceImageLabel.setStyleSheet("background-color: rgb(64, 64, 64);")
        self.sourcePixmap = None
        self.sourceImageLabel.setAlignment(QtCore.Qt.AlignCenter)

        # Setup source target label
        self.targetImageLabel = CroppedImageLabel(self.centralWidget)
        self.targetImageLabel.setGeometry(QtCore.QRect(0, 0, 550, 620))
        self.targetImageLabel.move(766, 74)
        self.targetImageLabel.setObjectName("targetImageLabel")
        self.targetImagePixmap = None
        self.targetImageLabel.setStyleSheet("background-color: rgb(64, 64, 64);")
        self.setCentralWidget(self.centralWidget)
        self.targetImageLabel.setAlignment(QtCore.Qt.AlignCenter)

        # Setup open image button
        self.openImageButton = QtWidgets.QPushButton(self.centralWidget)
        self.openImageButton.setToolTip("Open Image")
        self.openImageButton.setGeometry(QtCore.QRect(246, 34, 158, 30))
        self.openImageButton.setText("Open Image")
        self.openImageButton.clicked.connect(self.openFile)

        # Setup save image button
        self.saveImageButton = QtWidgets.QPushButton(self.centralWidget)
        self.saveImageButton.setToolTip("Save Image")
        self.saveImageButton.setGeometry(QtCore.QRect(962, 34, 158, 30))
        self.saveImageButton.setText("Save Image")
        self.saveImageButton.clicked.connect(self.saveImage)

       # Setup undo image button
        self.undoButton = QtWidgets.QPushButton(self.centralWidget)
        self.undoButton.setToolTip("Undo")
        self.undoButton.setGeometry(QtCore.QRect(605, 74, 158, 30))
        self.undoButton.setText("Undo")
        self.undoButton.clicked.connect(self.undo)

        # Setup blur image button        
        self.blurImageButton = QtWidgets.QPushButton(self.centralWidget)
        self.blurImageButton.setToolTip("Blur")
        self.blurImageButton.setGeometry(QtCore.QRect(605, 109, 158, 30))
        self.blurImageButton.setText("Blur")
        self.blurImageButton.clicked.connect(self.blur)

        # Setup deblur image button
        self.deblurImageButton = QtWidgets.QPushButton(self.centralWidget)
        self.deblurImageButton.setToolTip("Deblur")
        self.deblurImageButton.setGeometry(QtCore.QRect(605, 144, 158, 30))
        self.deblurImageButton.setText("Deblur")
        self.deblurImageButton.clicked.connect(self.deblur)

        # Setup grayscale image button        
        self.grayscaleImageButton = QtWidgets.QPushButton(self.centralWidget)
        self.grayscaleImageButton.setToolTip("Grayscale")
        self.grayscaleImageButton.setGeometry(QtCore.QRect(605, 179, 158, 30))
        self.grayscaleImageButton.setText("Grayscale")
        self.grayscaleImageButton.clicked.connect(self.grayscale)

        # Setup crop image button
        self.cropImageButton = QtWidgets.QPushButton(self.centralWidget)
        self.cropImageButton.setToolTip("Crop")
        self.cropImageButton.setGeometry(QtCore.QRect(605, 214, 158, 30))
        self.cropImageButton.setText("Crop")
        self.cropImageButton.clicked.connect(self.crop)

        # Setup flip image button
        self.flipImageButton = QtWidgets.QPushButton(self.centralWidget)
        self.flipImageButton.setToolTip("Flip")
        self.flipImageButton.setGeometry(QtCore.QRect(605, 249, 158, 30))
        self.flipImageButton.setText("Flip")
        self.flipImageButton.clicked.connect(self.flip)

        # Setup mirror image button
        self.mirrorImageButton = QtWidgets.QPushButton(self.centralWidget)
        self.mirrorImageButton.setToolTip("Mirror")
        self.mirrorImageButton.setGeometry(QtCore.QRect(605, 284, 158, 30))
        self.mirrorImageButton.setText("Mirror")
        self.mirrorImageButton.clicked.connect(self.mirror)

        # Setup rotate image button
        self.rotateImageButton = QtWidgets.QPushButton(self.centralWidget)
        self.rotateImageButton.setToolTip("Rotate")
        self.rotateImageButton.setGeometry(QtCore.QRect(605, 319, 158, 30))
        self.rotateImageButton.setText("Rotate")
        self.rotateImageButton.clicked.connect(self.rotate)
        
        # Setup reverse color button
        self.reverseColorButton = QtWidgets.QPushButton(self.centralWidget)
        self.reverseColorButton.setToolTip("Reverse the Color")
        self.reverseColorButton.setGeometry(QtCore.QRect(605, 354, 158, 30))
        self.reverseColorButton.setText("Reverse the Color")
        self.reverseColorButton.clicked.connect(self.reverseColor)

        # Setup change color balance button        
        self.changeColorBalanceButton = QtWidgets.QPushButton(self.centralWidget)
        self.changeColorBalanceButton.setToolTip("Change Color Balance")
        self.changeColorBalanceButton.setGeometry(QtCore.QRect(605, 389, 158, 30))
        self.changeColorBalanceButton.setText("Change Color Balance")
        self.changeColorBalanceButton.clicked.connect(self.changeColorBalance)

        # Setup adjust brightness increase button        
        self.adjustBrightnessIncreaseButton = QtWidgets.QPushButton(self.centralWidget)
        self.adjustBrightnessIncreaseButton.setToolTip("Adjust Brightness (+)")
        self.adjustBrightnessIncreaseButton.setGeometry(QtCore.QRect(605, 424, 158, 30))
        self.adjustBrightnessIncreaseButton.setText("Adjust Brightness (+)")
        self.adjustBrightnessIncreaseButton.clicked.connect(self.adjustBrightnessIncrease)

        # Setup adjust brightness decrease button        
        self.adjustBrightnessDecreaseButton = QtWidgets.QPushButton(self.centralWidget)
        self.adjustBrightnessDecreaseButton.setToolTip("Adjust Brightness (-)")
        self.adjustBrightnessDecreaseButton.setGeometry(QtCore.QRect(605, 459, 158, 30))
        self.adjustBrightnessDecreaseButton.setText("Adjust Brightness (-)")
        self.adjustBrightnessDecreaseButton.clicked.connect(self.adjustBrightnessDecrease)

        # Setup adjust contrast increase button 
        self.adjustContrastIncreaseButton = QtWidgets.QPushButton(self.centralWidget)
        self.adjustContrastIncreaseButton.setToolTip("Adjust Contrast (+)")
        self.adjustContrastIncreaseButton.setGeometry(QtCore.QRect(605, 494, 158, 30))
        self.adjustContrastIncreaseButton.setText("Adjust Contrast (+)")
        self.adjustContrastIncreaseButton.clicked.connect(self.adjustContrastIncrease)

        # Setup adjust contrast decrease button 
        self.adjustContrastDecreaseButton = QtWidgets.QPushButton(self.centralWidget)
        self.adjustContrastDecreaseButton.setToolTip("Adjust Contrast (-)")
        self.adjustContrastDecreaseButton.setGeometry(QtCore.QRect(605, 529, 158, 30))
        self.adjustContrastDecreaseButton.setText("Adjust Contrast (-)")
        self.adjustContrastDecreaseButton.clicked.connect(self.adjustContrastDecrease)

        # Setup adjust saturation increase button 
        self.adjustSaturationIncreaseButton = QtWidgets.QPushButton(self.centralWidget)
        self.adjustSaturationIncreaseButton.setToolTip("Adjust Saturation (+)")
        self.adjustSaturationIncreaseButton.setGeometry(QtCore.QRect(605, 564, 158, 30))
        self.adjustSaturationIncreaseButton.setText("Adjust Saturation (+)")
        self.adjustSaturationIncreaseButton.clicked.connect(self.adjustSaturationIncrease)
        
        # Setup adjust saturation decrease button 
        self.adjustSaturationDecreaseButton = QtWidgets.QPushButton(self.centralWidget)
        self.adjustSaturationDecreaseButton.setToolTip("Adjust Saturation (-)")
        self.adjustSaturationDecreaseButton.setGeometry(QtCore.QRect(605, 599, 158, 30))
        self.adjustSaturationDecreaseButton.setText("Adjust Saturation (-)")
        self.adjustSaturationDecreaseButton.clicked.connect(self.adjustSaturationDecrease)
        
        # Setup add noise button 
        self.addNoiseButton = QtWidgets.QPushButton(self.centralWidget)
        self.addNoiseButton.setToolTip("Add Noise")
        self.addNoiseButton.setGeometry(QtCore.QRect(605, 634, 158, 30))
        self.addNoiseButton.setText("Add Noise")
        self.addNoiseButton.clicked.connect(self.addNoise)

        # Setup detect edges button 
        self.detectEdgesButton = QtWidgets.QPushButton(self.centralWidget)
        self.detectEdgesButton.setToolTip("Detect Edges")
        self.detectEdgesButton.setGeometry(QtCore.QRect(605, 669, 158, 30))
        self.detectEdgesButton.setText("Detect Edges")
        self.detectEdgesButton.clicked.connect(self.detectEdges)

        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)


    def saveImage(self):
        """
        Saves image.
        """
        if self.checkSourceImage():
            if self.checkSourceImage():
                fname = QFileDialog.getSaveFileName(self, "Save file", os.getcwd(), 'Images (*.png *.xmp *.jpg *.jpeg *.tiff *.gif)')
                if fname != ('', ''):
                    filters.saveImage(self.targetImage, fname[0])
        
    
    def undo(self):
        """
        Undo applied filter
        """
        # Check if there is an image to undo.
        if isinstance(self.targetImage, type(None)) and isinstance(self.sourceImage, type(None)):
            self.show_popup('There is nothing to undo.')
            return

        # undo images.
        self.targetImage = self.lastTargetImage
        self.sourceImage = self.lastSourceImage
        
        if not isinstance(self.targetImage, type(None)):
            self.setupTargetImageLabel()
            if not isinstance(self.sourceImage, type(None)):
                self.setupSourceImageLabel()
        else: # Clear labels if source and target images have been restored.
            self.targetImageLabel.clear()
            self.sourceImageLabel.clear()


    def openFile(self):
            """
            Opens an image.
            """
            # setup source image
            fname = QFileDialog.getOpenFileName(self, "Open file", os.getcwd(), 'Images (*.png *.xmp *.jpg *.jpeg *.tiff *.gif)')
            if fname != ('', ''):

                self.lastTargetImage = self.targetImage # save last target image
                self.lastSourceImage = self.sourceImage # save last source image

                self.sourceImage = filters.openImage(fname[0])
                self.sourceImagePixmap =  QtGui.QPixmap(fname[0])
                self.sourceImagePixmap = self.sourceImagePixmap.scaled(550, 620, QtCore.Qt.KeepAspectRatio)
                self.sourceImageLabel.setGeometry(self.sourceImageLabel.x() , self.sourceImageLabel.y(), self.sourceImagePixmap.width(),self.sourceImagePixmap.height())
                self.sourceImageLabel.setPixmap(self.sourceImagePixmap)

                # setup target image
                self.targetImage = filters.openImage(fname[0])
                self.targetImagePixmap = QtGui.QPixmap(fname[0])
                self.targetImagePixmap = self.targetImagePixmap.scaled(550, 620, QtCore.Qt.KeepAspectRatio)
                self.targetImageLabel.setGeometry(self.targetImageLabel.x() , self.targetImageLabel.y(), self.targetImagePixmap.width(),self.targetImagePixmap.height())
                self.targetImageLabel.setPixmap(self.targetImagePixmap)
                self.targetImageLabel.cropCoordinates = None

    def blur(self):
        """
         Applies gaussianBlurImage function to an image if source image exists.
        """   
        if self.checkSourceImage(): # If there is an image to be filtered
            self.lastTargetImage = self.targetImage # save last target image
            self.targetImage = filters.gaussianBlurImage(self.targetImage)
            self.setupTargetImageLabel()


    def deblur(self):
        """
         Applies deblurImage function to an image if source image exists.
        """   
        if self.checkSourceImage(): # If there is an image to be filtered
            self.lastTargetImage = self.targetImage # save last target image
            self.targetImage = filters.deblurImage(self.targetImage)
            self.setupTargetImageLabel()


    def grayscale(self):
        """
         Applies grayscale function to an image if source image exists.
        """   
        if self.checkSourceImage(): # If there is an image to be filtered
            errorText = "Grayscale: The source image is already grayscale! Please be sure to give a proper colorful image."
            if not self.checkSameReference(self.targetImage, filters.ConvertToGrayScale(self.targetImage), errorText):
                self.lastTargetImage = self.targetImage # save last target image
                self.targetImage = filters.ConvertToGrayScale(self.targetImage)
                self.setupTargetImageLabel()
            

    def crop(self):
        """
         Applies CropImage function to an image if source image exists.
        """    
        if self.checkSourceImage(): # If there is an image to be filtered
            if not isinstance(self.sourceImage, type(None)):
                if not isinstance(self.targetImageLabel.cropCoordinates, type(None)):
                    self.lastTargetImage = self.targetImage # save last target image
                    # When crop function is applied scaling factor of image must be taken into account.
                    factor_x = self.targetImage.size[0] / self.targetImageLabel.width() #scaling factor in x axis
                    factor_y = self.targetImage.size[1] / self.targetImageLabel.height() #scaling factor in y axis
                    left = self.targetImageLabel.cropCoordinates[0] * factor_x # left coordinate
                    top = self.targetImageLabel.cropCoordinates[1] * factor_y # top coordinate
                    right = self.targetImageLabel.cropCoordinates[2] * factor_x # right coordinate
                    bottom = self.targetImageLabel.cropCoordinates[3] * factor_y # bottom coordinate
                    self.targetImage = filters.CropImage(self.targetImage, left, top, right, bottom)
                    self.setupTargetImageLabel()

                else:
                    self.show_popup("Please select an area to crop.")
            else:
                self.show_popup("If you have applied a filter, you should select an area on the right.")


    def flip(self):
        """
         Applies flip function to an image if source image exists.
        """   
        if self.checkSourceImage(): # If there is an image to be filtered
            self.lastTargetImage = self.targetImage # save last target image
            self.targetImage = filters.flip(self.targetImage)
            self.setupTargetImageLabel()


    def mirror(self):
        """
         Applies MirrorImage function to an image if source image exists.
        """   
        if self.checkSourceImage(): # If there is an image to be filtered
            self.lastTargetImage = self.targetImage # save last target image
            self.targetImage = filters.MirrorImage(self.targetImage)
            self.setupTargetImageLabel()


    def rotate(self):
        """
         Applies rotateImage function to an image if source image exists.
        """   
        if self.checkSourceImage():   # If there is an image to be filtered
            self.lastTargetImage = self.targetImage # save last target image
            self.targetImage = filters.rotateImage(self.targetImage)
            self.setupTargetImageLabel()


    def reverseColor(self):
        """
         Applies InvertImage function to an image if source image exists.
        """    
        if self.checkSourceImage():   # If there is an image to be filtered
            self.lastTargetImage = self.targetImage # save last target image
            self.lastSourceImage = self.sourceImage # save last source image
            self.targetImage = filters.InvertImage(self.targetImage)
            self.setupTargetImageLabel()


    def changeColorBalance(self):
        """
         Applies changeColorBalance function to an image if source image exists.
        """
        if self.checkSourceImage():   # If there is an image to be filtered
            errorText = "Change Color Balance: The source image is grayscale! Please be sure to give a proper colorful image."
            if not self.checkSameReference(self.targetImage, filters.changeColorBalance(self.targetImage), errorText):
                self.lastTargetImage = self.targetImage # save last target image
                self.lastSourceImage = self.sourceImage # save last source image
                self.targetImage = filters.changeColorBalance(self.targetImage)
                self.setupTargetImageLabel()


    def adjustBrightnessIncrease(self): # If there is an image to be filtered
        """
         Applies adjustBrightness function to an image if source image exists.
         It increases brightness.
        """
        if self.checkSourceImage():
            self.lastTargetImage = self.targetImage # save last target image
            self.lastSourceImage = self.sourceImage # save last source image
            self.targetImage = filters.AdjustBrightness(self.targetImage, 1.5)
            self.setupTargetImageLabel()

    def adjustBrightnessDecrease(self): # If there is an image to be filtered
        """
         Applies adjustBrightness function to an image if source image exists.
         It decreases brightness.
        """
        if self.checkSourceImage():
            self.lastTargetImage = self.targetImage # save last target image
            self.lastSourceImage = self.sourceImage # save last source image
            self.targetImage = filters.AdjustBrightness(self.targetImage, 0.75)
            self.setupTargetImageLabel()

    def adjustContrastIncrease(self):
        """
         Applies adjustContrast function to an image if source image exists.
         It increases contrast.
        """
        if self.checkSourceImage():   # If there is an image to be filtered
            self.lastTargetImage = self.targetImage # save last target image
            self.lastSourceImage = self.sourceImage # save last source image
            self.targetImage = filters.adjustContrast(self.targetImage, 1.5)
            self.setupTargetImageLabel()

    def adjustContrastDecrease(self):
        """
         Applies adjustContrast function to an image if source image exists.
         It decreases contrast.
        """
        if self.checkSourceImage():   # If there is an image to be filtered
            self.lastTargetImage = self.targetImage # save last target image
            self.lastSourceImage = self.sourceImage # save last source image
            self.targetImage = filters.adjustContrast(self.targetImage, 0.75)
            self.setupTargetImageLabel()

    def adjustSaturationIncrease(self):
        """
         Applies adjustSaturation function to an image if source image exists.
         It increases saturation.
        """
        if self.checkSourceImage():   # If there is an image to be filtered
            self.lastTargetImage = self.targetImage # save last target image
            self.lastSourceImage = self.sourceImage # save last source image
            self.targetImage = filters.AdjustSaturation(self.targetImage, 1.5)
            self.setupTargetImageLabel()

    def adjustSaturationDecrease(self):
        """
         Applies adjustSaturation function to an image if source image exists.
         It decreases saturation.
        """
        if self.checkSourceImage():   # If there is an image to be filtered
            self.lastTargetImage = self.targetImage # save last target image
            self.lastSourceImage = self.sourceImage # save last source image
            self.targetImage = filters.AdjustSaturation(self.targetImage, 0.75)
            self.setupTargetImageLabel()

    def addNoise(self):
        """
         Applies addNoise function to an image if source image exists.
        """
        if self.checkSourceImage():   # If there is an image to be filtered
            self.lastTargetImage = self.targetImage # save last target image
            self.lastSourceImage = self.sourceImage # save last source image
            self.targetImage = filters.AddNoise(self.targetImage)
            self.setupTargetImageLabel()


    def detectEdges(self):
        """
         Applies detectEdges function to an image if source image exists.
        """
        if self.checkSourceImage():   # If there is an image to be filtered
            self.lastTargetImage = self.targetImage # save last target image
            self.lastSourceImage = self.sourceImage # save last source image
            self.targetImage = filters.detectEdges(self.targetImage)
            self.setupTargetImageLabel()


    def checkSourceImage(self):
        """Check if the source image to be saved exists or not

        Returns:
            Boolean: True if the source image exists.
        """
        if isinstance(self.targetImage, type(None)):
            self.show_popup('There is no source image. Please open a file.')
            return False
        return True


    def setupTargetImageLabel(self):
        """
        This function is called when a filter is applied to an image.
        """
        image = ImageQt.ImageQt(self.targetImage)
        self.targetImagePixmap =  QtGui.QPixmap.fromImage(image)
        self.targetImagePixmap = self.targetImagePixmap.scaled(550, 620, QtCore.Qt.KeepAspectRatio)
        self.targetImageLabel.setPixmap(self.targetImagePixmap)
        self.targetImageLabel.cropCoordinates = None 
        self.targetImageLabel.setGeometry(self.targetImageLabel.x(), self.targetImageLabel.y(), self.targetImagePixmap.width(),self.targetImagePixmap.height())


    def setupSourceImageLabel(self):
        """
        This function is called when a filter is applied to an image.
        """
        image = ImageQt.ImageQt(self.sourceImage)
        self.sourceImagePixmap =  QtGui.QPixmap.fromImage(image)
        self.sourceImagePixmap = self.sourceImagePixmap.scaled(550, 620, QtCore.Qt.KeepAspectRatio)
        self.sourceImageLabel.setPixmap(self.sourceImagePixmap)
        self.sourceImageLabel.cropCoordinates = None 
        self.sourceImageLabel.setGeometry(self.sourceImageLabel.x(), self.sourceImageLabel.y(), self.sourceImagePixmap.width(),self.sourceImagePixmap.height())


    def checkSameReference(self,object1, object2, errorText):
        """ Check if two object reference to same address.
        If if two object reference to same address, show popup.
        Args:
            object1 
            object2 
            errorText (str): Error message that will be printed on the screen.

        Returns:
            Boolean: returns True if two object reference to same address.
        """
        if object1 is object2:
            self.show_popup(errorText)
            return True
        return False
    

    def show_popup(self, errorText):
        msg = QMessageBox()
        msg.setText(errorText)
        msg.setWindowTitle("Error")
        msg.setIcon(QMessageBox.Critical)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()


class CroppedImageLabel (QtWidgets.QLabel):
    """
    This class creates an QLabel object. Mouse event can be detected using this class.
    
    """

    def __init__(self, parentQWidget = None):
        super(CroppedImageLabel, self).__init__(parentQWidget)
        self.cropCoordinates = None


    def mousePressEvent (self, eventQMouseEvent):
        self.originQPoint = eventQMouseEvent.pos()
        self.qRubberBand = QtWidgets.QRubberBand(QtWidgets.QRubberBand.Rectangle, self)
        self.qRubberBand.setGeometry(QtCore.QRect(self.originQPoint, QtCore.QSize()))
        self.qRubberBand.show()


    def mouseMoveEvent (self, eventQMouseEvent):
        self.qRubberBand.setGeometry(QtCore.QRect(self.originQPoint, eventQMouseEvent.pos()).normalized())


    def mouseReleaseEvent (self, eventQMouseEvent):
        self.qRubberBand.hide()
        currentQRect = self.qRubberBand.geometry()
        self.qRubberBand.deleteLater()
        self.cropCoordinates =(currentQRect.left(), currentQRect.top(), currentQRect.right(), currentQRect.bottom() )