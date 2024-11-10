from tkinter import *
from objects import *

from client import *
from PIL import Image, ImageTk


if not os.path.exists("data.pkl"):
    with open("data.pkl", 'wb') as f:
        pickle.dump(0,f)



drag_data = {"x": 0, "y": 0}

def on_drag_start(event):
    drag_data["x"] = event.x_root
    drag_data["y"] = event.y_root

def on_drag_motion(event):
    delta_x = event.x_root - drag_data["x"]
    delta_y = event.y_root - drag_data["y"]
    
    new_x = root.winfo_x() + delta_x
    new_y = root.winfo_y() + delta_y
    root.geometry(f"+{new_x}+{new_y}")

    drag_data["x"] = event.x_root
    drag_data["y"] = event.y_root


root = Tk()
root.geometry("1200x930")
root.maxsize(1200,930)
root.overrideredirect(True)
root.minsize(1200,930)

root.title("Milo")


AIEngine = MiloAI()
Display = Scrollable(master=root,x=320,y=30)
GameDisp = GameDisplay(master=root, x=320, y=30, GetAds=get_image_from_server)
InfoDisp = InfoDisplay(master=root, x=320,y=30)
AIDispl = AIDisplay(master=root, x=320, y=30, AIEngine=AIEngine)



AllDisplay = [Display, GameDisp, AIDispl]

MenuObj = Menubar(master=root, AllDisplay=AllDisplay)

TitleBar = Frame(root,width=1200,height=30,bg="#212121")
TitleBar.place(x=0, y=0)
Button(TitleBar, text="⬤", fg="#ff6b68", bg="#212121", command=root.destroy, width=3,
       relief="flat", border=0, font=("Arial", 15),
       activebackground="#212121",
       activeforeground="#ab0400").place(x=1165, rely=0.5, anchor=W)

TitleBar.bind("<Button-1>", on_drag_start)
TitleBar.bind("<B1-Motion>", on_drag_motion)

server_responde = download_files()
update_games = get_games()
update_assets = get_images()
posts = len(server_responde)


for i in range(posts):
    display_images = []
    with open(f'appdata/pet_info_{i+1}.json', 'r') as file:
        data = json.load(file)


    for j in range(len(server_responde[str(i+1)])):
        display_images.append((Image.open(f"appdata/image_{i+1}_{j+1}.jpg")))

    Display.add_widgets(Listing(Display, data['pet']['name'], display_images, data, InfoDisp))

print("done")


Display.show_elem()


Display.hide()
Display.show()



print('done2')







root.mainloop()
