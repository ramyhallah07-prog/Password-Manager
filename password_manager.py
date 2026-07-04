import string
from random import choices
import secrets
import dae
import time
import os


# whar suka in the world is happening right now





class PasswordManager:
    def __init__(self):
        self.user = None
        self.login = False
    
    def create_password_maneger_account(self, user, master_password):#Done
        if dae.account_validation('users/users.csv', user):
            raise ValueError('username already existe')
        self.user = user
        dae.add_user(user, master_password)
        answer = input('do you want to login automaticly? (y/n): ')
        if answer == 'y':
            self.login = True
        elif answer == 'n':
            dae.encrypt_folder(self.user)
            print('you need to login to continue')

    def login_user(self, username, master_password):#need to add the decryption for the file 
        if dae.loguserin(username, master_password):
            if not self.login:
                self.login = True
                self.user = username
                if os.path.isfile(f'users/{self.user}.zip') : dae.decrypt_folder(self.user)
                return f'{self.user} Logged in Successfully'
            elif self.login and self.user == username:
                return 'user already logegd in'
            elif self.login and self.user != username:
                return f'to login with {username} you should logout from the current account "{self.user}"'
        raise AttributeError('Failed to login')
    
    def logout_user(self, username):#need to add encryption to userfile
        if not self.login:
            raise AttributeError('you\'re not logged in')
        if self.user == username:
            self.user = None
            self.login = False
            dae.encrypt_folder(username)
            return f'{username} Logged out Successfully'
        elif self.user != username:
            return f'you\'re not logged in as {username}'
        
    def remove_user(self, master_password):#Done
        if not self.login:
            raise AttributeError('You\'re not logged in')
        answer = input('are you sure you want to delete your Password Manager account? (y/n): ')
        if answer == 'y':
            confirmation = input('if you delete you Password Manager account all your passwords will desapear are you sure you want to do that? (y/n): ')
            if confirmation == 'y' and self.login:
                dae.delete_user(self.user, master_password)
                return 'your accout was deleted successfully all your data was erased'
            elif confirmation == 'n':
                return 'the operation was canceled thank you for staying with us'
        elif answer == 'n':
            return 'the operation was canceled thank you for staying with us'

    def change_password(self, url, username, new_password):#Done
        if not self.login:
            raise ValueError('Login Failed')
        url = f'{url}.csv'
        if dae.account_validation(f'users/{self.user}',url, isdir= True) and dae.show_account(f'users/{self.user}/{url}', username):
            if dae.decrypt(dae.show_account(f'users/{self.user}/{url}', username)['password']) == new_password:
                return 'You can\'t change the password into the same password'     
            elif dae.show_account(f'users/{self.user}/{url}', username)["username"] == username and dae.decrypt(dae.show_account(f'users/{self.user}/{url}', username)["password"]) != new_password:
                dae.change_password(f'users/{self.user}/{url}', username, new_password)
                return 'password has been changed seccessfully'
        else:
            return 'account was not found'

    def add_account(self, url, username, password):#Done
        if not self.login:
            raise ValueError('Login Failed')
        elif self.login:
            dae.creat_account(self.user, url, username, password)
            return 'Account added seccessfully'
        else:
            print(f'username {username} already exicte')
           
    def delete_account(self, url, username):#Done
        if not self.login:
            raise ValueError('Login Failed')
        url = f'{url}.csv'
        if not dae.account_validation(f'users/{self.user}/{url}', username):
            return 'couldn\'t find the account'
        answer = input('are you sure you want to delete your account? (y/n): ')
        if answer == 'y' and self.login:
            dae.remove_account(f'users/{self.user}/{url}', username)
            return 'account was deleted sccessfully'
        elif answer == 'n':
            return 'the delete operation was canceled'
        else:
            print('account was not found')
   
    def show_account(self, url, username):#Done
        if not self.login:
            raise ValueError('Login Failed')
        url = f'{url}.csv'
        if dae.account_validation(f'users/{self.user}/{url}', username):
            return f'Usename: {dae.show_account(f'users/{self.user}/{url}', username)['username']},  Password: {dae.decrypt(dae.show_account(f'users/{self.user}/{url}', username)['password'])}'
        else:
            return 'account was not found'

    def password_generator(self, lenth, lower = None , upper = None , nums = None , spetial_char = None, addition = None):
        global char
        char = string.ascii_letters
        global char_low
        char_low = string.ascii_lowercase
        global char_up
        char_up = string.ascii_uppercase
        global num
        num = string.digits
        global spetials
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
        if 0 <= password_score < 30:
            print('Weak Password!!')
        elif 30 <= password_score < 60:
            print("Normal Password")
        elif 60 <= password_score < 90:
            print("Strong Password")    
        elif password_score >= 90:
            print("Very Strong Password!!")
        return max(password_score, 0)






def main():
    hello = 'shut up'
    pm = PasswordManager()
    # pm.create_password_maneger_account('benyator', 'ramy123')
    # pm.create_password_maneger_account('zahra', 'ramy123')
    print(pm.login_user('zahra', 'ramy123'))
    # print(pm.login_user('bouchra', 'ramy123'))
    # print(pm.logout_user('zahra'))
    # print(pm.remove_user('ramy123'))
    # print(pm.add_account('instagram', 'ramy', 'ramy20074'))

    print(pm.add_account('google', 'ramy', 'ramy20074'))
    print(pm.add_account('instagram', 'ramy', 'ramy20074'))
    print(pm.add_account('github', 'ramy', 'ramy20074'))
    print(pm.add_account('facebook', 'ramy', 'ramy20074'))
    print(pm.change_password('facebook', 'ramy', 'ramy13'))
    print(pm.delete_account('facebook', 'ramy'))
    print(pm.show_account('github', 'bousba3'))
    # pm.logout_user('zahra')

    





    # generated_password = pm.password_generator(13, 4, 4, 4, 5, 'ramy')
    # print(generated_password)
    # pm.add_account('www.google.com', 'sabersukkakka@gmail.com', 'ramy@2007')
    # pm.add_account('www.google.com', 'ramy20074@gmail.com', 'ramy@0402')
    # pm.add_account('www.google.com', 'ramy.uchiha7@gmail.com', 'zahrablyat')
    # pm.delete_account('google.csv', 'ramy20074@gmail.com')
    # pm.show_account('www.google.com', 'ramy.uchiha7@gmail.com')
    # pm.change_password('www.google.com', 'ramy.uchiha7@gmail.com', 'ramy567')
    # pm.show_account('www.google.com', 'ramy.uchiha7@gmail.com')

    # print(pm.users)




    # ramy = PasswordManager()
    # ramy.add_account('www.zahra.dz', 'zahrablyat@suka.dz', 'fuckzahra123')
    # print(ramy.show_accounts)


    # print(f"password_generator(20, 0, 0, 0, 0, '') {len('VK`3p>^BsC;n9GLT<!ck')}")
    # print(f"password_generator(20, 4, 0, 0, 0, '') {len('!>9EcyxgXxZK+DIO')}")
    # print(f"password_generator(20, 4, 4, 0, 0, '') {len('vw"C>WwM]H}K')}")
    # print(f"password_generator(20, 4, 4, 4, 0, '') {len('59?a)njR')}")
    # print(gg)












if __name__ == '__main__':
    main()