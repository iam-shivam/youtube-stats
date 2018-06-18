import getpass
import os
import time
import sys
import configparser
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import selenium.webdriver.support.expected_conditions as EC
import selenium.webdriver.support.ui as ui

currentDirectory = os.path.dirname(os.path.realpath(__file__)).replace("\\\\","\\")
sys.path.append(currentDirectory.replace('SupportFiles','Drivers'))

try:
    config = configparser.ConfigParser()
    configfile = os.path.join(currentDirectory,"config.ini")
    config.read(configfile)
    selectedbrowser = int(config.get('Browser', 'selected'))
except:
    print('Error. Switching Back To Chrome')
    selectedbrowser = 1


if(selectedbrowser is 2):
    profile = webdriver.FirefoxProfile()
    profile.accept_untrusted_certs = True
    driver = webdriver.Firefox(firefox_profile=profile)
elif(selectedbrowser is 3):
    driver = webdriver.Edge()
else:
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    driver = webdriver.Chrome(chrome_options=options)


def get_element(cssSelector):
    try:
        ele = ui.WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, cssSelector)))
        return ele
    except TimeoutException:
        return None


def scroll_down():
    spinner = get_element('paper-spinner')
    driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
    lenofpage = driver.execute_script("var lenofpage=document.documentElement.scrollHeight; return lenofpage;")
    match = False
    while (match == False):
        lastCount = lenofpage
        lenofpage = driver.execute_script(
            "window.scrollTo(0, document.documentElement.scrollHeight);var lenofpage=document.documentElement.scrollHeight;return lenofpage;")

        lenofpage = driver.execute_script("return document.documentElement.scrollHeight")
        spinner = get_element('paper-spinner')
        if lastCount == lenofpage:
            if(spinner is None and lenofpage == lastCount):
                print("No Spinner Found. Checking if we're at the end. Be back in 5.")
                time.sleep(5)
                lenofpage = driver.execute_script("return document.documentElement.scrollHeight")
                spinner = get_element('paper-spinner')
                if(spinner is None and lenofpage == lastCount):
                    print("Final checking... Be back in 15.s")
                    time.sleep(15)
                    lenofpage = driver.execute_script("return document.documentElement.scrollHeight")
                    spinner = get_element('paper-spinner')
                    if(spinner is None and lenofpage == lastCount):
                        print('Already At The End?')
                        match = True
    	
    #sleepTime = 3600
    #print('See You In ',sleepTime/60,' mins')
    #time.sleep(sleepTime)
    print('Waiting for stuff to load...')
    channels = int(len(driver.find_elements_by_css_selector('yt-formatted-string > a')))
    times = int(len(driver.find_elements_by_css_selector('ytd-thumbnail-overlay-time-status-renderer>span')))
    print(channels, times)
    while(channels - times > 2):
        channels = int(len(driver.find_elements_by_css_selector('yt-formatted-string > a')))
        times = int(len(driver.find_elements_by_css_selector('ytd-thumbnail-overlay-time-status-renderer>span')))
        print(channels, times)

    return True


def login():
    global userid
    global userpass

    userid = input('\nGoogleID: ')
    if userid.find('@') == -1:
        userid = userid[:] + "@gmail.com"
    	
    userpass = getpass.getpass("Password (Keep typing. It won't show up on screen): ")
    twoway = input('Do You Use Mobile Auth? [Enter n if you don\'t know] (y/n): ')
    print("\n\nLay Back. Rock Up. We'll let you know when something happens.")
    time.sleep(0.5)

    driver.get("https://www.youtube.com")
    signin = get_element("ytd-button-renderer>a")
    signin.click()
    time.sleep(0.5)

    uname = get_element("input[type='email']")
    uname.clear()
    uname.send_keys(userid)
    time.sleep(0.5)
    uname.send_keys(Keys.RETURN)
    
    if twoway=='y' and get_element("input[type='password']") is None:
        i = 15
        while i!=0:
            print('Check Your Mobile! You Have',i,'secs Left To Authenticate ', end='\r')
            i-=1
            time.sleep(1)
    else:
        pwd = get_element("input[type='password']")
        pwd.clear()
        pwd.send_keys(userpass)
        time.sleep(0.5)
        pwd.send_keys(Keys.RETURN)

    time.sleep(10)
    scrap()

