import string
from random import choices
import secrets
import dae
import time
import os


class PasswordManager:
    def __init__(self):
        self.__user = None
        self.__login = False
    
    def create_password_maneger_account(self, user, master_password):#Done
        if dae.account_validation('users/users.csv', user):
            raise ValueError('username already existe')
        if self.passwors_validation(master_password) < 60: 
            raise AttributeError('Your Password is too weak')
        self.__user = user
        dae.add_user(user, master_password)
        dae.generate_uk(user)
        os.system(f'attrib +h "users"')
        answer = input('do you want to login automaticly? (y/n): ')
        if answer == 'y':
            self.__login = True
        elif answer == 'n':
            dae.encrypt_folder(self.__user)
            return 'you need to login to continue'

    def login_user(self, username, master_password):#need to add the decryption for the file 
        if dae.loguserin(username, master_password):
            if not self.__login:
                self.__login = True
                self.__user = username
                if os.path.isfile(f'users/{self.__user}.zip') : dae.decrypt_folder(self.__user)
                return f'{self.__user} Logged in Successfully'
            elif self.__login and self.__user == username:
                return 'user already logegd in'
            elif self.__login and self.__user != username:
                return f'to login with {username} you should logout from the current account "{self.__user}"'
        raise AttributeError('Failed to login')
    
    def logout_user(self, username):#need to add encryption to userfile
        if not self.__login:
            raise AttributeError('you\'re not logged in')
        if self.__user == username:
            dae.encrypt_folder(self.__user)
            self.__user = None
            self.__login = False
            return f'{username} Logged out Successfully'
        elif self.__user != username:
            return f'you\'re not logged in as {username}'
        
    def remove_user(self, master_password):#Done
        if not self.__login:
            raise AttributeError('You\'re not logged in')
        answer = input('are you sure you want to delete your Password Manager account? (y/n): ')
        if answer == 'y':
            confirmation = input('if you delete you Password Manager account all your passwords will desapear are you sure you want to do that? (y/n): ')
            if confirmation == 'y' and self.__login:
                dae.delete_user(self.__user, master_password)
                return 'your accout was deleted successfully all your data was erased'
            elif confirmation == 'n':
                return 'the operation was canceled thank you for staying with us'
        elif answer == 'n':
            return 'the operation was canceled thank you for staying with us'

    def change_password(self, url, username, new_password):#Done
        if not self.__login:
            raise ValueError('Login Failed')
        url = f'{url}.csv'
        path = f'users/{self.__user}/{url}'
        password = dae.show_account(path, username)['password']
        if dae.account_validation(f'users/{self.__user}',url, isdir= True) and dae.show_account(path, username):
            if dae.decrypt(password, self.__user) == new_password:
                return 'You can\'t change the password into the same password'     
            if dae.show_account(path, username)["username"] == username and dae.decrypt(password, self.__user) != new_password:
                dae.change_password(path, username, new_password, self.__user)
                return 'password has been changed seccessfully'
        else:
            return 'account was not found'

    def add_account(self, url, username, password):#Done
        if not self.__login:
            raise ValueError('Login Failed')
        elif dae.account_validation(f'users/{self.__user}/{url}.csv', username):
            print(dae.uk_loader(self.__user))
            return f'username {username} already exicte in {url}'
        elif self.__login and not dae.account_validation(f'users/{self.__user}/{url}.csv', username):
            dae.creat_account(self.__user, url, username, password, uk=True)
            return 'Account added seccessfully'
           
    def delete_account(self, url, username):#Done
        if not self.__login:
            raise ValueError('Login Failed')
        url = f'{url}.csv'
        if not dae.account_validation(f'users/{self.__user}/{url}', username):
            return 'couldn\'t find the account'
        answer = input('are you sure you want to delete your account? (y/n): ')
        if answer == 'y' and self.__login:
            dae.remove_account(f'users/{self.__user}/{url}', username)
            return 'account was deleted sccessfully'
        elif answer == 'n':
            return 'the delete operation was canceled'
        else:
            return 'account was not found'
   
    def show_account(self, url, username):#Done
        if not self.__login:
            raise ValueError('Login Failed')
        url = f'{url}.csv'
        if dae.account_validation(f'users/{self.__user}/{url}', username):
            password = dae.show_account(f'users/{self.__user}/{url}', username)['password']
            return f'Usename: {username},  Password: {dae.decrypt(password, self.__user)}'
        else:
            return 'account was not found'

    def password_generator(self, lenth, lower = None , upper = None , nums = None , spetial_char = None, addition = None):
        char = string.ascii_letters
        char_low = string.ascii_lowercase
        char_up = string.ascii_uppercase
        num = string.digits
        spetials = string.punctuation
        additions = addition
        _password = ''
        if lower:
            _password = ''.join(secrets.choice(char_low) for _ in range(lower))
        if upper:
            _password += ''.join(secrets.choice(char_up) for _ in range(upper))
        if nums:
            _password += ''.join(secrets.choice(num) for _ in range(nums))
        if spetial_char:
            _password += ''.join(secrets.choice(spetials) for _ in range(spetial_char))
        if addition:
            password = _password.join(secrets.choice(char+num+spetials) for _ in range(lenth - len(_password)-len(addition))) if len(_password) < lenth else ''.join(secrets.choice(_password) for _ in range(lenth- len(addition)))
            password += addition
        elif not addition:
             password = _password.join(secrets.choice(char+num+spetials) for _ in range(lenth - len(_password))) if len(_password) < lenth else ''.join(secrets.choice(_password) for _ in range(lenth))
        return password
       
    def passwors_validation(self, password):
        char = string.ascii_letters
        char_low = string.ascii_lowercase
        char_up = string.ascii_uppercase
        num = string.digits
        spetials = string.punctuation

        COMMON_PATTERNS = [
    "1234", "12345", "123456", "123456789",
    "password", "password123", "admin", "admin123",
    "qwerty", "asdfgh", "zxcvbn",
    "letmein", "welcome", "login", "root",
    "abc123", "iloveyou",
    "1111", "0000", "123123"
]
        password_score = 0
        if any(lower in password for lower in char_low):
            password_score += 10
        else:
            password_score -= 5
        if any(upper in password for upper in char_up):
            password_score += 10
        else:
            password_score -= 5
        if any(n in password for n in num):
            password_score += 10
        else:
            password_score -= 5
        if any(spetial_char in password for spetial_char in spetials):
            password_score += 15
        else:
            password_score -= 5
        if len(set(password)) < len(password) / 2:
             password_score -= 10
        password_score += min(len(password)*2, 20)
        if len(password) >= 16 : password_score += 20
        elif len(password) >= 12 : password_score += 10
        if len(password) < 8:
            password_score -= 20
        if any(patern in password.lower() for patern in COMMON_PATTERNS):
                password_score -= 30
        # if 0 <= password_score < 30:
        #     print('Weak Password!!')
        # elif 30 <= password_score < 60:
        #     print("Normal Password")
        # elif 60 <= password_score < 90:
        #     print("Strong Password")    
        # elif password_score >= 90:
        #     print("Very Strong Password!!")
        return max(password_score, 0)

    def UI():
        ...





