import os
from google import genai #Imports the SDK
import json
from google.genai import errors

api_key = os.environ["GEMINI_API_KEY"]
#Set the GEMINI_API_KEY environment variable before running the script.
#simply type: $env:GEMINI_API_KEY = "YOUR_KEY_HERE" in your TERMINAL
client = genai.Client(api_key=api_key)
#the above creates the object that will be used to make requests
#A SDK is used to automatically make HTTP, JSON body, and headers. using this avoids extra headache


with open("questions.txt","r") as question_files:
    text = question_files.read()


questions = text.splitlines()

results = []
for question in questions:
    stripped_question = question.strip()

    if stripped_question != "":
        try:
            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=stripped_question
            )

            print(response.text)

            results.append({
                "question": stripped_question,
                "answer": response.text
            })

        except errors.APIError as error:
            print("Request failed:", error)

            results.append({
                "question": stripped_question,
                "answer": None,
                "error": str(error)
            })
#adding our results to a json file (named "answers.json")
with open("answers.json", "w", encoding="utf-8") as output_file:
    json.dump(results, output_file, indent=4)

print("Results saved to answers.json")


    