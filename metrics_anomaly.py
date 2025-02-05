import os
import requests
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


url = "https://api.na-01.st-ssp.solarwinds.com/v1/metrics/trace.service.response_time/measurements"

payload = {}
headers = {
  'Authorization': os.getenv('SWO_API_TOKEN')
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)
prompt = response.json()
open_ai_token = os.getenv("OPEN_AI_TOKEN")
client = OpenAI(
    api_key=open_ai_token,
)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content":
                       f"In the attached file, find values (value) that deviate from the norm (one or more values). "
                       # f"In the attached file, find value (value) that deviate from the norm (one value only). "
                       f"Provide only the value if they exist. Do not provide comments or the method of reaching conclusions"
                       # f"Additionally the value must be either below 1 or above 5."
                       f"If the value does not exist, provide the value NULL '{prompt}'"
        }
    ],
    model="gpt-4o-mini",
)
print(chat_completion.choices[0].message.content)