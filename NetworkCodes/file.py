import PySimpleGUI as sg 
import os.path 

def draw():
    Layout =[[
        sg.FileBrowse()
    ]]
    window = sg.Window("hello",Layout)
    
    while True:
        values = window.read()
        



def main():
    draw()

if __name__ == '__main__':
    main()