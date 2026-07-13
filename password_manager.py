import string
import random
import secrets
import dae
import time
import os
from tkinter import *
from threading import Timer

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

    def login_user(self, username, master_password):#need to add the decryption for the file 
        if dae.loguserin(username, master_password):
            if not self.__login:
                self.__login = True
                self.__user = username
                if os.path.isfile(f'users/{self.__user}.zip'): dae.decrypt_folder(self.__user)
                return f'{self.__user} Logged in Successfully'
            elif self.__login and self.__user == username:
                return 'user already logegd in'
            elif self.__login and self.__user != username:
                return f'to login with {username} you should logout from the current account "{self.__user}"'
        elif not dae.loguserin(username, master_password):
            return 'Wrong password'
    
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

    def change_user_password(self, username, new_masterpassword, masterpassword = None, forgotpassword= False):
        if self.passwors_validation(new_masterpassword) < 60: 
            raise AttributeError('Your Password is too weak')
        if forgotpassword:
            dae.remove_account('users/users.csv', username)
            dae.add_user(username, new_masterpassword, change_password=True)
            return 'Password Changed Seccessfully'
        else:
            if dae.loguserin(username, masterpassword):
                dae.remove_account('users/users.csv', username)
                dae.add_user(username, new_masterpassword, change_password=True)
            return 'Password Changed Seccessfully'

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

    @property
    def log_status(self):
        return self.__login

    def add_account(self, url, username, password):#Done
        if not self.__login:
            raise ValueError('Login Failed')
        elif dae.account_validation(f'users/{self.__user}/{url}.csv', username):
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
        answer = input('\tare you sure you want to delete your account? (y/n): ')
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
        if len(password) >= 16: password_score += 20
        elif len(password) >= 12: password_score += 10
        if len(password) < 8:
            password_score -= 20
        if any(patern in password.lower() for patern in COMMON_PATTERNS):
                password_score -= 30
        return max(password_score, 0)
    
    def username_generator(self, lenth):
        char = string.ascii_letters
        username = ''.join(random.choice(char) for _ in range(lenth)) 
        return username
    
    @property
    def vault(self):
        if not self.__login:
            raise ValueError('Login Failed')
        else:
            dae.show_all_accounts(self.__user)
    



