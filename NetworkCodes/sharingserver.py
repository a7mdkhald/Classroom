from vidstream import StreamingServer
import threading

receiver = StreamingServer('192.168.1.5',9000)

t= threading.Thread(target=receiver.start_server)

t.start()

while input("") !='STOP':
    continue
receiver.stop_server()