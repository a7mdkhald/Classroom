from vidstream import ScreenShareClient
import threading

sender = ScreenShareClient('192.168.33.1',8080)
t= threading.Thread(target=sender.start_stream)

t.start()

while input("") !='STOP':
    continue
sender.stop_stream()