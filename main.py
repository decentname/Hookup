import socket
import random
import threading,traceback, os, subprocess, stat, shutil, StringIO, sys, select,mimetypes,urlparse
import kivy
kivy.require('1.7.2')
from kivy.utils import platform
if platform() == "android":
	from jnius import cast
	from jnius import autoclass
	from plyer import camera

if platform()!= "android":
	from sendfile import sendfile	
#from jnius import cast
#from jnius import autoclass

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.listview import ListView, ListItemButton
from kivy.uix.popup import Popup
from kivy.base import runTouchApp 
from kivy.adapters.dictadapter import ListAdapter
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.network.urlrequest import UrlRequest
 


#req = UrlRequest(url, on_success, on_redirect, on_failure, on_error,
 #                on_progress, req_body, req_headers, chunk_size,
  #               timeout, method, decode, debug, file_path, ca_file,
   #              verify)


#from Crypto.Cipher import _AES

mPeer=''
peer_list=[]
file_list=[]
status='Run'
peername_privatechat=''
file_tofetch=''
tracker_ip='192.168.43.1'


def chatclient(c,peername,message):
    global status    
    print('chatclient called')
    while True:
            
        if message == 'CHATEXIT':
            print ("Sorry ",peername, " is offline" )            
            break
        else:
            mlist=[]            
            print(message)
            mlist.append(message)
            name='Chat - '+peername
            res=TextInput(multiline=False)
            datasend='CHAT_START:'+mPeer+':'+str(res)
            if res == None:
                datas='CHAT_START:'+mPeer+':CHAT_EXIT'
                c.send(datas.encode())
                #droid.makeToast('going offline')
                
                break
            print('Sending : ',datasend)
            c.send(datasend.encode())
        mssg_type=c.recv(4096).decode()
        print('Receiving : ',mssg_type)
        peername=mssg_type.split(':')[1]
        message=mssg_type.split(':')[2]
    status='Run'
    main_menu()


def client(self,msg_type):
		global tracker_ip
		global peer_list
		global file_list
		global mPeer
		
		print "msg_type:",msg_type
		self.clear_widgets()
		s=socket.socket()
		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		if tracker_ip != None:
		    s.connect((tracker_ip,9989))
		    print 'Connected to tracker'
		    
		    try:
		        if msg_type=='PEERLIST':                
		            s.send('PEERLIST')
		            peer_list=[]       
		            self.rows=3
		            bt=Button(text="Back",size_hint=(0.2,0.2))
		            bt.bind(on_press=self.welcome)
		            self.add_widget(Label(text="Available peers",pos_hint={'center_x':0.5,'center_y':0.9}))        
		            while True:
					
		                temp=[]
		                datapeerip=s.recv(4096)
		                if not datapeerip:
		                    break
		                s.send('OK')
		                datapeername=s.recv(4096)
		                
		                if not datapeername:
		                    break                        
		                s.send('OK')
		                print datapeerip,datapeername
		                temp.append(datapeerip)
		                temp.append(datapeername)
		                peer_list.append(temp)
		                
		            print('Peer list retrieved as follows:')
		            print(peer_list)
		            
		            list_view = ListView(item_strings=[i[1] for i in peer_list])
		            self.add_widget(list_view)
		            self.add_widget(bt)
		            
		            return 'OK'
		            
		        elif msg_type=='FILELIST':
		            s.send('FILELIST')
		            file_list=[]
		            while True:					
		                datafilename=s.recv(4096)					
		                if not datafilename:
		                    break		            
		                s.send('OK')
		                datapeerip=s.recv(4096)
		                if not datapeerip:
		                    break		            
		                s.send('OK')
		                temp=[]
		                temp.append(datafilename)
		                temp.append(datapeerip)
		                file_list.append(temp)
		                size=len(file_list)
		                
		            self.rows=3
		            #layout4.add_widget(Label(text="your files"))
		            self.add_widget(Label(text="Files available for download"))
		            #self.add_widget(layout4)

		            print('File list retrieved as follows:')
		            print(file_list)
		            
		            list_view = ListView(item_strings=[i[0] for i in file_list])
		            self.add_widget(list_view)
		            bt=Button(text='Back',size_hint=(0.2,0.2))
		            bt.bind(on_press=self.welcome)
		            self.add_widget(bt)

		            return 'OK'
		    except:
		        traceback.print_exc()
		else:
		    print('Could not connect to tracker_ip')
		    print(traceback.print_exc())
		    return 'TRACKER ERROR'


	
