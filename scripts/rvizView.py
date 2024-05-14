
from jointRos import*
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import roslib; roslib.load_manifest('rviz_python_tutorial')
import sys

import roslaunch
from rviz import bindings as rviz
from geometry_msgs.msg import Pose

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


Offset = [512,512,512,512,512]
DEGS=[[0, 0, 0, 0, 0],
      [-20, 20, -20, 20, 0],
      [30,-30, 30, -30, 0],
      [-90, 15, -55, 17, 0],
      [ -90, 45, -55, 45, 10]]


class RVizControlWindow(QMainWindow):
    global Goal
    
    def __init__(self):
        super().__init__()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.launch_button = QPushButton("Launch RViz")
        self.launch_button.clicked.connect(self.launch_rviz)
        self.layout.addWidget(self.launch_button)

        self.stop_button = QPushButton("Stop RViz")
        self.stop_button.clicked.connect(self.stop_rviz)
        self.stop_button.setEnabled(False)
        self.layout.addWidget(self.stop_button)

        self.radio_layout = QHBoxLayout()
        self.radio_buttons = []

        for i in range(5):
            radio_button = QRadioButton(f"Option {i+1}")
            self.radio_layout.addWidget(radio_button)
            self.radio_buttons.append(radio_button)

        self.layout.addLayout(self.radio_layout)

        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.submit_options)
        self.submit_button.setEnabled(False)
        self.layout.addWidget(self.submit_button)

    def launch_rviz(self):
        self.launch_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.submit_button.setEnabled(True)

        self.frame = rviz.VisualizationFrame()

        self.frame.initialize()

        reader = rviz.YamlConfigReader()
        config = rviz.Config()
        reader.readFile( config, "config.rviz" )
        self.frame.load( config )

        # Set initial pose of the robot
        initial_pose = Pose()
        initial_pose.position.x = 0.0  # Set X position
        initial_pose.position.y = 0.0  # Set Y position
        initial_pose.position.z = 0.0  # Set Z position
        initial_pose.orientation.x = 0.0  # Set X orientation
        initial_pose.orientation.y = 0.0  # Set Y orientation
        initial_pose.orientation.z = 0.0  # Set Z orientation
        initial_pose.orientation.w = 1.0  # Set W orientation
    

        # Access the RViz configuration properties and modify the Displays group to add the RobotModel display
        display_group = config.mapGetChild("Visualization Manager").mapGetChild("Displays")
        robot_display_name = "RobotModel"
        robot_display_config = rviz.Config()
        robot_display_config.mapSetValue("Name", robot_display_name)
        robot_display_config.mapSetValue("Class", "rviz/RobotModel")
        robot_display_config.mapSetValue("Enabled", True)
        robot_display_config.mapSetValue("Alpha", 1)
        robot_display_config.mapSetValue("Collision Enabled", False)
        robot_display_config.mapSetValue("Visual Enabled", True)
        robot_display_config.mapSetValue("TF Prefix", "")
        robot_display_config.mapSetValue("Update Interval", 0)
        robot_display_config.mapSetValue("Robot Description", "robot_description")
        robot_display_config.mapSetValue("Robot Namespace", "/")
        robot_display_config.mapSetValue("Use TF Prefix", False)
        display_group.mapSetValue(robot_display_name, robot_display_config)

        # Publish the modified RVIZ configuration
        manager = self.frame.getManager()
        manager.setFixedFrame("base_link")  # Set the fixed frame
        manager.load(config)

        self.setWindowTitle(config.mapGetChild("Title").getValue())
        
        
        ## Here we disable the menu bar (from the top), status bar
        ## (from the bottom), and the "hide-docks" buttons, which are
        ## the tall skinny buttons on the left and right sides of the
        ## main render window.
        self.frame.setMenuBar( None )
        self.frame.setStatusBar( None )
        self.frame.setHideButtonVisibility( False )

        ## frame.getManager() returns the VisualizationManager
        ## instance, which is a very central class.  It has pointers
        ## to other manager objects and is generally required to make
        ## any changes in an rviz instance.
        self.manager = self.frame.getManager()

        ## Since the config file is part of the source code for this
        ## example, we know that the first display in the list is the
        ## grid we want to control.  Here we just save a reference to
        ## it for later.
        self.grid_display = self.manager.getRootDisplayGroup().getDisplayAt( 0 )
        
        ## Here we create the layout and other widgets in the usual Qt way.
        layout = QVBoxLayout()
        layout.addWidget( self.frame )
        
        thickness_slider = QSlider( Qt.Horizontal )
        thickness_slider.setTracking( True )
        thickness_slider.setMinimum( 1 )
        thickness_slider.setMaximum( 1000 )
        thickness_slider.valueChanged.connect( self.onThicknessSliderChanged )
        layout.addWidget( thickness_slider )       
        
        
        h_layout = QHBoxLayout()
        
        top_button = QPushButton( "Top View" )
        top_button.clicked.connect( self.onTopButtonClick )
        h_layout.addWidget( top_button )
        
        side_button = QPushButton( "Side View" )
        side_button.clicked.connect( self.onSideButtonClick )
        h_layout.addWidget( side_button )
        
        layout.addLayout( h_layout )

        self.layout.addLayout(layout)  # Add layout to main window layout

    def onThicknessSliderChanged( self, new_value ):
        if self.grid_display != None:
            self.grid_display.subProp( "Line Style" ).subProp( "Line Width" ).setValue( new_value / 1000.0 )

    def onTopButtonClick( self ):
        self.switchToView( "Top View" )
        
    def onSideButtonClick( self ):
        self.switchToView( "Side View" )
        
    def switchToView( self, view_name ):
        view_man = self.manager.getViewManager()
        for i in range( view_man.getNumViews() ):
            if view_man.getViewAt( i ).getName() == view_name:
                view_man.setCurrentFrom( view_man.getViewAt( i ))
                return
        print( "Did not find view named %s." % view_name )
    
    def stop_rviz(self):
        self.launch_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.submit_button.setEnabled(False)

        # Code to stop RViz goes here

    def submit_options(self):
        selected_option = None
        for i, button in enumerate(self.radio_buttons):
            if button.isChecked():
                selected_option = i + 1
                break

        if selected_option is not None:
            moveGoal(Goal.get()).place(x=W,y=H*7)
        else:
            print("Please select an option.")
    
    def getGoal(value):
        print(value)
        return
    
    def moveGoal(value):
        moveRobot(DEGS[value-1],0.5)
        return

if __name__ == "__main__":
    listener()
    

    import sys

    app = QApplication(sys.argv)
    window = RVizControlWindow()
    #window.resize( 500, 500 )
    window.setWindowTitle("RViz Control")
    window.show()
    app.exec_()