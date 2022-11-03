import json
from base64 import b64decode
from time import sleep, time
from art import tprint
from requests import get, post
from os.path import abspath, isfile
from os import remove
from prettytable import PrettyTable


class EDNAuto:
    init = True
    cookie = ''
    courseId = ''
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
    evaluateGradeUrl = []
    users = None
    insideGroupXSSCheckList = []
    outsideGroupXSSCheckList = []

    def getAccessToken(self):
        tokenFile = abspath('./token.txt')
        if not isfile(tokenFile):
            print('Next time, put your cookie in token.txt! Exiting...')
        else:
            try:
                self.accessToken = open(
                    tokenFile, 'r', encoding='utf-8').readlines()[0]
            except:
                print("token.txt is empty! Pls paste your cookie in that file!")

    def greeting(self):
        if not self.init:
            return
        info = self.accessToken.split('.')[1]
        info = b64decode(info+'==')
        info = json.loads(info)
        username = info["UserName"]
        self.username = username[:username.index("@")]
        print("")
        tprint(self.username, font='small')
        sleep(2)

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
        x = [104, 116, 116, 112, 115, 58, 47, 47, 102, 117, 97, 112, 105, 46, 101, 100, 117, 110, 101, 120, 116, 46, 118, 110, 47, 108, 101, 97, 114, 110, 47, 118, 50, 47, 99, 108, 97, 115, 115, 101,
             115, 47, 112, 114, 101, 115, 101, 110, 116, 99, 114, 105, 116, 105, 99, 97, 108, 47, 101, 118, 97, 108, 117, 97, 116, 101, 45, 105, 110, 115, 105, 100, 101, 45, 103, 114, 111, 117, 112]
        self.apiEvaluateInsideGroup = ''.join(chr(i) for i in x)
        x = [104,116,116,112,115,58,47,47,102,117,97,112,105,46,101,100,117,110,101,120,116,46,118,110,47,99,111,109,109,101,110,116,47,118,49,47,97,99,116,105,118,105,116,121,47,103,101,116,45,99,111,109,109,101,110,116,115]
        self.apiGetComments = ''.join(chr(i) for i in x)
        x = [104,116,116,112,115,58,47,47,102,117,97,112,105,46,101,100,117,110,101,120,116,46,118,110,47,99,111,109,109,101,110,116,47,118,49,47,97,99,116,105,118,105,116,121,47,97,100,100,45,99,111,109,109,101,110,116]
        self.apiAddComment = ''.join(chr(i) for i in x)
        x = [104,116,116,112,115,58,47,47,102,117,46,101,100,117,110,101,120,116,46,118,110,47,101,110,47,115,101,115,115,105,111,110,47,97,99,116,105,118,105,116,121,63]
        self.activityURL = ''.join(chr(i) for i in x)

    def getHeaderForAPI(self):
        header = {
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br",
            "authorization": self.accessToken,
            "cache-control": "no-cache",
            'content-type': 'application/json',
            "origin": self.url,
            "pragma": "no-cache",
            "referer": self.url,
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "sec-gpc": "1",
        }
        self.APIHeader = header

    def getSubjectInput(self):
        subj = input('Course Code: ')
        while (subj == ''):
            print("Course Code should not be empty!!")
            subj = input('Course Code: ')
        self.courseId = subj

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
            print("\nToken INVALID, pls consider to get a new token!")
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

    def showActions(self):
        table = PrettyTable()
        table.field_names = ["ID", "Action"]
        table.align["Action"] = "l"
        table.add_row(["1", "Auto Grade"])
        table.add_row(["2", "XSS Check"])
        table.add_row(["3", "Auto Answer"])
        table.add_row(["4", "Auto Vote"])
        print(table)
        self.actionCode = input(">>> ")
        if int(self.actionCode) > 3:
            print("Not Implemented! Please comeback later!")
            self.showActions()

    def getCourseDetail(self):
        self.classId = self.selectedCourse["classId"]
        self.courseId = self.selectedCourse["id"]
        params = {
            "classId": self.classId,
            "courseId": self.courseId
        }
        self.selectedCourseDetail = json.loads(
            get(self.apiClassSessionsDetails, params=params, headers=self.APIHeader).text)

    def getGradeUrl(self):
        try:
            self.users = None
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
                        if self.users == None:
                            users = self.getUsersInGroup(
                                groupId, activityId, self.classId)
                            self.users = users
                        self.evaluateGradeUrl.append(
                            self.apiEvaluateInsideGroup+f"?groupid={groupId}&activityId={activityId}&classId={self.classId}")
        except KeyboardInterrupt:
            print("\n\nOK! Grade on current urls\n\n")
            sleep(2)
            pass

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
        res = json.loads(get(self.apiGetUsersInGroup,
                         params=params, headers=self.APIHeader).text)
        return res["data"]

    def autoGrade(self):
        self.getGradeUrl()
        json_data = []
        for user in self.users:
            user_id = user["userId"]
            json_data.append(
                {
                    'userId': user_id,
                    'hardWorkingPoint': 5,
                    'goodPoint': 5,
                    'cooperativePoint': 5,
                }
            )
        number_of_url = len(self.evaluateGradeUrl)
        while (self.evaluateGradeUrl):
            url = self.evaluateGradeUrl.pop(0)
            res = post(url, headers=self.APIHeader, json=json_data)
            if res.ok:
                print(f'+ Grading {number_of_url-len(self.evaluateGradeUrl)}/{number_of_url}', end="\r")
        tprint("DONE", font="small")

    def getUrlForXSSCheck(self):
        self.insideGroupXSSCheckList = self.outsideGroupXSSCheckList = []
        try:
            for session in self.selectedCourseDetail["data"]["sessions"]:
                sessionid = session["sessionId"]
                for section in session["sections"]:
                    sectionTitle = section["title"]
                    print(sectionTitle)
                    for activity in section["activities"]:
                        activityId = activity["id"]
                        activityTitle = activity["title"]
                        print(f'\t{activityTitle}')
                        groupId = self.getGroupId(sessionid, activityId)
                        params = f"?Contextid={activityId}&CourseId{self.courseId}&ParentKey={groupId}&isPublic="
                        insideUrl = self.apiGetComments+params+"false"
                        outsideUrl = self.apiGetComments+params+"true"
                        self.insideGroupXSSCheckList.append(insideUrl)
                        self.outsideGroupXSSCheckList.append(outsideUrl)
        except KeyboardInterrupt:
            print("\n\nOK! Perform check on current urls\n\n")
            sleep(2)
            pass

    def isXSSInfected(self, comment):
        if "<script>" in comment:
            return True
        return False

    def xssCheck(self):
        self.getUrlForXSSCheck()
        table_inside = PrettyTable()
        table_outside = PrettyTable()
        table_inside.align = "l"
        table_outside.align = "l"
        table_inside.field_names = ["URL", "Content"]
        table_outside.field_names = ["URL", "Content"]
        print("+ Check INSIDE Group")
        number_of_url = len(self.insideGroupXSSCheckList)
        found = 0
        try:
            while self.insideGroupXSSCheckList:
                url = self.insideGroupXSSCheckList.pop(0)
                comments = json.loads(get(url, headers=self.APIHeader).text)["Comments"]
                print(f"+ Checking {number_of_url-len(self.insideGroupXSSCheckList)}/{number_of_url} --- Found: [ {found} ]", end="\r")
                for comment in comments:
                    content = comment["Content"]
                    if (self.isXSSInfected(content)):
                        found += 1
                        table_inside.add_row([url, content])
        except Exception as e:
            print("Error happen :) Sorry")
            print(e)
            input()
            pass
        
        try:
            print("+ Check OUTSIDE group")
            number_of_url = len(self.outsideGroupXSSCheckList)
            found = 0
            while self.outsideGroupXSSCheckList:
                url = self.outsideGroupXSSCheckList.pop(0)
                comments = json.loads(get(url, headers=self.APIHeader).text)["Comments"]
                print(f"+ Checking {number_of_url-len(self.outsideGroupXSSCheckList)}/{number_of_url} --- Found: [ {found} ]", end="\r")
                for comment in comments:
                    content = comment["Content"]
                    if (self.isXSSInfected(content)):
                        found += 1
                        table_outside.add_row([url, content])
        except Exception as e:
            print("Error happen :) Sorry")
            print(e)
            input()
            pass

        print("")
        print("XSS INSIDE")
        print(table_inside)
        print("XSS OUTSIDE")
        print(table_outside)


    def addComment(self):
        pass

    def autoAnswer(self):
        pass


    def action(self):
        if self.actionCode == '1':
            self.autoGrade()
        elif self.actionCode == '2':
            self.xssCheck()
        elif self.actionCode == '3':
            pass
            # self.autoAnswer()
        print("\n>> Press Enter to Continue <<\n")
        input()

    def init(self):
        self.createURL()
        self.getAccessToken()
        self.getHeaderForAPI()
        self.getCourses()

    def start(self):
        self.init()
        self.greeting()
        self.showCourses()
        self.getSubjectInput()
        self.courseLookUp()
        self.getCourseDetail()
        self.showActions()
        self.action()
