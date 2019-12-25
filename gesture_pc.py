import subprocess
import threading 
import time
import serial
import serial.tools.list_ports
import pyautogui
from win32gui import GetWindowText,GetForegroundWindow
from pushbullet import Pushbullet



try:
    Arduino_Serial = serial.Serial('com3',9600)
except:
    print('Problem connection to Serial port')

        

VOLUP=7
VOLDN=8
RIGHT=1
LEFT=2
UP=3
DOWN=4
NEAR=5
FAR=6




#function for get data from serial
def getdata():
    try:    
        value=int(str(Arduino_Serial.readline())[2:6])
        return value               
    except:
        try:
            value=int(str(Arduino_Serial.readline())[2:3])
            return value
        except:
            getdata()


#function for gesture        
def gesture(status):
    appName=GetWindowText(GetForegroundWindow()).split('- ')[-1]
    #print(appName,status)
    

    if status==VOLUP:
         pyautogui.press('volumeup')
    elif status==VOLDN:
         pyautogui.press('volumedown')
     
    elif appName=='Groove Music':
         if status==RIGHT:
             pyautogui.press('nexttrack')
         elif status==LEFT:
             pyautogui.press('prevtrack')
         elif status==NEAR:
             pyautogui.press('playpause')
         elif status==UP:
             pyautogui.hotkey('ctrl','t')
         elif status==DOWN:
             pyautogui.hotkey('ctrl','h')

    elif appName=='VLC media player':
         if status==RIGHT:
             pyautogui.hotkey('ctrl','right')             
         elif status==LEFT:
             pyautogui.hotkey('ctrl','left')
         elif status==UP:
             pyautogui.press('prevtrack')
         elif status==DOWN:
             pyautogui.press('nexttrack')
         elif status==NEAR:
             pyautogui.press('playpause')
         elif status==FAR:
             pyautogui.press('f')
    
    elif appName=='Google Chrome':
         if status==RIGHT:
             pyautogui.press('browserforward')         
         elif status==LEFT:
             pyautogui.press('browserback')
         elif status==UP:
             pyautogui.press('pageup')
         elif status==DOWN:
             pyautogui.press('pagedown')
         elif status==NEAR:
             pyautogui.hotkey('ctrl','+') 
         elif status==FAR:
             pyautogui.hotkey('ctrl','-')

    elif appName=='Power Point':
         if status==RIGHT:
             pyautogui.press('pagedown')       
         elif status==LEFT:
             pyautogui.press('pageup')
         elif status==UP:
             pyautogui.press('pageup')
         elif status==DOWN:
             pyautogui.press('pagedown')
         elif status==NEAR:
             pyautogui.press('f5')
         elif status==FAR:
             pyautogui.press('esc')

    elif appName=='Photos':
         if status==RIGHT:
             pyautogui.press('right')       
         elif status==LEFT:
             pyautogui.press('left')
         elif status==UP:             
             pyautogui.press('f5')
         elif status==DOWN:
             pyautogui.hotkey('ctrl','r')
         elif status==NEAR:
             pyautogui.hotkey('ctrl','+') 
         elif status==FAR:
             pyautogui.hotkey('ctrl','-')

    status=0

    
#function for air mouse
def mouse(value):
    if value == 0:
        value=1
        
    else:
        rvalue = value

        a =int((rvalue)%10)
        b =int((rvalue/10)%10)
        c =int((rvalue/100)%10)
        d =int((rvalue/1000)%10)
        #print(d)

        if (d == 2 ):
            xReading =  -30
        elif (d == 3 ):
            xReading =  -15
        elif (d == 4 ):
            xReading =  -5
        elif (d == 7 ):
            xReading =  5
        elif (d == 8 ):
            xReading =  15
        elif (d == 9 ):
            xReading =  30
        else:
            xReading =  0
        
        
        if (c == 2 ):
            yReading =  30
        elif (c == 3 ):
            yReading =  15
        elif (c == 4 ):
            yReading =  5
        elif (c == 7 ):
            yReading = -5
        elif (c == 8 ):
            yReading = -15
        elif (c == 9 ):
            yReading = -30
        else:
            yReading =  0

        #print(xReading,yReading)
        pyautogui.moveRel(xReading,yReading,duration=0)
        #pyautogui.moveRel(yReading,xReading,duration=0.05)


        

#pushbullet authenticatin

    
try:
    pb = Pushbullet("o.ix3hgbGjbdBaBnmY42mF3GNo3XouLS8a")
    pb.delete_pushes()#delete all pushes
except:
    print('Problem connection to Messege Server')
     


#funttion for pushbullet shutdown
def pushbullet():
    time.sleep(2)

    #exeption handle for null push messege
    try:
        pushes = str(pb.get_pushes()[0]).split(': ')[-1].strip('{''}'"'").upper()
        print("Messege :",pushes)
        
    except:
         #print('NO Messege')
         pushbullet()

                
    if pushes=='SHUTDOWN':
        pb.delete_pushes()
        subprocess.call(["shutdown", "/s"])        
        #print('shutdown')
        
    elif pushes=='LOGOUT':
        pb.delete_pushes()
        subprocess.call(["shutdown", "/l"])
        #print('logout')
        
    pushbullet()



#multithreading
try:            
    t1 = threading.Thread(target=pushbullet)
    t1.start() 
except:
    print('Internet connection falior')



#print(pyautogui.KEYBOARD_KEYS)



while True:
    #time.sleep(5)
    data=getdata()
    #print(data)
    if (data>=1000):
        mouse(data)
    else:
        gesture(data)
    #print('..')    
