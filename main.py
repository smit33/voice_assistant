import tkinter as tk
import threading
import pyttsx3
import speech_recognition as sr
import datetime
import os
import random
import pyjokes
import webbrowser
import requests
import json


weather_api_key = "ENTER YOUR API KEY HERE"


root = tk.Tk();
root.title('Friday')
root.geometry('500x500')

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice','voices[0].id')   # 0 indicates male voice

isListening = False
th = None

# Create label
statusLabel = tk.Label(root, text = "")
statusLabel.config(font =("Courier", 14))

listeningGIF = tk.Label(root)

inputLabel = tk.Label(root, text="")
inputLabel.config(font =("Courier", 14))
inputStatementVar = tk.StringVar()
inputStatementVar.set("")
inputStatement = tk.Entry(root, textvariable = inputStatementVar, state="disabled")


def speak(text):
    engine.say(text)
    engine.runAndWait()

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening')
        statusLabel.config(text="Listening...")
        r.adjust_for_ambient_noise(source, duration = 1)
        audio = r.listen(source)
        if isListening == False:
            return ""
        try:
            print("Recognizing")
            statusLabel.config(text="Recognizing...")
            Query = r.recognize_google(audio, language='en-in')
            print("the command is printed=", Query)

        except Exception as e:
            print(e)
            speak("Say that again sir")
            return "None"

        return Query

def getTimeAndDate():  
    todays_date = datetime.date.today()
    monthName = {
            1: 'january',
            2: 'febuary',
            3: 'march',
            4: 'april',
            5: 'may',
            6: 'june',
            7: 'july',
            8: 'august',
            9: 'september', 
            10: 'october',
            11: 'november',
            12: 'december'
    }
    time = datetime.datetime.now().time()
    statement = f"{monthName[todays_date.month]} {todays_date.day} {todays_date.year} {time.hour} hour and {time.minute} minutes"
    speak(statement);

def shutdown():
    speak('Are you sure you want to shutdown your computer')
    choice = takeCommand().lower()
    if 'yes' in choice:
        speak('shutting down computer')
        os.system("shutdown /s /t 30")
    else:
        speak('ok sir')

def restart():
    speak('Are you sure you want to restart your computer')
    choice = takeCommand().lower()
    if 'yes' in choice:
        speak('restarting down computer')
        os.system("shutdown /r /t 1")
    else:
        speak('ok sir')

def greetings(*args):
    hour = datetime.datetime.now().time().hour
    if hour < 12:
        speak('Good Morning boss')
    elif hour < 17:
        speak('Good Afternoon boss')
    elif hour < 21:
        speak('Goog Evening boss')
    else:
        speak('Good Night boss')

def flipCoin():
    value = random.randint(0,1)
    speak('Flipping a coin')
    if value == 0:
        speak('Its a head')
    else:
        speak('Its a tail')

def tellJoke():
    speak(pyjokes.get_joke())

def googleSearch(statement):
    statement = statement[7:]
    try:
        webbrowser.open_new_tab('https://www.google.com/search?q=' + statement)  # Open a tab of your search
    except Exception as e:
        print(e)
        print("* Error in opening new tab *")

def openYoutube(statement):
    statement = " ".join(statement.split(' ')[1:])
    print(statement)
    try:
        webbrowser.open_new_tab('https://www.youtube.com/results?search_query=' + statement)  # Open a tab of your search
    except Exception as e:
        print(e)
        print("* Error in opening new tab *")

def getNews(statement):
    if 'news about' in statement:
        news = " ".join(statement.split(' ')[2:])
        try:
            webbrowser.open_new_tab(f'https://news.google.com/search?q={news}&hl=en-IN&gl=IN&ceid=IN%3Aen')  # Open a tab of your search
        except Exception as e:
            print(e)
            print("* Error in opening new tab *")
        return

    try:
        webbrowser.open_new_tab('https://news.google.com/foryou?hl=en-IN&gl=IN&ceid=IN%3Aen')  # Open a tab of your search
    except Exception as e:
        print(e)
        print("* Error in opening new tab *")

def getWeather(statement):
    try:
        base_url = "http://api.openweathermap.org/data/2.5/weather?"
        city_name = statement.split(' ')[-1]
        complete_url = base_url + "appid=" + weather_api_key + "&q=" + city_name
        
        response = requests.get(complete_url)
        data = response.json()
        
        if data["cod"] == "404":
            speak("There is some error")
            return

        description = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        speak(f"Temprature in {city_name} is {temp - 273.15} celcius. {description} in {city_name}")
    except:
        speak("Unexpected error. please try again")

def startListening():
    while True:
        # speak("Tell me how can I help you now?")
        if isListening == False:
            break;

        statement = takeCommand().lower()
        if isListening == False:
            break;
        inputLabel.config(text="Input: ")
        inputStatementVar.set(statement)
        if 'hello' in statement:
            speak('Hello how are you boss')
        elif 'time' in statement:
            getTimeAndDate()
        elif 'weather' in statement:
            getWeather(statement)
        elif 'shutdown computer' in statement:
            shutdown()
        elif 'restart computer' in statement:
            restart()
        elif 'flip coin' in statement or 'flip a coin' in statement:
            flipCoin()
        elif 'joke' in statement:
            tellJoke()
        elif 'google' in statement:
            googleSearch(statement)
        elif 'youtube' in statement:
            openYoutube(statement)
        elif 'news' in statement:
            getNews(statement)
        elif 'exit' in statement or 'bye' in statement:
            break


def showGif():
    frameCnt = 69
    frames = [tk.PhotoImage(file='listening.gif',format = 'gif -index %i' %(i)) for i in range(frameCnt)]

    def update(ind):
        if isListening == False:
            return
        frame = frames[ind]
        ind += 1
        if ind == frameCnt:
            ind = 0
        listeningGIF.configure(image=frame)
        root.after(30, update, ind)

    listeningGIF.grid(row=3, column=0)
    root.after(0, update, 0)

def startThread():
    global isListening, th
    isListening = True
    th = threading.Thread(target=startListening)
    th.start()
    showGif()
    statusLabel.grid(row=2, column=0)
    inputLabel.grid(row=4, column=0)
    inputStatement.grid(row=5, column=0)

def stopListen():
    global isListening, th
    if isListening == False:
        return
    isListening = False
    statusLabel.config(text="Stopping...")
    th.join()
    statusLabel.grid_forget()
    inputLabel.grid_forget()
    listeningGIF.grid_forget()
    inputStatement.grid_forget()

startButton = tk.Button(text = 'Start', width = 20, command = startThread, bg = '#5C85FB', font=("Courier", 12))
startButton.grid(row=0, column=0)

stopButton = tk.Button(text = 'Stop', width = 20, command = stopListen, bg = '#5C85FB', font=("Courier", 12))
stopButton.grid(row=1, column=0)


root.after(50, greetings, 0)

def on_closing():
    root.destroy()
    exit(0)

# root.grid(sticky="nsew")
root.grid_columnconfigure(0, weight=1)
root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()
