import os
import tempfile
import time
import cv2
import pyautogui
import numpy as np
import sounddevice as sd
import scipy.io.wavfile as wav
import imageio

def take_screenshot(output_path=None):
    """Captura uma screenshot da tela atual"""
    try:
        
        screenshot = pyautogui.screenshot()
        
       
        if not output_path:
            output_path = os.path.join(tempfile.gettempdir(), f"screenshot_{int(time.time())}.png")
            
        
        screenshot.save(output_path)
        return output_path
    except Exception as e:
        return {'error': str(e)}

def capture_webcam(output_path=None):
    """Captura uma imagem da webcam"""
    try:
      
        cam = cv2.VideoCapture(0)
        
       
        ret, frame = cam.read()
        
       
        cam.release()
        
        if not ret:
            return {'error': 'Falha ao capturar imagem da webcam'}
            
        
        if not output_path:
            output_path = os.path.join(tempfile.gettempdir(), f"webcam_{int(time.time())}.png")
            
        
        cv2.imwrite(output_path, frame)
        return output_path
    except Exception as e:
        return {'error': str(e)}

def record_audio(seconds=10, output_path=None):
    """Grava áudio do microfone"""
    try:
        
        fs = 44100 
        
        
        recording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
        sd.wait()  
        
        
        if not output_path:
            output_path = os.path.join(tempfile.gettempdir(), f"audio_{int(time.time())}.wav")
            
        
        wav.write(output_path, fs, recording)
        return output_path
    except Exception as e:
        return {'error': str(e)}

def record_screen(duration=10, fps=30, output_path=None):
    """Grava tela em um vídeo"""
    try:
       
        if not output_path:
            output_path = os.path.join(tempfile.gettempdir(), f"screen_recording_{int(time.time())}.mp4")
            
       
        screen_width, screen_height = pyautogui.size()
        
        
        frames = []
        
        
        start_time = time.time()
        end_time = start_time + duration
        
        while time.time() < end_time:
            
            img = pyautogui.screenshot()
            
            
            frames.append(np.array(img))
            
           
            time.sleep(1/fps)
        
       
        writer = imageio.get_writer(output_path, fps=fps, codec='libx264', quality=7)
        for frame in frames:
            writer.append_data(frame[:, :, ::-1])  
        writer.close()
        
        return output_path
    except Exception as e:
        return {'error': str(e)}