def clientinfo(self,msg_type):
    global tracker_ip
    global peer_list
    global file_list
    global mPeer
    self.clear_widgets()
		
    s=socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    if tracker_ip != None:
        s.connect((tracker_ip,9989))
        print 'Connected to tracker'
        try:
            if msg_type=='PEERLIST':                
                s.send('PEERLIST')
                peer_list=[]               
                while True:
					
                    temp=[]
                    datapeerip=s.recv(4096)
                    if not datapeerip:
                        break
                    s.send('OK')
                    datapeername=s.recv(4096)
                    print 'hey'
                    print type(datapeername)
                    if not datapeername:
                        break                        
                    s.send('OK')
					#print datapeerip,datapeername
                    temp.append(datapeerip)
                    temp.append(datapeername)
                    peer_list.append(temp)
                    #data=s.recv(4096).decode()
                    #peer_list=pickle.loads(data)
                print('Peer list retrieved as follows:')
                print(peer_list)
                
                return 'OK'
            elif msg_type=='FILELIST':
                s.send('FILELIST')
                file_list=[]
                while True:
					
                    datafilename=s.recv(4096)
					
                    if not datafilename:
                        break
                
                    s.send('OK')
                    datapeerip=s.recv(4096)
                    if not datapeerip:
                        break
                
                    s.send('OK')
                    temp=[]
                    temp.append(datafilename)
                    temp.append(datapeerip)
                    file_list.append(temp)
                
                print('File list retrieved as follows:')
                print(file_list)
                
                return 'OK'
        except:
            traceback.print_exc()
    else:
        print('Could not connect to tracker_ip')
        print(traceback.print_exc())
        return 'TRACKER ERROR'





def handlepeerclient(c):
    global mPeer
    mssg_type=c.recv(1024)
    global path
    if mssg_type == 'NAME':
        global tracker_ip
        
        print('sending ',mPeer,'to ',tracker_ip)
        c.send(mPeer)
        c.close()
    elif mssg_type == 'FILELIST':
        print('filelist called')
        list_sharedfiles=[]
        for filename in os.listdir(path):
            list_sharedfiles.append(filename)
        print(list_sharedfiles )
        if len(list_sharedfiles) > 0:
            #data_shared=pickle.dumps(list_sharedfiles)
            for i in list_sharedfiles:
                if i!='Downloads':
                    c.send(i)
                    c.recv(1024)
            
            c.close()
        else:
            c.send('EMPTY')
            c.close()
            
        
    elif mssg_type.split(':')[0] == 'CHAT_START':
        global status
        print('INITIATING CHAT MODULE')
        print(mssg_type)
        peername=mssg_type.split(':')[1]
        message=mssg_type.split(':')[2]
        status='Exit'
        chatclient(c,peername,message)
        
    elif mssg_type.split(':')[0] == 'FILETRANSFER':
        peername=mssg_type.split(':')[1]
        filename=mssg_type.split(':')[2]
        #os.path='/sdcard/Hookup/'
        print('INITIATING FILE TRANSFER')
        #sendfile(c,peername,filename)
        try:
            myfile=open('/sdcard/Hookup/'+filename,'rb')
            offset=0
            blocksize=os.path.getsize('/sdcard/Hookup/'+filename)
            while True:
            	if platform()!="android":
            		sent=sendfile(c.fileno(),myfile.fileno(),offset,blocksize)
            		if sent==0:
            			break
            		offset+=sent
            	else:
            		l = myfile.read(4096)
            		while (l):
            			c.send(l)
            			l = myfile.read(4096)
                		if not l:
                			myfile.close()
                			c.close()
                    		break
               	print(" File Successfully Send on android")	
            	
            #obj=file_transfer_server.ClientThread(c)
            #obj.run(filename)
            #droid.makeToast(filename+' sent to '+peername+' successfully!')
        except Exception as e:
            print(e)
            
    elif mssg_type == 'VOICEMESSAGE':
        c.send('READY')
        try:
            with open("/sdcard/Hookup/sample_audio.mp3","wb") as f: 
                while True:
                    data=c.recv(1024)
                    if not data:
                        f.close()
                        break
                    f.write(data)
            #droid.makeToast("audio file recveived!")   
        except Exception as e:
            print(e)


