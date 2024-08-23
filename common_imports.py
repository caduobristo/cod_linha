import socket
import string
import random
import threading
import numpy as np
import tkinter as tk
from tkinter import scrolledtext
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def encrypt_decrypt(string, key):
    return ''.join(chr(ord(c) ^ ord(key[i % len(key)])) for i, c in enumerate(string))
    
def update_text_area(decoded_message, text_area):
    text_area.delete('1.0', tk.END)
    text_area.insert(tk.END, decoded_message + '\n')

def plot_waveform(message, frame, titulo, root):
    wave = []

    for i in range(len(message)):
        if message[i] == '1' and message[i-1] != '-':
            wave.append(1)
        elif message[i] == '0':
            wave.append(0)
        elif message[i] == '-':
            i += 1
            wave.append(-1)
        
    def update_plot():
        if hasattr(plot_waveform, 'fig'):
            ax = plot_waveform.ax
            ax.clear()
        else:
            plot_waveform.fig, ax = plt.subplots()
            plot_waveform.ax = ax

        x = np.linspace(0, len(wave)-1, 10*len(wave))
        ax.step(x, np.repeat(wave, 10), where='mid')

        ax.set_ylim([-1.5, 1.5])
        ax.set_title(titulo)
            
        if hasattr(plot_waveform, 'canvas'):
            plot_waveform.canvas.draw()
        else:
            plot_waveform.canvas = FigureCanvasTkAgg(plot_waveform.fig, master=frame)
            plot_waveform.canvas.draw()
            plot_waveform.canvas.get_tk_widget().pack(pady=5)

    root.after(0, update_plot)
