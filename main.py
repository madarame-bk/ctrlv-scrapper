import string
import random
import requests
from bs4 import BeautifulSoup
import os
import threading

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def znaky(kolik):
    return "".join(random.choice(string.digits + string.ascii_uppercase + string.ascii_lowercase) for i in range(kolik))

os.makedirs("obrazky", exist_ok=True)

f=[]
o = open("f.txt", "r")
r=o.read()


#mod a+ je op jak svine, otevre se vsema pravomocema a jeste vytvori kdyz neexistuje coooo
batches=open("batches.txt", "a+")
batches.seek(0)
content=batches.read()
if len(content)==0:
    batches.write("1\n")
    current_batch=f"batch-1"
else:
    nm=int(max(content))+1
    current_batch=f"batch-{nm}"
    batches.write(f"{nm}\n")
print(current_batch)



pocet = int(input("Number of images: "))
if pocet == 0:
    exit()

os.makedirs(f"obrazky/{current_batch}", exist_ok=True)

def get_img():
    for i in range(pocet):
        znak=znaky(4)
        if znak in r:
            i -= 1
            print("skipped")
            continue
        page = requests.get(f"http://ctrlv.cz/{znak}")
        soup = BeautifulSoup(page.content, 'html.parser')
        shot=soup.find("img", {"alt": "Odeslaný screenshot obrázek "})
        #print(shot)
        if "notexists" not in str(shot):
            imgsrc=f"http://ctrlv.cz/{shot['src']}"
            #imgsrc=f"http://ctrlv.cz/3Qcj"
            img_data = requests.get(imgsrc).content
            #print(img_data)
            
            img_name = f"{znak}.png"
            
            f.append(znak)
            
            with open(f"obrazky/{current_batch}/{img_name}", 'wb') as handler:
                handler.write(img_data)
            print(f"{bcolors.OKGREEN}{znak}{bcolors.ENDC}")
            
        else:
            print(f"{bcolors.FAIL}{znak}{bcolors.ENDC}")
            f.append(znak)
            
    
    
numofthreads = int(input("Number of threads: "))
threads = []

for i in range(numofthreads):
    thread = threading.Thread(target=get_img)
    threads.append(thread)
    thread.start()

# Wait for all threads to complete
for thread in threads:
    thread.join()
    
with open("f.txt", "w") as file:
    for i in f:
        file.write(i+",")
print(f"{bcolors.BOLD}{bcolors.OKBLUE}done{bcolors.ENDC}")
