from tkinter import *
from vidstream import StreamingServer
from vidstream import ScreenShareClient
import threading


class ClassroomApp:
    def __init__(self, master):
        self.master = master
        master.title("Classroom App")

        # create labels
        self.teacher_label = Label(master, text="Teacher")
        self.student_label = Label(master, text="Student")

        # create entry boxes
        self.teacher_entry = Entry(master)
        self.student_entry = Entry(master)

        # create buttons
        self.connect_button = Button(
            master, text="Start sharing ", command=self.connect1
        )
        self.connect2_button = Button(
            master, text="Start Veiwing ", command=self.connect2
        )
        self.quit_button = Button(master, text="Quit", command=master.quit)

        # layout widgets
        self.teacher_label.grid(row=0, column=0)
        self.teacher_entry.grid(row=0, column=1)
        self.student_label.grid(row=1, column=0)
        self.student_entry.grid(row=1, column=1)
        self.connect_button.grid(row=2, column=0)
        self.connect2_button.grid(row=2 , column=3)
        self.quit_button.grid(row=2, column=1)

    def connect1(self):
        teacher_ip = self.teacher_entry.get()
        student_ip = self.student_entry.get()
        print(f"Connecting {student_ip} to {teacher_ip}")

        # # create a new window for streaming content
        # stream_window = Toplevel(self.master)
        # stream_window.title(f"{teacher_ip}'s Stream")

        # # create a canvas for displaying content
        # stream_canvas = Canvas(stream_window, bg="white", width=800, height=600)
        # stream_canvas.pack(side=LEFT, fill=BOTH, expand=True)

        # # create a scrollbar for the canvas
        # stream_scrollbar = Scrollbar(
        #     stream_window, orient=VERTICAL, command=stream_canvas.yview
        # )
        # stream_scrollbar.pack(side=RIGHT, fill=Y)

        # # configure the canvas to use the scrollbar
        # stream_canvas.configure(yscrollcommand=stream_scrollbar.set)
        # stream_canvas.bind(
        #     "<Configure>",
        #     lambda e: stream_canvas.configure(scrollregion=stream_canvas.bbox("all")),
        # )

        # # create a frame inside the canvas for displaying content
        # stream_frame = Frame(stream_canvas)

        receiver = StreamingServer(teacher_ip,9000)

        t= threading.Thread(target=receiver.start_server)

        t.start()

        while input("") !='STOP':
            continue
        sender.stop_stream()
                


    def connect2(self):
            teacher_ip = self.teacher_entry.get()
            student_ip = self.student_entry.get()
            print(f"Connecting {student_ip} to {teacher_ip}")

            

            sender = ScreenShareClient(student_ip,9000)
            t= threading.Thread(target=sender.start_stream)

            t.start()

            while input("") !='STOP':
                continue
            sender.stop_stream()

                
root = Tk()
my_classroom = ClassroomApp(root)
root.mainloop()
