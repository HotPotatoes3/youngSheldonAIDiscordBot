import os

import google.generativeai as genai

TOKEN2 = os.environ['TOKEN2']
genai.configure(api_key=TOKEN2)

model = genai.GenerativeModel('gemini-pro')


def handle_response(message) -> str:
    p_message = message.lower()

    if p_message == '?help':
        return '**Commands:**\n\n**?asksheldon {Your question/statement}:** Responds as sheldon Griffin from Young Sheldon'
    if p_message[0:11] == "?asksheldon":
        try:
            response = model.generate_content(
                'Answer the following question/statement as if you are the character Sheldon Cooper from the TV show "Young Sheldon" (try to act egotistical and emotionless, and try to include a reference from the show in your response): ' + p_message[12:])
            sheldonResponse = response.text
            return sheldonResponse
        except Exception as e:
            print(e)
            return (
                "I cannot respond to that question/statement as it may contain harmful/offensive language. If you believe this is a mistake, please contact the developer")

def slash_response(type, input):
    if type == 'asksheldon':
        try:
            response = model.generate_content('Answer the following question/statement as if you are the character Sheldon Cooper from the TV show "Young Sheldon" (try to act egotistical and emotionless, and try to include a reference from the show in your response): ' + input)
            sheldonResponse = response.text
            return sheldonResponse
        except Exception as e:
            print(e)
            return("I cannot respond to that question/statement as it may contain harmful/offensive language. If you believe this is a mistake, please contact the developer")

    elif type == 'help':
        return '**Commands:**\n\n**?asksheldon {Your question/statement}:** Responds as Sheldon Cooper from Young Sheldon'

