import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import os
import wikipedia
import pyautogui
import schedule
import time
import pywhatkit as kit
import requests
import subprocess
import psutil  # For battery and system info
import shutil  # For file/folder operations

# Initialize Text-to-Speech Engine
engine = pyttsx3.init()

# Special directories for files and folders
FILE_DIRECTORY = "C:\\Users\\utkar\\Documents\\bb\\Files"
FOLDER_DIRECTORY = "C:\\Users\\utkar\\Documents\\bb\\Folders"

# Create special directories if they don't exist
if not os.path.exists(FILE_DIRECTORY):
    os.makedirs(FILE_DIRECTORY)
if not os.path.exists(FOLDER_DIRECTORY):
    os.makedirs(FOLDER_DIRECTORY)

# Function to speak text
def speak(text):
    print(text)
    engine.say(text)
    engine.runAndWait()

# Function to take voice commands
def take_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        try:
            print("Recognizing...")
            query = recognizer.recognize_google(audio, language="en-US")
            print(f"User said: {query}")
            return query.lower()
        except sr.UnknownValueError:
            speak("Sorry, I didn't understand that.")
            return None
        except sr.RequestError:
            speak("Sorry, my speech service is down.")
            return None

# Function to open important applications
def open_application(app_name):
    app_paths = {
        "notepad": "notepad.exe",
        "wordpad": "write.exe",
        "word": "winword.exe",
        "powerpoint": "powerpnt.exe",
        "excel": "excel.exe",
        "task manager": "taskmgr.exe",
        "settings": "ms-settings:",
        "whatsapp": "https://web.whatsapp.com",
        "spotify": "spotify.exe",
        "chrome": "chrome.exe",
        "edge": "msedge.exe",
    }

    if app_name in app_paths:
        if app_name in ["whatsapp"]:
            webbrowser.open(app_paths[app_name])
        else:
            os.startfile(app_paths[app_name])
        speak(f"Opening {app_name}")
    else:
        speak(f"Application {app_name} not found.")

# Function to print the current page (simulates Ctrl+P)
def print_page():
    pyautogui.hotkey('ctrl', 'p')
    speak("Print command sent.")

def snipping_tool():
    pyautogui.hotkey('win', 'shift', 's')
    speak("Snipping tool opened.")


# Function to create a file
def create_file():
    speak("What should be the file name?")
    file_name = take_command()
    speak("What should be the file extension?")
    extension = take_command()

    # Ask the user if they want to save the file in a specific folder
    speak("Do you want to save the file in a specific folder? Please say yes or no.")
    folder_choice = take_command()

    if folder_choice == "yes":
        speak("Please specify the folder name.")
        folder_name = take_command()
        folder_path = os.path.join(FOLDER_DIRECTORY, folder_name)

        # Check if the folder exists, if not, create it
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            speak(f"Folder {folder_name} created in {FOLDER_DIRECTORY}.")

        file_path = os.path.join(folder_path, f"{file_name}.{extension}")
    else:
        file_path = os.path.join(FILE_DIRECTORY, f"{file_name}.{extension}")

    try:
        with open(file_path, "w") as f:
            f.write("")  # Create an empty file
        speak(f"File {file_name}.{extension} created successfully in {os.path.dirname(file_path)}.")
    except Exception as e:
        speak(f"Failed to create file: {e}")

# Function to delete a file
def delete_file():
    speak("Which file should I delete? Please specify the file name.")
    file_name = take_command()
    file_path = os.path.join(FILE_DIRECTORY, file_name)

    if os.path.isfile(file_path):
        speak(f"Are you sure you want to delete {file_name}? Please say yes or no.")
        confirmation = take_command()
        if confirmation == "yes":
            try:
                os.remove(file_path)
                speak(f"File {file_name} deleted successfully.")
            except Exception as e:
                speak(f"Failed to delete file: {e}")
        else:
            speak("Deletion canceled.")
    else:
        speak(f"File {file_name} does not exist.")