#MENUS:
class CLI(PasswordManager):
    def __init__(self):
        super().__init__()
        self._username = None
        self.logout_timer = None
        self._timer = 60*15

    def home_menu(self):
        if dae.file_validator('users/users.csv'):
            print('Password Manager: \n')
            print('\t1- Create New PasswordManager Account\n\t2- Login with existing PasswordManager Account\n\t3- Exit\n\t')
            operation = int(input('\tOperation: '))
            if operation == 1:
                self.newuser_menu()
            elif operation == 2:
                self.loging_menu()    
            elif operation == 3:
                os.system('Exit')
            else:
                raise AttributeError('Unvalid Operation')
        else:
            print('1- Create New PasswordManager Account\n\t2- Exit\n\t')
            operation = int(input('\tOperation: '))
            if operation == 1:
                self.newuser_menu()
            elif operation == 2:
                os.system('Exit')
            else:
                raise AttributeError('Unvalid Operation')

    def newuser_menu(self):
        print('\nCreating New User Account: \n')
        username = input('\tUsernaem: ').strip()
        password = input('\tPassword: ')
        self._username = username
        print(f'\t{self.create_password_maneger_account(username, password)}')
        print(f'\tKeep this recovery key in a safe place\nRecovery key:"{dae.add_user(MastrPassword= password, return_password=True)}"')
        answer = input('Do you want to Login automaticly? (y/n): ')
        if answer == 'y':
            self.login_user(username, password)
        elif answer == 'n':
            dae.encrypt_folder(self._username)
            print('You need to Login to continue to the main menu')
            self.home_menu()
        else:
            self.logoutandexit()
            raise AttributeError('Unvalid Operation')

    def loging_menu(self):
        print('\nLogging in: \n')
        username = input('\tUsernaem: ').strip()
        password = input('\tPassword: ')
        self._username = username
        print(f'\t{self.login_user(username, password)}')
        self.forget_password(password)
        if self.log_status:
            self.cooldown()
            self.main_menu()

    def main_menu(self):
        if self.log_status:
            print('\nMain Menu: \n')
            print('\t1- Show password\n\t2- Add Account \n\t3- Delete Account\n\t4- Change Account\'s password\n\t5- Vault\n\t6- Settings\n\t7- Logout And Exit\n')
            operation = int(input('\tOperation: '))
            if operation == 1:
                self.show_password()
            elif operation == 2:
                self.add_account()
            elif operation == 3:
                self.delete_account()
            elif operation == 4:
                self.change_account_password()
            elif operation == 5:
                self.vault
                print('\n\t1- Back to Main Menu\n\t2-Logout And Exit')
                operation = int(input('\n\tOperation: '))
                if operation == 1:
                    self.main_menu()
                elif operation == 2:
                    self.logoutandexit()
                else:
                    raise AttributeError('Unvalid Operation')
            elif operation == 6:
                self.settings()
            elif operation == 7:
                self.logoutandexit()
            else:
                self.logoutandexit()
                raise AttributeError('Unvalid Operation')

    def show_password(self):
        print('\nSHOW PASSWORD: \n')
        url = input('\tName of website/application account: ')
        account_username = input('\twhat username are you searching for? ')
        print(f'\t{self.show_account(url, account_username)}')
        print('\n\t1- Back to Main Menu\n\t2-Logout And Exit')
        operation = int(input('\n\tOperation: '))
        if operation == 1:
            self.main_menu()
        elif operation == 2:
            self.logoutandexit()
        else:
            self.logoutandexit()
            raise AttributeError('Unvalid Operation')

    def add_account(self):
        print('\nADD ACCOUNT: \n')
        add_url = input('\tName of website/application: ')
        Gusername = input('\tGenerate Username (y/n): ')
        if Gusername == 'y':
            lenth = int(input('\tLenth of username: '))
            add_username = self.username_generator(lenth)
        elif Gusername == 'n':
            add_username = input('\tUsername: ')
        else:
            self.logoutandexit()
            raise ValueError
        Gpassword = input('\tGenerate Password (y/n): ')
        if Gpassword == 'y':
            lenth = int(input('\n\tPassword Lenth: '))
            low = input('\tLower Characters (y/n): ')
            up = input('\tUpper Characters (y/n): ')
            num = input('\tNumbers (y/n): ')
            spetial = input('\tSpetial Characters (y/n): ')
            add = input('\taddition (y/n): ')
            lower = int(input('\tLower: ')) if low == 'y' else None
            upper = int(input('\tUpper: ')) if up == 'y' else None
            nums = int(input('\tNumbers: ')) if num == 'y' else None
            spetials = int(input('\tSpetial Characters: ')) if spetial == 'y' else None
            additions = input('\tAdditions: ') if add == 'y' else None
            add_password = self.password_generator(lenth, lower, upper, nums, spetials, additions)
        elif Gpassword == 'n':
            add_password = input('\tPassword: ')
        else:
            self.logoutandexit()
            raise ValueError
        password_score = self.passwors_validation(add_password)
        if 0 <= password_score < 30:
            print('\tWeak Password!!')
        elif 30 <= password_score < 60:
            print("\tNormal Password")
        elif 60 <= password_score < 90:
            print("\tStrong Password")    
        elif password_score >= 90:
            print("\tVery Strong Password!!")
        print(f'\n\t{super().add_account(add_url, add_username, add_password)}')
        print('\n\t1- Back to Main Menu\n\t2- Logout And Exit')
        operation = int(input('\n\tOeration: '))
        if operation == 1:
            print()
            self.main_menu()
        elif operation == 2:
            self.logoutandexit()

    def delete_account(self):
        print('\nDELETE ACCOUNT: \n')
        del_url = input('\tName of website/application: ')
        del_username = input('\tUsername: ')
        print(f'\t{super().delete_account(del_url, del_username)}')
        print('\n\t1- Back to Main Menu\n\t2-Logout And Exit')
        operation = int(input('\n\tOperation: '))
        if operation == 1:
            self.main_menu()
        elif operation == 2:
            self.logoutandexit()
        else:
            self.logoutandexit()
            raise AttributeError('Unvalid Operation')

    def change_account_password(self):
        print('\nCHANGE ACCOUNT\'S PASSWORD: \n')
        change_url = input('\tName of website/application: ')
        change_username = input('\tUsername: ')
        generate_password = input('\n\tGenerate Password (y/n): ')
        if generate_password == 'n':
            change_password = input('\tNew_Password: ')
        elif generate_password == 'y':
            lenth = int(input('\n\tPassword Lenth: '))
            low = input('\tLower Characters (y/n): ')
            up = input('\tUpper Characters (y/n): ')
            num = input('\tNumbers (y/n): ')
            spetial = input('\tSpetial Characters (y/n): ')
            add = input('\taddition (y/n): ')
            lower = int(input('\tLower: ')) if low == 'y' else None
            upper = int(input('\tUpper: ')) if up == 'y' else None
            nums = int(input('\tNumbers: ')) if num else None
            spetials = int(input('\tSpetial Characters: ')) if spetial == 'y' else None
            additions = input('\tAdditions: ') if add == 'y' else None
            change_password = self.password_generator(lenth, lower, upper, nums, spetials, additions)
        print(f'\t{self.change_password(change_url, change_username, change_password)}')
        password_score = self.passwors_validation(change_password)
        if 0 <= password_score < 30:
            print('\tWeak Password!!')
        elif 30 <= password_score < 60:
            print("\tNormal Password")
        elif 60 <= password_score < 90:
            print("\tStrong Password")    
        elif password_score >= 90:
            print("\tVery Strong Password!!")
        print('\n\t1- Back to Main Menu\n\t2-Logout And Exit')
        operation = int(input('\n\tOperation: '))
        if operation == 1:
            self.main_menu()
        elif operation == 2:
            self.logoutandexit()
        else:
            self.logoutandexit()
            raise AttributeError('Unvalid Operation')

    def settings(self):
        print('\nSETTINGS: \n')
        print('\t1- Logout Cooldown Timer\n\t2- Change Users MasterPassword\n\t3- Back to Main Menu\n\t4- Delete User\n')
        operation =int(input( '\tOperation: '))
        if operation == 1:
            timer = float(input('\tSet Logout Cooldown for: '))
            self._timer = timer
            self.cooldown()
            print(f'\tTimer was seccessfully set for {timer} minut(s)')
            print('\n\t1- Back to Main Menu\n\t2-Logout And Exit')
            operation = int(input('\n\tOperation: '))
            if operation == 1:
                self.main_menu()
            elif operation == 2:
                self.logoutandexit()
            else:
                self.logoutandexit()
                raise AttributeError('Unvalid Operation')
        elif operation == 2: 
            print('\nChanging User\'s MasterPassword: \n')
            old_password = input('\tEnter Your Old MasterPassword: ')
            if self.login_user(self._username, old_password) == 'Wrong password':
                print('\tWrong MasterPassowrd\n')
                self.forget_password(old_password)
            else:
                new_passwoerd = input('\tEnter The New Password: ')
                print(f"\t{self.change_user_password(self._username, new_passwoerd, old_password)}")
                print(f'\tYour new recovery key "{dae.add_user(MastrPassword= new_passwoerd, return_password=True)}"')

        elif operation == 3:
            if self.log_status:
                self.main_menu()
        elif operation == 4:
            print('\nDelete Password Manager Account: ')
            username = input('\tUsername: ')
            password = input('\tPassword: ')
            dae.delete_user(username, password)
            print('\n\t1- Back to Home Menu\n\t2-Logout And Exit')
            operation = int(input('\n\tOperation: '))
            if operation == 1:
                self.home_menu()
            elif operation == 2:
                self.logoutandexit()
            else:
                self.logoutandexit()
                raise AttributeError('Unvalid Operation')

    def forget_password(self, password):
        if self.login_user(self._username, password) == 'Wrong password':
            print('Availible operations: \n\t1- Forgot Password\n\t2- Back to Home Menu\n\t3- Exit\n')
            operation = int(input('\tOperation: '))
            tries = 4
            cooldown = 20
            if operation == 1:
                recovery_key = input('\tEnter Your recovery key: ')
                while tries:
                    tries -= 1
                    cooldown *= 2
                    if dae.loguserin(self._username, recovery_key, encrypt= False):
                        new_password = input('\tEnter you new password: ')
                        print(self.change_user_password(self._username, new_password, forgotpassword=True))
                        print(f'\tYour new recovery key "{dae.add_user(MastrPassword= password, return_password=True)}"')
                        login = input('\tDo you want to login? (y/n): ')
                        if login == 'y':
                            print(self.login_user(self._username, new_password))
                            print('\n\t1- Back to Main Menu\n\t2-Logout And Exit')
                            operation = int(input('\n\tOperation: '))
                            if operation == 1:
                                self.main_menu()
                            elif operation == 2:
                                self.logoutandexit()
                            else:
                                self.logoutandexit()
                                raise AttributeError('Unvalid Operation')
                        elif login == 'n':
                            self.logoutandexit()
                        else:
                            self.logoutandexit()
                            raise AttributeError('Unvalid Operation')
                    else:
                        recovery_key = input('\n\twrong recovery key please wait for the cooldown and try again: ')
                        if not dae.loguserin(self._username, recovery_key, encrypt= False):
                            for s in range(cooldown, 0, -1):
                                seconds = s % 60
                                minuts = int(s/60) % 60
                                print(f'{minuts:02}: {seconds:02} seconds', end = '\r')
                                time.sleep(1)
                if tries == 0:
                    self.logoutandexit()
                    raise ValueError('wrong recovery key') 
            elif operation == 2:
                self.home_menu()
                tries -= 1
                if tries == 0:
                    self.logoutandexit()
                    raise ValueError('wrong recovery key') 
            elif operation == 3:
                os._exit()
                
    def cooldown(self):
        if self.logout_timer:
            self.logout_timer.cancel()
        self.logout_timer = Timer(self._timer,self.logoutandexit)
        self.logout_timer.daemon = True
        self.logout_timer.start()

    def logoutandexit(self):
        if self.logout_timer:
            self.logout_timer.cancel()

        if self.log_status:
            self.logout_user(self._username)
            self._username = None
            os.system('Exit')
    
