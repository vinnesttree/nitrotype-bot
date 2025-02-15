from autocorrect import spell
try:
    from PIL import Image
except ImportError:
    import Image
import pyautogui as pg
pg.FAILSAFE = False
import pytesseract
import random
from autocorrect import spell
import string
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe" #if this is not the correct directory then change it
import cv2
import mss.tools as mt
from mss import mss
def correct(queue):
    queue.translate(str.maketrans('', '', string.punctuation))
    str_list = queue.split()
    result_list = []
    for word in str_list:
        sympos = []
        if (word.translate(str.maketrans('', '', string.punctuation)) == word):
            result_list.append(word)
        else:
            _word = list(word)
            for symbol in string.punctuation:
                for char in range(len(_word)):
                    if _word[char] == symbol:
                        sympos.append([char, symbol])
            adj = 0
            for item in sympos:
                _word.pop(item[0]-adj)
                adj+=1
            _word = list(spell(''.join(_word)))
            for item in sympos:
                _word.insert(item[0],item[1])
            result_list.append("".join(_word))
    queue = " ".join(result_list)
    queue+=",."
    #queue+=random.choice(string.ascii_letters)
    #queue+=random.choice(string.ascii_letters)
    return queue
def do_ocr(filename):
    return((pytesseract.image_to_string(Image.open(filename))))
def screenshot(filename):
    with mss() as sct:
        screen = sct.shot(output=filename)
    return(screen)
print("[Debug] Starting OCR Racer")
import time
#time.sleep(2)
end = False
refresh = ['%','%','%']
while True:
    pg.scroll(1000)
    screenshot("screen.png")
    imageObject  = Image.open("screen.png")
    imageObject.crop((700,840,1210,868)).save('line.png') # THESE VALUES MUST CHANGE TO WHERE IT SAYS "PLEASE WAIT..." ON THE GAME
    imageObject.crop((700,410,1200,470)).save('race.png') #THIS VALUE MUST CHANGE TO WHERE IT SAYS "RACE FINISHED"
    if(open("race.png","rb").read() == open("RESULTS.png","rb").read()): #YOU MUST CHANGE "RESULTS.png" FOR THIS TO WORK
        print('[Debug] Race End Detected')
        pg.press("enter")
        time.sleep(2)
        pg.scroll(1000)
        while True:
            screenshot("screen.png")
            imageObject  = Image.open("screen.png")
            imageObject.crop((700,840,1210,868)).save('waiting.png') # THESE VALUES MUST CHANGE (needs to be the same as line.png)
            if (open("waiting.png","rb").read() != open("wait.png","rb").read()):
                break
    imageObject.crop((700,840,1210,868)).save('line.png') # THESE VALUES MUST CHANGE (needs to be the same as waiting.png and line.png)
    queue = do_ocr("line.png")
    #print(queue)
    queue = queue.replace('’',"'")
    refresh.pop(0)
    refresh.append(queue)
    print(refresh)
    queue = correct(queue)
    queue = queue.replace('’',"'")
    #print(queue)
    pg.typewrite(queue, interval=random.uniform(0.03, 0.04))
    if (random.randint(1,4)==3):
        pg.typewrite(random.choice(string.ascii_letters)+random.choice(string.ascii_letters))
    pg.press('space')
    pg.scroll(1000)
    #time.sleep(0.2)
    if (len(set(refresh))==1 and (refresh[0] != 'Please wait. Typing content will')):
        #print("[Debug] Failsafe Triggered")
        #print(refresh)
        #pg.press('f5')
        time.sleep(5)
        refresh = ['%','%','%']
    if(refresh == ['Please wait. Typing content will', 'Please wait. Typing content will', 'Please wait. Typing content will']):
        screenshot("screen.png")
        #imageObject  = Image.open("screen.png")
        #imageObject.crop((750,300,1150,520)).save('isdq.png')
        pg.click(x=1017, y=482)
        time.sleep(5)
        #if (open("isdq.png","rb").read() == open("dq.png","rb").read()):
        #    print('[Debug] Disqualified (in another race)')
        #    pg.press('f5')
        #    time.sleep(3)
    screenshot("screen.png")
    imageObject  = Image.open("screen.png")
    imageObject.crop((750,300,1150,450)).save('inactive.png') #YOU NEED TO CHANGE THESE VALUES
    if (open("inactive.png","rb").read() == open("ia.png","rb").read()): #YOU MUST CHANGE "ia.png"
            print('[Debug] Disqualified (inactivity)')
            pg.press('f5')
            time.sleep(3)
