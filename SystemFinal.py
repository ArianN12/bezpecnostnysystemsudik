from importantKeyPad import keypad
from time import sleep
import threading
import RPi.GPIO as GPIO
import smtplib
import time
from email.message import EmailMessage
import LCD1602

PIRpin = 11
GPIO.setmode(GPIO.BOARD)
GPIO.setup(PIRpin, GPIO.IN, GPIO.PUD_DOWN)
LCD1602.init(0x27,1)

myPad = keypad(retChar = '*')
myString = ''
pwd = '1234'
pwdStop = '#7687'
pwdStopAlarm = 'D1234'
OutMenu = 'B'
previous_state = False
current_state = False
from_email_addr = "bezpecnostsudik@gmail.com"
from_email_pass = "fnjg cdtr vdqd pgjo"
to_email_addr = "bezpecnostsudik@gmail.com"

def readKP():
    global current_state
    global previous_state
    global from_email_addr 
    global from_email_pass 
    global to_email_addr
    
    global myString
    global CMD
    global OutMenu
    
    while myString != pwdStop:
        myString = myPad.readKeypad()
        sleep(.5)
readThread = threading.Thread(target = readKP,)
readThread.daemon = True
readThread.start()
LCD1602.write(0,0,'Preparing...          ')
sleep(3)
while myString != 'B' and myString != pwdStop:
    if myString != '1' and myString != '2' and myString != '3' or myString == 'B1' or myString == 'B2' or myString == 'B3':
        LCD1602.write(0,0,'Welcome in Menu!          ')
        LCD1602.write(0,1,'Move:1,2,3                 ')
    while myString == '1' and myString != pwdStop and myString != 'B1':
        LCD1602.write(0,0,'Arm system:A          ')
        LCD1602.write(0,1,'Disarm system:D                  ')
        if myString == pwdStop:
            LCD1602.write(0,0,'          ')
            break
        if myString == 'B':
            break
        if myString == 'B1':
            break
       
        pass
    
    while myString == '2' and myString != pwdStop and myString != 'B2':
        LCD1602.write(0,0,'Change pass:C          ')
        LCD1602.write(0,1,'Deactivate:#                  ')
        if myString == pwdStop:
            LCD1602.clear()
            break
        if myString == 'B':
            break
        if myString == 'B2':
            break
        pass
    
    while myString == '3' and myString != pwdStop and myString != 'B3':
        LCD1602.write(0,0,'OutMenu:B         ')
        LCD1602.write(0,1,'                  ')   
        if myString == pwdStop:
            LCD1602.clear()
            break
        if myString == 'B':
            break
        if myString == 'B3':
            break
        pass
    
LCD1602.clear()      
sleep(.1)
if myString == 'B':
    
    LCD1602.write(0,0,'Waiting...         ')
    LCD1602.write(0,1,'Choose an action        ')    
    

    
    
while myString != pwdStop:
    CMD = myString
    
    k = 0    
    if CMD == 'A' + pwd:
        if k == 0:
            for i in range(30,0, -1):
                i = str(i)
                LCD1602.write(0,0,'System preparing            ')
                LCD1602.write(0,1,'Time left: ' + str(i) +'    ')
                i = int(i)
                time.sleep(1)
            k += 1
        LCD1602.write(0,0,'System armed          ')
        LCD1602.write(0,1,'Disarm system:D                  ')
        j = 1
        while myString != pwdStop and j < 5 and myString != 'D' + pwd:
            LCD1602.write(0,1,'Disarm system:D          ')
                    
            
            
            previous_state = current_state
            current_state = GPIO.input(PIRpin)
          
            if current_state != previous_state and j < 5:
                new_state = "HIGH" if current_state else "LOW"
            
                msg = EmailMessage()
                body = "Alarm aktivovany!!!!!"
                msg.set_content(body)
                
                msg['From'] = from_email_addr
                msg['To'] = to_email_addr
                msg['Subject'] = 'DETEKTOR POHYBU'
                
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(from_email_addr, from_email_pass)
                
                server.send_message(msg)
                LCD1602.write(0,1,'Email sent          ')
                sleep(5)
                LCD1602.clear()
                LCD1602.write(0,0,'System armed            ')
                server.quit()
                time.sleep(30)
                j += 1
                print(j)
            if j == 5:
                while myString != 'B' and myString != pwdStop:
                    LCD1602.write(0,0,'System restored...             ')
                    LCD1602.write(0,1,'B for backup                ')
                    if myString == 'B':
                        LCD1602.clear()
                        LCD1602.write(0,0,'System backuping             ')
                        time.sleep(2)
                        LCD1602.write(0,0,'Waiting ...            ')
                        LCD1602.write(0,1,'Choose an action           ')
                        break
                    if myString == pwdStop:
                        break
                    pass
                
                
                
                    
                    
                
                
        
                
                
            
    if CMD == 'D' + pwd:
        LCD1602.write(0,0,'System disarmed           ')
        LCD1602.write(0,1,'                       ')
    if CMD == 'C' + pwd:
        LCD1602.write(0,0,'Password?      ')
        LCD1602.write(0,1,'                   ')
        while myString == 'C' + pwd:
            pass
        pwd = myString
        LCD1602.write(0,0,'Password changed     ')
        time.sleep(3)
        
        LCD1602.write(0,0,'Waiting...                 ')
        LCD1602.write(0,1,'Choose an action                ')
        
        
        
        
            
            
            
sleep(1)
LCD1602.clear()
LCD1602.write(0,0,'Deactivating...                     ')
sleep(3)
GPIO.cleanup()
LCD1602.clear()
msg = EmailMessage()
body = "System deaktivovany!!!!!"
msg.set_content(body)
                
msg['From'] = from_email_addr
msg['To'] = to_email_addr
msg['Subject'] = 'DETEKTIVACIA SYSTEMU'
                
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(from_email_addr, from_email_pass)
                
server.send_message(msg)
LCD1602.write(0,0,'Email sent          ')
sleep(5)
LCD1602.clear()
              
server.quit()
print('GPIO Good to Go')
    
    