def scrap():
    driver.get("https://www.youtube.com/feed/history")
    demo = scroll_down()

    channels = driver.find_elements_by_css_selector('yt-formatted-string > a')
    channelnames = dict()
    for channel in channels:
        key = channel.get_attribute('innerHTML')
        key = key[key.rfind('/')+1 : ]
        channelnames[key] = channelnames.get(key, 0) + 1

    videoLen = dict()
    videoLen['0-5'] = 0
    videoLen['5-15'] = 0
    videoLen['15-59'] = 0
    videoLen['>60'] = 0

    nettime = 0
    minutes = 0
    sec = 0

    resumePer = dict()
    resumePer['0-25'] = 0
    resumePer['25-50'] = 0
    resumePer['50-75'] = 0
    resumePer['75-100'] = 0

    times = driver.find_elements_by_css_selector('ytd-thumbnail-overlay-time-status-renderer>span')
    resume = driver.find_elements_by_css_selector('ytd-thumbnail-overlay-resume-playback-renderer>div')
    for tim in times:
        t = tim.get_attribute('innerHTML')
        t = t[2: t.rfind('\n')].strip()
        global a
        global b
        a = t[:t.find(':')]
        b = t[t.find(':')+1 :]

        if b.find(':')!=-1:
            c = b[b.find(':')+1 :]
            b = b[:b.find(':')]
            minutes = minutes + (60 * int(a))
            a = b
            b = c
            a = int(a)
            b = int(b)

            videoLen['>60'] += 1
            if (int(a) <= 5):
                videoLen['0-5'] -= 1
            elif (int(a) <= 15):
                videoLen['5-15'] -= 1
            elif (int(a) <= 59):
                videoLen['15-59'] -= 1


        if(int(a)<=5):
            videoLen['0-5'] += 1
        elif (int(a) <= 15):
            videoLen['5-15'] += 1
        elif (int(a) <= 59):
            videoLen['15-59'] += 1

        minutes = minutes + int(a)
        sec = sec + int(b)

    nettime = float(sec/3600) + float(minutes/60)
    netmins = float(nettime - int(nettime))*60
    netsecs = float(netmins - int(netmins))*60

    for res in resume:
        res = res.get_attribute('style')
        res = int(res[res.find(':')+1:res.find('%')].strip())
        if (res <= 25):
            resumePer['0-25'] += 1
        elif (res <= 50):
            resumePer['25-50'] += 1
        elif (res <= 75):
            resumePer['50-75'] += 1
        else:
            resumePer['75-100'] +=1

    for k in sorted(channelnames, key=channelnames.get):
        print(k,' : ', channelnames[k], '\n')

    print('\n--------------------------------------- \n')
    print('<--TOTAL VIDEOS-->\n')
    print('Total Videos: ', len(channels))
    print('\n--------------------------------------- \n')
    print('<--PLAYTIME-->\n')
    print('' , minutes , " minutes and " , sec , " Seconds")
    print('\n', int(nettime), 'Hours and ', int(netmins), 'Minutes and ', int(netsecs), 'Seconds. ')
    print('\n--------------------------------------- \n')
    print('<--VIDEO LENGTHS-->\n')
    print(videoLen)
    print('\n--------------------------------------- \n')
    print('<--HOW MUCH DID YOU WATCH?-->\n')
    print(resumePer)
	
    dir_path = currentDirectory.replace('SupportFiles','Stats')
    filename = userid[:userid.find('@')] + ' - YoutubeStats.txt'
    filepath = os.path.join(dir_path,filename)
    f = open(filepath , 'w', encoding='utf-8')

    f.write('\n<--CHANNELS-->\n\n')
    for k in sorted(channelnames, key=channelnames.get):
        f.write('%s : %d\n\n' % (k, channelnames[k]))
    f.write('\n\n--------------------------------------- \n')
    f.write('\n<--TOTAL VIDEOS-->\n\n')
    f.write('Total Videos: %d' % len(channels))
    f.write('\n\n--------------------------------------- \n')
    f.write('\n<--PLAYTIME-->\n\n')
    f.write("%d minutes and %d Seconds" % (minutes, sec))
    f.write('\n%d Hours and %d Minutes and %d Seconds. ' % (int(nettime),int(netmins),int(netsecs)))
    f.write('\n\n--------------------------------------- \n')
    f.write('\n<--VIDEO LENGTHS-->\n\n')
    for k, v in videoLen.items():
        f.write(str(k) + ' : ' + str(v) + '\n\n')
    f.write('\n\n--------------------------------------- \n')
    f.write('\n<--HOW MUCH DID YOU WATCH?-->\n\n')
    for k, v in resumePer.items():
        f.write(str(k) + '% : ' + str(v) + '\n\n')
    f.write('\n--------------------------------------- \n')


login()
