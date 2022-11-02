import requests

TOKEN = ""
with open('token.txt', 'r') as f:
    TOKEN = f.readline();


headers = {
    'authority': 'fuapi.edunext.vn',
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.6',
    'authorization': TOKEN,
    'content-type': 'application/json',
    'origin': 'https://fu.edunext.vn',
    'referer': 'https://fu.edunext.vn/',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'sec-gpc': '1',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
}

params = {
    'activityId': '1416587',
    'classId': '5605',
    'groupid': '664519',
}	

json_data = [
    {
        'userId': 7706,
        'hardWorkingPoint': 5,
        'goodPoint': 5,
        'cooperativePoint': 5,
    },
    {
        'userId': 12037,
        'hardWorkingPoint': 5,
        'goodPoint': 5,
        'cooperativePoint': 5,
    },
    {
        'userId': 10874,
        'hardWorkingPoint': 5,
        'goodPoint': 5,
        'cooperativePoint': 5,
    },
    {
        'userId': 12040,
        'hardWorkingPoint': 5,
        'goodPoint': 5,
        'cooperativePoint': 5,
    },
]

response = requests.post('https://fuapi.edunext.vn/learn/v2/classes/presentcritical/evaluate-inside-group', params=params, headers=headers, json=json_data)
