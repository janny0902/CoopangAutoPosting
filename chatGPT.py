import os
import openai

class chatGPTMethod:
    def questionFunction(questionString):
        openai.api_key = os.getenv("OPENAI_API_KEY")
        print(questionString)
        response = openai.Completion.create(
        model="text-davinci-003",
        prompt=questionString,
        temperature=0.7,
        max_tokens=3500,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
        )


        return response.choices[0].text.strip()
