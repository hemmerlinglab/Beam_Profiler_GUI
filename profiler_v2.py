
import sys
from PyQt5.QtWidgets import QSizePolicy, QTextEdit, QMainWindow, QApplication, QWidget, QAction, QTableWidget,QTableWidgetItem,QVBoxLayout,QPushButton, QHBoxLayout, QTabWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
import numpy as np
import scipy
import lmfit 
from lmfit import Minimizer, Parameters, report_fit
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QLineEdit

import random



from matplotlib.backends.qt_compat import QtCore, QtWidgets, is_pyqt5
if is_pyqt5():
    from matplotlib.backends.backend_qt5agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
else:
    from matplotlib.backends.backend_qt4agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure




# define objective function: returns the array to be minimized
# function to minimize
def fcn2min(params, x, data, plot_fit = False):
    """Model a decaying sine wave and subtract data."""
    amplitude = params['amplitude']
    waist     = params['waist']
    x_offset  = params['x_offset']
    y_offset  = params['y_offset']
    
    if plot_fit == False:
        model = amplitude/2.0 * (1 - scipy.special.erf(np.sqrt(2.0) * (x - x_offset)/waist)) + y_offset
        
        return model - data
    else:
        x_plot = np.linspace(np.min(x), np.max(x), 100)
        model = amplitude/2.0 * (1 - scipy.special.erf(np.sqrt(2.0) * (x_plot - x_offset)/waist)) + y_offset
        return (x_plot, model)

def fcn2min_profile(params, x, data, plot_fit = False):
    """Model a decaying sine wave and subtract data."""
    waist     = params['waist']
    x_offset  = params['x_offset']
    my_lambda  = params['my_lambda']
    
    zR = np.pi * waist**2/my_lambda

    if plot_fit == False:
        model = waist * np.sqrt( 1 + (x - x_offset)**2/zR**2 )
        
        return model - data
    else:
        x_plot = np.linspace(np.min(x), np.max(x), 100)
        model = waist * np.sqrt( 1 + (x_plot - x_offset)**2/zR**2 )
        return (x_plot, model)


   