# Function to create a folder
def create_folder():
    speak("What should be the folder name?")
    folder_name = take_command()
    folder_path = os.path.join(FOLDER_DIRECTORY, folder_name)

    try:
        os.mkdir(folder_path)
        speak(f"Folder {folder_name} created successfully in {FOLDER_DIRECTORY}.")
    except FileExistsError:
        speak(f"Folder {folder_name} already exists.")
    except Exception as e:
        speak(f"Failed to create folder: {e}")

# Function to delete a folder
def delete_folder():
    speak("Which folder should I delete? Please specify the folder name.")
    folder_name = take_command()
    folder_path = os.path.join(FOLDER_DIRECTORY, folder_name)

    if os.path.isdir(folder_path):
        speak(f"Are you sure you want to delete {folder_name}? Please say yes or no.")
        confirmation = take_command()
        if confirmation == "yes":
            try:
                shutil.rmtree(folder_path)
                speak(f"Folder {folder_name} deleted successfully.")
            except Exception as e:
                speak(f"Failed to delete folder: {e}")
        else:
            speak("Deletion canceled.")
    else:
        speak(f"Folder {folder_name} does not exist.")

# Function to check CPU, RAM, and disk usage
def system_info():
    cpu_usage = psutil.cpu_percent()
    ram_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent
    speak(f"CPU usage is at {cpu_usage} percent.")
    speak(f"RAM usage is at {ram_usage} percent.")
    speak(f"Disk usage is at {disk_usage} percent.")

# Function to list running processes
def list_processes():
    speak("Listing running processes.")
    for proc in psutil.process_iter(['pid', 'name']):
        print(f"PID: {proc.info['pid']} - Name: {proc.info['name']}")

# Function to terminate a process
def terminate_process():
    speak("Please say the process name to terminate.")
    process_name = take_command()
    for proc in psutil.process_iter(['pid', 'name']):
        if process_name.lower() in proc.info['name'].lower():
            psutil.Process(proc.info['pid']).terminate()
            speak(f"Process {proc.info['name']} terminated.")
            return
    speak(f"Process {process_name} not found.")

# Function to check internet speed
def check_internet_speed():
    speak("Checking internet speed...")
    response = requests.get("https://www.speedtest.net/api/js/servers?https_functional=true")
    if response.status_code == 200:
        speak("Internet connection is active.")
    else:
        speak("No internet connection detected.")

# Function to get IP address
def get_ip_address():
    ip_address = requests.get("https://api64.ipify.org?format=json").json()["ip"]
    speak(f"Your IP address is {ip_address}")

# Function to take a screenshot
def take_screenshot():
    screenshot = pyautogui.screenshot()
    screenshot.save("screenshot.png")
    speak("Screenshot taken and saved as screenshot.png.")

# Function to copy files
def copy_file():
    speak("Please provide the source file path.")
    src = take_command()
    speak("Please provide the destination directory path.")
    dest = take_command()
    try:
        shutil.copy(src, dest)
        speak("File copied successfully.")
    except Exception as e:
        speak(f"Failed to copy file: {e}")

# Function to move files
def move_file():
    speak("Please provide the source file path.")
    src = take_command()
    speak("Please provide the destination directory path.")
    dest = take_command()
    try:
        shutil.move(src, dest)
        speak("File moved successfully.")
    except Exception as e:
        speak(f"Failed to move file: {e}")

# Function to get disk usage
def disk_usage():
    usage = shutil.disk_usage("/")
    speak(f"Total disk space: {usage.total // (1024 ** 3)} GB")
    speak(f"Used disk space: {usage.used // (1024 ** 3)} GB")
    speak(f"Free disk space: {usage.free // (1024 ** 3)} GB")

# Function to tell the time
def tell_time():
    current_time = datetime.datetime.now().strftime("%I:%M %p")
    speak(f"The time is {current_time}")

# Function to tell the date
def tell_date():
    current_date = datetime.datetime.now().strftime("%B %d, %Y")
    speak(f"Today's date is {current_date}")

