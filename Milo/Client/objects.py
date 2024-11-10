from tkinter import *
import math
import threading
import inspect
from Engine import *
import webbrowser
import google.generativeai as genai
from PIL import ImageDraw




font = ("Century Gothic", 12)
fontBold = ("Century Gothic", 14, "bold")
fontMenu = ("Century Gothic", 25)

PrimaryColor = "#FFFFFF"
SecondaryColor = "#e7e7e7"
AmbientColor = "#d5d5d5"


class RoundedFrame(tk.Canvas):
    def __init__(self, parent, radius=20, bg="#007acc",back="pink", width=200, height=150, **kwargs):
        super().__init__(parent, width=width, height=height, bg=back, highlightthickness=0, **kwargs)

        self.radius = radius
        self.width = width
        self.height = height
        self.bg = bg


        # Create the rounded frame with rounded corners
        self._create_rounded_frame()

    def _create_rounded_frame(self):
        """Create a rounded frame background."""
        # Create an image for the rounded frame
        frame_image = Image.new("RGBA", (self.width, self.height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(frame_image)

        # Draw the rounded corners manually
        draw.rectangle([self.radius, 0, self.width - self.radius, self.height], fill=self.bg)  # top bar
        draw.rectangle([0, self.radius, self.width, self.height - self.radius], fill=self.bg)  # left & right bars
        draw.pieslice([0, 0, self.radius * 2, self.radius * 2], 180, 270, fill=self.bg)  # top-left corner
        draw.pieslice([self.width - self.radius * 2, 0, self.width, self.radius * 2], 270, 360, fill=self.bg)  # top-right corner
        draw.pieslice([0, self.height - self.radius * 2, self.radius * 2, self.height], 90, 180, fill=self.bg)  # bottom-left corner
        draw.pieslice([self.width - self.radius * 2, self.height - self.radius * 2, self.width, self.height], 0, 90, fill=self.bg)  # bottom-right corner

        # Convert the image to a format Tkinter can use
        self.frame_image = ImageTk.PhotoImage(frame_image)

        # Place the image on the canvas as the background
        self.create_image(0, 0, anchor="nw", image=self.frame_image)

    def add_widget(self, widget, **kwargs):
        """Add a widget to the frame (using place)."""
        widget.place(in_=self, **kwargs)


class RoundedButton(tk.Canvas):
    def __init__(self, parent, text="", radius=20, bg="#007acc", fg="black", fontSize=13, back=AmbientColor, command=None, width=200, height=60):
        super().__init__(parent, width=width, height=height, bg=back, highlightthickness=0)
        
        self.command = command
        self.radius = radius
        self.width = width
        self.height = height
        self.bg = bg
        self.fg = fg
        self.text = text
        self.font = ("Century Gothic",fontSize)

        # Create the button with rounded corners
        self._create_rounded_button()

        # Bind click events
        self.bind("<Button-1>", self._on_click)
        self.bind("<ButtonRelease-1>", self._on_release)

    def _create_rounded_button(self):
        # Create an image for the rounded button
        button_image = Image.new("RGBA", (self.width, self.height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(button_image)

        # Draw a rounded rectangle
        draw.rounded_rectangle(
            [(0, 0), (self.width, self.height)],
            radius=self.radius,
            fill=self.bg
        )

        # Convert the image to a format Tkinter can use
        self.button_image = ImageTk.PhotoImage(button_image)

        # Place the image on the canvas
        self.create_image(0, 0, anchor="nw", image=self.button_image)

        # Add the text to the button
        self.create_text(
            self.width // 2,
            self.height // 2,
            text=self.text,
            fill=self.fg,
            font=self.font
        )

    def _on_click(self, event):
        """Handle button press event."""
        if self.command:
            self.command()

    def _on_release(self, event):
        """Handle button release event."""
        self._create_rounded_button()

class MiloAI():
    def __init__(self):
        genai.configure(api_key="AIzaSyAXZ1Xidj4jh_5Kgf3Z5OblfncTiEh-sMc")
        self.model = genai.GenerativeModel("gemini-1.5-flash")
        
    def ask(self, prompt):
        response = self.model.generate_content(str(prompt))

        return response.text




class Ad_Spot(Frame):
    def __init__(self, master, x, y, GetAds):
        super().__init__(master=master)
        self.master = master
        self.config(height=155, width=850, bg="#212121")
        self.x = x
        self.y = y
        try:
            self.currentAd = GetAds()
        except:
            self.currentAd = None

        self.place_holder = Label(self, text="No Ads Available", font=("Century Gothic", 40, "bold"), bg="#212121", fg=SecondaryColor)
        self.place_holder.place(relx=0.5, rely=0.5, anchor=CENTER)
        try:
            self.ads_holder = Label(self, image=self.currentAd, bg="#212121")
            self.ads_holder.place(x=0,y=0)
        except:
            pass

        self.place(x=self.x,y=self.y)

        




class FullDisplay(Frame):
    def __init__(self, master, x, y, GetAds):
        super().__init__(master=master)
        self.master = master
        self.config(height=900, width=880, bg=SecondaryColor)
        self.x = x
        self.y = y
        self.GetAds = GetAds

        
    
    def HideGame(self):
        try:
            self.GameWindow.place_forget()
            self.backButton.place_forget()
            self.place_forget()
        except:
            pass

    def manager(self, game_ID, gameClass):
        self.lift()
        self.place(x=self.x, y=self.y)
        self.GameWindow = Engine(master=self, x=15,y=15, gameClass=gameClass)
        self.Ad = Ad_Spot(self, x=15, y=730, GetAds=self.GetAds)
        self.backButton = Button(self, text="<", font=("Century Gothic", 24, "bold"), command=self.HideGame,
                                    bg=SecondaryColor,
                                    fg="black",
                                    border=0,
                                    activebackground=SecondaryColor,
                                    activeforeground="black")
        self.backButton.place(x=10, y=0)

class GameObj(Frame):
    def __init__(self, master, FullDisplay, game_ID, gameClass):
        super().__init__(master=master)

        self.config(width=440, height=300, bg=SecondaryColor)

        self.frame = RoundedFrame(self, width=420, height=280, bg=AmbientColor, back=SecondaryColor)
        self.frame.place(relx=0.5, rely=0.5, anchor=CENTER)

        self.bFrame = RoundedFrame(self.frame, width=410, height=270, bg=SecondaryColor, back=AmbientColor)
        self.bFrame.place(relx=0.5, rely=0.5, anchor=CENTER)

        self.imgFrame = RoundedFrame(self.bFrame, width=400,height=195, bg=PrimaryColor, back=SecondaryColor)
        self.imgFrame.place(x=5, y=5)


        self.img = self.resize_and_crop_center(Image.open(f"assets/{game_ID}.png"), target_height=195, target_width=400)
        self.img = ImageTk.PhotoImage(self.img)

        self.banner = Label(self.imgFrame, image=self.img, bg=SecondaryColor)
        self.banner.place(relx=0.5, rely=0.5, anchor=CENTER)


        RoundedButton(self.bFrame, text="P L A Y", command=lambda : FullDisplay.manager(game_ID, gameClass), width=400, fontSize=30, bg=PrimaryColor, back=SecondaryColor).place(relx=0.5, rely=0.87, anchor=CENTER)

    def resize_and_crop_center(self, image, target_width=184, target_height=200, corner_radius=20):
        # Resize the image to fit the target height while maintaining aspect ratio
        aspect_ratio = image.width / image.height
        new_width = int(target_height * aspect_ratio)
        resized_image = image.resize((new_width, target_height), Image.ANTIALIAS)

        # Crop the image to the target width from the center
        left = (new_width - target_width) // 2
        cropped_image = resized_image.crop((left, 0, left + target_width, target_height))

        # Create a new image with an alpha channel (transparent background)
        rounded_image = Image.new("RGBA", (target_width, target_height), (0, 0, 0, 0))

        # Draw rounded corners directly on the image
        mask = Image.new("L", (target_width, target_height), 0)
        draw = ImageDraw.Draw(mask)
        draw.rounded_rectangle([(0, 0), (target_width, target_height)], radius=corner_radius, fill=255)

        # Apply the mask directly to the cropped image
        cropped_image.putalpha(mask)
        rounded_image.paste(cropped_image, (0, 0), cropped_image)

        return rounded_image

class MessageFrame(Frame):
    def __init__(self, parent, text, width, height, is_client, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.text = text
        self.width = width
        self.Gheight = height
        self.font_size = 15
        self.parent = parent

        # Calculate the number of lines the message will take
        self.num_lines = self.calculate_lines(text, width)

        # Calculate the height based on font size and number of lines
        self.height = self.calculate_height(self.num_lines)

        # Container frame for image and text
        content_frame = Frame(self, bg="white")
        content_frame.pack(padx=5, pady=5, fill="both")

        # Load the image
        self.image = ImageTk.PhotoImage(Image.open("AppAssets/MiloAvatar.png"))

        # Add the image on the left
        self.image_label = Label(content_frame, image=self.image, bg="white")
        if not is_client:
            self.image_label.pack(side="left", padx=5, pady=5)

        # Add the text on the right
        self.label = Label(
            content_frame,
            text=self.text,
            font=("Century Gothic", self.font_size),
            wraplength=self.width * 9,
            justify="left",
            bg="white"
        )
        self.label.pack(side="left", padx=10, pady=5)

        # Adjust the parent height
        self.Gheight += self.height + 30
        parent.config(height=self.Gheight)

    def calculate_lines(self, text, width):
        """Calculate the number of lines the message will take based on wraplength and font size."""
        avg_chars_per_line = width * 9 // self.font_size
        num_lines = len(text) // avg_chars_per_line + (1 if len(text) % avg_chars_per_line else 0)
        return num_lines

    def calculate_height(self, num_lines):
        """Calculate the height based on the number of lines and font size."""
        return num_lines * self.font_size + 30

        



class HoverButton(Button):
    def __init__(self, master, hoverColor, **kwargs):
        super().__init__(master,  **kwargs)
        self.default_color = self.cget("background")
        self.hover_color = hoverColor  # Default hover color is lightblue
        
        # Bind the enter and leave events to change button color
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
    
    def on_enter(self, event):
        self.config(background=self.hover_color)
    
    def on_leave(self, event):
        self.config(background=self.default_color)



class AIDisplay(Frame):
    def __init__(self, master, x, y, AIEngine):
        super().__init__(master=master)
        self.master = master
        self.config(height=900, width=880, bg=SecondaryColor)
        self.x = x
        self.y = y



        # Lists to store messages
        self.ClientMessages = []
        self.MiloAIMessages = []

        self.AIEngine = AIEngine

        # Entry box for user input
        self.EntryType = Text(self, height=2, wrap=WORD, bg=AmbientColor,
                              font=("Century Gothic", 20), width=50, bd=0, padx=10, pady=10)
        self.EntryType.place(x=10, y=805)

        # Send button frame
        self.send_holder = Frame(self, height=85, width=80, bg=SecondaryColor)
        self.send_holder.place(x=790, y=805)
        Button(self.send_holder, font=("Century Gothic", 40), text=">",
               relief="flat", border=0, bg="#212121", fg=SecondaryColor,
               highlightbackground="#212121", highlightthickness=0,
               activebackground="#212121", activeforeground=SecondaryColor,
               command=self.send_message).place(relx=0.5, rely=0.5, anchor=CENTER)

        self.DisplayCanvas = Canvas(self, width=870, height=790, bg=SecondaryColor)
        self.DisplayCanvas.place(x=5, y=5)

        self.Scrollbar = Scrollbar(self, orient="vertical", command=self.DisplayCanvas.yview)
        self.Scrollbar.place(x=860, y=5, height=795)

        self.DisplayCanvas.configure(yscrollcommand=self.Scrollbar.set)
        self.MessagesFrame = Frame(self.DisplayCanvas, bg=SecondaryColor, width=850, height=790)
        self.MessagesFrame.pack_propagate(False)
        self.DisplayCanvas.create_window((0, 0), window=self.MessagesFrame, anchor="nw")


        self.MessagesFrame.bind("<Configure>", lambda e: self.DisplayCanvas.configure(scrollregion=self.DisplayCanvas.bbox("all")))

        self.MiloAIMessages.append(f"Hello, I'm MiloAI, your friendly and knowledgeable AI veterinarian expert!")
        self.draw_message(f"Hello, I'm MiloAI, your friendly and knowledgeable AI veterinarian expert!", from_client=False)

    def send_message(self):
        """Handles sending a message and displaying it."""
        client_message = self.EntryType.get("1.0", "end-1c").strip()
        if not client_message:
            return

        # Store and display client message
        self.ClientMessages.append(client_message)
        self.draw_message(client_message, from_client=True)

        def sub_proccess():
            try:
                res = self.AIEngine.ask(prompt=str(client_message))
            except:
                res = "Sorry, I couldn't understand that."
            ai_response = res.replace("\n", "")
            ai_response = ai_response.replace("*", "")
            self.MiloAIMessages.append(ai_response)
            self.draw_message(ai_response, from_client=False)
        threading.Thread(target=sub_proccess).start()

        # Clear the entry box
        self.EntryType.delete("1.0", END)


    def draw_message(self, message, from_client):
        """Draws a message on the canvas."""
        width = 60


        height = self.MessagesFrame.winfo_height()

        self.message_frame = MessageFrame(self.MessagesFrame, message, width, height, from_client)
        self.DisplayCanvas.configure(scrollregion=self.DisplayCanvas.bbox("all"))
        
        

        if from_client:
            self.message_frame.pack(side=TOP, anchor="e", pady=10, fill='y')
        else:
            self.message_frame.pack(side=TOP, anchor="w", pady=10, fill='y')

        
        



        self.DisplayCanvas.update_idletasks()
        self.DisplayCanvas.yview_moveto(1.0)



    def show(self):
        """Show the chatbox."""
        self.place(x=self.x, y=self.y)

    def hide(self):
        """Hide the chatbox."""
        self.place_forget()




class GameDisplay(Frame):
    def __init__(self, master, x, y, GetAds):
        super().__init__(master=master)
        self.master = master
        self.config(height=900, width=880, bg=SecondaryColor)
        self.x = x
        self.y = y

        self.games = []
        import games
        self.ServerGame = [
            cls for name, cls in inspect.getmembers(games, inspect.isclass)
            if cls.__module__ == "games"
        ]

        

        



        self.GameDisp = FullDisplay(master=self, x=0,y=0, GetAds=GetAds)



        for i in range(1,len(self.ServerGame)+1):
            self.add_games(i, self.ServerGame[i-1])


    def add_games(self, game_ID, gameClass):
        row = 1
        col = 1

        for i in range(len(self.games)):
            row+=1
            if row==3:
                col+=1
                row=1


        tempG = GameObj(self, self.GameDisp, game_ID, gameClass)
        tempG.place(x=440*row-440,y=300*col-300)
        
        self.games.append(tempG)


    
    def show(self):
        self.place(x=self.x, y=self.y)

    def hide(self):
        self.place_forget()



class Menubar(Frame):

    class Listing(Frame):
        def __init__(self, master, k, text, commandy):
            super().__init__(master=master)
            self.master = master
            self.config(bg=PrimaryColor, width=320, height=110)
            self.place(x=0, y=k*110-110+47)

            self.frame = Frame(self, width=310, height=100)
            self.frame.place(relx=0.5, rely=0.5, anchor=CENTER)

            HoverButton(self.frame, text=text, font=fontMenu, width=26, height=4,
                command=commandy,bg=PrimaryColor,
                highlightbackground=SecondaryColor,
                highlightcolor=SecondaryColor,
                hoverColor=SecondaryColor).place(relx=0.5, rely=0.5, anchor=CENTER)

    class Logo(Frame):
        def __init__(self, master, k):
            super().__init__(master=master)
            self.master = master
            self.config(bg=PrimaryColor, width=320, height=157)
            self.place(x=0, y=k*110-110)

            #adauga logo
            self.logoImage = ImageTk.PhotoImage(Image.open("AppAssets/MiloSmallLogo.png"))
            Label(self, image=self.logoImage, bg=PrimaryColor).place(relx=0.5, rely=0.5, anchor=CENTER)


    class CurrencyDisplay(Frame):
        def __init__(self,master, k):
            super().__init__(master=master)
            self.master
            self.config(bg=PrimaryColor, width=320, height=110)
            self.place(x=0, y=k*110-110+47)

            self.intCurreny = 0


            self.image = ImageTk.PhotoImage(Image.open("AppAssets/coin.png"))
        

            self.coin_frame = Frame(self, bg=PrimaryColor)
            self.coin_frame.place(relx=0.5, rely=0.5, anchor=CENTER)



            self.coin = Label(self.coin_frame, image=self.image, bg="white")
            self.coin.pack(side=LEFT, padx=(0, 10))


            self.intCurrency = 100
            self.label = Label(self.coin_frame, text=str(self.intCurrency), font=("Century Gothic", 30), bg="white")
            self.label.pack(side=LEFT)


        def load_data(self):

            if os.path.exists('data.pkl'):
                with open('data.pkl', 'rb') as f:
                    data = pickle.load(f)
                return data
            else:
                return 0

        def update_currency(self):
            self.intCurreny = self.load_data()
            self.label.config(text=str(self.intCurreny))

            self.after(1000, self.update_currency)



    def __init__(self, master, AllDisplay):
        super().__init__(master=master)
        self.master = master
        self.config(bg=PrimaryColor, width=320, height=900)

        self.AllDisplay = AllDisplay

        self.widgets = []

        self.place(x=0, y=30)

        self.CurrentLogo = self.Logo(self, 1)
        self.CurrencyTab = None
        self.Browse()


    def HideAllDisplay(self):
        for i in self.AllDisplay:
            i.hide()
    
    


    def ShowBrowse(self):
        self.remove_widgets()
        self.HideAllDisplay()
        self.AllDisplay[0].show()
        self.CurrentLogo = self.Logo(self, 1)
        self.Browse()
            
    def ShowGames(self):
        self.remove_widgets()
        self.HideAllDisplay()
        self.AllDisplay[1].show()
        self.CurrentLogo = self.Logo(self,1)
        self.Games()

    def ShowAI(self):
        self.remove_widgets()
        self.HideAllDisplay()
        self.AllDisplay[2].show()
        self.CurrentLogo = self.Logo(self,1)
        self.AI()


    def Browse(self):
        self.add_widgets(3.2,"Browse", self.ShowBrowse)
        self.add_widgets(4.2,"Play&Help", self.ShowGames)
        self.add_widgets(5.2,"MiloAI", self.ShowAI)
        self.CurrencyTab = self.CurrencyDisplay(self, 7.5)
        self.CurrencyTab.update_currency()

    def Games(self):
        self.add_widgets(3.2,"Browse", self.ShowBrowse)
        self.add_widgets(4.2,"Play&Help", self.ShowGames)
        self.add_widgets(5.2,"MiloAI", self.ShowAI)
        self.CurrencyTab = self.CurrencyDisplay(self, 7.5)
        self.CurrencyTab.update_currency()
    
    def AI(self):
        self.add_widgets(3.2, "Browse", self.ShowBrowse)
        self.add_widgets(4.2,"Play&Help", self.ShowGames)
        self.add_widgets(5.2,"MiloAI", self.ShowAI)
        self.CurrencyTab = self.CurrencyDisplay(self, 7.5)
        self.CurrencyTab.update_currency()

    


    def add_widgets(self, k, text, command):
        self.widgets.append(self.Listing(self, k, text, command))
    
    def remove_widgets(self):
        for i in range(len(self.widgets)):
            try:
                self.widgets[i].place_forget()
                self.widgets.pop(i)
            except:
                pass
        try:
            self.CurrentLogo.place_forget()
        except:
            pass
        try:
            self.CurrencyTab.place_forget()
        except:
            pass

        
        
                



class ImageShow(Frame):
    def __init__(self, master, imagesList):
        super().__init__(master=master)
        self.master = master

        self.InsideFrame = Frame(self, bg=AmbientColor, height=590, width=630)
        self.InsideFrame.place(relx=0.5, rely=0.5, anchor=CENTER)

        self.Images = imagesList
        self.imageK = 0

        
        self.CurrentImage = ImageTk.PhotoImage(self.resize_and_crop_center(self.Images[self.imageK], target_height=590, target_width=630, corner_radius=0))


        self.ImageLabel = Label(self.InsideFrame, image=self.CurrentImage, relief="flat", border=0)
        self.ImageLabel.place(relx=0.5, rely=0.5, anchor=CENTER)

        

        Button(self, text=">", command=lambda : self.change_image(">"),
               relief="flat",
               border=0,
               bg="#212121",
               fg=SecondaryColor,
               highlightbackground="#212121",
               highlightthickness=0,
               activebackground="#212121",
               font=("Century Gothic", 20, "bold"),
               activeforeground=SecondaryColor).place(relx=0.95, rely=0.5, anchor=CENTER)
        Button(self, text="<", command=lambda : self.change_image("<"),
               relief="flat",
               border=0,
               bg="#212121",
               fg=SecondaryColor,
               highlightbackground="#212121",
               highlightthickness=0,
               activebackground="#212121",
               font=("Century Gothic", 20, "bold"),
               activeforeground=SecondaryColor).place(relx=0.05, rely=0.5, anchor=CENTER)
        self.config(bg=AmbientColor, height=600, width=640)
    
    def resize_and_crop_center(self, image, target_width=184, target_height=200, corner_radius=20):
        # Resize the image to fit the target height while maintaining aspect ratio
        aspect_ratio = image.width / image.height
        new_width = int(target_height * aspect_ratio)
        resized_image = image.resize((new_width, target_height), Image.ANTIALIAS)

        # Crop the image to the target width from the center
        left = (new_width - target_width) // 2
        cropped_image = resized_image.crop((left, 0, left + target_width, target_height))

        # Create a new image with an alpha channel (transparent background)
        rounded_image = Image.new("RGBA", (target_width, target_height), (0, 0, 0, 0))

        # Draw rounded corners directly on the image
        mask = Image.new("L", (target_width, target_height), 0)
        draw = ImageDraw.Draw(mask)
        draw.rounded_rectangle([(0, 0), (target_width, target_height)], radius=corner_radius, fill=255)

        # Apply the mask directly to the cropped image
        cropped_image.putalpha(mask)
        rounded_image.paste(cropped_image, (0, 0), cropped_image)

        return rounded_image

    def change_image(self, gId):

        if gId == "<":
            self.imageK +=1

            if self.imageK == len(self.Images):
                self.imageK = 0
            self.NextImge = ImageTk.PhotoImage(self.resize_and_crop_center(self.Images[self.imageK], target_height=590, target_width=630, corner_radius=0))
            self.ImageLabel.config(image=self.NextImge)
        elif gId == ">":
            self.imageK -= 1

            if self.imageK == -1:
                self.imageK = len(self.Images)-1
            self.NextImge = ImageTk.PhotoImage(self.resize_and_crop_center(self.Images[self.imageK], target_height=590, target_width=630, corner_radius=0))
            self.ImageLabel.config(image=self.NextImge)


class ShelterObject(Frame):
    def __init__(self, master, x, data):
        super().__init__(master=master)
        self.master = master

        self.config(bg=AmbientColor, width=320, height=180)


        self.x = x
        self.y = 0

        self.frame = Frame(self, bg=SecondaryColor, width=310, height=170)
        self.frame.place(relx=0.5, rely=0.5, anchor=CENTER)

        Label(self.frame, text=f"E-mail: {data['shelter']['contact']['email']}", font=("Century Gothic", 11), bg=SecondaryColor).place(x=0, y=-5)
        Label(self.frame, text=f"Phone: {data['shelter']['contact']['phone']}", font=("Century Gothic", 11), bg=SecondaryColor).place(x=0, y=20)
        Label(self.frame, text=f"Website: {data['shelter']['contact']['website']}", font=("Century Gothic", 11), bg=SecondaryColor).place(x=0, y=45)

        Label(self.frame, text=f"Address: {data['shelter']['location']['address']}", font=("Century Gothic", 11), bg=SecondaryColor).place(x=0, y=70)
        Label(self.frame, text=f"City: {data['shelter']['location']['city']}", font=("Century Gothic", 11), bg=SecondaryColor).place(x=0, y=95)
        Label(self.frame, text=f"State: {data['shelter']['location']['state']}", font=("Century Gothic",11), bg=SecondaryColor).place(x=0, y=120)
        Label(self.frame, text=f"Zipcode: {data['shelter']['location']['zip']}", font=("Century Gothic", 11), bg=SecondaryColor).place(x=0, y=145)
    
    def show(self):
        self.place(x=self.x, y=self.y)
    
    def hide(self):
        self.place_forget()

        
class ContactObject(Frame):
    def __init__(self, master, x, data):
        super().__init__(master=master)
        self.master = master

        self.config(bg=AmbientColor, width=320, height=180)

        self.x = x
        self.y = 0

        self.frame = Frame(self, bg=SecondaryColor, width=310, height=170)
        self.frame.place(relx=0.5, rely=0.5, anchor=CENTER)

        Label(self.frame, text=f"{data['shelter']['name']}", bg=SecondaryColor, font=("Century Gothic", 30)).place(relx=0.5, rely=0.1, anchor=N)
        RoundedButton(self, text="Contact", fontSize=20,
               bg="#212121",
               fg=SecondaryColor,
               width=200,
               back=SecondaryColor,
               command=lambda : self.ContactOpen(data['shelter']['contact']['website'])).place(relx=0.5, rely=0.7, anchor=CENTER)

    def ContactOpen(self, website):
        try:
            webbrowser.open(website)
        except:
            pass

    def show(self):
        self.place(x=self.x ,y=self.y)

    def hide(self):
        self.place_forget()


class DetailObject(Frame):
    def __init__(self, master, y, text, var, font, fontB):
        super().__init__(master=master)
        self.master = master

        self.x = 0
        self.y = y
        
        

        self.config(bg=AmbientColor, width=180, height=80)


        self.frame = Frame(self, bg="#BBBBBB", width=170, height=70)
        self.frame.place(relx=0.5, rely=0.5, anchor=CENTER)

        Label(self.frame, text=text, font=fontB, bg="#BBBBBB").place(relx=0.5, rely=0.3, anchor=CENTER)
        Label(self.frame, text=var, font=font, bg="#BBBBBB").place(relx=0.5, rely=0.7, anchor=CENTER)
    
    def show(self):
        self.place(x=self.x, y=self.y)

    def hide(self):
        self.place_forget()
    





class Listing(Frame):
    def __init__(self, master, title, images, data, InfoDisp):
        super().__init__(master)
        self.master = master
        self.title = str(title)
        self.images = images
        self.data = data
        self.InfoDisp = InfoDisp

        self.outline_thickness_X = 10
        self.outline_thickness_Y = 10
        self.width = 200
        self.height = 280

        self.config(width=self.width + (int(self.outline_thickness_X * 2)),
                    height=self.height + (int(self.outline_thickness_Y * 2)),
                    background=SecondaryColor)  # Replace with your desired background color

        self.create_widget()

    def create_widget(self):
        # Create and position the border frame with rounded corners
        self.Border = RoundedFrame(self, width=self.width + 10, height=self.height + 10, bg=AmbientColor, back=SecondaryColor)
        self.Border.place(relx=0.5, rely=0.5, anchor="center")

        # Create and position the main frame with rounded corners
        self.MainFrame = RoundedFrame(self.Border, width=self.width, height=self.height, bg=SecondaryColor, back=AmbientColor)
        self.MainFrame.place(relx=0.5, rely=0.5, anchor="center")

        # Create the action bar at the bottom of the main frame
        self.ActionBar = Frame(self.MainFrame, width=200, height=70, bg=AmbientColor)
        self.ActionBar.place(relx=0.5, y=215, anchor="n")

        # Label with title
        self.lbl = RoundedFrame(self.ActionBar, bg=SecondaryColor, back=AmbientColor, width=200, height=50)
        self.lbl.place(relx=0.5, y=28, anchor="s")
        Label(self.lbl, text=self.title, font=("Century Gothic", 16, "bold"),fg="#212121", bg=SecondaryColor, width=12).place(relx=0.5, rely=0.635, anchor=CENTER)


        RoundedButton(self.ActionBar, text="VIEW", command=lambda: self.InfoDisp.manager(self.data, self.images, "Info"),
                      width=165, height=30, bg=SecondaryColor, fg="black").place(x=0, rely=0.7, anchor="w")

        # Donation sub-frame and button
        self.donateSub = Frame(self.ActionBar, width=36, height=36, bg=AmbientColor)
        self.donateSub.place(x=169, rely=0.7, anchor="w")
        RoundedButton(self.donateSub, text="$", command=lambda: self.InfoDisp.manager(self.data, self.images, "Donate"),
                      width=26, radius=20, height=30, bg=SecondaryColor, fg="black").place(x=2, y=2)

        # Image sub-frame for displaying the image
        self.TempImage = self.resize_and_crop_center(self.images[0])
        self.CurrentImage = ImageTk.PhotoImage(self.TempImage)

        sub = Frame(self, width=184, height=200, bg="blue")  # Replace with your desired color
        sub.place(relx=0.5, rely=0.39, anchor="center")
        Label(sub, image=self.CurrentImage, bg=SecondaryColor).place(relx=0.5, rely=0.5, anchor="center")

    def resize_and_crop_center(self, image, target_width=184, target_height=200, corner_radius=20):
        # Resize the image to fit the target height while maintaining aspect ratio
        aspect_ratio = image.width / image.height
        new_width = int(target_height * aspect_ratio)
        resized_image = image.resize((new_width, target_height), Image.ANTIALIAS)

        # Crop the image to the target width from the center
        left = (new_width - target_width) // 2
        cropped_image = resized_image.crop((left, 0, left + target_width, target_height))

        # Create a new image with an alpha channel (transparent background)
        rounded_image = Image.new("RGBA", (target_width, target_height), (0, 0, 0, 0))

        # Draw rounded corners directly on the image
        mask = Image.new("L", (target_width, target_height), 0)
        draw = ImageDraw.Draw(mask)
        draw.rounded_rectangle([(0, 0), (target_width, target_height)], radius=corner_radius, fill=255)

        # Apply the mask directly to the cropped image
        cropped_image.putalpha(mask)
        rounded_image.paste(cropped_image, (0, 0), cropped_image)

        return rounded_image


class DonateWidget(Frame):
    def __init__(self, master,x,y, data, text, price, imagePath):
        super().__init__(master=master)
        self.config(height=158, width=440, bg=SecondaryColor)
        self.x = x
        self.y = y

        

        self.frame = Frame(self, bg=AmbientColor, width=430, height=148)
        self.frame.place(relx=0.5, rely=0.5, anchor=CENTER)

        self.sub = Frame(self.frame, bg=SecondaryColor, width=420, height=138)
        self.sub.place(relx=0.5, rely=0.5, anchor=CENTER)

        self.imageFrame = Frame(self.sub, bg=AmbientColor, width=128, height=128)
        self.imageFrame.place(x=5, y=5)

        try:
            self.Aimage = ImageTk.PhotoImage(Image.open(imagePath).resize((118, 118)))
            self.image = Label(self.imageFrame, image=self.Aimage)
            self.image.place(relx=0.5, rely=0.5, anchor=CENTER)
        except:
            pass
        Label(self.sub, text=text, font=("Century Gothic", 15), bg=SecondaryColor).place(relx=0.35, rely=0.5, anchor=W)
        self.btn = Button(
            self.sub,
            text=str(price),
            font=("Century Gothic", 25),
            width=5,
            relief="flat",
            border=0,
            bg="#212121",
            fg=SecondaryColor,
            highlightbackground="#212121",
            highlightthickness=0,
            activebackground="#212121",
            activeforeground=SecondaryColor,
        )
        self.btn.config(command=lambda btn=self.btn: self.buy(btn, int(price)))
        self.btn.place(relx=0.8, rely=0.5, anchor=CENTER)



        self.place(x=self.x, y=self.y)

    def buy(self, btn, price):
        if self.load_data() > price:
            btn.config(bg="#00fb68", fg="white", text="✔")
            self.update_data(price)


    def hide(self):
        self.place_forget()

    def load_data(self):
        if os.path.exists('data.pkl'):
            with open('data.pkl', 'rb') as f:
                data = pickle.load(f)
            return data
        else:
            return 0
        
    def update_data(self, N):
        """Remove N from the loaded data and overwrite the changes to 'data.pkl'."""
        # Load current data
        data = self.load_data()

        
        # Ensure the data is an integer
        if isinstance(data, int):
            # Subtract N from the loaded data
            updated_data = data - N
            
            # Overwrite the data in the file
            with open('data.pkl', 'wb') as f:
                pickle.dump(updated_data, f)
            
            print(f"Updated data: {updated_data}")
        else:
            print("Error: Loaded data is not an integer.")




class InfoDisplay(Frame):
    def __init__(self, master, x, y):
        super().__init__(master=master)
        self.master = master
        self.config(height=900, width=880, bg=SecondaryColor)
        self.x = x
        self.y = y

    def hideAll(self):
        try:

            self.title.place_forget()

            self.type.hide()
            self.age.hide()
            self.weight.hide()
            self.sex.hide()
            self.breed.hide()
            self.color.hide()
            self.vaccinated.hide()
            self.microchipped.hide()
            self.neutered.hide()
            self.fee.hide()

            self.animaldetail.place_forget()
            self.shelterdetail.place_forget()
            self.shelterWidget.hide()
            self.contactWidget.hide()

            self.img.place_forget()

            self.backButtton.place_forget()

            self.place_forget()
        except:
            pass

        try:
            self.backButton.place_forget()
            self.title.place_forget()
            self.place_forget()

            self.d1.hide()
            self.d2.hide()
            self.d3.hide()
            self.d4.hide()
            self.d5.hide()
            self.d6.hide()
            self.d7.hide()
            self.d8.hide()
            self.d9.hide()
            self.d10.hide()
        except:
            pass





    def manager(self, data, images, option):
        if option == "Info":

            self.backButton = Button(self, text="<", font=("Century Gothic", 20, "bold"), command=self.hideAll,
                                    bg=SecondaryColor,
                                    fg="black",
                                    border=0,
                                    activebackground=SecondaryColor,
                                    activeforeground="black")
            self.backButton.place(x=20, y=20)
        
            self.title = Label(self, text=data['pet']['name'], font=("Century Gothic", 30, "bold"), bg=SecondaryColor)
            self.title.place(x=80, y=20)

            self.img  = ImageShow(self, images)
            self.img.place(x=20, y=80)

            

            self.animaldetail = Frame(self, bg="yellow", height=800, width=180)
            self.animaldetail.place(x=680, y=80)
            

            self.shelterdetail = Frame(self, bg="purple", height=180, width=640)
            self.shelterdetail.place(x=20, y=700)

            self.type = DetailObject(self.animaldetail,1*80-80,text="Type",var=data['pet']['details']['type'], font=font, fontB=fontBold)
            self.age = DetailObject(self.animaldetail,2*80-80,text="Age",var=f"{data['pet']['details']['age']} Year Old", font=font, fontB=fontBold)
            self.weight = DetailObject(self.animaldetail,3*80-80,text="Weight",var=f"{data['pet']['details']['weight']} KG", font=font, fontB=fontBold)
            self.sex = DetailObject(self.animaldetail,4*80-80,text="Sex",var=data['pet']['details']['sex'], font=font, fontB=fontBold)
            self.breed = DetailObject(self.animaldetail,5*80-80,text="Breed",var=data['pet']['details']['breed'], font=font, fontB=fontBold)
            self.color = DetailObject(self.animaldetail,6*80-80,text="Color",var=data['pet']['details']['color'], font=font, fontB=fontBold)
            self.vaccinated = DetailObject(self.animaldetail,7*80-80,text="Vaccinated",var="Yes" if data['pet']['details']['vaccinated'] == 1 else "No", font=font, fontB=fontBold)
            self.microchipped = DetailObject(self.animaldetail,8*80-80,text="Microchipped",var="Yes" if data['pet']['details']['microchipped'] == 1 else "No", font=font, fontB=fontBold)
            self.neutered = DetailObject(self.animaldetail,9*80-80,text="Neutered",var="Yes" if data['pet']['details']['spayed_neutered'] == 1 else "No", font=font, fontB=fontBold)
            self.fee = DetailObject(self.animaldetail,10*80-80,text="Adoption Fee",var=f"{data['pet']['details']['adoption_fee']}€", font=font, fontB=fontBold)

            self.type.show()
            self.age.show()
            self.weight.show()
            self.sex.show()
            self.breed.show()
            self.color.show()
            self.vaccinated.show()
            self.microchipped.show()
            self.neutered.show()
            self.fee.show()


            

            self.shelterWidget = ShelterObject(self.shelterdetail, 0, data)
            self.shelterWidget.show()

            self.contactWidget = ContactObject(self.shelterdetail, 320, data)
            self.contactWidget.show()

            self.place(x=self.x, y=self.y)

        elif option == "Donate":

            self.backButton = Button(self, text="<", font=("Century Gothic", 24, "bold"), command=self.hideAll,
                                    bg=SecondaryColor,
                                    fg="black",
                                    border=0,
                                    activebackground=SecondaryColor,
                                    activeforeground="black")
            self.backButton.place(x=20, y=20)

            self.title = Label(self, text=data['pet']['name'], font=("Century Gothic", 40), bg=SecondaryColor)
            self.title.place(relx=0.5, y=20, anchor=N)



            #158 440 
            self.d1 = DonateWidget(self, 0*440, 110+(0*158), data, "Food /day", 5000, "AppAssets/Food.png")
            self.d2 = DonateWidget(self, 0*440, 110+(1*158), data, "Toy Ball", 5000, "AppAssets/Bal.png")
            self.d3 = DonateWidget(self, 0*440, 110+(2*158), data, "Medicine", 10000, "AppAssets/Med2.png")
            self.d4 = DonateWidget(self, 0*440, 110+(3*158), data, "Vet Care", 20000, "AppAssets/Med.png")
            self.d5 = DonateWidget(self, 0*440, 110+(4*158), data, "Bed", 10000, "AppAssets/Bed.png")

            self.d6 = DonateWidget(self, 1*440, 110+(0*158), data, "Plushie", 7500, "AppAssets/Plu.png")
            self.d7 = DonateWidget(self, 1*440, 110+(1*158), data, "Leash", 4000, "AppAssets/Col.png")
            self.d8 = DonateWidget(self, 1*440, 110+(2*158), data, "Clothes", 10000, "AppAssets/Clo.png")
            self.d9 = DonateWidget(self, 1*440, 110+(3*158), data, "Snack", 1000, "AppAssets/Foo.png")
            self.d10 = DonateWidget(self, 1*440, 110+(4*158), data, "Hygiene", 5000, "AppAssets/Car.png")



            self.place(x=self.x, y=self.y)

    def load_data(self):

            if os.path.exists('data.pkl'):
                with open('data.pkl', 'rb') as f:
                    data = pickle.load(f)
                return data
            else:
                return 0

    def update_currency(self):
        self.intCurreny = self.load_data()
        self.label.config(text=str(self.intCurreny))

        self.after(1000, self.update_currency)


    








class Scrollable(Frame):
    def __init__(self, master, x, y):
        super().__init__(master)
        self.master = master

        self.x = x
        self.y = y

        self.widgets = []
        self.scroll_factor = 20

        self.first_elem = None
        self.last_elem = None

        self.elem_pos = []

        self.config(height=900, width=880, background=SecondaryColor)
        self.place(x=self.x,y=self.y)

        self.bind("<MouseWheel>", self.scroll_win64)
        self.bind("<Button-4>", self.scroll_up_linx)
        self.bind("<Button-5>", self.scroll_down_linx)

    def hide(self):
        self.place_forget()
    
    def show(self):
        self.place(x=self.x, y=self.y)

    def add_widgets(self, widget):

        def get_all_children(widget):
            kids = widget.winfo_children()
            for child in kids:
                kids.extend(get_all_children(child))
            return kids
        kids = get_all_children(widget)
        number_of_widgets = len(self.widgets)
        self.widgets.append(widget)



        if number_of_widgets == 0:
            self.first_elem = self.widgets[0]
        self.last_elem = widget

        widget.bind("<MouseWheel>", self.scroll_win64)
        widget.bind("<Button-4>", self.scroll_up_linx)
        widget.bind("<Button-5>", self.scroll_down_linx)

        for i in kids:
            i.bind("<MouseWheel>", self.scroll_win64)
            i.bind("<Button-4>", self.scroll_up_linx)
            i.bind("<Button-5>", self.scroll_down_linx)

    
    def scroll_win64(self, event):
        if event.delta > 0:
            if self.first_elem.winfo_y()<0:
                for kid in range(len(self.widgets)):
                    try:
                        if self.elem_pos[kid] > -500:
                            self.widgets[kid].place(x=self.widgets[kid].winfo_x(),y=self.elem_pos[kid]+self.scroll_factor)
                        self.elem_pos[kid] = self.elem_pos[kid]+self.scroll_factor
                    except:
                        pass

            try:
                self.load_unload()
            except:
                pass
            
        else:
            if self.last_elem.winfo_y() + self.last_elem.height+self.last_elem.outline_thickness_X*2 > self.winfo_height():
                for kid in range(len(self.widgets)):
                    try:
                        self.widgets[kid].place(x=self.widgets[kid].winfo_x(),y=self.elem_pos[kid]-self.scroll_factor)
                        self.elem_pos[kid] = self.elem_pos[kid]-self.scroll_factor
                    except:
                        pass
            try:
                self.load_unload()
            except:
                pass

    def scroll_down_linx(self, event):
        if self.last_elem.winfo_y() + self.last_elem.height+self.last_elem.outline_thickness_X*2 > self.winfo_height():
            for kid in range(len(self.widgets)):
                try:
                    self.widgets[kid].place(x=self.widgets[kid].winfo_x(),y=self.elem_pos[kid]-self.scroll_factor)
                    self.elem_pos[kid] = self.elem_pos[kid]-self.scroll_factor
                except:
                    pass

        try:
            self.load_unload()
        except:
            pass


    def scroll_up_linx(self, event):
        if self.first_elem.winfo_y()<0:
            for kid in range(len(self.widgets)):
                try:
                    if self.elem_pos[kid] > -500:
                        self.widgets[kid].place(x=self.widgets[kid].winfo_x(),y=self.elem_pos[kid]+self.scroll_factor)
                    self.elem_pos[kid] = self.elem_pos[kid]+self.scroll_factor
                except:
                    pass

        try:
            self.load_unload()
        except:
            pass

    
    def load_unload(self):
        height_limit_lower = -500
        height_limit_upper = self.winfo_height() + 500
        

        widgets_to_unload = [
            self.widgets[i] for i in range(len(self.widgets))
            if self.elem_pos[i] < height_limit_lower or self.elem_pos[i] > height_limit_upper
        ]
        

        for widget in widgets_to_unload:
            widget.place_forget()
        

    



    def show_elem(self):
        def sub_procces():
            row = -1
            col = 0
            widgets_per_row = 4
            self.rows = math.ceil(len(self.widgets) / widgets_per_row)

            for k, widget in enumerate(self.widgets):
                if k % widgets_per_row == 0:
                    row += 1
                    col = 0
                else:
                    col += 1

                pos_x = col * (widget.width + 2 * widget.outline_thickness_X)
                pos_y = row * (widget.height + 2 * widget.outline_thickness_Y)

                widget.place(x=pos_x, y=pos_y)
                self.elem_pos.append(pos_y)

            self.update()

        threading.Thread(target=sub_procces).start()

        




        
        
