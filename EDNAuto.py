import json
from time import sleep
from art import tprint
from requests import get, post
from os.path import abspath, isfile
from os import remove
from prettytable import PrettyTable


class EDNAuto:
    cookie = ''
    courseId = ''
    HTMLHeader = {}
    APIHeader = {}
    accessToken = ''
    username = ''
    url = ''
    apiURL = ''
    apiCourseCurrentUser = ''
    apiClassSessionsDetails = ''
    courseData = {}
    listOfCourses = []
    selectedCourse = {}
    token = ''

    def getCookie(self):
        cookieFile = abspath('./cookie.txt')
        if not isfile(cookieFile):
            print('Next time, put your cookie in cookie.txt! Exiting...')
        else:
            try:
                self.cookie = open(
                    cookieFile, 'r', encoding='utf-8').readlines()[0]
            except:
                print("cookie.txt is empty! Pls paste your cookie in that file!")

    def createURL(self):
        x = [104, 116, 116, 112, 115, 58, 47, 47, 102, 117, 46, 101, 100, 117,
             110, 101, 120, 116, 46, 118, 110, 47, 101, 110, 47, 104, 111, 109, 101]
        self.url = ''.join(chr(i) for i in x)
        x = [104, 116, 116, 112, 115, 58, 47, 47, 102, 117, 97, 112,
             105, 46, 101, 100, 117, 110, 101, 120, 116, 46, 118, 110]
        self.apiURL = ''.join(chr(i) for i in x)
        x = [104, 116, 116, 112, 115, 58, 47, 47, 102, 117, 97, 112, 105, 46, 101, 100, 117, 110, 101, 120, 116, 46, 118, 110, 47, 108, 101, 97, 114, 110, 47, 118, 50, 47,
             99, 108, 97, 115, 115, 101, 115, 47, 103, 101, 116, 45, 99, 111, 117, 114, 115, 101, 45, 99, 117, 114, 114, 101, 110, 116, 45, 111, 102, 45, 117, 115, 101, 114]
        self.apiCourseCurrentUser = ''.join(chr(i) for i in x)
        x = [104, 116, 116, 112, 115, 58, 47, 47, 102, 117, 97, 112, 105, 46, 101, 100, 117, 110, 101, 120, 116, 46, 118, 110, 47, 108, 101, 97, 114, 110, 47, 118, 50, 47,
             99, 108, 97, 115, 115, 101, 115, 47, 103, 101, 116, 45, 99, 108, 97, 115, 115, 45, 115, 101, 115, 115, 105, 111, 110, 115, 45, 100, 101, 116, 97, 105, 108, 115]
        self.apiClassSessionsDetails = ''.join(chr(i) for i in x)
        x = [104, 116, 116, 112, 115, 58, 47, 47, 102, 117, 97, 112, 105, 46, 101, 100, 117, 110, 101, 120, 116, 46, 118, 110, 47, 108, 101, 97, 114, 110, 47, 118, 50, 47,
             99, 111, 117, 114, 115, 101, 47, 103, 101, 116, 45, 115, 101, 115, 115, 105, 111, 110, 45, 97, 99, 116, 105, 118, 105, 116, 121, 45, 100, 101, 116, 97, 105, 108]
        self.apiSessionActivityDetail = ''.join(chr(i) for i in x)
        x = [104, 116, 116, 112, 115, 58, 47, 47, 102, 117, 97, 112, 105, 46, 101, 100, 117, 110, 101, 120, 116, 46, 118, 110, 47, 108, 101, 97, 114, 110, 47, 118, 50, 47, 99, 108, 97, 115, 115, 101, 115, 47, 112, 114,
             101, 115, 101, 110, 116, 99, 114, 105, 116, 105, 99, 97, 108, 47, 103, 101, 116, 45, 101, 118, 97, 108, 117, 97, 116, 101, 45, 105, 110, 115, 105, 100, 101, 45, 103, 114, 111, 117, 112, 45, 115, 99, 111, 114, 101]
        self.apiGetUsersInGroup = ''.join(chr(i) for i in x)
        x = [104,116,116,112,115,58,47,47,102,117,97,112,105,46,101,100,117,110,101,120,116,46,118,110,47,108,101,97,114,110,47,118,50,47,99,108,97,115,115,101,115,47,112,114,101,115,101,110,116,99,114,105,116,105,99,97,108,47,101,118,97,108,117,97,116,101,45,105,110,115,105,100,101,45,103,114,111,117,112]
        self.apiEvaluateInsideGroup = ''.join(chr(i) for i in x)

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
        self.HTMLHeader = dataPayload

    def getHeaderForAPI(self):
        header = {
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.9",
            "authorization": f"Bearer {self.accessToken}",
            "cache-control": "no-cache",
            'content-type': 'application/json',
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
        subj = input('Course Code: ')
        while (subj == ''):
            print("Course Code should not be empty!!")
            subj = input('Course Code: ')
        self.courseId = subj

    def getPage(self):
        print(r'Connecting to Server...', end='\r')
        res = get(self.url, headers=self.HTMLHeader)
        if (res.ok):
            return res.text
        else:
            print(
                "\nCookie may died, pls consider to get a new cookie!\nRemoving cookie.txt")
            remove(abspath('./cookie.txt'))
            print("Error connecting to server! Exiting...")
            exit(1)

    def getUserInfo(self):
        page = self.getPage().split('\n')
        self.getPage()
        accessTokenRaw = page[31]
        emailRaw = page[44]
        self.username = emailRaw.split(
            '=')[-1].strip().replace(";", '').replace('"', "").split('@')[0]
        self.accessToken = accessTokenRaw.split(
            '=')[-1].strip().replace(";", '').replace('"', "")

    def getCourses(self):
        res = get(self.apiCourseCurrentUser, headers=self.APIHeader)
        if (res.ok):
            courses = json.loads(res.text)
            self.listOfCourses = courses["data"]["listCourseOfUser"]
            for course in courses["data"]["listCourseOfUser"]:
                self.courseData[course["id"]] = {
                    "code": course["externalcode"],
                    "classId": course["classId"]
                }
        else:
            print(
                "\nCookie may died, pls consider to get a new cookie!\nRemoving cookie.txt")
            remove(abspath('./cookie.txt'))
            print("Error getting Courses! Exiting...")
            exit(1)

    def getClassIdByCourseId(self):
        for id, data in self.courseData:
            if id == self.courseId:
                return data
        print("Error when getting data. Exiting...")
        exit(1)

    def showCourses(self):
        table = PrettyTable()
        table.field_names = ["ID", "Course Code", "Class ID"]
        table.align["ID"] = "c"
        table.align["Course Code"] = "c"
        table.align["Class ID"] = "l"
        for id, data in self.courseData.items():
            table.add_row([id, data["code"], data["classId"]])
        print(table)

    def courseLookUp(self):
        for course in self.listOfCourses:
            if course['externalcode'] == self.courseId:
                self.selectedCourse = course
                return
        print('Course not found! Exiting...')
        exit(1)

    def showCourseInfo():
        ...

    def showActions(self):
        table = PrettyTable()
        table.field_names = ["ID", "Action"]
        table.align["Action"] = "l"
        table.add_row(["1", "Auto Grade"])
        table.add_row(["2", "Auto Answer"])
        table.add_row(["3", "Auto Vote"])
        print(table)
        self.actionCode = input(">>> ")
        if int(self.actionCode) > 2:
            print("Not Implemented! Please comeback later!")
            self.showActions()

    def getSessionsDetails(self):
        classId = self.selectedCourse["classId"]
        courseId = self.selectedCourse["id"]
        params = {
            "classId": classId,
            "courseId": courseId
        }
        self.selectedCourseDetail = json.loads(
            get(self.apiClassSessionsDetails, params=params, headers=self.APIHeader).text)
        for session in self.selectedCourseDetail["data"]["sessions"]:
            sessionid = session["sessionId"]
            for section in session["sections"]:
                sectionTitle = section["title"]
                print(f"Section {sectionTitle}")
                for activity in section["activities"]:
                    activityId = activity["id"]
                    activityTitle = activity["title"]
                    print(f"\tQuestion {activityTitle}")
                    groupId = self.getGroupId(sessionid, activityId)
                    users = self.getUsersInGroup(groupId, activityId, classId)
                    self.grade(groupId, activityId, classId, users)
            print("\n\n\n")

    def getGroupId(self, sid, aid):
        params = {
            "sessionid": sid,
            "activityId": aid
        }
        res = json.loads(get(self.apiSessionActivityDetail,
                         params=params, headers=self.APIHeader).text)
        return res["data"]["groupId"]

    def getUsersInGroup(self, gid, aid, cid):
        params = {
            "groupid": gid,
            "activityId": aid,
            "classId": cid
        }
        res = json.loads(get(self.apiGetUsersInGroup, params=params, headers=self.APIHeader).text)
        return res["data"]

    def grade(self, gid, aid, cid, users):
        params = {
            "groupid": str(gid),
            "activityId": str(aid),
            "classId": str(cid)
        }
        json_data = []
        for user in users:
            user_id = user["userId"]
            json_data.append(
                {
                    'userId': user_id,
                    'hardWorkingPoint': 5,
                    'goodPoint': 5,
                    'cooperativePoint': 5,
                }
            )
        res = post(self.apiEvaluateInsideGroup, params=params, headers=self.APIHeader, json=json_data)

    def autoGrade(self):
        ...

    def greeting(self):
        print()
        tprint(self.username, font="small")
        sleep(1)

    def action(self):
        if (self.actionCode == '1'):
            self.getSessionsDetails()

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
        self.showActions()
        self.action()
