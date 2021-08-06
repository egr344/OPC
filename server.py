import time
import random
import logging
from opcua import Server
from threading import Thread


class VarUpdater(Thread):
    def __init__(self, temp, timeWork):
        Thread.__init__(self)
        self.stopMark = False
        self.temp = temp
        self.timeWork = timeWork

    # Функция меняет значения марекра остановки
    def stop(self):
        self.stopMark = True

    # Функция устанавливает значения для температуры и времени работы
    def run(self):
        startTime = time.time()
        while not self.stopMark:
            self.temp.set_value(random.randint(56, 60))
            self.timeWork.set_value("{0:.0f}:{1:02.0f}:{2:02.0f}".format(
                (time.time() - startTime)//3600,
                (time.time() - startTime)//60 % 60,
                (time.time() - startTime) % 60))
            time.sleep(0.1)


try:
    from IPython import embed
except ImportError:
    import code
    # запускает интерактивную консоль
    def embed():
        myvars = globals()
        myvars.update(locals())
        shell = code.InteractiveConsole(myvars)
        shell.interact()

# Останавливает работу сервера и работу потоков, в которых устанавливается значение температуры и времени
def stop_server():
    sensor_1Updater.stop()
    sensor_2Updater.stop()
    sensor_3Updater.stop()
    server.stop()
    print("The server has stopped")

# Запускает работу сервера и работу потоков, в которых устанавливается значение температуры и времени
def start_server():
    server.start()
    sensor_1Updater.start()
    sensor_2Updater.start()
    sensor_3Updater.start()
    print("The server is up")


logging.basicConfig(
    format=u'[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
    level=logging.ERROR)
server = Server()
server.set_endpoint("opc.tcp://localhost:4840")

uri = "MyServerOPC"
idx = server.register_namespace(uri)
node = server.get_objects_node()

sensor_1 = node.add_object(idx, "Sensor_1")
temp_s1 = sensor_1.add_variable(idx, "Tempreture", 0)
velocity_s1 = sensor_1.add_variable(idx, "Velocity", 0)
velocity_s1.set_writable()
force_s1 = sensor_1.add_variable(idx, "Force", 0)
force_s1.set_writable()
time_s1 = sensor_1.add_variable(idx, "Time", 0)

sensor_2 = node.add_object(idx, "Sensor_2")
temp_s2 = sensor_2.add_variable(idx, "Tempreture", 0)
velocity_s2 = sensor_2.add_variable(idx, "Velocity", 0)
velocity_s2.set_writable()
force_s2 = sensor_2.add_variable(idx, "Force", 0)
force_s2.set_writable()
time_s2 = sensor_2.add_variable(idx, "Time", 0)

sensor_3 = node.add_object(idx, "Sensor_3")
temp_s3 = sensor_3.add_variable(idx, "Tempreture", 0)
velocity_s3 = sensor_3.add_variable(idx, "Velocity", 0)
velocity_s3.set_writable()
force_s3 = sensor_3.add_variable(idx, "Force", 0)
force_s3.set_writable()
time_s3 = sensor_3.add_variable(idx, "Time", 0)

sensor_1Updater = VarUpdater(temp_s1, time_s1)
sensor_2Updater = VarUpdater(temp_s2, time_s2)
sensor_3Updater = VarUpdater(temp_s3, time_s3)
try:
    start_server()
    embed()
finally:
    stop_server()
