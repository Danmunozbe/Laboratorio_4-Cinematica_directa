from jointRos import*
import roslib; roslib.load_manifest('rviz_python_tutorial')
import sys
import numpy as np

import roslaunch
from rviz import bindings as rviz
from geometry_msgs.msg import Pose

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

# ROS and Moveit
import moveit_commander
import moveit_msgs.msg
from moveit_commander.conversions import pose_to_list
import geometry_msgs.msg
from std_msgs.msg import String

Offset = [512,512,512,512,511]
DEGS=[[0, 0, 0, 0, 0],
      [-20, 20, -20, 20, 0],
      [30,-30, 30, -30, 0],
      [-90, 15, -55, 17, 0],
      [ -90, 45, -55, 45, 10]]

class RVizControlWindow(QMainWindow):
    
    
    def __init__(self):
        
        self.PosReal = np.array([])
        rospy.init_node('joint_listener', anonymous=True)
        rospy.Subscriber("/dynamixel_workbench/joint_states", JointState, self.callback)  # Subscribe to joint_states topic

        
        self.Goal = QSpinBox()
        self.Goal.setMinimum(1)
        self.Goal.setMaximum(5)
        
        super().__init__()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)
        
        

        self.launch_button = QPushButton("Iniciar RViz")
        self.launch_button.clicked.connect(self.launch_rviz)
        self.layout.addWidget(self.launch_button)

        self.stop_button = QPushButton("Detener RViz")
        self.stop_button.clicked.connect(self.stop_rviz)
        self.stop_button.setEnabled(False)
        self.layout.addWidget(self.stop_button)

        self.radio_layout = QHBoxLayout()
        self.radio_buttons = []

        for i in range(5):
            radio_button = QRadioButton(f"Opción {i+1}")
            self.radio_layout.addWidget(radio_button)
            self.radio_buttons.append(radio_button)

        self.layout.addLayout(self.radio_layout)

        
        #Botón para modificar posición
        self.submit_button = QPushButton("Configurar")
        self.submit_button.clicked.connect(self.submit_options)
        self.submit_button.setEnabled(False)
        self.layout.addWidget(self.submit_button)
        
        # Create the QLabel for robot pose
        self.pose_label = QLabel("Valores articulares [q1, q2, q3, q4, q5]: ")
        self.layout.addWidget(self.pose_label)
        
        # Add labels layout
        labels_layout = QHBoxLayout()  # Layout for the labels
        self.layout.addLayout(labels_layout)  # Add it to the main layout

        # Add labels
        self.Daniel = QLabel("Daniel Muñoz \nDanmunozbe \ndanmunozbe@unal.edu.co")
        labels_layout.addWidget(self.Daniel)
        
        self.Christian = QLabel("Christian Vargas \nCVarPer \nchvargasp@unal.edu.co")
        labels_layout.addWidget(self.Christian)
        
    def launch_rviz(self):
        self.launch_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.submit_button.setEnabled(True)

        '''self.frame = rviz.VisualizationFrame()
        self.frame.initialize()

        # Create Displays
        manager = self.frame.getManager()

        

        # Grid Display
        grid_display = manager.createDisplay("rviz/Grid", "Grid", True)
        grid_display.subProp("Plane").setValue("XY")
        grid_display.subProp("Color").setValue(QColor(160, 160, 164))
        grid_display.subProp("Line Style").subProp("Line Width").setValue(0.03)
        grid_display.subProp("Plane Cell Count").setValue(10)

        # Robot Model Display
        urdf_path = "urdf/px_collision.urdf"  # Provide the actual path here
        rospy.set_param("/robot_description", urdf_path)
        robot_display = manager.createDisplay("rviz/RobotModel", "RobotModel", True)
        robot_display.subProp("Robot Description").setValue(urdf_path)
        robot_display.subProp("Update Interval").setValue(0.2)
        robot_display.subProp("Visual Enabled").setValue(True)
        robot_display.subProp("Collision Enabled").setValue(False)

        tf_display = manager.createDisplay("rviz/TF", "TF", True)
        tf_display.subProp("Frames").setValue({"/base_link": True})  # Adjust frame names as needed

        # Set fixed frame
        manager.setFixedFrame("base_link")

        # Set the layout
        self.frame.setMenuBar(None)
        self.frame.setStatusBar(None)
        self.frame.setHideButtonVisibility(False)

        # Add the frame to the layout
        layout = QVBoxLayout()
        layout.addWidget(self.frame)

        self.layout.addLayout(layout) '''
    
    
    def onThicknessSliderChanged( self, new_value ):
        if self.grid_display != None:
            self.grid_display.subProp( "Line Style" ).subProp( "Line Width" ).setValue( new_value / 1000.0 )
        
    def stop_rviz(self):
        self.launch_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.submit_button.setEnabled(False)

        # Code to stop RViz goes here

    def getGoal(self):
        print(self)
        return
    
    #Actualizar posición del robot
    def moveGoal(self, selected_option):
        moveRobot(DEGS[selected_option-1],0.1)
        self.update_pose_label(self.PosReal)
        return
    
    #Actualizar etiqueta de indicación de posición
    def update_pose_label(self, pose):
        # Update the text of the pose label with the received pose
        self.pose_label.setText(f"Valores articulares [q1, q2, q3, q4, q5]: {np.array2string(pose, precision=2, separator=', ', suppress_small=True, prefix='', suffix='')}")

    # Callback function to update PosReal
    def callback(self, data):
        self.PosReal = np.rad2deg(data.position)
    
    def submit_options(self):
        selected_option = None
        for i, button in enumerate(self.radio_buttons):
            if button.isChecked():
                selected_option = i + 1
                break

        if selected_option is not None:
            self.moveGoal(selected_option)
        else:
            print("Please select an option.")
    
    

if __name__ == "__main__":
    listener()

    app = QApplication(sys.argv)
    window = RVizControlWindow()
    #window.resize( 500, 500 )
    window.setWindowTitle("RViz Control")
    window.show()
    app.exec_()
