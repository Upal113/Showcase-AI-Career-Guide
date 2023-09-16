import json


taken_courses = ["CS 120", "CS 121", "CS 150"]

basic_skills = ""
inter_skills = ""
advanced_skills = ""

with open("courses.json", "r") as course_json:
    course_data = json.load(course_json)

for i in course_data["u of i"]["courses"]:
    if i["course_code"] in taken_courses:
        basic_skill = ",".join(i["skills"]["basic"])
        basic_skills += basic_skill + ","
        inter_skill = ",".join(i["skills"]["intermediate"])
        inter_skills += inter_skill + ","
        advanced_skill = ",".join(i["skills"]["advanced"])
        advanced_skills += advanced_skill + ","

print(basic_skills)
print(inter_skills)
print(advanced_skills)

with open("jobs.json", "r") as jobs:
    jobs_json = json.load(jobs)

import requests

# Set your OpenAI API key here
API_KEY = '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'

# API endpoint
API_URL = 'https://api.openai.com/v1/chat/completions'

# Prompt to start the conversation



for jobs in jobs_json["jobs"]:
    basic_skilled_requied = ",".join(jobs["skills"]["basic"])
    intermediate_skilled_requied = ",".join(jobs["skills"]["intermediate"])    
    advanced_skilled_requied = ".".join(jobs["skills"]["advanced"])
    user_input = "I want to work as a " + jobs["job"] + " at " + jobs["company"] + " They require basic skills " + basic_skilled_requied + " I have basic skills " + basic_skills + " They require intermediate skills " + intermediate_skilled_requied + " I have intermediate skills " + inter_skills +" They require advanced skills " + advanced_skilled_requied + " I have advanced skills " + advanced_skills + "Suggest me how to work on my skiils and suggest online courses in this format : Course1:Description"
    print(user_input)
    # Construct the payload with only user input
    payload = {
        "messages": [{"role": "user", "content": user_input}],
        "model": "gpt-3.5-turbo",
        "max_tokens": 1000  # You can adjust this value as needed
    }

    # Make the API request
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    response = requests.post(API_URL, json=payload, headers=headers)

    # Parse and display the assistant's response
    data = response.json()
    assistant_reply = data['choices'][0]['message']['content']
    print(f"ChatGPT: {assistant_reply}")





