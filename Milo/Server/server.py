from tkinter import *
import threading
import sys
from mainserver import *





ServerRunning = False
server_thread = None



def run_server():
    app.run(port=5000)



def ServerListener():
    global server_thread
    if ServerRunning:
        server_thread = threading.Thread(target=run_server)
        server_thread.daemon = True
        server_thread.start()
    else:
        sys.exit()

    

        

def StartButtonLogic():
    global StartButton
    global ServerRunning
    if ServerRunning == False:
        StartButton.config(bg="dark red",
                        fg="red",
                        text="STOP",
                        activebackground="dark red",
                        activeforeground="red")
        ServerRunning = True
    elif ServerRunning == True:
        StartButton.config(bg="light green",
                        fg="green",
                        text="START",
                        activebackground="light green",
                        activeforeground="green")
        ServerRunning = False
    ServerListener()




root = Tk()

root.geometry("600x600")
root.title("Server Controller")



StartButton = Button(root,
                    text="START",
                    width=11,
                    fg="green",
                    bg="light green",
                    font=("Arial", 70),
                    activeforeground="green",
                    activebackground="light green",
                    command=StartButtonLogic)
StartButton.place(relx=0.5, rely=0.805, anchor=N)





root.mainloop()