def main():
    hello = 'shut up'
    pm = PasswordManager()
    # pm.create_password_maneger_account('zahra', 'ramy123')
    # print(pm.login_user('bouchra', 'ramy123'))
    # print(pm.logout_user('zahra'))
    # print(pm.add_account('instagram', 'ramy', 'ramy20074'))
    print(pm.login_user('el-hawwary', 'Ramy@04_2007'))
    pm.remove_user('Ramy@04_2007')
    # pm.create_password_maneger_account('el-hawwary', 'Ramy@04_2007')

    # print(pm.add_account('google', 'ramy', 'hrhrh'))
    # print(pm.add_account('instagram', 'ramy', 'drgndrgndrgn'))
    # print(pm.add_account('github', 'ramy', 'rgigigi74'))
    # print(pm.add_account('facebook', 'ramy', 'ramy1997'))
    # print(pm.show_account('facebook', 'ramy'))
    # print(pm.change_password('facebook', 'ramy', 'ramy grgr'))
    # print(pm.show_account('facebook', 'ramy'))
    # print(pm.delete_account('instagram', 'ramy'))
    # print(pm.show_account('github', 'ramy'))
    # pm.logout_user('el-hawwary')
    # pm.login_user('ramy', 'Ramy@04_2007')
    # pm.create_password_maneger_account('ramy', 'Ramy@04_2007')
    # pm.login_user('ramy', 'Ramy@04_2007')
    # print(pm.add_account('google', 'ramyhallah07@gmail.com', 'Ramy@04_2007'))
    # print(pm.show_account('google', 'ramyhallah07@gmail.com'))
    # print(pm.remove_user('Ramy@04_2007'))
    # pm.logout_user('ramy')













if __name__ == '__main__':
    main()

















# """

# Traceback (most recent call last):
#   File "c:\Users\ramyh\Password-Manager\password_manager.py", line 243, in <module>
#     main()
#     ~~~~^^
#   File "c:\Users\ramyh\Password-Manager\password_manager.py", line 212, in main
#     print(pm.add_account('google', 'ramy', 'hrhrh'))
#           ~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^
#   File "c:\Users\ramyh\Password-Manager\password_manager.py", line 92, in add_account
#     dae.creat_account(self.__user, url, username, password, uk=True)
#     ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#   File "c:\Users\ramyh\Password-Manager\dae.py", line 180, in creat_account
#     add_account(csv_path, username, password,user=user)
#     ~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#   File "c:\Users\ramyh\Password-Manager\dae.py", line 189, in add_account
#     adder.writerow({'username' : username, 'password': encrypt(password, user)})
#                                                        ~~~~~~~^^^^^^^^^^^^^^^^
#   File "c:\Users\ramyh\Password-Manager\dae.py", line 145, in encrypt
#     fernet = Fernet(key)
#   File "C:\Users\ramyh\AppData\Local\Programs\Python\Python314\Lib\site-packages\cryptography\fernet.py", line 35, in __init__
#     key = base64.urlsafe_b64decode(key)
#   File "C:\Users\ramyh\AppData\Local\Programs\Python\Python314\Lib\base64.py", line 129, in urlsafe_b64decode
#     s = _bytes_from_decode_data(s)
#   File "C:\Users\ramyh\AppData\Local\Programs\Python\Python314\Lib\base64.py", line 42, in _bytes_from_decode_data
#     raise TypeError("argument should be a bytes-like object or ASCII "
#                     "string, not %r" % s.__class__.__name__) from None
# TypeError: argument should be a bytes-like object or ASCII string, not 'NoneType'
#       f0y4hZH2RdITx7w2VUzxjSxJ_hS44egue-8eWN99nVs=
# """