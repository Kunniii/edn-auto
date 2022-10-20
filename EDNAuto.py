import json
from time import sleep
from art import tprint
from requests import get
from os.path import abspath, isfile
from os import remove

class EDNAuto:
  cookie = ''
  subject = ''
  HTMLHeader = {}
  APIHeader = {}
  accessToken = ''
  username = ''
  url = ''
  apiURL = ''
  apiCourseURL = ''
  coursesCodeName = {}
  listOfCourses = []
  selectedCourse = {}

  def getCookie(self):
    cookieFile = abspath('./cookie.txt')
    if not isfile(cookieFile):
      print('Next time, put your cookie in cookie.txt! Exiting...')
    else:
      try:
        self.cookie = open(cookieFile, 'r', encoding='utf-8').readlines()[0]
      except:
        print("cookie.txt is empty! Pls paste your cookie in that file!")

  def createURL(self):
    x = [104,116,116,112,115,58,47,47,102,117,46,101,100,117,110,101,120,116,46,118,110,47,101,110,47,104,111,109,101]
    self.url = ''.join(chr(i) for i in x)
    x = [104,116,116,112,115,58,47,47,102,117,97,112,105,46,101,100,117,110,101,120,116,46,118,110]
    self.apiURL = ''.join(chr(i) for i in x)
    x = [104,116,116,112,115,58,47,47,102,117,97,112,105,46,101,100,117,110,101,120,116,46,118,110,47,108,101,97,114,110,47,118,50,47,99,108,97,115,115,101,115,47,103,101,116,45,99,111,117,114,115,101,45,99,117,114,114,101,110,116,45,111,102,45,117,115,101,114]
    self.apiCourseURL = ''.join(chr(i) for i in x)

  def getHeaderForHTML(self):
    dataPayload = {
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9',
    'cookie':  self.cookie,
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Microsoft Edge";v="96"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'image',
    'sec-fetch-mode': 'no-cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36 Edg/96.0.1054.53'
    }
    self.HTMLHeader = dataPayload;

  def getHeaderForAPI(self):
    header = {
      "accept": "*/*",
      "accept-encoding": "gzip, deflate, br",
      "accept-language": "en-US,en;q=0.9",
      "authorization": f"Bearer {self.accessToken}",
      "cache-control": "no-cache",
      "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
      "origin": self.url,
      "pragma": "no-cache",
      "referer": self.url,
      "sec-fetch-dest": "empty",
      "sec-fetch-mode": "cors",
      "sec-fetch-site": "same-site",
      "sec-gpc": "1",
      "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"
    }
    self.APIHeader = header

  def getSubjectInput(self):
    subj = input('Subject code (ABC123): ')
    while (subj == ''):
      print("Subject should not be empty!!")
      subj = input('Subject code (ABC123): ')
    self.subject = subj

  def getPage(self):
    print(r'Connecting to Server...',end='\r')
    res = get(self.url, headers=self.HTMLHeader)
    if (res.ok):
      return res.text
    else:
      print("\nCookie may died, pls consider to get a new cookie!\nRemoving cookie.txt")
      remove(abspath('./cookie.txt'))
      print("Error connecting to server! Exiting...")
      exit(1)

  def getUserInfo(self):
    page = self.getPage().split('\n')
    self.getPage()
    accessTokenRaw = page[31]
    emailRaw = page[44]
    self.username = emailRaw.split('=')[-1].strip().replace(";",'').replace('"',"").split('@')[0]
    self.accessToken = accessTokenRaw.split('=')[-1].strip().replace(";",'').replace('"',"")

  def getCourses(self):
    res = get(self.apiCourseURL, headers=self.APIHeader)
    if (res.ok):
      courses = json.loads(res.text)
      self.listOfCourses = courses["data"]["listCourseOfUser"]
      for course in courses["data"]["listCourseOfUser"]:
        self.coursesCodeName[course["externalcode"]] = course["title"]
    else:
      print("\nCookie may died, pls consider to get a new cookie!\nRemoving cookie.txt")
      remove(abspath('./cookie.txt'))
      print("Error getting Courses! Exiting...")
      exit(1)

  def showCourses(self):
    for externalcode, title in self.coursesCodeName.items():
      print(f"> {externalcode:5} : {title}")

  def courseLookUp(self):
    for course in self.listOfCourses:
      if course['externalcode'] == self.subject:
        self.selectedCourse = course
        return
    print('Course not found! Exiting...')
    exit(1)

  def greeting(self):
    print()
    tprint(self.username,font="small")
    sleep(1)

  def init(self):
    self.createURL()
    self.getCookie()
    self.getHeaderForHTML()
    self.getUserInfo()
    self.getHeaderForAPI()
    self.getCourses()

  def start(self):
    self.init()
    self.greeting()
    self.showCourses()
    self.getSubjectInput()
    self.courseLookUp()