from PIL import Image, ImageStat,ImageQt
import numpy
import matplotlib.pyplot as plt
import numpy as np
from PyQt5 import QtWidgets,QtCore,QtGui
from GUI import Ui_MainWindow
import sys
import cv2
import pyqtgraph as pg
from pyqtgraph import PlotWidget, plot
from PIL import Image
from sklearn.svm import SVC
import joblib
from NN import SavModel
import math

class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(ApplicationWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.Browse.clicked.connect(self.Browse)
        self.ui.Segment.clicked.connect(self.Kmeans_Function)
        self.ui.SVM.clicked.connect(lambda file:self.SVC_NN(3))
        self.ui.NN.clicked.connect(lambda file:self.SVC_NN(2))
        self.ui.Clear.clicked.connect(self.Clear)
        self.ui.Input.setBackground('w')
        self.ui.Output.setBackground('w')
        self.ui.Output.hideAxis('left')
        self.ui.Output.hideAxis('bottom')
        self.ui.Input.hideAxis('left')
        self.ui.Input.hideAxis('bottom')
        self.centroids = []

    def Clear(self):
        self.ui.Output.clear()
        self.ui.Input.clear()

    def Browse(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","Images (*.bmp)", options=options)
        if fileName:
            image=fileName
            img = cv2.imread(image)
            if image.endswith('.bmp'):
                img= cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            else:
                img = cv2.imread(image)

            img1=pg.ImageItem(img)
            self.ui.Input.clear()
            self.ui.Input.addItem(img1)

            self.img_width = img1.width()
            self.img_height=img1.height()
            self.im=Image.open(image)
            self.px = self.im.load()

#--------------------------------------------------- K-mean part-------------------------------
    def converged(self,centroids, old_centroids): 
        #comparing all centroides value with new one
        #checking their values are not equal
        if len(old_centroids) == 0:
            return False

        for i in range(0, len(centroids)):
            cent = centroids[i]
            old_cent = old_centroids[i]

            if ((int(old_cent[0]) - 1) <= cent[0] <= (int(old_cent[0]) + 1)) and ((int(old_cent[1]) - 1) <= cent[1] <= (int(old_cent[1]) + 1)) and ((int(old_cent[2]) - 1) <= cent[2] <= (int(old_cent[2]) + 1)):
                continue
            else:
                return False
        return True

    def assignPixels(self,centroids): 
        #get the pixel with the min distance from the 
        #centroid assign it to the nearest cluster
        clusters = {}

        for x in range(0, self.img_width):
            for y in range(0, self.img_height):
                p = self.px[x, y]
                minIndex = self.getMin(self.px[x, y], centroids)
            
                try:
                    clusters[minIndex].append(p)

                except KeyError:
                    clusters[minIndex] = [p]

                
        return clusters

    def getMin(self,pixel, centroids):
        #get the min distance between the pixel and the centroid
        d=0
        minDist = 9999
        minIndex = 0

        for i in range(0, len(centroids)):
            for j in range(3): #3=R,B,G  3D
                d += int((centroids[i][j] - pixel[j]))**2
            d=numpy.sqrt(d)
            if d < minDist:
                minDist = d
                minIndex = i

        return minIndex
    
    def adjustCentroids(self,clusters):
        #recalculate the position of the centroids
        new_centroids = []
        keys = sorted(clusters.keys())
        for k in keys:
            n = numpy.mean(clusters[k], axis=0)
            new = (int(n[0]), int(n[1]), int(n[2]))
            new_centroids.append(new) #new centroids
        return new_centroids
    
    def Kmeans_Function(self):
        
        k_number=int(self.ui.KValue.toPlainText())
        old_centroids =[]
        i = 1
        [self.centroids.append(self.px[numpy.random.randint(0, self.img_width), numpy.random.randint(0, self.img_height)]) for k in range(0, k_number)]
        
        #Updating the new values of the centroids and stop when the new and old values are equal
        while not self.converged(self.centroids, old_centroids) and i <= 20:
            i += 1
            clusters = self.assignPixels(self.centroids)
            self.centroids = self.adjustCentroids(clusters) 
        
        self.drawOutput()
        
    def drawOutput(self):
        result=self.centroids
        image = Image.new('RGB', (self.img_width, self.img_height), "white")
        p = image.load()
        for x in range(image.size[0]):
            for y in range(image.size[1]):
                RGB_value = result[self.getMin(self.px[x, y], result)] 
                p[x, y] = RGB_value
        img1=pg.ImageItem(np.asarray(image))
        self.ui.Output.clear()
        self.ui.Output.addItem(img1) 

#----------------------------------SVM and NN part-------------------------------
    def SVC_NN(self,file_num):
        if file_num==2:
            filename = 'P2_model.sav'
        elif file_num==3:
            filename = 'P3_model.sav'
        loaded_model = joblib.load(filename)
        SVC_image=np.asarray(self.im)
        output=[]
        for i in range(self.img_width):
            for j in range(self.img_height):
                output.append(SVC_image[i,j]/255)
        if file_num==2:
            y_pred=loaded_model.Predict(output)
        elif file_num==3:
            y_pred=loaded_model.predict(output)
        self.Draw_output_SVC_NN(output,y_pred)

    
    
    def Draw_output_SVC_NN(self,X,Y):
        Back_list=[]
        inner_list=[]
        outer_list=[]

        for i in range(len(X)):
        
            if(Y[i] ==0):
                Back_list.append(X[i])
            if(Y[i] ==1):
                inner_list.append(X[i])
            if(Y[i] ==2):
                outer_list.append(X[i])
        
        back_pix=np.mean(Back_list, axis=0)
        inner_pix=np.mean(inner_list, axis=0)
        outer_pix=np.mean(outer_list, axis=0)
        output = np.zeros((self.img_width,self.img_height,3),dtype=np.uint8)
        inc=0
        for i in range(self.img_width):
            for j in range(self.img_height):
                if(Y[inc]==0):
                    output[i,j]=back_pix *255

                if(Y[inc]==1):
                    output[i,j]= inner_pix *255

                if(Y[inc]==2):
                    output[i,j]=outer_pix *255

                inc+=1   
        img=pg.ImageItem(np.asarray(output))
        self.ui.Output.clear()
        self.ui.Output.addItem(img)

   

def main():
    app = QtWidgets.QApplication(sys.argv)
    application = ApplicationWindow()
    application.setWindowTitle("WDC")
    application.show()
    app.exec_()


  
if __name__ == "__main__":
    main()