# Function to search the web
def search_web(query):
    speak("Searching the web...")
    query = query.replace("search", "")
    webbrowser.open(f"https://www.google.com/search?q={query}")

# Function to search Wikipedia
def search_wikipedia(query):
    speak("Searching Wikipedia...")
    query = query.replace("wikipedia", "")
    results = wikipedia.summary(query, sentences=2)
    webbrowser.open(f"https://en.wikipedia.org/wiki/{query}")
    speak("According to Wikipedia...")
    print(results)
    speak(results)

# Function to perform mathematical calculations
def calculate(expression):
    try:
        result = eval(expression)
        speak(f"The result is {result}")
        print(f"Result: {result}")
    except Exception as e:
        speak("Sorry, I couldn't calculate that.")
        print(e)

# Function to set reminders
def set_reminder(reminder_text, reminder_time):
    speak(f"Reminder set for {reminder_time}: {reminder_text}")
    schedule.every().day.at(reminder_time).do(lambda: speak(f"Reminder: {reminder_text}"))

# Function to play music on YouTube
def play_music(song_name):
    speak(f"Playing {song_name} on YouTube")
    kit.playonyt(song_name)

# Function to control media playback
def control_media(action):
    if "play" in action:
        pyautogui.press("playpause")
        speak("Media played")
    elif "pause" in action:
        pyautogui.press("playpause")
        speak("Media paused")
    elif "next" in action:
        pyautogui.press("nexttrack")
        speak("Next track")
    elif "previous" in action:
        pyautogui.press("prevtrack")
        speak("Previous track")

# Function to fetch weather information using FreeWeather API
def get_weather(city):
    api_key = "bce39296fc274c5d94c65901250903"  # Replace with your FreeWeather API key
    base_url = f"https://api.weatherapi.com/v1/current.json?key={api_key}&q={city}"
    response = requests.get(base_url).json()
    if "error" not in response:
        temperature = response["current"]["temp_c"]
        condition = response["current"]["condition"]["text"]
        speak(f"The temperature in {city} is {temperature}°C, and the condition is {condition}.")
    else:
        speak("City not found.")

# Function to process commands
def process_command(query):
    if "wikipedia" in query:
        search_wikipedia(query)
    elif "open" in query:
        app_name = query.replace("open", "").strip()
        open_application(app_name)
    elif "time" in query:
        tell_time()
    elif "date" in query:
        tell_date()
    elif "search" in query:
        search_web(query)
    elif "calculate" in query:
        expression = query.replace("calculate", "")
        calculate(expression)
    elif "set a reminder" in query:
        speak("What should I remind you?")
        reminder_text = take_command()
        speak("At what time? (HH:MM)")
        reminder_time = take_command()
        set_reminder(reminder_text, reminder_time)
    elif "play music" in query:
        play_music(query.replace("play music", "").strip())
    elif "media" in query:
        control_media(query)
    elif "weather" in query:
        get_weather(query.replace("weather", "").strip())
    elif "cpu usage" in query or "system info" in query:
        system_info()
    elif "process list" in query:
        list_processes()
    elif "terminate process" in query:
        terminate_process()
    elif "internet speed" in query:
        check_internet_speed()
    elif "ip address" in query:
        get_ip_address()
    elif "snipping tool" in query:
        snipping_tool()
    elif "screenshot" in query:
        take_screenshot()
    elif "copy file" in query:
        copy_file()
    elif "move file" in query:
        move_file()
    elif "disk usage" in query:
        disk_usage()
    elif "print page" in query:
        print_page()
    elif "create file" in query:
        create_file()
    elif "delete file" in query:
        delete_file()
    elif "create folder" in query:
        create_folder()
    elif "delete folder" in query:
        delete_folder()
    elif "exit" in query or "stop" in query:
        speak("Goodbye!")
        return False
    else:
        speak("Sorry, I don't know how to do that yet.")
    return True

# Main function
def main():
    speak("Hello, I am your AI assistant. How can I help you today?")
    while True:
        query = take_command()
        if query:
            if not process_command(query):
                break

if __name__ == "__main__":
    main()