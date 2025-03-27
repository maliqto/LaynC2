import platform
import os
import socket
import requests
import ctypes
from datetime import datetime

def get_system_info():
    """Obtém informações básicas do sistema"""
    try:
        
        try:
            ip = requests.get('https://api.ipify.org').text
        except:
            ip = "Desconhecido"
        
      
        info = {
            "hostname": platform.node(),
            "os": f"{platform.system()} {platform.release()}",
            "username": os.environ.get("USERNAME", "unknown"),
            "ip": ip,
            "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        return info
    except Exception as e:
        return {"error": str(e)}

def is_admin():
    """Verifica se tem privilégios de administrador"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except:
        return False