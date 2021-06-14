from tkinter import *
import tkinter.messagebox
from tkinter import filedialog
from pygame import mixer
from mutagen.mp3 import MP3
from tkinter import ttk
from ttkthemes import themed_tk as tk
import time
import threading
import os

#creating the window
root = tk.ThemedTk()
root.get_themes()
root.set_theme("elegance")
root.title("RHYTHM")
root.iconbitmap(r'RHYTHM.ico')

#creating the statusbar
statusbar=ttk.Label(root, text="Welcome to RHYTHM music player", relief=SUNKEN, anchor=W, font="Arial 10 bold")
statusbar.pack(side=BOTTOM, fill=X)

#creating the menubar
menubar=Menu(root)
root.config(menu=menubar)

#creating submenu-1
playlist= []
def search_file():
    global filepath
    filepath=filedialog.askopenfilename()
    playlist_addition(filepath)
def playlist_addition(filename):
    filename=os.path.basename(filename)
    index=0
    List.insert(index, filename)
    playlist.insert(index, filepath)
    index+=1
submenu=Menu(menubar,tearoff=0)
menubar.add_cascade(label="File", menu=submenu)
submenu.add_command(label="open", command=search_file)
submenu.add_command(label="exit", command=root.destroy)

#creating submenu-2
def about_us():
    tkinter.messagebox.showinfo('About RHYTHM','This is a music player build using python by PPM')
def use():
    tkinter.messagebox.showinfo('How to use','Click on the add button or go to the open option  from File submenu to add song from your device to the listbox , Select the song you want to listen to, then click on the play button to enjoy the music')
submenu=Menu(menubar,tearoff=0)
menubar.add_cascade(label="Help", menu=submenu)
submenu.add_command(label="About us", command=about_us)
submenu.add_command(label="How to use", command=use)

mixer.init()

#setting the left frame
leftframe = Frame(root)
leftframe.pack(side=LEFT, padx=30)
List=Listbox(leftframe)
List.pack()
btn1 =ttk.Button(leftframe, text=" Add", command=search_file)
btn1.pack(side=LEFT)
def delete():
    song = List.curselection()
    song = int(song[0])
    List.delete(song)
    playlist.pop(song)
btn2 =ttk.Button(leftframe, text="Del", command=delete)
btn2.pack(side=LEFT)

#setting the right frame
rightframe=Frame(root)
rightframe.pack()
topframe = Frame(rightframe)
topframe.pack()
total_time=ttk.Label(topframe, text="Total time-00:00", )
total_time.pack(pady=5)

def details(play):
    file_details = os.path.splitext(play)
    if file_details[1] == '.mp3':
        audio = MP3(play)
        total_length=audio.info.length
    else:
        a = mixer.Sound(play)
        total_length=a.get_length()
    mins, secs = divmod(total_length, 60)
    mins = round(mins)
    secs = round(secs)
    timeformat = '{:02d}:{:02d}'.format(mins, secs)
    total_time['text'] = "Total time" + ' - ' + timeformat

def play_music():
    global paused
    if paused:
        mixer.music.unpause()
        statusbar['text'] = "Music Resumed"
        paused = FALSE
    else:
        stop_music()
        time.sleep(1)
        song =List.curselection()
        song = int(song[0])
        play = playlist[song]
        mixer.music.load(play)
        mixer.music.play()
        statusbar['text'] = "Playing music" + ' - ' + os.path.basename(play)
        details(play)

def stop_music():
    mixer.music.stop()
    statusbar['text'] = "Music Stopped"

paused = FALSE
def pause_music():
    global paused
    paused = TRUE
    mixer.music.pause()
    statusbar['text'] = "Music Paused"

def rewind_music():
    play_music()
    statusbar['text']='Music rewinded'

def set_volume(value):
    volume=float(value)/100
    mixer.music.set_volume(volume)

muted=FALSE
def mute_music():
    global muted
    if muted:
        mixer.music.set_volume(0.7)
        VolumeButton.configure(image=VolumePhoto)
        scale.set(70)
        muted=FALSE
    else:
        mixer.music.set_volume(0)
        VolumeButton.configure(image=MutePhoto)
        muted=TRUE

midframe=Frame(topframe)
midframe.pack(pady=10)

PlayPhoto=PhotoImage(file='PLAY.png')
PlayButton=ttk.Button(midframe, image=PlayPhoto, command=play_music)
PlayButton.grid(row=0, column=0, padx=10)

StopPhoto=PhotoImage(file='stop.png')
StopButton=ttk.Button(midframe, image=StopPhoto, command=stop_music)
StopButton.grid(row=0, column=1, padx=10)

PausePhoto=PhotoImage(file='PAUSE.png')
PauseButton=ttk.Button(midframe, image=PausePhoto, command=pause_music)
PauseButton.grid(row=0, column=2, padx=10)

bottomframe=Frame(topframe)
bottomframe.pack(pady=10)

RewindPhoto=PhotoImage(file='rewind.png')
RewindButton=ttk.Button(bottomframe , image=RewindPhoto ,command=rewind_music)
RewindButton.grid(row=0 , column=0)

MutePhoto=PhotoImage(file='MUTE.png')
VolumePhoto=PhotoImage(file='VOL.png')
VolumeButton=ttk.Button(bottomframe , image=VolumePhoto , command=mute_music)
VolumeButton.grid(row=0, column=1)

scale=Scale(bottomframe, from_=0, to=100, orient=HORIZONTAL, command=set_volume)
scale.set(70)
mixer.music.set_volume(0.7)
scale.grid(row=0, column=2, pady=15, padx=30)


def on_closing():
    stop_music()
    root.destroy()

root.protocol("WM_DELETE_WINDOW",on_closing)
root.mainloop()