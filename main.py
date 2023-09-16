import requests

# Set your OpenAI API key here
API_KEY = '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'

# API endpoint
API_URL = 'https://api.openai.com/v1/chat/completions'

# Prompt to start the conversation
conversation_history = []

while True:
    user_input = input("You: ")
    conversation_history.append({"role": "user", "content": user_input})

    # Construct the payload
    payload = {
        "messages": conversation_history,
        "model": "gpt-3.5-turbo"
    }

    # Make the API request
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    response = requests.post(API_URL, json=payload, headers=headers)

    # Parse and display the response
    data = response.json()
    print(data)
