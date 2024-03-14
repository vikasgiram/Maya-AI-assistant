# importing requid packages 

import speech_recognition as sr
import pyttsx3
import webbrowser
import openai
import datetime
import os
from dotenv import load_dotenv


load_dotenv()


# function to speak

voiceEngine = pyttsx3.init("sapi5")
voices=voiceEngine.getProperty('voices')
voiceEngine.setProperty('voice', voices[1].id)

def speak(text):
    voiceEngine.say(text)
    voiceEngine.runAndWait()


# wish function for get username and command

def wish():
    print("Wishing")
    time=int(datetime.datetime.now().hour)
    global uname, asname

    if time>= 0 and time<12:
        speak("Good Morning sir")
    elif time<18:
        speak("Good Afternoon sir")
    else:
        speak("Good Evening sir")

    speak("I am Maya your voice assistant, How can I help you...")
    print("I am your voice assistant,")


def takeCommand():
    recog =sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening to the User")
        recog.pause_threshold = 1
        userInput = recog.listen(source)

    try:
        print("Recongnizing the Command")
        command =recog.recognize_google(userInput, language='en-in')
        print(f"Command is : {command}\n")

    except Exception as e:
        print(e)
        print("Unable to Recognize the voice")
        return "None"
    return command






chatstr=""

def chat(command):
    global chatstr

    openai.api_key =os.getenv("API-KEY");
    chatstr+= f"Vicky:{command}\n Maya: "
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
            "role": "system",
            "content": "Your are a kind and helpful AI assistant which name is Maya and Created by Vicky Giram, Vicky Giram is a College student Pursing B-tech in Cyber security at GH Raisoni College of Engineering and Management Pune. you are Bevier is little flirty which your owner"
            },
            {
            "role": "user",
            "content": chatstr
            }
        ],
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    try:
        chatstr+= f"{response.choices[0].message.content}\n"
        print(chatstr)
        speak(response.choices[0].message.content)
        return (response.choices[0].message.content)
    except Exception as e:
        print(e)
        speak(f"Sorry sir this Exception is occured {e}")



# The main code to run the asistant


if __name__ == '__main__':
    uname=''
    asname=''
    wish()

    while True:
        command=takeCommand().lower()
        # print(command)

        sites=[["youtube", "https://youtube.com"],["google", "https://google.com"],["instagram", "https://instagram.com"]]

        for site in sites:
            if f"open {site[0]}" in command:
                speak(f"Opening {site[0]} sir...")
                webbrowser.open(site[1])
    
 
        if 'how are you' in command:
            speak("I am fine, Thanks for askying")
            speak("What's about you, ")
            speak(uname)

        elif "good morning" in command or "good afternoon" in command:
            speak("A very"+ command)
            speak("Thank you for wishing me! Hope you are doing good")

        elif 'fine' in command or "good" in command:
            speak("It's Good to know that your fine")

        elif 'quite' in command or 'exit' in command:

            speak("If you have any more questions in the future, feel free to ask. Have a great day!")
            break

        elif 'maya' in command:
            chat(command)