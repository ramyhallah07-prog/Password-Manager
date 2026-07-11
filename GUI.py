import tkinter as tk
import customtkinter as ctk
from password_manager import CLI as c
ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('dark-blue')
pm = ctk.CTk()

pm.geometry('680x680')
pm.title('Password Manager')
get_username = ctk.CTkEntry(pm,placeholder_text='Username')
get_password = ctk.CTkEntry(pm, placeholder_text='Password', show = '*' )
get_username.pack(pady = 58)
get_password.pack(pady = 59)

def password_view():
    if show_password.get() == 1:
        get_password.configure(show = '')
    else:
        get_password.configure(show = '*')

show_password = ctk.CTkCheckBox(pm, checkbox_height=25, checkbox_width=25, text= 'show password', command= password_view)
show_password.pack()
lable = ctk.CTkLabel(pm, text='')
lable.pack(pady = 70)
def yourname():
    username = get_username.get()
    lable.configure(text = f'your name is {username}, suuuuuukkkkaaaaaaa {username}')
botton = ctk.CTkButton(pm, text= 'submit', command=yourname)
botton.pack(pady = 60)
icon = tk.PhotoImage(file='D:\Python\Projects\Password Manager\logo.png')
pm.wm_iconphoto(True, icon)
pm.mainloop()