# Creation of the Widget
class App(QWidget):
    # initialization of class
    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 table - pythonspot.com'
        self.left = 0
        self.top = 0
        self.width = 1500
        self.height = 500
        self.no_of_rows = 20
        self.initUI()
 
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.tabs = QTabWidget()

        self.tab_waist = QWidget()
        self.tab_profile = QWidget()

        self.tabs.addTab(self.tab_waist, "Waist Fit")
        self.tabs.addTab(self.tab_profile, "Profile Fit")


        self.create_waist_tab()
        self.create_profile_tab()

        # add tabs
        self.layout = QHBoxLayout()
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

        # Show widget
        self.show()
        
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
      
        self.show()

    def create_waist_tab(self):
        self.createTable()
 	
	# Creating a button which fits the data to the error function 
	# Defined from the qt library, defines the widgets here
	# qt library is a collection of widgets
	# obtains the object push button
        
        # Fit button
        self.button = QPushButton('Fit', self)
        self.button.clicked.connect(self.button_click)
        
        # Fit to sample data button
        self.button2 = QPushButton('Fit to Sample Data?', self)
        self.button2.clicked.connect(self.sample_data_button_click)
        
        # Reset button
     #   self.button3 = QPushButton('Reset', self)
    #    self.button3.clicked.connect(self.reset)

	# sets up the Figure Plotting
        self.canvas = PlotCanvas(self, width=5, height=4)
        self.canvas.move(0,0)

        
        self.textbox = QTextEdit()

        # Add box layout, add table to box layout and add box layout to widget
	# To add any kind of new widget, you must add it to your layout
        self.tab_waist.layout = QHBoxLayout()              # The QHBoxLayout class lines up widgets horizontally, create widget
	
	# List of widgets being added
        #self.layout.addWidget(self.tableWidget)  # Table widget to put the data in
        self.tab_waist.layout.addWidget(self.text_x)
        self.tab_waist.layout.addWidget(self.text_y)
        self.tab_waist.layout.addWidget(self.canvas)       # Creates the plot widget   
        self.tab_waist.layout.addWidget(self.button)       # button widget which fits the data
        self.tab_waist.layout.addWidget(self.button2)      # button widget which reinitializes the plot
    #    self.layout.addWidget(self.button3)      # button widget which clears the previous plot data
        self.tab_waist.layout.addWidget(self.textbox)      # textbox to output the relevant params: waist, amplitude, offsets
        self.tab_waist.setLayout(self.tab_waist.layout)              # sets it all up            


    def create_profile_tab(self):
        self.text_x_profile = QTextEdit()
        self.text_y_profile = QTextEdit()

        # Sample data that will fit to error function
        self.x = [0]
        self.y = [1]

        self.text_x.setText(self.conv2str(self.x))
        self.text_y.setText(self.conv2str(self.y))

        # Fit button
        self.button_profile = QPushButton('Fit', self)
        self.button_profile.clicked.connect(self.button_profile_click)
       
	# sets up the Figure Plotting
        self.canvas_profile = PlotCanvas(self, width=5, height=4)
        self.canvas_profile.move(0,0)

        
        self.textbox_profile = QTextEdit()

        self.tab_profile.layout = QHBoxLayout()              # The QHBoxLayout class lines up widgets horizontally, create widget
	
	# List of widgets being added
        self.tab_profile.layout.addWidget(self.text_x_profile)
        self.tab_profile.layout.addWidget(self.text_y_profile)
        self.tab_profile.layout.addWidget(self.canvas_profile)       # Creates the plot widget   
        self.tab_profile.layout.addWidget(self.button_profile)       # button widget which fits the data
        self.tab_profile.layout.addWidget(self.textbox_profile)      # textbox to output the relevant params: waist, amplitude, offsets
        self.tab_profile.setLayout(self.tab_profile.layout)              # sets it all up            


    def sample_data(self):
        hlp = np.array([
           [ 1524,3.66 ], 
           [ 1651,3.5 ],
           [ 1676.4,3.17 ],
           [ 1701.8,2.53 ],
           [ 1727.2,1.71 ],
           [ 1752.6,0.87 ],
           [ 1778,0.32 ],
           [ 1803.4,0.1 ],
           [ 1828.8,0.016 ],
           [ 1854.2,0.001 ],
            ])
        return hlp
       
    @pyqtSlot()
    def button_click(self):
        print('Fit Button Pressed')
        self.x = self.conv2list(self.text_x.toPlainText())
        self.y = self.conv2list(self.text_y.toPlainText())

        print(self.x)
        print(self.y)

	# convert
        offset = self.x[0]
        self.x = (self.x - self.x[0]) * 1.0/10.0 * 25.4 * 1000.0 # in um

        params = Parameters()
        params.add('amplitude', value=np.max(self.y), min=(np.max(self.y) - np.min(self.y))/2.0, max=(np.max(self.y) - np.min(self.y)))
        params.add('waist', value=(np.max(self.x)-np.min(self.x))/2.0, min=10.0, max=2000)
        params.add('x_offset', value=np.mean(self.x), min=np.min(self.x), max = np.max(self.x))
        params.add('y_offset', value=np.min(self.y), min=0.00, max=np.max(self.y), vary = False)

        # do fit, here with leastsq model
        minner = Minimizer(fcn2min, params, fcn_args=(self.x, self.y))
        result = minner.minimize()
        
        # Store the Confidence data from the fit
        con_report = lmfit.fit_report(result.params)
        

        # write error report
        self.textbox.setText("")
        for k in params.keys():
            my_str = str(result.params[k].value)
            self.textbox.append(str(k) + " = " + my_str + "\n")
        self.textbox.append(con_report) # include the confidence data in the textbox

        self.canvas.x = self.x
        self.canvas.y = self.y

        (fit_x, fit_y) = fcn2min(result.params, self.x, None, plot_fit = True)
        self.canvas.plot(fit_plot = [fit_x, fit_y])
        print(params)
    
    @pyqtSlot()
    def button_profile_click(self):
        print('Fit Profile Button Pressed')
        self.x2 = self.conv2list(self.text_x_profile.toPlainText())
        self.y2 = self.conv2list(self.text_y_profile.toPlainText())

        print(self.x2)
        print(self.y2)

        # convert
        self.x2 = (self.x2) * 1000.0 # in um

        params = Parameters()
        params.add('waist', value=200.0, min=10.0, max=2000)
        params.add('x_offset', value=np.mean(self.x2), min=-3000.0e3, max = +3000.0e3)
        params.add('my_lambda', value = 780e-9/1e-6, vary = False) # all units are in um

        # do fit, here with leastsq model
        minner = Minimizer(fcn2min_profile, params, fcn_args=(self.x2, self.y2))
        result = minner.minimize()
        
        # Store the Confidence data from the fit
        con_report = lmfit.fit_report(result.params)
        

        # write error report
        self.textbox_profile.setText("")
        for k in params.keys():
            my_str = str(result.params[k].value)
            self.textbox.append(str(k) + " = " + my_str + "\n")
        self.textbox_profile.append(con_report) # include the confidence data in the textbox

        self.canvas_profile.x = self.x2
        self.canvas_profile.y = self.y2

        (fit_x, fit_y) = fcn2min_profile(result.params, self.x2, None, plot_fit = True)
        self.canvas_profile.plot(fit_plot = [fit_x, fit_y])
        print(params)
    

    @pyqtSlot()
    def sample_data_button_click(self):
        print('sample data button pressed')
        self.x = np.array([])
        self.y = np.array([])

        hlp = self.sample_data()
         
        self.x = hlp[:,0]
        self.y = hlp[:,1]
        
        print(self.x)
        print(self.y)

        params = Parameters()
        params.add('amplitude', value=np.max(self.y), min=(np.max(self.y) - np.min(self.y))/2.0, max=(np.max(self.y) - np.min(self.y)))
        params.add('waist', value=(np.max(self.x)-np.min(self.x))/2.0, min=10.0, max=2000)
        params.add('x_offset', value=np.mean(self.x), min=np.min(self.x), max = np.max(self.x))
        params.add('y_offset', value=0.0, min=0.00, max=np.max(self.y), vary = False)

        # do fit, here with leastsq model
        minner = Minimizer(fcn2min, params, fcn_args=(self.x, self.y))
        result = minner.minimize()       
       
        # Store the Confidence data from the fit
        con_report = lmfit.fit_report(result.params)          
       
       # write error report
        self.textbox.setText("")
        for k in params.keys():
            my_str = str(result.params[k].value)
            self.textbox.append(str(k) + " = " + my_str + "\n")
        self.textbox.append(con_report) # include the confidence data in the textbox

        self.canvas.x = self.x
        self.canvas.y = self.y

        (fit_x, fit_y) = fcn2min(result.params, self.x, None, plot_fit = True)
        self.canvas.plot(fit_plot = [fit_x, fit_y])
        print(params)

    def createTable(self):

        self.text_x = QTextEdit()
        self.text_y = QTextEdit()


        # Sample data that will fit to error function
        hlp = self.sample_data()

        self.x = hlp[:, 0]
        self.y = hlp[:, 1]

        self.text_x.setText(self.conv2str(self.x))
        self.text_y.setText(self.conv2str(self.y))
       
    def conv2str(self, mylist):

        hlp = ""
        for k in mylist:
            hlp += str(k) + ',' + "\n"
        return hlp[0:-2]

    def conv2list(self, mystr):

        return np.fromstring(mystr, dtype = float, sep = ',')


class PlotCanvas(FigureCanvas):
 
    def __init__(self, parent=None, width=3, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
 
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
 
        FigureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.x = []
        self.y = []
        self.plot()
        fig.clear() # clears old plot data
       
 
 
    def plot(self, fit_plot = None):
        ax = self.figure.add_subplot(111)
        # data
        ax.plot(self.x, self.y, 'ro')  
        
	# fit
        if not fit_plot is None:
            ax.plot(fit_plot[0], fit_plot[1])
        ax.set_xlabel('Position (um)')
        ax.set_ylabel('Integrated Intensity')
        self.figure.tight_layout()  # ensures the view of the layout is always visible no matter size of GUI
        self.draw()
        ax.clear()  #clears old plot data
    
    




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
