import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import os
import time
import subprocess
import wolframalpha
import requests
import cv2
import pyautogui
from pprint import pprint
# ------------------------------
engine = pyttsx3.init()
engine.setProperty('rate',150)
voices = engine.getProperty('voices')
engine.setProperty('voices',voices[0].id)

def speak(text):
    engine.say(text)
    engine.runAndWait()
    engine.stop()

text = "Hi, how are you"
# speak(text)

# def take_command():
#     r = sr.Recognizer()
    
#     with sr.Microphone() as source:
#         print("listenning...")
#         audio = r.listen(source)
#     try:
#         cm = r.recognize_amazon(audio,language="en-US")
#         print(f"you said:{cm}\n")

#     except:
#         print("i didnt understand what you said.")
#         speak("i didnt understand what you said.")
#         return "None"

#     return cm
# for index,name in enumerate(sr.Microphone.list_microphone_names()):
#     print("Micro with name \"{1}\" found for `Microphone(device_index={0})`".format(index,name))

def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("listenning...")
        audio = r.listen(source)
    try:
        cm = r.recognize_google(audio, language="en-US")
        print(f"you said: {cm}\n")
    except sr.UnknownValueError:
        print("Speech recognition could not understand your audio")
    except sr.RequestError as e:
        print(f"Error sending request to Amazon Transcribe: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
        return "None"
    return cm    

        
  
NAME = "none"

def welcome():
    hour = datetime.datetime.now().hour
    if 0<= hour < 12:
        print("Hello good morning")
        speak("Hello good morning")
    elif 12<= hour < 16 :
        print("Hello good afternoon")
        speak("Hello good afternoon")

    else:
        print("Hello good evening")
        speak("Hello good evening")

    global NAME
    while True:
        # NAME = take_command().lower()
        NAME = "mohammad"
        if NAME != "none":
            break

    print(f"Welcome {NAME}, lets start!\n")
    speak(f"Welcome {NAME}, lets start!")

welcome()

while True:
    print("how can i help you")
    speak("how can i help you")

    command = take_command().lower()
    
    if "bye" in command or "stop" in command:
        print(f"Good Bye{NAME}")
        speak(f"Good Bye{NAME}")
        break
    
    if "wikipedia" in command :
        print("Searching in wikipedia") 
        speak("Searching in wikipedia") 

        command = command.replace("wikipedia","")
        print("How many results? ")
        speak("How many results? ")

        try:
            sentence = take_command()
        except:
            sentence = 3
        
        result = wikipedia.summary(command,sentences=sentence)
        print(f"{sentence} sentences of your search results in wikipedia:\n")
        speak(f"{sentence} sentences of your search results in wikipedia")
        pprint(result + "\n")
        speak(result)
            
    elif "youtube" in command:
        webbrowser.open_new_tab("http://www.youtube.com")
        print("oppening youtube...")
        speak("oppening youtube...")
        time.sleep(5)
        

    elif "market" in command:
        webbrowser.open_new_tab("https://www.toinfshop.com")
        print("Opening toinfshop.\n")
        speak("Opening toinfshop.")
        time.sleep(5)

    elif "news" in command:
        webbrowser.open_new_tab("https://news.google.com")
        print("Opening news.\n")
        speak("Opening news.")
        time.sleep(5)
    elif "time" in command:
        str_time = datetime.datetime.now().strftime("%H:%M:%S")
        print(str_time+"\n")
        speak(f"the time is {str_time}")
    elif "camera" in command or "photo" in command:
        camera = cv2.VideoCapture(0)
        ret, frame = camera.read()
        if ret:
            cv2.imwrite("your_photo.png", frame)
        camera.release()
        cv2.destroyAllWindows()
        print("Your photo was taken.\n")
        speak("Your photo was taken.")
    elif "screenshot" in command:
        my_screenshot = pyautogui.screenshot()
        my_screenshot.save("screenshot.png")
        print("Your Screenshot was taken.\n")
        speak("Your Screenshot was taken.")
    elif "search" in command:
        command = command.replace("search", "")
        print(f"Searching {command}\n")
        speak(f"Searching {command}")
        webbrowser.open_new_tab(command)
        time.sleep(5)
    elif "question" in command:
        print("Now I can answer your calculation and geography questions.\n")
        speak("Now I can answer your calculation and geography questions.")
        question = take_command()
        app_id = "GLJER7-G45W94GJ8X"
        client = wolframalpha.Client(app_id)
        res = client.query(question)
        answer = next(res.results).text
        print(answer+"\n")
        speak(answer)

    elif "who" in command:
        print("Hello. I am version 1 of the voice assistant and was programmed by Reza.\n")
        speak("Hello. I am version 1 of the voice assistant and was programmed by Reza.")

    elif "write note" in command:
        print(f"What should i write {NAME}?\n")
        speak(f"What should i write {NAME}?")
        note = take_command()
        print(f"{NAME}, should I include time?\n")
        speak(f"{NAME}, should I include time?")
        ans = take_command()
        if "y" in ans:
            str_time = datetime.datetime.now().strftime("%H:%M:%S")
            with open("note.txt", "w",mode="utf-8") as file:
                file.write(str_time + "\n")
                file.write("-" * 40 + "\n")
                file.write(note)
        else:
            with open("note.txt", "w") as file:
                file.write(note)
    elif "show note" in command:
        print("Showing Notes:\n")
        speak("Showing Notes:")
        with open("note.txt", "r",mode="utf-8") as file:
            s = file.read()
            print(s + "\n")
            speak(s)
            
    elif "telegram" in command:
        print("Opening Telegram!\n")
        speak("Opening Telegram!")
        subprocess.call(["open", "-n", "/Applications/Telegram.app"])
        time.sleep(5)

    elif "shutdown" in command:
        print("Your system shutdown after 30 seconds!\n")
        speak("Your system shutdown after 30 seconds!")
        time.sleep(5)
        shut_down = ["shutdown", "-f", "-s", "-t", "30"]
        subprocess.call(shut_down)

    elif "restart" in command:
        print("Your system restart after 30 seconds!\n")
        speak("Your system restart after 30 seconds!")
        time.sleep(5)
        re_start = ["shutdown", "-f", "-r", "-t", "30"]
        subprocess.call(re_start)
        
        
    elif "weather" in command:
        api_key = "0b04c27a1c6002bbb77c6570dbe1d85c"
        base_url = "https://api.openweathermap.org/data/2.5/weather?"
        print("What is the city name?\n")
        speak("What is the city name?")
        city_name = take_command()
        complete_url = base_url + "appid=" + api_key + "&q=" + city_name
        response = requests.get(complete_url)
        res = response.json()
        if res["cod"] != "404":
            main = res["main"]
            temperature = main["temp"]
            humidity = main["humidity"]
            weather = res["weather"]
            weather_description = weather[0]["description"]
            print(f"temperature in kelvin unit = {temperature}\n")
            speak(f"temperature in kelvin unit = {temperature}")
            print(f"humidity = {humidity}\n")
            speak(f"humidity = {humidity}")
            print(f"weather description = {weather_description}\n")
            speak(f"weather description = {weather_description}")
