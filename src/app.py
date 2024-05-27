import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.ttk import Progressbar
from pytube import YouTube
import threading
import pickle

# Função para salvar as preferências do usuário
def save_preferences(destination_folder):
    with open("preferences.pkl", "wb") as f:
        pickle.dump(destination_folder, f)

# Função para carregar as preferências do usuário
def load_preferences():
    try:
        with open("preferences.pkl", "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return ""

# Função para escolher a pasta destino
def choose_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        destination_folder.set(folder_selected)
        save_preferences(folder_selected)

# Função para atualizar a barra de progresso
def update_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    progress = int((bytes_downloaded / total_size) * 100)
    progress_var.set(progress)
    progress_bar.update()

# Função para baixar o vídeo
def download_video():
    url = url_entry.get()
    folder = destination_folder.get()

    if not url:
        messagebox.showwarning("Erro", "Por favor, insira um link do YouTube.")
        return

    if not folder:
        messagebox.showwarning("Erro", "Por favor, selecione uma pasta de destino.")
        return

    try:
        yt = YouTube(url, on_progress_callback=update_progress)
        stream = yt.streams.get_highest_resolution()
        video_title.set(f"Baixando: {yt.title}")
        stream.download(output_path=folder)
        messagebox.showinfo("Sucesso", "Download concluído!")
        video_title.set("")
        progress_var.set(0)
        progress_bar.update()
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}")
        video_title.set("")
        progress_var.set(0)
        progress_bar.update()

# Função para iniciar o download em uma thread separada
def start_download():
    download_thread = threading.Thread(target=download_video)
    download_thread.start()

# Criação da janela principal
root = tk.Tk()
root.title("YouTube Video Downloader")

# Variáveis de controle
url_entry = tk.StringVar()
destination_folder = tk.StringVar(value=load_preferences())
progress_var = tk.IntVar()
video_title = tk.StringVar()

# Layout da GUI
tk.Label(root, text="Link do YouTube:").grid(row=0, column=0, padx=10, pady=10)
tk.Entry(root, textvariable=url_entry, width=50).grid(row=0, column=1, padx=10, pady=10)
tk.Button(root, text="Escolher Pasta", command=choose_folder).grid(row=1, column=0, padx=10, pady=10)
tk.Label(root, textvariable=destination_folder).grid(row=1, column=1, padx=10, pady=10)
tk.Button(root, text="Baixar", command=start_download).grid(row=2, column=0, columnspan=2, pady=10)

tk.Label(root, textvariable=video_title).grid(row=3, column=0, columnspan=2)
progress_bar = Progressbar(root, variable=progress_var, maximum=100, length=400)
progress_bar.grid(row=4, column=0, columnspan=2, pady=10)

# Iniciar a GUI
root.mainloop()
