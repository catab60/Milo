#-------------------------
import pygame
import tkinter as tk
import win32gui
import win32con
import sys
from PIL import Image, ImageTk
import pickle
import os
#-------------------------


class Engine(tk.Frame):
    def __init__(self, master,x,y, gameClass):
        super().__init__(master=master)
        pygame.init()
        self.screen_height = 700
        self.screen_width = 850

        self.master = master
        self.config(width=self.screen_width, height=self.screen_height)
        
        
        
        self.screen = pygame.display.set_mode((self.screen_width,self.screen_height))
        self.game = gameClass(self.screen)
        self.place(x=x,y=y)
        self.clock = pygame.time.Clock()
        self.IsRunning = True
        self.label = tk.Label(self)
        self.label.place(relx=0.5, rely=0.5, anchor="center")
        self.cnv = tk.Canvas(self, width=self.screen_width, height=self.screen_height, highlightthickness=0)
        self.cnv.pack()
        self.cnv.bind("<Motion>", self.get_position)
        self.cnv.bind("<Button-1>", self.click_press_pos)
        self.img = self.cnv.create_image(0,0,image=None, anchor="nw")
        self.hwnd = pygame.display.get_wm_info()["window"]
        win32gui.SetParent(self.hwnd, self.label.winfo_id())
        win32gui.ShowWindow(self.hwnd, win32con.SW_SHOWNORMAL)
        self.master.after(1, self.update_game)
        self.Gy = 0
        self.Gx = 0
        self.click = False
        self.held_keys = {'Left':False , 'Up' : False , 'Down' : False , 'Right' : False} # asta am schimbat
        self.master.focus_set()
        self.master.bind("<KeyPress>", self.on_key_press)
        self.master.bind("<KeyRelease>", self.on_key_release)


    def get_position(self, event):
        self.Gx = event.x
        self.Gy = event.y

    def Add_Credits(self, k):
        if os.path.exists('data.pkl'):
            with open('data.pkl', 'rb') as f:
                data = pickle.load(f)
        else:
            data = 0
        data += k
        with open('data.pkl', 'wb') as f:
            pickle.dump(data, f)


    def click_press_pos(self, event):
        self.click = True
        self.game.update(self.screen, self.held_keys, self.Gx, self.Gy, self.click, self.Add_Credits)
        self.reset_click()
        

    def reset_click(self):
        self.click = False

        

    def on_key_press(self, event):
        self.held_keys[event.keysym] = True

    def on_key_release(self, event):
        self.held_keys[event.keysym] = False

    def update_game(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        self.game.update(self.screen, self.held_keys, self.Gx, self.Gy, self.click, self.Add_Credits)
        self.reset_click()

        pygame.display.flip()
        self.pygame_image_str = pygame.image.tostring(self.screen, "RGBA")
        self.image = Image.frombytes('RGBA', (self.screen_width,self.screen_height), self.pygame_image_str)
        self.tk_image = ImageTk.PhotoImage(self.image)
        self.cnv.itemconfig(self.img, image=self.tk_image)
        self.master.update()
        try:
            self.master.after(0, self.update_game)
        except:
            pass

        self.clock.tick(60) # aici am schimbat


