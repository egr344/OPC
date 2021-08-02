import logging
import time
from opcua import ua,Client
from threading import Thread

class ParamWriter(Thread):
    def __init__(self,sensorsAndServer):
        Thread.__init__(self)
        self.sensorsAndServer = sensorsAndServer
        self.stopMark = False
    def stop(self):
        self.stopMark = True
    def run(self):
        while not self.stopMark:
            with open("test.txt", "a") as myfile:
                myfile.write("\n")
                for i in range(1,len(sensorsAndServer),1):
                    myfile.write("Sensor {}\n".format(i))
                    for param in sensorsAndServer[i].get_variables():
                        myfile.write("{1}:{2:.2f} ".format(i,param.get_description().to_string(),param.get_value()))
                    myfile.write("\n")
            time.sleep(30)

try:
    from IPython import embed
except ImportError:
    import code

    def embed():
        vars = globals()
        vars.update(locals())
        shell = code.InteractiveConsole(vars)
        shell.interact()

logging.basicConfig(format = u'[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s', level = logging.WARN)
client = Client("opc.tcp://localhost:4840")
try:
    client.connect()
    idx = client.get_namespace_index("MyServerOPC")
    sensorsAndServer = client.get_root_node().get_children()[0].get_children()
    pm = ParamWriter(sensorsAndServer)
    pm.start()
    embed()
finally:
    client.disconnect()
