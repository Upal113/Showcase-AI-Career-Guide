from flask import Flask, request, jsonify
import json
import asyncio

from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Load the jobs data from the jobs.json file
with open('jobs.json', 'r') as jobs_file:
    jobs_data = json.load(jobs_file)

@app.route('/recommend', methods=['POST'])
def recommend_courses():
    try:
        # Get the course and industry selections from the JSON request
        data = request.get_json()

        if 'courses' not in data or 'industry' not in data:
            return jsonify({'error': 'Both courses and industry must be provided in the request.'})

        selected_courses = data['courses']
        selected_industry = data['industry']
        taken_courses = selected_courses

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
        full_suggestion = []


        async def process_jobs(jobs, full_suggestion):
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
            print(full_suggestion)

            # Filter jobs based on the selected industry

            # Your code for processing selected_courses and generating recommendations goes here
            # Use filtered_jobs as the list of jobs to consider

            full_suggestion.append({'Job' : jobs['job'],
                'Company' : jobs['company'],
                'industry' : jobs['industry'],  
                'recommendation': assistant_reply})
        async def main(full_suggestion):
            tasks = [asyncio.create_task(process_jobs(jobs, full_suggestion)) for jobs in jobs_json["jobs"]]
            await asyncio.gather(*tasks)
        asyncio.run(main(full_suggestion))
        print(full_suggestion)
        with open('full_suggestion.json', 'w') as json_file:
            json.dump(full_suggestion, json_file, indent=4)
        return jsonify(full_suggestion)
    except Exception as e:
        return jsonify({'error': str(e)})
if __name__ == '__main__':
    app.run(debug=True)