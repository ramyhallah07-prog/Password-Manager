import csv
from cryptography.fernet import Fernet
import hashlib
import os
import shutil
import subprocess


def main():
    # encrypt_file('accounts.csv')
    # decrypt_file('accounts.csv', 'Ramy@04_2007')
    # creat_account('saber', 'www.snapshat.com','ramy_hallah', 'ramy123')
    # creat_account('zahra_hallah', 'ramy1233')
    # creat_account('ramyhallah', 'ramy1433')
    # print(decrypt_account('zahra_hallah', 'accounts.csv'))
    # print(encrypt('ramy2007'))
    # print(decrypt(b'gAAAAABqQTCyYPZSkluDgRWYSTuOEuBdCFgmMxgGJJ16LmKxwPjLtV97Eil3kLiAMRKffIQ0oPtHueNigUUMa-aWY_rpmhCA3g=='))
    # generate_uk('ramy')
    user = 'el-hawwary'
    decrypt_folder(user)

    # passw = encrypt('hrgmhrmhrgm',user)
    # creat_account('ramy', 'google', 'ramy20074@gmail.com', 'ramy@1812', uk= True)
    # print(decrypt('gAAAAABqSqHZq0fOBL-FYC9ch5iByPv1nmFBdTe3DHdJVIWG3uvph9ulhhnoySWzlUeMMlLFfK0ZDHXPYUfVlWPwIRvjSdgFZg==', user))
    # print(account_validation('users/ramy/google.csv', 'ramy'))
    # print(decrypt('gAAAAABqSm2Af4CTkrP35LC-dN9mn-upjC5Em5UQHiQpMRWtIOFGlBIB5IaZJw2O93OVrqg2TbQ61fiuXlJHwKIX5iLJ7fg8ZA=='))
    # print(decrypt(passw, user))
    # myaccount = show_account('users/ramy/google.csv', 'ramy20074@gmail.com')
    # print(decrypt(myaccount['password'], user))
    # creat_account('ramy', 'www.google.com', 'sukkam', 'ramy@1812')
    # creat_account('ramy', 'www.google.com', 'suk', 'ramy@1812')
    # creat_account('ramy', 'www.google.com', 'ramy@gmail.com', 'raaaaaaaaaa')
    # creat_account('ramy','www.google.com', 'ramy.uchiha7@gmail.com', 'ramy@2007')
    # remove_account('users/ramy/google.csv', 'ramy.uchiha7@gmail.com')
    # change_password('users/ramy/google.csv', 'ramy20074@gmail.com', 'ramy@2007suka')
    # add_user('zouhir', 'chibchib cho')
    # add_user('saber', 'saberkk16')
    # delet_user('saber', 'saberkk16')
    # print(add_account('users/users.csv','samybatata', 'chibchib cho'))
    # print(loguserin('zahra', 'ramy123'))
    user = "zahra"
    url = "facebook.csv"
    # uk_loader(user)
    # cipher = encrypt('ramyhallah2007', user)
    # print(cipher)
    # print(decrypt(cipher))
    # decrypt_folder(user)
    # print(account_validation('users/zahra/facebook.csv', 'ramy'), 'account validation')
    # print(change_password(f'users/{user}/{url}', 'ramy', 'ramy123'), 'change password')
    # print(show_account(f'users/{user}/{url}', 'moph')['username'])
    # print(account_validation('users/zahra', 'google.csv', isdir=True))
    # print(account_validation(f'users/{user}/{url}', 'ramy'))
    # print(os.path.isfile(f'users/{user}/{url}'))
    # folder = 'users/zahra'
    # for file in os.listdir(folder):
    #     print(file)
    # print(show_account('users/zahra', 'ramy'))

    # print(account_validation('users/users.csv', 'saber'))
    
#mJyCw2ZetH5nzbenbva11_tfokE2Zs9N-OQxAUJxjjw=

Mpass = ''
h = hashlib.new('sha512')
h.update(Mpass.encode())
Mpass = h.hexdigest()


def loguserin(username, MasterPassword):
    hmp = hashlib.new('sha512')
    hmp.update(MasterPassword.encode())
    MasterPassword = hmp.hexdigest()
    with open('users/users.csv', 'r') as usersCSV:
        users = csv.DictReader(usersCSV)
        for user in users: 
            if MasterPassword == user['password'] and username == user['username']:
                return True
        return False               

def add_user(username, MastrPassword):
    user_path = 'users/users.csv'
    hmp = hashlib.new('sha512')
    hmp.update(MastrPassword.encode())
    MastrPassword = hmp.hexdigest()
    add_account(user_path, username, MastrPassword, encrypting=False)
    os.makedirs(f'users/{username}', exist_ok=True)

def delete_user(username, MasterPassword):
    if loguserin(username, MasterPassword):
        remove_account('users/users.csv', username)
        shutil.rmtree(f'users/{username}', ignore_errors=True)
    elif not loguserin:
        return 'wrong password'

