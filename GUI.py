#what I'm gion to do is basecally build a windows for each task then I'm goin to start linking them with CLI or even better PasswordManager
import tkinter as tk
from tkinter import PhotoImage
import customtkinter as ctk
from password_manager import GUI
from PIL import Image
import os
from Fonts_and_Colors import *




def main():
    paswordmanager = App()
     


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title('The Vault')
        self.geometry('800x800')
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.iconbitmap(os.path.join(base_dir, 'Design', 'Logos', 'Vault_main_logo_vector.ico'))
        menu = LoginMenu(self)
        menu.layout()








        # run
        self.mainloop()


class LoginMenu(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent, fg_color= PRIMARY_COLOR)
        #banner
        image = Image.open('Design/Logos/Vault_banner_vector.png')
        banner_image = ctk.CTkImage(light_image=image,
                                    dark_image=image,
                                    size=(800,200))
        self.banner = ctk.CTkLabel(self, image=banner_image, text='')
        self.banner.bind('<Configure>', lambda event: (banner_image.configure(size=(event.width, 250)) if banner_image.cget('size')[0] != event.width and event.widget == self else None))

        #VARIABLES
        uservar = tk.StringVar(value=' ')
        passvar = tk.StringVar(value='')





        #Login entrys
        self.log_setup = ctk.CTkFrame(self, fg_color=SURFACE_COLOR)
        username = ctk.CTkLabel(self.log_setup, 
                                fg_color='transparent', 
                                text='Username', 
                                font=TITLE_SMALL)
        self.username_entry = ctk.CTkEntry(self.log_setup, 
                                      placeholder_text='Enter Your Username',
                                      font=ENTRY)
        password = ctk.CTkLabel(self.log_setup, 
                                fg_color='transparent', 
                                text='Password', 
                                font=TITLE_SMALL)
        self.password_entry = ctk.CTkEntry(self.log_setup, 
                                      placeholder_text='Enter Your Password', 
                                      font=ENTRY,
                                      show='*')
        log_button = ctk.CTkButton(self.log_setup, 
                                   text='LogIn', 
                                   text_color= TEXT_COLOR, 
                                   fg_color=ACCENT_COLOR, 
                                   hover_color=HOVER_COLOR, 
                                   font=BODY_LARGE, 
                                   command= self.log_in)
        self.forgetpassword_frame = ctk.CTkFrame(self.log_setup, fg_color=SURFACE_COLOR)
        self.forget_password = ctk.CTkButton(self.forgetpassword_frame, 
                                        text= 'forget password',
                                        text_color= TEXT_COLOR,
                                        fg_color='transparent',
                                        hover_color= SURFACE_COLOR,
                                        font=LABEL,
                                        command= self.forgot_password)
        self.create_account =  ctk.CTkButton(self.forgetpassword_frame, 
                                        text= 'Create Account',
                                        text_color= TEXT_COLOR,
                                        fg_color='transparent',
                                        hover_color= SURFACE_COLOR,
                                        font=LABEL,
                                        command= self.create_acc)
        self.bottom = ctk.CTkFrame(self, fg_color=SURFACE_COLOR)

        #logics:
        self.username_entry.bind('<KeyPress-Return>', self.go_password)
        self.password_entry.bind('<KeyPress-Return>', self.go_login)
        self.forget_password.bind('<Enter>', lambda e: self.forget_password.configure(text_color = HOVER_COLOR))
        self.forget_password.bind('<Leave>', lambda e: self.forget_password.configure(text_color = TEXT_COLOR))
        self.create_account.bind('<Enter>', lambda e: self.create_account.configure(text_color = HOVER_COLOR))
        self.create_account.bind('<Leave>', lambda e: self.create_account.configure(text_color = TEXT_COLOR))







        #layouts
        self.log_setup.rowconfigure((0,1,2,3,4,5), weight=1, uniform='a')
        self.log_setup.columnconfigure((0,1,2,3), weight=1)
        username.grid(row=0, column=1, sticky= 'sw', columnspan= 2,pady=10)
        self.username_entry.grid(row=1, column=1, sticky= 'nwe', columnspan= 2,pady=10)
        password.grid(row=2, column=1, sticky= 'sw', columnspan= 2,pady=10)
        self.password_entry.grid(row=3, column=1, sticky= 'nwe', columnspan= 2,pady=10)
        log_button.grid(row= 4, column=0, sticky='s', columnspan=4)
        self.forget_password.pack(side='left', fill='x')
        self.create_account.pack(side='left', fill='x')
        self.forgetpassword_frame.grid(row= 5, column = 1, sticky='n', columnspan=2, pady=30)



        self.pack(fill='both', expand=True)


    def layout(self):
        self.banner.pack(fill='x')
        self.log_setup.pack(expand=True, fill='both')
        self.bottom.pack(fill='both')

    def layout_forget(self):
        self.banner.pack_forget()
        self.log_setup.pack_forget()
        self.bottom.pack_forget()

    def go_password(self, event):
        self.password_entry.focus_set()

    def go_login(self, event):
        self.log_in()

    def log_in(self):
        print(self.username_entry.get()+"\n"+self.password_entry.get())

    def forgot_password(self):
        print(f'{self.username_entry.get()} forget your password')

    def create_acc(self):
        self.layout_forget()
        ctk.CTkFrame(self, fg_color='red').pack(expand=True, fill= 'both')
        
        print('creating account')


#connect with CLI

if __name__ == '__main__':
    main()