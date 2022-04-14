from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import pyautogui
import pytube
import csv
from pytube import Search 
import os
#newline char to avoid list out of index (done)
# escape literal path error (done)
# error in which songs (done)
#rechecking (done)
#prioritise by relevance
#updation
driver = webdriver.Chrome(executable_path=r'C:\Users\Aditya Choudhary\Downloads\chromedriver_win32\chromedriver.exe')
pl_url=[]
accounts=[]
iterations=0
new_iterations=0
tracklist=[]
def constructor_step(end,start=2,i=0):
    global tracklist
    driver.implicitly_wait(10)
    try:
        j=0
        for x in range(start,end):
            temp=driver.find_element_by_xpath(f'//div[@aria-rowindex="{x}"]')
            l=temp.text.split('\n')
            if len(l)==7:
                l.pop(2)
            tempsong=Song(l[1],l[2],l[3],l[5])
            print(x,tempsong.name,tempsong.artist,tempsong.duration,tempsong.album)
            tracklist.append(tempsong)
            i+=1
            j+=1
        return i,j
    except Exception as e:
        print('const st ex code',e)
        return i,j
        
def playlists(account):
        playlists={}
        while True:
            if name=='':
                break
            else:
                name=input('Enter Name')
                playlists[name]=playlist.constructor()
        accounts[account]=playlist
class playlist:
    def __init__(self,url,user):
        self.user=user
        self.url=url
        self.name=self.extract_name(url)
        self.tracks=[]
        driver.implicitly_wait(5)
        self.implicit_tracknumber=len(self.tracks)
        self.explicit_tracknumber=int(self.extract_tracknumber(url))
        print(self.name , self.explicit_tracknumber)
        try:
            handle=open(f'{user} {self.name} data export','r',newline='',encoding='utf-16')
            
            self.implicit_tracknumber=len(handle.readlines())
            print('tr',self.implicit_tracknumber)
        except Exception as e:
            print('init ex code',e)



    def extract_name(self,url):
        driver.get(self.url)
        driver.implicitly_wait(5)
        return driver.find_element_by_xpath('//h1[@class="Type__TypeElement-goli3j-0 olqUm"]').text
    def extract_tracknumber(self,url):
        driver.get(self.url)
        driver.implicitly_wait(5)
        return driver.find_element_by_xpath('//span[@class="Type__TypeElement-goli3j-0 ebHsEf RANLXG3qKB61Bh33I0r2"]').text.split()[0]
    def constructor(self):
        global tracklist
        driver.get(self.url)        
        driver.implicitly_wait(30)
        pyautogui.scroll(-700)
        time.sleep(1)
        tracklist=[]
        while True:
            global iterations
            try:
                iterations,new_iterations=constructor_step(end=self.explicit_tracknumber+2,start=iterations+2,i=iterations)   
                print('new iterations',new_iterations)
                if iterations==self.explicit_tracknumber:
                    print('constructed')
                    self.tracks=tracklist
                    break
                pyautogui.scroll(-(new_iterations*56))
                time.sleep(2)
            except Exception as e:
                self.tracks.extend(tracklist)
                iterations,tracklist=0,[]
                print('const ex code',e)
        iterations,tracklist=0,[]
    def show(self):
        print(self.name,end='\n\n')
        print(self.explicit_tracknumber,end='\n\n') 
        for song in self.tracks:
            print(song.name , song.artist , song.duration , song.album , sep='  ')
    def exportplaylist(self,user):
        tracklist_export=self.tracks
        handle=open(f'{user} {self.name} data export','a',newline='',encoding='utf-16')
        writer=csv.writer(handle)
        for x in tracklist_export:
            try:
                
                writer.writerow([str(x.name),str(x.artist),str(x.album),str(x.duration)])
            except Exception as e:
                print('exp ex code',e)
        handle.close()
    def download(self,storage_path,filepath='',trackl=[]):
        download_errors=False
        queries=[]
        flag_dl=0
        if filepath!='':
            handle=open(r'{}'.format(filepath),'r',newline='',encoding='utf-16')
            tempdata=csv.reader(handle)
            for x in tempdata:
                print(type(x))
                queries.append(x)
            flag_dl=1
        elif trackl!=[]:
            queries=trackl
        else:
            queries=self.tracks  
        print(queries)
            
        for x in queries:
            if x!=[]:
                if flag_dl:
                    print(x)
                    searchtext=str(x[0])+' '+str(x[1])
                else:
                    searchtext=str(x.name)+' '+str(x.artist)    
            search=Search(searchtext)
            try:    
                for search_res in search.results:
                    if flag_dl:
                        if search_res.length in range(int(x[3].split(':')[0])*60+int(x[3].split(':')[1])-10,int(x[3].split(':')[0])*60+int(x[3].split(':')[1])+10):
                            streams=search_res.streams.filter(only_audio=True)
                            print(type(streams),len(streams))
                            searchtext=name_verification(searchtext)
                            print(searchtext)
                            streams.order_by('abr').last().download(r'{}'.format(storage_path),r'{}'.format(searchtext)+'.mp3')
                            print(f'downloaded {searchtext}')
                            break
                    else:
                        if search_res.length in range(int(x.duration.split(':')[0])*60+int(x.duration.split(':')[1])-10,int(x.duration.split(':')[0])*60+int(x.duration.split(':')[1])+10):
                            streams=search_res.streams.filter(only_audio=True)
                            searchtext=name_verification(searchtext)
                            streams.order_by('abr').last().download(r'{}'.format(storage_path),r'{}'.format(searchtext)+'.mp3')
                            print(f'downloaded {searchtext}')
                            break
                else:
                    searchtext=name_verification(searchtext)
                    search_res[0].filter(only_audio=True).order_by('abr').last().download(r'{}'.format(storage_path),r'{}'.format(searchtext)+'.mp3')
            except Exception as e:
                print(searchtext)
                handle=open(f'{self.name} download errors','a',newline='',encoding='utf-16')
                writer=csv.writer(handle)
                writer.writerow([searchtext,e])
                handle.close()
                print('dnl ex code',e)
                download_errors=True
        if download_errors:
            try:    
                self.download(storage_path,r'C:\Users\Aditya Choudhary\Documents\PyProjects\SpotiPy\{}'.format(f'{self.name} download errors'))
                os.remove(r'C:\Users\Aditya Choudhary\Documents\PyProjects\SpotiPy\{}'.format(f'{self.name} download errors'))
            except Exception as e:
                print('dnl err error',e)
    
    def playlist_creator(self,pl_name):
        pass
    def update(self,storage_path):
        
        self.constructor()
        handle=open(f'{self.user} {self.name} data export','a',newline='',encoding='utf-16')
        writer=csv.writer(handle)
        tracklist_export=self.tracks[self.implicit_tracknumber:]
        for x in tracklist_export:
            try:
                writer.writerow([str(x.name),str(x.artist),str(x.album),str(x.duration)])
            except Exception as e:
                print('upd ex code',e)
        handle.close()
        self.download(storage_path,trackl=self.tracks[self.implicit_tracknumber:])


        
class Song:
    def __init__(self,name,artist,album,duration):
        self.name=name
        self.artist=artist
        self.album=album
        self.duration=duration
def name_verification(name):
    name_l=list(name)
    forbidden_char=['<','>','/','\\','|','*',':','"','?',"'"]
    name_out=[]
    for x in range(len(name_l)):
        if name_l[x] in forbidden_char:
            print(name_l[x],x)
        else:
            name_out.append(name_l[x])
    print(name,''.join(name_out))
    return ''.join(name_out)
#main redacted 