def file_validator(file_name):
    accountsCSV = []
    with open(file_name, 'r') as file:
        for row in file:
            accountsCSV.append(row)
        if accountsCSV and accountsCSV[0] == 'username,password\n':
            pass
        else:       
            with open(file_name, 'w') as file:
                file .write('username,password\n')

def account_validation(path, username, isdir = False):
    if not isdir:
        if os.path.isfile(path):
            with open(path, 'r') as Path:
                user = csv.DictReader(Path)
                if any(u['username'] == username for u in user): return True
                return False
    elif isdir:
        if os.path.isdir(path):
            if any(file == username for file in os.listdir(path)): return True
            return False

def generate_key():
    key = Fernet.generate_key()
    with open('secret key', 'wb') as secret_key:
        secret_key.write(key)

def keyloeader():
    return open('systemfiles', 'rb').read()

def encrypt_file(filename):
    key = keyloeader()
    fernet = Fernet(key)
    with open(filename, 'rb') as file:
        original_data = file.read()
    encrypted_data = fernet.encrypt(original_data)
    with open(filename, 'wb') as file:
        file.write(encrypted_data)

def decrypt_file(filename):
    key = keyloeader()
    fernet = Fernet(key)
    with open(filename, 'rb') as file:
        encrypted_data = file.read()
        oreginal_data = fernet.decrypt(encrypted_data)
    with open(filename, 'wb') as file:
        file.write(oreginal_data)
       
def encrypt(password, user= None):
    key = keyloeader() if not user else uk_loader(user)
    fernet = Fernet(key)
    cipher_password = fernet.encrypt(password.encode()).decode()
    return cipher_password

def decrypt(cipher_password, user= None):
    key = keyloeader() if not user else uk_loader(user)
    fernet = Fernet(key)
    password = fernet.decrypt(cipher_password.encode()).decode()
    return password

def encrypt_folder(user):
    shutil.make_archive(f'users/{user}', 'zip', f'users/{user}')
    shutil.rmtree(f'users/{user}', ignore_errors=True)
    encrypt_file(f'users/{user}.zip')

def decrypt_folder(user):
    decrypt_file(f'users/{user}.zip')
    shutil.unpack_archive(f'users/{user}.zip', f'users/{user}')
    os.remove(f'users/{user}.zip')


def decrypt_account(username, filename):
    with open(filename) as accounts_file:
        accounts = csv.DictReader(accounts_file)
        for account in accounts:
            if account['username'] == username:
                password = account['password']
                return f'username : {username} , password : {decrypt(password)}'
        return 'username not found'
    
def creat_account(user, url, username, password, uk = False):
    path = os.path.join('users', user)
    csv_path = os.path.join('users', user, f'{url}.csv')
    os.makedirs(path, exist_ok= True)
    if uk :
        add_account(csv_path, username, password,user=user)
    if not uk:add_account(csv_path, username, password)

def add_account(path, username, password, encrypting= True, user = None):
    if not account_validation(path, username):
        with open(path, 'a', newline='') as adder:
            file_validator(path)
            adder = csv.DictWriter(adder, fieldnames=['username', 'password'])
            if encrypting and user:
                adder.writerow({'username' : username, 'password': encrypt(password, user)})
            elif encrypting and not user:
                adder.writerow({'username' : username, 'password': encrypt(password)})
            elif not encrypting:
                adder.writerow({'username' : username, 'password' : password})
        return True
    else:
        return False

def remove_account(path, username):
    if account_validation(path,username):
        with open(path, 'r') as accounts:
            ACCOUNT = csv.DictReader(accounts)
            loa = [ account for account in ACCOUNT if account['username'] != username]
        with open(path, 'w', newline= '') as accounts:
            accounts.write('username,password\n')
        with open(path, 'a', newline='') as accounts:
            ar = csv.DictWriter(accounts, fieldnames=['username', 'password'])
            ar.writerows(account for account in loa)
    else:
        return 'account not fount'
    
def change_password(path, username, new_password):
    if account_validation(path, username):
        remove_account(path, username)
        add_account(path, username, new_password)
    else:
        return 'account not found'

def show_account(path, username):
    with open(path, 'r') as accounts:
        accreader = csv.DictReader(accounts)
        for account in accreader:
            if account['username'] == username:
                return account
        return False

def generate_uk(user):
    uk = Fernet.generate_key()
    kuser_path = os.path.join('users', user)
    os.makedirs(kuser_path, exist_ok=True)
    secret_path = os.path.join(kuser_path, 'systemfiles1')
    if not os.path.isfile(secret_path):
        with open(secret_path, 'wb') as user_key:
            user_key.write(uk)
        subprocess.run(['attrib', '+h', secret_path], shell=True)
    else: 
        return

def uk_loader(user):
    if os.path.isfile(f'users/{user}/systemfiles1'):
        return open(f'users/{user}/systemfiles1', 'rb').read()
    else:
        print('key was not found')

if __name__ == '__main__':
    main()