def filechooser(self):
    filename=''
    file_selected=False
    #start='/storage/emulated/0/'
    start='/sdcard/Hookup/'
    while file_selected==False:
        list = [] 
        for filenames in os.listdir(start):     
            list.append(filenames)
            
        temp=list
        self.clear_widgets()
        self.list_adapter = ListAdapter(data=[i for i in temp],cls=ListItemButton,sorted_keys=[])
        self.list_adapter.bind(on_selection_change=self.display_selectedfile)
        list_view= ListView(adapter=self.list_adapter)
        self.add_widget(list_view)
        self.add_widget(Button(text="Upload file", on_press=self.fetch_onclick))
        

def fetchfile(self,filename,ip):
    global mPeer
    global file_tofetch
    try:
        s = socket.socket()         
        host = socket.gethostname()
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
        port = 9989             
        #s.bind((host, port))
        s.connect((ip,9989))
        print('Sending filename ',filename,' to ',ip)
        data='FILETRANSFER:'+mPeer+':'+filename
        s.send(data)
        try:
        	with open('/sdcard/Hookup/Downloads/'+filename, 'wb') as f:
		    	while True:
		        	data = s.recv(4096)
		        	if not data:
		        		f.close()
		        		break
		        	f.write(data)
			print('Successfully get the file')
			s.close()
            #file_transfer_client.receive(filename)
            #droid.makeToast('File received successfully in Hookup/Downloads folder')
        except Exception as e:
            print(e)
    except Exception as ee:
        print(ee)
   

def startchat(self,peerip,peername):
    global mPeer
    global mssg_privatechat
    print('startchat called')
    try:
        s=socket.socket()
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.connect((peerip,9989))
        #droid2=android.Android()
        while True:
            name='Chat - '+peername
            rs=TextInput(multiline=False)
            res=rs.text.encode('utf-8')
            datasend='CHAT_START:'+mPeer+':'+str(res)
            if res == None:
                datas='CHAT_START:'+mPeer+':CHAT_EXIT'
                s.send(datas)
                #droid.makeToast('going offline')
                s.close()
                break
            print('Send : ',datasend)
            s.send(datasend)
            datarec=s.recv(4096)
            print('Receive : ',datarec)
            if datarec.split(':')[2] == 'CHAT_EXIT':
                #droid2.dialogCreateAlert('Sorry, '+peername+' is offline')
                #droid2.dialogSetPositiveButtonText("OKAY")   
                #droid2.dialogShow()
                #response = droid2.dialogGetResponse().result           
                s.close()
                break
            
            #droid2.dialogCreateAlert('Message from '+peername,datarec.split(':')[2])
            #droid2.dialogSetPositiveButtonText("OKAY")   
            
            #droid2.dialogShow()
            #response = droid2.dialogGetResponse().result  
    except Exception as e:
        print(e)
        

    

def server():
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('',9989))
    s.listen(10)
    while True:
        #global tracker_ip
        c,addr = s.accept()
        print('Connected to ',addr[0])
        #tracker_ip=addr[0]
        threading.Thread(target=handlepeerclient, args=(c,)).start()        

def startserverpeer():
		#self.clear_widgets()
		global mPeer
		try:
			threading.Thread(target=server).start()
		except Exception,e:
			print e	
	        
	
