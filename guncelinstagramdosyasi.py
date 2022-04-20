from selenium import webdriver
from getpass import getpass
import time
import requests
import json
import re
import os
import sys
import locale
import subprocess
import shutil
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
dil=locale.getdefaultlocale()
os.system('cls' if os.name == 'nt' else 'clear')
def intro():
    if dil[0]=="tr_TR":
       print("""
    #######################################################
    #                                                     #  
    # Cüneyt TANRISEVER // instagram resim toplama aracı  #
    #                                                     #  
    #######################################################
    """)
    else:
       print("""
    ########################################################
    #                                                      #    
    # Cüneyt TANRISEVER // instagram image collection tool #
    #                                                      #  
    ########################################################
    """)
intro()
options = Options()
options.add_argument('--no-sandbox')
options.add_argument('--disable-gpu')
options.add_argument('--log-level=3')

sira=0
sorskul=["İnstagram kullanıcı adınızı giriniz = ","Enter your username = "]
sorssifre=["İnstagram kullanıcı şifrenizi giriniz = ","Enter your user password = "]
kullaniciadi = input(sorskul[0] if dil[0] == 'tr_TR' else sorskul[1])
kulsifre = getpass(sorssifre[0] if dil[0] == 'tr_TR' else sorssifre[1])


sor1=["Resimlerini İndirmek İstediğiniz Kullanıcıyı Giriniz = ","Enter the User whose Pictures You Want to Download ="]
sor=input(sor1[0] if dil[0] == 'tr_TR' else sor1[1])

dizin=os.path.isdir(sor)
try:
    if dizin:
        kmt="RD /S /Q {}".format(sor)
        lnxkmt="rm -rf {}".format(sor)
        os.system(kmt if os.name=="nt" else lnxkmt)
        shutil.rmtree(sor)
except:
    pass
os.mkdir(sor)
os.chdir(sor)
sira=0
driver = webdriver.Chrome(options=options)
os.system('cls' if dil[0] == 'tr_TR' else 'clear')
intro()
bilgi=["İnstagram'a giriş yapılıyor...","Logging into instagram..."]
print(bilgi[0] if dil[0] == 'tr_TR' else bilgi[1])
driver.get("https://www.instagram.com/")
driver.implicitly_wait(7)
kulladi = driver.find_element_by_name('username')
sifre = driver.find_element_by_name('password')
giris = driver.find_element_by_xpath("//button[@type='submit']")
kulladi.send_keys(kullaniciadi)
sifre.send_keys(kulsifre)
giris.click()
driver.implicitly_wait(10)
try:
    buton=driver.find_element_by_xpath("//*[@id=\"react-root\"]/div/div/section/main/div/div/div/div/button")
except NoSuchElementException:
    buton=driver.find_element_by_xpath("//*[@id=\"react-root\"]/section/main/div/div/div/div/button")
buton.click()
driver.implicitly_wait(5)
buton2=driver.find_element_by_xpath("/html/body/div[5]/div/div/div/div[3]/button[2]")
buton2.click()
driver.implicitly_wait(5)
time.sleep(2)


addrs="https://www.instagram.com/"+sor+"/"
paddrs=addrs+"?__a=1"
driver.get(addrs)
say=0
resimlinkleri=[]
ekle="https://www.instagram.com/p/"
def say1():
    global say
    say+=1
    time.sleep(3)
sor1=["Resimler seçiliyor. Lütfen bekleyiniz...","Pictures are selected. Please wait..."]
print(sor1[0] if dil[0] == 'tr_TR' else sor1[1])
while True:
    if say==2:
        break
    else:
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
        time.sleep(3)
        kaynak=driver.page_source
        ara=re.findall("<a href=\"/p/(.*?)/\" tabindex=\"0\">",kaynak)
        #print(ara)
        for i in ara:
            ekle1=ekle+i+"/?__a=1"
            #print(ekle1)
            if ekle1 not in resimlinkleri:
                resimlinkleri.append(ekle1)
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
        time.sleep(3)
        kaynak1=driver.page_source
        
        if kaynak==kaynak1:
            say1()
        else:
            pass
resimlinkleri=list(set(resimlinkleri))
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36',
}
cookies = driver.get_cookies()
rq=requests.session()
for cookie in cookies:
    rq.cookies.set(cookie['name'], cookie['value'])
rq.headers.update(headers)
prf=rq.get(paddrs)
kaynak2=prf.content
a="<html><head></head><body><pre style=\"word-wrap: break-word; white-space: pre-wrap;\">"
dex4=json.loads(kaynak2)
resim=dex4["graphql"]["user"]["profile_pic_url_hd"]
rsm=resim.replace("amp;","")
git=rq.get(rsm)
open(sor+"_profil.jpg", 'wb').write(git.content)
resimsayisi=0
ensontoplam=len(resimlinkleri)+resimsayisi
bul="{\"width\":1080,\"height\":1080,\"url\":\"(.*?)\"},"
sor2=["İndirme başladı. Lütfen bekleyiniz...","Download started. Please wait..."]
print(sor2[0] if dil[0] == 'tr_TR' else sor2[1])
yaz5=open("linkler.txt","a")

for i in resimlinkleri:
    print(i)
    
    git=rq.get(i)
    dex1=git.content
   # print(dex1)
    cc= str(dex1).encode("utf-8")
    ara=re.findall(bul,str(cc))
    #print(ara)
    if len(ara)!=0:
        resimsayisi+=len(ara)
    fazlalik_azalt=[]
    for j in set(ara):
        #print (j)
        
        yaz5.write(str(j)+"\n")
        ayir=str(j).split("src")
        a=str(ayir[-1]).split(",")
        urlc=a[0].replace("\":","").replace("\\\\u0026","&").replace("\"","")
        git1=rq.get(urlc)
        sira+=1
        ad=sor+str(sira)+".jpg"
        open(ad, 'wb').write(git1.content)
ab=[str(sira+1)+" tane resim indirildi.",str(sira)+"  image has been downloaded."]
print(ab[0] if dil[0] == 'tr_TR' else ab[1])
print("--------------------------------------------------")
os.chdir("../")
ckm=os.getppid()
kmt="Taskkill /F /PID {}".format(ckm)
kmt1="kill -9 {}".format(ckm)
driver.close()
driver.quit()
if os.name == 'nt':
    output = subprocess.check_output(kmt, shell=True)
else:
    output = subprocess.check_output(kmt1, shell=True)
sys.exit()

