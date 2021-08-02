import sys
import time
import random
import logging
from opcua import ua,uamethod,Server
from threading import Thread

class VarUpdater(Thread):
    def __init__(self,temp,velocity,timeWork):
        Thread.__init__(self)
        self.stopMark = False
        self.temp = temp
        self.velocity = velocity
        self.timeWork = timeWork

    def stop(self):
        self.stopMark = True

    def run(self):
        startTime = time.time()
        while not self.stopMark:
            self.temp.set_value(random.randint(56,60))
            self.velocity.set_value(random.uniform(0,90))
            self.timeWork.set_value(time.time() - startTime)
            time.sleep(0.1)

try:
    from IPython import embed
except ImportError:
    import code

    def embed():
        myvars = globals()
        myvars.update(locals())
        shell = code.InteractiveConsole(myvars)
        shell.interact()


def stopServer():
    sensor_1Updater.stop()
    sensor_2Updater.stop()
    sensor_3Updater.stop()
    server.stop()
    print("The server has stopped")

def startServer():
    server.start()
    sensor_1Updater.start()
    sensor_2Updater.start()
    sensor_3Updater.start()
    print("The server is up")


logging.basicConfig(format = u'[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s', level = logging.ERROR)
server = Server()
server.set_endpoint("opc.tcp://localhost:4840")
server.set_security_policy([
                ua.SecurityPolicyType.NoSecurity,
                ua.SecurityPolicyType.Basic256Sha256_SignAndEncrypt,
                ua.SecurityPolicyType.Basic256Sha256_Sign])

uri = "MyServerOPC"
idx = server.register_namespace(uri)
node = server.get_objects_node()

sensor_1 = node.add_object(idx,"Sensor_1")
temp_s1 = sensor_1.add_variable(idx,"Tempreture",0)
velocity_s1 = sensor_1.add_variable(idx,"Velocity",0)
time_s1 = sensor_1.add_variable(idx,"Time",0)

sensor_2 = node.add_object(idx,"Sensor_2")
temp_s2 = sensor_2.add_variable(idx,"Tempreture",0)
velocity_s2 = sensor_2.add_variable(idx,"Velocity",0)
time_s2 = sensor_2.add_variable(idx,"Time",0)

sensor_3 = node.add_object(idx,"Sensor_3")
temp_s3 = sensor_3.add_variable(idx,"Tempreture",0)
velocity_s3 = sensor_3.add_variable(idx,"Velocity",0)
time_s3 = sensor_3.add_variable(idx,"Time",0)

sensor_1Updater = VarUpdater(temp_s1,velocity_s1,time_s1)
sensor_2Updater = VarUpdater(temp_s2,velocity_s2,time_s2)
sensor_3Updater = VarUpdater(temp_s3,velocity_s3,time_s3)
try:
    startServer()
    embed()
finally:
    stopServer()
