import rospy
import numpy as np
from std_msgs.msg import String
from sensor_msgs.msg import JointState
from dynamixel_workbench_msgs.srv import DynamixelCommand
offset=[0,0,0,0,0]
def callback(data):
    global PosActual,PosReal
    PosReal=np.multiply(data.position,180/np.pi)
    PosActual=np.add(PosReal,offset)
    
def listener():
    rospy.init_node('joint_listener', anonymous=True)
    rospy.Subscriber("/dynamixel_workbench/joint_states", JointState, callback)
    rospy.spin()

def moveRobot(pos,time):
    print(len(pos))
    for i in range(len(pos)):
        jointCommand('',i+1,'Goal_Position',pos[i],time)
        time.sleep(0.2)

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