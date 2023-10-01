import pyautogui, webbrowser
from time import sleep
import pywhatkit
# include your country code and no spaces


# open whatsapp web
webbrowser.open('https://web.whatsapp.com/send?phone=+59899468304')
sleep(5)

pywhatkit.sendwhatmsg("hola mundo")
   