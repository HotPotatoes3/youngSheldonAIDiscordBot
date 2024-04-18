import os

import google.generativeai as genai

import requests
import json


TOKEN2 = os.environ['TOKEN2']
genai.configure(api_key=TOKEN2)

model = genai.GenerativeModel('gemini-pro')
model2 = genai.GenerativeModel('gemini-pro-vision')




def ai_response(type, input, image):
    if type == 'asksheldon':
        try:
            while True:
                response = model.generate_content(
                                'Answer the following question/statement as if you are the character Sheldon Cooper from the TV show "Young Sheldon" in less than 2000 characters (try to sound as pretentious and obnoxious as possible, and include a gag/reference from the show in your response): ' + input,
                                safety_settings={'HARM_CATEGORY_HARASSMENT': 'block_none', 'HARM_CATEGORY_HATE_SPEECH': 'block_none',
                                                 'HARM_CATEGORY_SEXUALLY_EXPLICIT': 'block_none',
                                                 'HARM_CATEGORY_DANGEROUS_CONTENT': 'block_none'})

                sheldonResponse = response.text
                if len(sheldonResponse) < 2000:
                    break
            return sheldonResponse
        except Exception as e:
            print(e)
            return "An error occured"
    elif type == 'asksheldon2':
        try:
            while True:
                response = model2.generate_content([
                                                       'React to the following image and question/statement as if you are the character Sheldon Cooper from the TV show "Young Sheldon in less than 2000 characters (try to sound as pretentious and obnoxious as possible, and include a gag/reference from the show in your response): ' + input,
                                                       image], safety_settings={'HARM_CATEGORY_HARASSMENT': 'block_none',
                                                                                'HARM_CATEGORY_HATE_SPEECH': 'block_none',
                                                                                'HARM_CATEGORY_SEXUALLY_EXPLICIT': 'block_none',
                                                                                'HARM_CATEGORY_DANGEROUS_CONTENT': 'block_none'})

                sheldonResponse = response.text
                if len(sheldonResponse) < 2000:
                    break
            return sheldonResponse
        except Exception as e:
            print(e)
            return "An error occured"

    elif type == 'help':
        return '**Commands:**\n\n**?asksheldon {Your question/statement}: ** Responds as Sheldon Cooper from Young Sheldon\n**?asksheldonpro {Your question/statement + an image attachment}: **Responds to an image and text as Sheldon Cooper from Young Sheldon'

