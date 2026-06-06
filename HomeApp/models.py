from django.db import models
from google import genai


# Create your models here.
class SecAdmin(models.Model):
    name=models.CharField(max_length=25)
    email=models.EmailField()
    section=models.CharField(max_length=40)

    def __str__(self):
        return self.name
    
class Ai:
    def __init__(self,quest,file):
        self.asked=quest
        self.path=file

    def process(self):
        client=genai.Client(api_key="your api key here")  # model access key
        #model = genai.GenerativeModel("gemini-3-flash-preview")
        model="gemini-3.5-flash"
        role=self.tune()
        uploaded_file = client.files.upload(file=self.path)

        inputformat = [
            {
                "role": "user",
                "parts": [
                    {"text": role}, 
                    {"file_data": {"file_uri": uploaded_file.uri}}, 
                    {"text": self.asked} 
                ]
            }
        ]


        
        response = client.models.generate_content(
            model=model, contents=inputformat
        )
          # storing reply or response from api
        return response.text
    def tune(self):
        mentor='''
        Read the following file and understand user's question/query/doubt properly as Teacher/mentor, your role would be as mentor and you have
        to answer the questions asked by students, use the words and sentences in the file for responses.
        Or extract the answer from file Itself only! not on othersources -- high Priority,
        Must follow => metion "<br>" html tag for next line and don't inclue "*" and "**" this symbols unless it is in file.
        if related answer not exist, then say : "Sorry, I could not found anything about that!"
        "Kindly restrict your responses to file-related queries only;
        casual messages or greetings are not required". Always recheck before providing response.
        '''
        return mentor