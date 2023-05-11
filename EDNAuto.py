from requests import get, post
import json
from art import tprint
from prettytable import PrettyTable
from time import sleep


class EDNAuto:
    stars = 5
    token = ""
    headers = {
        "content-type": "application/json",
        "authority": "fugw-edunext.fpt.edu.vn:4433",
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-GB,en;q=0.9,en-US;q=0.8",
        "access-control-allow-headers": "Content-Type",
        "access-control-allow-methods": "*",
        "access-control-allow-origin": "*",
        "content-type": "application/json",
        "dnt": "1",
        "origin": "https://fu-edunext.fpt.edu.vn",
        "referer": "https://fu-edunext.fpt.edu.vn/",
        "sec-ch-ua": '"Microsoft Edge";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.3",
    }
    user_data = {}
    courses = []
    selected_course = None
    class_info = None
    class_slots = []

    def __init__(self, token, stars=5) -> None:
        self.stars = stars
        self.token = token
        self.headers["authorization"] = f"Bearer {token}"

    def clean(self):
        self.user_data = {}
        self.courses = []
        self.selected_course = None
        self.class_info = None
        self.class_slots = []

    def auth(self):
        response = post(
            "https://fugw-edunext.fpt.edu.vn:8443/api/auth/token", headers=self.headers
        )
        self.user_data = response.json()["data"]

    def greeting(self):
        tprint(self.user_data["email"].split("@")[0].capitalize(), font="small")

    def get_courses(self):
        response = get(
            f"https://fugw-edunext.fpt.edu.vn:4433/api/v1/class/home/student?id={self.user_data['userId']}&semesterName=DEFAULT",
            headers=self.headers,
        )
        self.courses = response.json()

    def choose_course(self):
        table = PrettyTable()
        table.field_names = ["No", "Course Code", "Course Name"]
        table.align["Course Name"] = "l"
        for i, course in enumerate(self.courses):
            table.add_row([i + 1, course["courseCode"], course["title"]])
        print(table)
        course = int(input(">> "))
        self.selected_course = self.courses[course - 1]

    def load_course(self):  # returns Slots
        print()
        tprint(self.selected_course["courseCode"][:6])
        sleep(1)
        self.class_info = get(
            f"https://fugw-edunext.fpt.edu.vn:4433/api/v1/course/course-detail?id={self.selected_course['classId']}&currentPage=1&pageSize=10&statusClickAll=true",
            headers=self.headers,
        ).json()["data"]

    def parse_slots(self):  # returns list of Question in Slot
        self.class_slots = []
        for slot in self.class_info:
            self.class_slots.append(
                {
                    "slot": slot["order"],
                    "courseId": slot["courseId"],
                    "sessionId": slot["sessionId"],
                    "classroomSessionId": slot["classroomSessionId"],
                    "questions": json.loads(slot["questions"]),
                    "classroomId": self.selected_course["classId"],
                }
            )

    def get_group(self, classroomSessionId):
        response = post(
            f"https://fugw-edunext.fpt.edu.vn:4433/api/v1/group/list-group?classroomSessionId={classroomSessionId}",
            headers=self.headers,
        ).json()

        for group in response:
            for user in group["listStudentByGroups"]:
                if user["email"] == self.user_data["email"]:
                    return group

    def vote_indie(self):
        for slot in self.class_slots:
            print(f"Slot: {slot['slot']}")
            my_group = self.get_group(slot["classroomSessionId"])
            for question in slot["questions"]:
                try:
                    print(f"\tQuestion: {question['title']} ", end="")
                    gradeTeammatesList = []
                    groupId = my_group["id"]
                    classroomSessionId = my_group["classroomSessionId"]
                    privateCqId = question["privateCqId"]
                    for user in my_group["listStudentByGroups"]:
                        userIsGraded = user["id"]
                        userIsGradedId = user["id"]
                        gradeTeammatesList.append(
                            {
                                "groupId": groupId,
                                "classroomSessionId": classroomSessionId,
                                "privateCqId": privateCqId,
                                "userIsGraded": userIsGraded,
                                "userIsGradedId": userIsGradedId,
                                "hardWorking": self.stars,
                                "goodKnowledge": self.stars,
                                "teamWorking": self.stars,
                            }
                        )
                    json_data = {"gradeTeammatesList": gradeTeammatesList}
                    with open("gradeList.json", "w+", encoding="utf-8") as f:
                        f.write(json.dumps(json_data))
                    response = post(
                        "https://fugw-edunext.fpt.edu.vn:4433/api/v1/grade/grade-teammates",
                        # "http://localhost:8080/",
                        headers=self.headers,
                        data=json.dumps(json_data),
                    )
                    if response.ok:
                        print("OK")
                    else:
                        print("ERROR")
                except:
                    print("NOT STARTED!")

    def vote_group(self):
        ...

    def start_vote(self):
        ...

    def start(self):
        self.clean()
        self.auth()
        self.greeting()
        self.get_courses()
        self.choose_course()
        self.load_course()
        self.parse_slots()
        self.vote_indie()
