import rospy
import numpy as np
import time
from std_msgs.msg import String
from sensor_msgs.msg import JointState
from dynamixel_workbench_msgs.srv import DynamixelCommand
offset = [512,512,512,512,512]
def callback(data):
    global PosActual,PosReal
    PosReal=np.rad2deg(data.position) 
    #PosActual=np.subtract(PosReal,np.multiply(offset,0.29))
    return

def listener():
    rospy.init_node('joint_listener', anonymous=True)
    rospy.Subscriber("/dynamixel_workbench/joint_states", JointState, callback)
    return

def moveRobot(pos,t):
    for i in range(len(pos)):
        position=int(np.round(pos[i]/0.29)+offset[i])
        jointCommand('',i+1,'Goal_Position',position,t)
        time.sleep(0.2)
    time.sleep(2)
    print(PosReal)
    #print(PosActual)
    return

def jointCommand(command, id_num, addr_name, value, time):
    #rospy.init_node('joint_node', anonymous=False)
    rospy.wait_for_service('dynamixel_workbench/dynamixel_command')
    try:        
        dynamixel_command = rospy.ServiceProxy(
            '/dynamixel_workbench/dynamixel_command', DynamixelCommand)
        result = dynamixel_command(command,id_num,addr_name,value)
        rospy.sleep(time)
        return result.comm_result
    except rospy.ServiceException as exc:
        print(str(exc))