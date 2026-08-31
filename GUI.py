#what I'm gion to do is basecally build a windows for each task then I'm goin to start linking them with CLI or even better PasswordManager
import tkinter as tk
from tkinter import PhotoImage
import customtkinter as ctk
from PIL import Image
import os
from Fonts_and_Colors import *
from password_manager import PasswordManager as pm



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
        menu.log_layout()








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
        self.show_password = tk.BooleanVar(value=False)
        self.password_security = tk.StringVar(value= 'Weak Password!!')
        self.remember_my_account = tk.BooleanVar(value=False)
        





        #Login menu
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
                                        font=BUTTON,
                                        command= self.forgot_password)
        self.create_account =  ctk.CTkButton(self.forgetpassword_frame, 
                                        text= 'Create Account',
                                        text_color= TEXT_COLOR,
                                        fg_color='transparent',
                                        hover_color= SURFACE_COLOR,
                                        font=BUTTON,
                                        command= self.create_acc)
        self.showpassword_rememberemail = ctk.CTkFrame(self.log_setup, fg_color=SURFACE_COLOR)
        self.showpassword = ctk.CTkCheckBox(self.showpassword_rememberemail,
                                            text= 'Show Password',
                                            font=ENTRY,
                                            fg_color=ACCENT_COLOR,
                                            hover_color= HOVER_COLOR,
                                            variable=self.show_password,
                                            command=self.showing_password)
        self.bottom = ctk.CTkFrame(self, fg_color=SURFACE_COLOR)

        #logics:
        self.username_entry.bind('<KeyPress-Return>', lambda e: self.go_password(self.password_entry))
        self.password_entry.bind('<KeyPress-Return>', self.log_in)
        self.forget_password.bind('<Enter>', lambda e: self.forget_password.configure(text_color = HOVER_COLOR))
        self.forget_password.bind('<Leave>', lambda e: self.forget_password.configure(text_color = TEXT_COLOR))
        self.create_account.bind('<Enter>', lambda e: self.create_account.configure(text_color = HOVER_COLOR))
        self.create_account.bind('<Leave>', lambda e: self.create_account.configure(text_color = TEXT_COLOR))


        #log_layouts
        self.log_setup.rowconfigure((0,1,2,3,4,5,6), weight=1, uniform='a')
        self.log_setup.columnconfigure((0,1,2,3), weight=1, uniform='e')
        username.grid(row=0, column=1, sticky= 'sw', columnspan= 2,pady=10)
        self.username_entry.grid(row=1, column=1, sticky= 'nwe', columnspan= 2,pady=10)
        password.grid(row=2, column=1, sticky= 'sw', columnspan= 2,pady=10)
        self.password_entry.grid(row=3, column=1, sticky= 'nwe', columnspan= 2,pady=10)
        log_button.grid(row= 5, column=0, sticky='s', columnspan=4)
        self.forget_password.pack(side='left', fill='x')
        self.create_account.pack(side='left', fill='x')
        self.showpassword_rememberemail.grid(row=4, column=1, sticky='w', columnspan=2, pady=10)
        self.showpassword.pack(side='left',fill='x', padx=10)
        self.forgetpassword_frame.grid(row= 6, column = 1, sticky='n', columnspan=2, pady=30)




        #craete new account menu
        self.cracc_menu = ctk.CTkFrame(self, fg_color= SURFACE_COLOR)
        self.cracc_title = ctk.CTkLabel(self.cracc_menu, 
                                  bg_color= SURFACE_COLOR, 
                                  text='Creating New Account', 
                                  font=TITLE_LARGE)
        self.cracc_username_label = ctk.CTkLabel(self.cracc_menu, 
                                           text='Create Usename', 
                                           fg_color='transparent',
                                           font=TITLE_SMALL)
        self.cracc_username = ctk.CTkEntry(self.cracc_menu, 
                                      placeholder_text='Enter a Username',
                                      font=ENTRY)                               
        self.cracc_password_label = ctk.CTkLabel(self.cracc_menu, 
                                                text='Create Password', 
                                                fg_color='transparent',
                                                font=TITLE_SMALL)
        self.cracc_password = ctk.CTkEntry(self.cracc_menu, 
                                      placeholder_text='Enter a Password', 
                                      font=ENTRY,
                                      show='*')
        self.cracc_password_confirmation = ctk.CTkEntry(self.cracc_menu, 
                                      placeholder_text='re-enter Your Password', 
                                      font=ENTRY,
                                      show='*')
        self.cracc_password_rating = ctk.CTkLabel(self.cracc_menu, 
                                            textvariable= self.password_security,
                                            font=TITLE_SMALL)
        self.cracc_password_progressbar = ctk.CTkProgressBar(self.cracc_menu, progress_color= WEAK_PASSWORD, fg_color=CARD_COLOR)
        self.cracc_showpassword_rememberaccount = ctk.CTkFrame(self.cracc_menu, fg_color=SURFACE_COLOR) 
        self.cracc_show_password = ctk.CTkCheckBox(self.cracc_showpassword_rememberaccount,
                                             text='show password',
                                             font=ENTRY,
                                             fg_color= ACCENT_COLOR,
                                             hover_color= HOVER_COLOR,
                                             variable=self.show_password,
                                             command=self.showing_password)
        self.cracc_rememberaccount =  ctk.CTkCheckBox(self.cracc_showpassword_rememberaccount,
                                             text='remember login',
                                             font=ENTRY,
                                             fg_color= ACCENT_COLOR,
                                             hover_color= HOVER_COLOR,
                                             variable=self.remember_my_account,
                                             command=self.remember_account)
        self.cracc_buttonframe = ctk.CTkFrame(self.cracc_menu, fg_color=SURFACE_COLOR)
        self.cracc_button = ctk.CTkButton(self.cracc_buttonframe, 
                                          text='Create Account', 
                                          text_color= TEXT_COLOR,
                                          fg_color= ACCENT_COLOR,
                                          hover_color= HOVER_COLOR,
                                          font=BODY_LARGE,
                                          state='disabled',
                                          command=lambda e: self.password_validation(self.cracc_password, self.cracc_password_progressbar))



                #cracc logics
        
        

        #cracc logic
        self.cracc_password_progressbar.set(0)
        self.cracc_password.bind('<KeyPress>', lambda e :self.password_validation(self.cracc_password, self.cracc_password_progressbar))
        self.cracc_password_confirmation.bind('<KeyRelease>', lambda e: self.confirme_password(self.cracc_password, self.cracc_password_confirmation, self.cracc_button))
        self.cracc_username.bind('<KeyPress-Return>', lambda e: self.go_password(self.cracc_password))
        self.cracc_password.bind('<KeyPress-Return>', lambda e: self.go_password(self.cracc_password_confirmation))
        # self.cracc_password_confirmation.bind('<KeyPress>', lambda e: self.go_login)




        #create new account layout
        self.cracc_menu.rowconfigure(0, weight=2, uniform='a')
        self.cracc_menu.rowconfigure((1,2,3,4,5,6,7,8,9), weight=1, uniform='a')
        self.cracc_menu.columnconfigure(0, weight=1)

        self.cracc_title.grid(row=0, column=0, sticky='news', padx=10, pady=10)
        self.cracc_username_label.grid(row= 1, column=0, sticky= 'sw', padx=100)
        self.cracc_username.grid(row=2, column=0, sticky='new', padx=100)
        self.cracc_password_label.grid(row=3, column=0, sticky='sw', padx=100)
        self.cracc_password.grid(row=4, column=0, sticky='new', padx=100)
        self.cracc_password_confirmation.grid(row=5, column=0, sticky='new', padx=100)
        self.cracc_password_rating.grid(row=6, column=0, sticky='sw', padx=100)
        self.cracc_password_progressbar.grid(row=7, column=0, sticky='new', padx=100)
        self.cracc_showpassword_rememberaccount.grid(row=8, column=0, sticky='news', padx=100, pady=10)
        self.cracc_show_password.pack(side='left',padx=10)
        self.cracc_rememberaccount.pack(side='left', padx=40)
        self.cracc_buttonframe.grid(row=9,column=0, sticky='ew', padx=100)
        self.cracc_button.pack(anchor='center')

        #Forget password
        self.fp_menu = ctk.CTkFrame(self, fg_color= SURFACE_COLOR)
        self.fp_title = ctk.CTkLabel(self.fp_menu,
                                     text='Password Recovery',
                                     font=TITLE_LARGE,
                                     fg_color=SURFACE_COLOR)
        self.fp_recovframe = ctk.CTkFrame(self.fp_menu, fg_color=SURFACE_COLOR)
        self.fp_recovery_code = ctk.CTkEntry(self.fp_recovframe,
                                          placeholder_text='Enter your recovery secret-key',
                                          font=ENTRY)
        self.fp_skvalidation = ctk.CTkButton(self.fp_recovframe,
                                           fg_color=ACCENT_COLOR,
                                           hover_color=HOVER_COLOR,
                                           text='Submit',
                                           font=BUTTON,
                                           command= self.confitm_sk)
        #enp = enter new password
        self.fp_enp_label = ctk.CTkLabel(self.fp_menu,
                                      text='New Password',
                                      font= TITLE_SMALL,
                                      fg_color='transparent')
        self.fp_enp = ctk.CTkEntry(self.fp_menu,
                                placeholder_text='Enter a new password',
                                font=ENTRY,
                                show='*')
        self.fp_enp_confirmation = ctk.CTkEntry(self.fp_menu,
                                placeholder_text='confirme the new password',
                                font=ENTRY,
                                show='*')
        self.fp_btnfrm =  ctk.CTkFrame(self.fp_menu, fg_color=SURFACE_COLOR)
        self.fp_enp_submit = ctk.CTkButton(self.fp_btnfrm,
                                        text= 'Change passowrd',
                                        font=BUTTON,
                                        fg_color=ACCENT_COLOR,
                                        hover_color=HOVER_COLOR,
                                        command=self.submit_np)
        self.fp_password_rating = ctk.CTkLabel(self.fp_menu, 
                                            textvariable= self.password_security,
                                            font=TITLE_SMALL)
        self.fp_password_progressbar = ctk.CTkProgressBar(self.fp_menu, progress_color= WEAK_PASSWORD, fg_color=CARD_COLOR)
        self.fp_showpassword_rememberaccount = ctk.CTkFrame(self.fp_menu, fg_color=SURFACE_COLOR) 
        self.fp_show_password = ctk.CTkCheckBox(self.fp_showpassword_rememberaccount,
                                             text='show password',
                                             font=ENTRY,
                                             fg_color= ACCENT_COLOR,
                                             hover_color= HOVER_COLOR,
                                             variable=self.show_password,
                                             command=self.showing_password)
        self.fp_rememberaccount =  ctk.CTkCheckBox(self.fp_showpassword_rememberaccount,
                                             text='remember login',
                                             font=ENTRY,
                                             fg_color= ACCENT_COLOR,
                                             hover_color= HOVER_COLOR,
                                             variable=self.remember_my_account,
                                             command=self.remember_account)



        #forget password logics
        self.fp_password_progressbar.set(0)
        self.fp_enp.bind('<KeyPress>', lambda e :self.password_validation(self.fp_enp, self.fp_password_progressbar))
        self.fp_enp_confirmation.bind('<KeyRelease>', lambda e: self.confirme_password(self.fp_enp, self.fp_enp_confirmation, self.fp_enp_submit))
        self.fp_enp.bind('<KeyPress-Return>', lambda e: self.go_password(self.fp_enp_confirmation))


        #Layout
        self.fp_menu.columnconfigure(0, weight=1, uniform='a')
        self.fp_menu.rowconfigure((0,1), weight=2, uniform='a')
        self.fp_menu.rowconfigure((2,3,4,5,6,7,8), weight=1, uniform='v')
        self.fp_title.grid(row=0, column=0, sticky='news', padx=10, pady=10)
        self.fp_recovframe.grid(row=1, column=0, sticky='news', padx=100, pady=20)
        self.fp_recovery_code.pack(side='left', fill='x', expand=True)
        self.fp_skvalidation.pack(side='left', padx=30)
        self.fp_enp_label.grid(row=2, column=0, sticky='sw', padx=100)
        self.fp_enp.grid(row=3, column=0, sticky='new', padx=100)
        self.fp_enp_confirmation.grid(row=4, column=0, sticky='new', padx=100)
        self.fp_password_rating.grid(row=5, column=0, sticky='sw', padx=100)
        self.fp_password_progressbar.grid(row=6, column=0, sticky='new', padx=100)
        self.fp_showpassword_rememberaccount.grid(row=7, column=0, sticky='news', padx=100, pady=10)
        self.fp_show_password.pack(side='left', padx=10)
        self.fp_rememberaccount.pack(side='left', padx=40)
        self.fp_btnfrm.grid(row=8, column=0, sticky='ew')
        self.fp_enp_submit.pack(anchor='center')

    
        










        self.pack(fill='both', expand=True)



    def log_layout(self):
        self.show_password.set(False)
        self.banner.pack(fill='x')
        self.log_setup.pack(expand=True, fill='both')
        self.bottom.pack(fill='both')

    def log_layout_forget(self):
        self.banner.pack_forget()
        self.log_setup.pack_forget()
        self.bottom.pack_forget()

    def go_password(self, target_label):
        target_label.focus_set()

    def go_login(self, event):
        self.log_in()

    def log_in(self):
        print(self.username_entry.get()+"\n"+self.password_entry.get())

    def forgot_password(self):
        self.log_layout_forget()
        self.fp_layout()

    def create_acc(self):
        self.log_layout_forget()
        self.cracc_layout()

    def cracc_layout(self):
        self.show_password.set(False)
        self.cracc_menu.pack(expand=True, fill='both')
        self.bottom.pack(fill='x')

    def cracc_layout_forget(self):
        self.cracc_menu.pack_forget()
        self.bottom.pack_forget()

    def fp_layout(self):
        self.show_password.set(False)
        self.fp_menu.pack(expand=True, fill='both')
        self.bottom.pack(fill='x')
    
    def showing_password(self):
        if self.show_password.get():
            self.password_entry.configure(show='')
            self.cracc_password.configure(show='')
            self.cracc_password_confirmation.configure(show='')
            self.fp_enp.configure(show='')
            self.fp_enp_confirmation.configure(show='')
        else:
            self.password_entry.configure(show='*')
            self.cracc_password.configure(show='*')
            self.cracc_password_confirmation.configure(show='*')
            self.fp_enp.configure(show='*')
            self.fp_enp_confirmation.configure(show='*')

    def password_validation(self, password, progressbar):
        score = pm.passwors_validation(password.get())
        progressbar.set(score/100)
        self.update_password_rating(score, self.password_security, progressbar)

    def update_password_rating(self, score, label, progressbar):
        if 0 <= score < 30:
            label.set("Weak Password!!")
            progressbar.configure(progress_color=WEAK_PASSWORD)
        elif 30 <= score < 60:
            label.set("Normal Password")
            progressbar.configure(progress_color=NORMAL_PASSWORD)
        elif 60 <= score < 90:
            label.set("Strong Password") 
            progressbar.configure(progress_color=STRONG_PASSWORD)   
        elif score >= 90:
            label.set("Very Strong Password!!")
            progressbar.configure(progress_color=VERY_STRONG_PASSWORD)

    def remember_account(self):
        ...

    def confirme_password(self, pass1, pass2, button):
        if pass1.get() == pass2.get() and pm.passwors_validation(pass1.get())>45:
            pass1.configure(border_color= SUCCESS)
            pass2.configure(border_color= SUCCESS)
            button.configure(state='normal')
        else:
            pass2.configure(border_color= ERROR_COLOR)

    def confitm_sk(self):
        ...

    def submit_np(self):
        ...
#connect with CLI

if __name__ == '__main__':
    main()