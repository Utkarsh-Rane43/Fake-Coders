# Voice Assistant README

## Project Overview
This is a Python-based voice assistant that can perform various tasks such as opening applications, creating and managing files/folders, retrieving system information, performing web searches, and interacting with users using voice commands.

## Features
- **Voice Recognition:** Uses `speech_recognition` to take user commands.
- **Text-to-Speech:** Uses `pyttsx3` to respond via voice.
- **Application Launcher:** Opens common applications such as Notepad, Chrome, Spotify, etc.
- **File & Folder Management:** Create, delete, move, and copy files and folders.
- **System Monitoring:** Checks CPU, RAM, and disk usage.
- **Web & Wikipedia Search:** Searches queries on Google and Wikipedia.
- **Screenshot & Snipping Tool:** Takes screenshots and opens Snipping Tool.
- **Task Management:** Lists and terminates running processes.
- **Internet & IP Address Check:** Checks internet speed and retrieves the system's IP address.
- **Mathematical Calculations:** Performs basic mathematical evaluations.

## Installation
### Prerequisites
Ensure you have Python installed (preferably Python 3.7 or higher). You also need the following Python packages:

```sh
pip install speechrecognition pyttsx3 wikipedia pyautogui schedule pywhatkit requests psutil shutil
```

## Usage
Run the script to start the voice assistant:
```sh
python voice_assistant.py
```
### Example Commands:
- "Open Notepad"
- "Create a file"
- "Delete a folder"
- "Search Wikipedia for Python programming"
- "Check my internet speed"
- "What is the current time?"

## Special Directories
- Files are saved in `C:\Users\utkar\Documents\bb\Files`
- Folders are managed in `C:\Users\utkar\Documents\bb\Folders`

## Future Improvements
- Implement NLP for better voice recognition.
- Add more integrations like weather updates and calendar scheduling.
- Support for multiple languages.

## Author
Utkarsh, Hanuman, Rohan, Prajwal

