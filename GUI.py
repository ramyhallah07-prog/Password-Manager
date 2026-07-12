#what I'm gion to do is basecally build a windows for each task then I'm goin to start linking them with CLI or even better PasswordManager
from tkinter import *
from tkinter import ttk
import customtkinter as ctk
from password_manager import CLI

def main():
    pm = Login_Menu()
    pm.mainloop()
#Creat Login menu
class Login_Menu(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title('VAULT PasswordManager')
        self.geometry('810x980')
        self.wm_iconbitmap('logo.ico')
        self.frame = ctk.CTkFrame(self)
        self.frame.configure
        self.frame.grid(row = 1, column = 0, sticky = 'nsew')
        self._username = ctk.CTkEntry(self.frame, placeholder_text='Enter Username')
        self._username.grid(row = 0, column = 0, pady = (20, 10), padx = 15)
        self._password = ctk.CTkEntry(self.frame, placeholder_text='Enter Password', show='*')
        self._password.grid(row = 1, column = 0, pady = (10, 5), padx= 15)
        self._show_password = ctk.CTkCheckBox(self.frame, height=10, width=10, corner_radius=10, text = 'Show password', command=self.show_password, onvalue=1, offvalue=0)
        self._show_password.grid(row = 2, column = 0, sticky = 'w', pady= (0,10), padx= 15)

    def show_password(self):
        if self._show_password.get() == 1:
            self._password.configure(show='')
        if self._show_password.get() == 0:
            self._password.configure(show='*')


#creat main menu





#creat settings menu







#connect with CLI




if __name__ == '__main__':
    main()