# LaynC2 Free - Discord RAT  

LaynC2 is a **remote administration system based on Discord**, designed for management and task automation. It uses a Discord bot to send commands and receive responses from remote machines.  

⚠️ **Legal Disclaimer:** This project is for educational and cybersecurity research purposes only. Misuse of this tool may violate laws and result in legal consequences. The author is not responsible for any misuse.  

## 🔹 Free Features  
- 📸 **Screen Capture:** Take screenshots of the remote system  
- 🎥 **Screen Recording:** Record screen activity on the target system  
- 🎭 **Webcam Access:** Capture images from the webcam  
- 🎤 **Audio Recording:** Record microphone audio  
- 📋 **Clipboard Monitoring:** Track clipboard content  
- ⌨️ **Keylogger:** Log keystrokes on the target machine  

## 🚀 Installation  

### Requirements  
discord.py>=2.0.0
pyautogui>=0.9.53
opencv-python>=4.5.0
numpy>=1.19.0
pyperclip>=1.8.0
keyboard>=0.13.0
sounddevice>=0.4.0
scipy>=1.6.0
imageio>=2.9.0
imageio-ffmpeg>=0.4.0
requests>=2.25.0
pillow>=8.0.0
python-dotenv>=0.19.0

### 🔧 Configuration  
Edit the `.env` file to set up:  
- Discord bot token  
- Discord server ID  
- Discord channel ID  
- Webhook URL for keylogger (optional)  

Set up your bot on the **[Discord Developer Portal](https://discord.com/developers/applications)**.  

## 💻 Usage  

### 🎮 Discord Commands  
Use `/help` to view the complete list of available commands.  
Use `!sync` to sync bot command slash

#### 🔹 Essential Commands:  
- `/screenshot` - Captures the target system's screen  
- `/screenrec [seconds]` - Records the screen for a specific time (max. 30s)  
- `/webcam` - Captures an image from the webcam  
- `/recordmic [seconds]` - Records microphone audio (max. 30s)  
- `/keylog <start/stop> [interval]` - Starts or stops the keylogger  
- `/clip <on/off>` - Enables or disables clipboard monitoring  

## 📁 Project Structure  
- `main.py` - Core system logic  
- `config.py` - Configuration file for tokens and settings  
- `libraries/` - Additional modules and libraries  
  - `layn.py` - Functions for screen capture, webcam, and audio  
  - `k333yl000g.py` - Keylogger implementation  
  - `clippb0004rf.py` - Clipboard monitoring  
  - `getinfo.py` - System information collection  
  - `utils.py` - Various utilities  

## 🛡️ Security Notice  
This tool is provided **ONLY** for educational and legitimate system administration purposes.  

Using this software on systems **without explicit permission** may violate local, state, or federal laws. The developers **assume no responsibility** for any misuse of this software.  

## 🔒 Legal Disclaimer  
The user is solely responsible for ensuring that the use of this software complies with all applicable laws and regulations. This project should only be used on systems that you own or have **explicit permission** to access.  

---  

⚠️ **Use responsibly. Unauthorized use is illegal.**  

### 🔥 Buy Premium Version 👉 **[Contact](https://t.me/operachonal)**.  
