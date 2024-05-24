# Lab4

Para la solucion, se hizo uso de un servicio y una subscricion a un topic.
El servicio utilizado es `dinamixel_command` usando `Goal_position` como posición de direccion (direccion de la instruccion como nombre), donde ademas recibe el `ID` de la articulacion a mover (el cual se ha definido en un archivo .yaml), y la posición en bits (0-1023).
Para la posición incial se tomó un valor de registro de 512, lo que implica 150°, esto debido a que segun el datasheet de los motores, este es el punto donde hay mayor rango para el movimiento. 

![imagen](https://emanual.robotis.com/assets/images/dxl/dx/dx_series_goal_position.png)
## Funciones de Rospy
En el archivo [jointRos.py](scripts/jointRos.py) se encuentran un conjunto de funciones que se utilizan para la interfaz.
### moveRobot
``` python
def moveRobot(pos,t):
    for i in range(len(pos)):
        position=int(np.round(pos[i]/0.29)+offset[i])
        jointCommand('',i+1,'Goal_Position',position,t)
        time.sleep(0.2)
    time.sleep(2)
    return
```
La funcion recibe 2 parametros, `pos` es un arreglo de angulos, donde en cada posición se encuentra la posicion deseada de la articulación (en grados); y `t` es un valor de tiempo ensegundos para la funcion jointCommand.
Notese que dentro de la función se hace llamada a la funcion [jointCommand](README.md#jointcommand) a travez de un ciclo, donde a este se le entrega el valor de la articulacion dividida en 0.29, esto debido a que este valor es la realcion entre angulos y del registro ( en otras palabras una unidad del resgistro, equivale a 0.29 grados), y luego se le suma un valor offset que no es mas que el valor del registro en su posicion inicial (512 como se menciono antes).  
### jointCommand
``` python
def jointCommand(command, id_num, addr_name, value, time):
    rospy.wait_for_service('dynamixel_workbench/dynamixel_command')
    try:        
        dynamixel_command = rospy.ServiceProxy(
            '/dynamixel_workbench/dynamixel_command', DynamixelCommand)
        result = dynamixel_command(command,id_num,addr_name,value)
        rospy.sleep(time)
        return result.comm_result
    except rospy.ServiceException as exc:
        print(str(exc))
```
La funcion recibe 5 parametros, command, id_num, addr_name,value y time. En este caso command se deje como un string en blanco; id_num el numero de la articulacion, addr_name el string del la función a usar, value el valor del registro objetivo (es decir la posicion final de la articulacion) y time el tiempo en segundos para que ROS se 'duerma' y detecte excepciones. En el codigo se espera a que el comando este disponible, y luego se intenta realizar la accion del servicio.
### listener
``` python
rospy.init_node('joint_listener', anonymous=True)
    rospy.Subscriber("/dynamixel_workbench/joint_states", JointState, callback)
    return
```
Para leer la configuracion actual del robot, se suscribe al topic joint_states que recibe la velocida, torque y posicion de las articulaciones. Estos datos luego son usados en la funcion callback
### callback
``` python
def callback(data):
    global PosActual,PosReal
    PosReal=np.rad2deg(data.position) 
    PosActual=np.subtract(PosReal,np.multiply(offset,0.29))
    return
```
En esta funcion se toma ls informacion brindada por suscriptor, donde solo se toma el valor de la posicion y se traduce a radianes. Hay dos variables globales definidas. Como se menciono anteriormente, se coloca el motor a 150 grados, por lo que se espera que la posicion recibida por el nodo, sea estos 150 más el movimiento realizado. Sin embargo lo mostrado en la realizacion del laboratorio, el nodo ya tiene en cuenta este desfase, por tanto no es necesario tomar el valor con el calculo hecho a mano.
## Comparacion de Configuraciones
### Configuración 1 (Home): 0, 0, 0, 0
![config1](imagenes/pos1M.png)
<img src="imagenes/pos1P.jpg" width=500px>
### Configuración 2: -20, 20, -20, 20
![config1](imagenes/pos2M.png)
<img src="imagenes/pos2P.jpg" width=500px>
### Configuración 3: 30,-30, 30, -30
![config1](imagenes/pos3M.png)
<img src="imagenes/pos3P.jpg" width=500px>
### Configuración 4: -90, 15, -55, 17
![config1](imagenes/pos4M.png)
<img src="imagenes/pos4P.jpg" width=500px>
### Configuración 5: -90, 45, -55, 45
![config1](imagenes/pos4M.png)
<img src="imagenes/pos4P.jpg" width=500px>