def UI():
    pm = CLI()
    print(f'{'*'*80}\nAvailible operations:')
    pm.home_menu()
    print(f'{'*'*80}')






class GUI(PasswordManager):
    def __init__(self):
        super().__init__()
        self._username = None
        self.logout_timer = None
        self._timer = 60*15

    def newuser_menu(self, username, password, klog):
        if klog == 1:
            self.login_user(username, password)
        elif klog == 2:
            dae.encrypt_folder(self._username)
            return 'You need to Login to continue to the main menu'
        else:
            self.logoutandexit()
            raise AttributeError('Unvalid Operation')
        self._username = username
        # Labels
        return f'{self.create_password_maneger_account(username, password)}\nKeep this recovery key in a safe place\nRecovery key:"{dae.add_user(MastrPassword= password, return_password=True)}"'

    def loging_menu(self, username, password):
        if self.log_status:
            self.cooldown()
        return f'{self.login_user(username, password)}'

    def show_password(self, url, account_username):
        return f'\t{self.show_account(url, account_username)}'
        #'\n\t1- Back to Main Menu\n\t2-Logout And Exit'
    def add_account(self):
        print('\nADD ACCOUNT: \n')
        add_url = input('\tName of website/application: ')
        Gusername = input('\tGenerate Username (y/n): ')
        if Gusername == 'y':
            lenth = int(input('\tLenth of username: '))
            add_username = self.username_generator(lenth)
        elif Gusername == 'n':
            add_username = input('\tUsername: ')
        else:
            self.logoutandexit()
            raise ValueError
        Gpassword = input('\tGenerate Password (y/n): ')
        if Gpassword == 'y':
            lenth = int(input('\n\tPassword Lenth: '))
            low = input('\tLower Characters (y/n): ')
            up = input('\tUpper Characters (y/n): ')
            num = input('\tNumbers (y/n): ')
            spetial = input('\tSpetial Characters (y/n): ')
            add = input('\taddition (y/n): ')
            lower = int(input('\tLower: ')) if low == 'y' else None
            upper = int(input('\tUpper: ')) if up == 'y' else None
            nums = int(input('\tNumbers: ')) if num == 'y' else None
            spetials = int(input('\tSpetial Characters: ')) if spetial == 'y' else None
            additions = input('\tAdditions: ') if add == 'y' else None
            add_password = self.password_generator(lenth, lower, upper, nums, spetials, additions)
        elif Gpassword == 'n':
            add_password = input('\tPassword: ')
        else:
            self.logoutandexit()
            raise ValueError
        password_score = self.passwors_validation(add_password)
        if 0 <= password_score < 30:
            print('\tWeak Password!!')
        elif 30 <= password_score < 60:
            print("\tNormal Password")
        elif 60 <= password_score < 90:
            print("\tStrong Password")    
        elif password_score >= 90:
            print("\tVery Strong Password!!")
        print(f'\n\t{super().add_account(add_url, add_username, add_password)}')
        print('\n\t1- Back to Main Menu\n\t2- Logout And Exit')
        operation = int(input('\n\tOeration: '))
        if operation == 1:
            print()
            self.main_menu()
        elif operation == 2:
            self.logoutandexit()

    def delete_account(self):
        print('\nDELETE ACCOUNT: \n')
        del_url = input('\tName of website/application: ')
        del_username = input('\tUsername: ')
        print(f'\t{super().delete_account(del_url, del_username)}')
        print('\n\t1- Back to Main Menu\n\t2-Logout And Exit')
        operation = int(input('\n\tOperation: '))
        if operation == 1:
            self.main_menu()
        elif operation == 2:
            self.logoutandexit()
        else:
            self.logoutandexit()
            raise AttributeError('Unvalid Operation')

    def change_account_password(self):
        print('\nCHANGE ACCOUNT\'S PASSWORD: \n')
        change_url = input('\tName of website/application: ')
        change_username = input('\tUsername: ')
        generate_password = input('\n\tGenerate Password (y/n): ')
        if generate_password == 'n':
            change_password = input('\tNew_Password: ')
        elif generate_password == 'y':
            lenth = int(input('\n\tPassword Lenth: '))
            low = input('\tLower Characters (y/n): ')
            up = input('\tUpper Characters (y/n): ')
            num = input('\tNumbers (y/n): ')
            spetial = input('\tSpetial Characters (y/n): ')
            add = input('\taddition (y/n): ')
            lower = int(input('\tLower: ')) if low == 'y' else None
            upper = int(input('\tUpper: ')) if up == 'y' else None
            nums = int(input('\tNumbers: ')) if num else None
            spetials = int(input('\tSpetial Characters: ')) if spetial == 'y' else None
            additions = input('\tAdditions: ') if add == 'y' else None
            change_password = self.password_generator(lenth, lower, upper, nums, spetials, additions)
        print(f'\t{self.change_password(change_url, change_username, change_password)}')
        password_score = self.passwors_validation(change_password)
        if 0 <= password_score < 30:
            print('\tWeak Password!!')
        elif 30 <= password_score < 60:
            print("\tNormal Password")
        elif 60 <= password_score < 90:
            print("\tStrong Password")    
        elif password_score >= 90:
            print("\tVery Strong Password!!")
        print('\n\t1- Back to Main Menu\n\t2-Logout And Exit')
        operation = int(input('\n\tOperation: '))
        if operation == 1:
            self.main_menu()
        elif operation == 2:
            self.logoutandexit()
        else:
            self.logoutandexit()
            raise AttributeError('Unvalid Operation')

    def settings(self):
        print('\nSETTINGS: \n')
        print('\t1- Logout Cooldown Timer\n\t2- Change Users MasterPassword\n\t3- Back to Main Menu\n\t4- Delete User\n')
        operation =int(input( '\tOperation: '))
        if operation == 1:
            timer = float(input('\tSet Logout Cooldown for: '))
            self._timer = timer
            self.cooldown()
            print(f'\tTimer was seccessfully set for {timer} minut(s)')
            print('\n\t1- Back to Main Menu\n\t2-Logout And Exit')
            operation = int(input('\n\tOperation: '))
            if operation == 1:
                self.main_menu()
            elif operation == 2:
                self.logoutandexit()
            else:
                self.logoutandexit()
                raise AttributeError('Unvalid Operation')
        elif operation == 2: 
            print('\nChanging User\'s MasterPassword: \n')
            old_password = input('\tEnter Your Old MasterPassword: ')
            if self.login_user(self._username, old_password) == 'Wrong password':
                print('\tWrong MasterPassowrd\n')
                self.forget_password(old_password)
            else:
                new_passwoerd = input('\tEnter The New Password: ')
                print(f"\t{self.change_user_password(self._username, new_passwoerd, old_password)}")
                print(f'\tYour new recovery key "{dae.add_user(MastrPassword= new_passwoerd, return_password=True)}"')

        elif operation == 3:
            if self.log_status:
                self.main_menu()
        elif operation == 4:
            print('\nDelete Password Manager Account: ')
            username = input('\tUsername: ')
            password = input('\tPassword: ')
            dae.delete_user(username, password)
            print('\n\t1- Back to Home Menu\n\t2-Logout And Exit')
            operation = int(input('\n\tOperation: '))
            if operation == 1:
                self.home_menu()
            elif operation == 2:
                self.logoutandexit()
            else:
                self.logoutandexit()
                raise AttributeError('Unvalid Operation')

    def forget_password(self, password):
        if self.login_user(self._username, password) == 'Wrong password':
            print('Availible operations: \n\t1- Forgot Password\n\t2- Back to Home Menu\n\t3- Exit\n')
            operation = int(input('\tOperation: '))
            tries = 4
            cooldown = 20
            if operation == 1:
                recovery_key = input('\tEnter Your recovery key: ')
                while tries:
                    tries -= 1
                    cooldown *= 2
                    if dae.loguserin(self._username, recovery_key, encrypt= False):
                        new_password = input('\tEnter you new password: ')
                        print(self.change_user_password(self._username, new_password, forgotpassword=True))
                        print(f'\tYour new recovery key "{dae.add_user(MastrPassword= password, return_password=True)}"')
                        login = input('\tDo you want to login? (y/n): ')
                        if login == 'y':
                            print(self.login_user(self._username, new_password))
                            print('\n\t1- Back to Main Menu\n\t2-Logout And Exit')
                            operation = int(input('\n\tOperation: '))
                            if operation == 1:
                                self.main_menu()
                            elif operation == 2:
                                self.logoutandexit()
                            else:
                                self.logoutandexit()
                                raise AttributeError('Unvalid Operation')
                        elif login == 'n':
                            self.logoutandexit()
                        else:
                            self.logoutandexit()
                            raise AttributeError('Unvalid Operation')
                    else:
                        recovery_key = input('\n\twrong recovery key please wait for the cooldown and try again: ')
                        if not dae.loguserin(self._username, recovery_key, encrypt= False):
                            for s in range(cooldown, 0, -1):
                                seconds = s % 60
                                minuts = int(s/60) % 60
                                print(f'{minuts:02}: {seconds:02} seconds', end = '\r')
                                time.sleep(1)
                if tries == 0:
                    self.logoutandexit()
                    raise ValueError('wrong recovery key') 
            elif operation == 2:
                self.home_menu()
                tries -= 1
                if tries == 0:
                    self.logoutandexit()
                    raise ValueError('wrong recovery key') 
            elif operation == 3:
                os._exit()
                
    def cooldown(self):
        if self.logout_timer:
            self.logout_timer.cancel()
        self.logout_timer = Timer(self._timer,self.logoutandexit)
        self.logout_timer.daemon = True
        self.logout_timer.start()

    def logoutandexit(self):
        if self.logout_timer:
            self.logout_timer.cancel()

        if self.log_status:
            self.logout_user(self._username)
            self._username = None
            os.system('Exit')
 









def main():
    # remove('ramy', 'Ramy@04_2007')
    UI()
    # window.mainloop()
    # pm.create_password_maneger_account('zahra', 'ramy123')
    # print(pm.login_user('zahra', 'RamyLovesZahra@<3'))
    # print(pm.logout_user('zahra'))
    # print(pm.add_account('instagram', 'ramy', 'ramy20074'))
    # print(pm.login_user('el-hawwary',))
    # pm.remove_user('Ramy@18_2016')
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
    # pm.remove_user('Ramy@04_2007')
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