class Home(GridLayout):
	def __init__(self,**kwargs):
		global mPeer
		global peername_tochat
		#sm.current='first'
		super(Home,self).__init__(**kwargs)
		self.rows=6
		self.add_widget(Label(text="Welcome To Hookup"))
		self.add_widget(Label(text='Enter Peername'))
		self.peername=TextInput(multiline=False,font_size=40,size_hint=(0.6,0.6))
		#mPeer=self.peername.text.encode('utf-8')
		self.add_widget(self.peername)
		bt=Button(text="Submit",size_hint=(0.2,0.5))
		bt.bind(on_press=self.welcome)
		self.add_widget(bt)
		self.add_widget(Label(text=''))
		self.add_widget(Label(text=''))
		startserverpeer()
	
	def welcome(self,instance):
		self.clear_widgets()
		
		global mPeer
		self.rows=10
		mPeer=(self.peername.text).encode('utf-8')
		head=GridLayout(cols=3)
		
		head.add_widget(Label(text=""))
		head.add_widget(Label(text="HOOkUP"))
		head.add_widget(Label(text="Hello" + " " + mPeer))
		self.add_widget(head)
		bt1=Button(text='My peers',size_hint=(0.3,0.3))
		bt2=Button(text='My Shared Folder',size_hint=(0.3,0.3))
		bt3=Button(text='Search file',size_hint=(0.3,0.3))
		bt4=Button(text='Upload file',size_hint=(0.3,0.3))
		bt5=Button(text='Send Voice Message',size_hint=(0.3,0.3))
		bt6=Button(text='Group chat',size_hint=(0.3,0.3))
		bt7=Button(text='Private chat',size_hint=(0.3,0.3))
		bt1.bind(on_press=self.func1)
		bt2.bind(on_press=self.func2)
		#bt1.bind(on_press=self.func3)
		#bt2.bind(on_press=self.func3)
		bt3.bind(on_press=self.func3)
		bt4.bind(on_press=self.func4)
		bt5.bind(on_press=self.func4)
		bt6.bind(on_press=self.func4)
		bt7.bind(on_press=self.func7)
				#layout1.add_widget(bt1)
		#layout1.add_widget(bt2)
		#layout1.add_widget(bt3)
		#layout1.add_widget(bt4)
		#layout1.add_widget(bt5)
		#layout1.add_widget(bt6)
		#layout1.add_widget(bt7)
		self.add_widget(bt1)
		self.add_widget(bt2)
		self.add_widget(bt3)
		self.add_widget(bt4)
		self.add_widget(bt5)
		self.add_widget(bt6)
		self.add_widget(bt7)
		if platform()=='android':
			bt8=Button(text='Take Picture',size_hint=(0.3,0.3))
			bt9=Button(text='Capture Video',size_hint=(0.3,0.3))
			bt8.bind(on_press=self.func8)
			bt9.bind(on_press=self.func9)
			self.add_widget(bt8)
			self.add_widget(bt9)
		
	
	
	
	
	
	def func1(self,instance):
		print("bt1 my peers called")
		returncode=client(self,'PEERLIST')
		
	def openfileThread(self,instance):
		global path
		filename =self.list_adapter.selection[0].text
		if platform() == "android":
			PythonActivity = autoclass('org.renpy.android.PythonActivity')
			Intent = autoclass('android.content.Intent')
			Uri = autoclass('android.net.Uri')
			location="/sdcard/Hookup/"
			print 'shared onclick called'
			
			locate="/sdcard/Hookup/"+filename
			mimetype = mimetypes.guess_type(locate)[0]
			image_uri = urlparse.urljoin('file://', locate)
			print("Starting intent...")
			intent = Intent()
			intent.setAction(Intent.ACTION_VIEW)
			intent.setDataAndType(Uri.parse(image_uri), mimetype)
			currentActivity = cast('android.app.Activity', PythonActivity.mActivity)
			currentActivity.startActivity(intent)
			print("Finished intent")
			
			#self.welcome()
			
		else:
			os.system("xdg-open " + path + filename)
	
	def func2(self,instance):
		global path
		print("bt2 Shared folder called")
		self.clear_widgets()
		self.rows=4
		list_sharedfiles=[]
		for filename in os.listdir(path):
			list_sharedfiles.append(filename)
		print list_sharedfiles
		temp=[]
		temp=list_sharedfiles
		self.add_widget(Label(text="Your Files:",size_hint=(0.3,0.3)))
		list_item_args_converter = lambda row_index, row_data: {'text':row_data, 'size_hint_y': None, 'height': '60dp'}
		self.list_adapter = ListAdapter(data=[i for i in list_sharedfiles],cls=ListItemButton,sorted_keys=[],args_converter=list_item_args_converter)
		self.list_adapter.bind(on_selection_change=self.display_selectedfile)
		list_view= ListView(adapter=self.list_adapter)
		self.add_widget(list_view)#bt=Button()
		self.add_widget(Button(text="Open file", size_hint=(0.2,0.2), on_press=self.openfileThread))
		bt=Button(text='Back',size_hint=(0.2,0.2))
		bt.bind(on_press=self.welcome)
		self.add_widget(bt)
		 
            
	def func3(self,instance):
		global file_list
		print("bt3 search file called")
		returncode=clientinfo(self,'FILELIST')
		if returncode =='OK':
			print(returncode)
			print file_list
			
			self.clear_widgets()
			#self.orientation='vertical'
			self.rows=3
		
			temp=[]
			for file in file_list:
				temp.append(file[0])
			#temp.append(peer[1])	
			print "temp"
			print temp
			list_item_args_converter = lambda row_index, row_data: {'text':row_data, 'size_hint_y': None, 'height': '60dp'}
			self.list_adapter = ListAdapter(data=[i for i in temp],cls=ListItemButton,sorted_keys=[],args_converter=list_item_args_converter)
			self.list_adapter.bind(on_selection_change=self.display_selectedfile)
			list_view= ListView(adapter=self.list_adapter)
			self.add_widget(list_view)
			#bt=Button()
			self.add_widget(Button(text="Fetch file", on_press=self.fetch_onclick,size_hint=(0.2,0.2)))
			self.add_widget(Button(text="Back",on_press=self.welcome,size_hint=(0.2,0.2)))
		
			#print('SELECTED file = ',choice[0],' by ',choice[1])
			#fetchfile(choice[0],choice[1])
		elif returncode == 'TRACKER ERROR':
			droid.makeToast('Could not connect to tracker ip')
                    
                    
                    

	def func4(self,instance):
		print("bt4 upload file called")
		filepath,filename=filechooser(self)
		print('File chosen is ',filename,' at',filepath)
		
	def func8(self,instance):
		num = random.randrange(1,20)
		filename = 'image'+str(num)+'.jpg'
		camera.take_picture('/sdcard/Hookup/'+filename, self.welcome)
		
	def func9(self,instance):
		num = random.randrange(1,20)
		filename = 'vid'+str(num) + '.mp4'
		camera.take_video('/sdcard/Hookup/'+filename, self.welcome)
	
	def display_selectedfile(self,adapter,*args):
		global file_tofetch		
		file_tofetch =self.list_adapter.selection[0].text 
		print 'selected item is: ',file_tofetch
		
			
		
	def sharedfile_onclick(self,instance):
		threading.Thread(target=self.openfileThread).start()
	
	
	def display_selectedpeer(self,adapter,*args):
		global peername_privatechat
		print 'selected item is:'		
		peername_privatechat =self.list_adapter.selection[0].text 
		print peername_privatechat
		
	
	
	def fetch_onclick(self,instance):
		self.clear_widgets()
		global file_tofetch
		global file_list
		self.rows=2
		self.add_widget(Label(text="hello world",size_hint=(0.2,0.2)))
		self.add_widget(Button(text="Back",on_press=self.welcome,size_hint=(0.2,0.2)))
		for p in file_list:
			if file_tofetch==p[0]:
				peerip=p[1]
    			
		fetchfile(self,file_tofetch,peerip)
			
		
	def startchat_onclick(self,instance):
		#super(LoginScreen, self).__init__(**kwargs)
		self.clear_widgets()
		global peername_privatechat
		global mssg_privatechat
		self.rows=2
		#footer = GridLayout()
		footer = GridLayout(cols=2, size_hint_y=None, height=40)
		self.label_privatechat=Label(text="hello world", size_hint_y=.8, halign='left', valign='top', markup=True)
		self.add_widget(self.label_privatechat)
		self.textinput_privatechat=TextInput(multiline=True,font_size=16)
		footer.add_widget(self.textinput_privatechat)		
		footer.add_widget(Button(text="Send", size_hint_x=None, width=100, on_press=self.privatechat_onclicksend))
		peerip_privatechat=''
		self.add_widget(footer)
		for p in peer_list:
			if peername_privatechat==p[1]:
				peerip_privatechat=p[0]
				peername_privatechat=p[1]
		print 'CHATTING WITH '+peerip_privatechat
		self.label_privatechat.text='[b]Chatting with '+peername_privatechat+'[/b]'
		try:
			
		    s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		    s.connect((peerip_privatechat,9989))
		    print 'Connected to', peername_privatechat
		    while 1:
		    	
				socket_list = [sys.stdin, s]
				print "1"         
				# Get the list sockets which are readable
				read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])
				 
				print "2"
				for sock in read_sockets:
				    #incoming message from remote server
				    print "hey"
				    if sock == s:
				        data = sock.recv(4096)
				        
				        
				        if not data :
				            print '\nDisconnected from chat server'
				            sys.exit()
				        else :
				        	print data
				        	self.label_privatechat.text=self.label_privatechat.text+'\n[b]'+peername_privatechat+'[/b] '+data
				            #print data
				            #sys.stdout.write(data)
				            #prompt()
				            
				     
				    #user entered a message
				    else :
				        msg = sys.stdin.readline()
				        
				        if(msg == 'EXITCHAT'):
				        	s.close()
				        	
				        s.send('CHAT_START:'+mPeer+':'+msg)
				        self.textinput_privatechat.text=''
				        #prompt()
		except Exception as e:
			print e		    
				        
    	
		
		
		#startchat(self,peerip_privatechat,peername_privatechat,textinput_privatechat)
		
	def privatechat_onclicksend(self, instance):
		self.label_privatechat.text=self.label_privatechat.text+'\n[b]You:[/b] '+self.textinput_privatechat.text.encode('utf-8')
		#self.textinput_privatechat.text=''
		sys.stdin = StringIO.StringIO(self.textinput_privatechat.text.encode('utf-8'))
		
		
			
		
	def func7(self,instance):
		global peer_list
		print("bt7 private chat called")
		returncode=clientinfo(self,'PEERLIST')
		plist=[]
		if returncode =='OK':
			print(returncode)
		print peer_list
		
		for peer in peer_list:
			plist.append(peer)
			
			
		#print plist
			
		#print plist
		
		temp=[]
		for peer in plist:
			temp.append(peer[1])	
			
		print temp
		
		self.clear_widgets()
		#self.orientation='vertical'
		self.rows=2
		
		self.list_adapter = ListAdapter(data=[i for i in temp],cls=ListItemButton,sorted_keys=[],selection_mode='single')
		self.list_adapter.bind(on_selection_change=self.display_selectedpeer)
		list_view= ListView(adapter=self.list_adapter)
		self.add_widget(list_view)
		self.add_widget(Button(text="Start Chat", on_press=self.startchat_onclick))
		
		
class MyApp(App):
	def build(self):
		return Home()
		
	def on_pause(self):
		return True
		
	def on_resume(self):
		pass


    
path='/sdcard/Hookup/'

if __name__=='__main__':
	MyApp().run()