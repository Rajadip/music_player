import tkinter as tk
from tkinter import filedialog as fd , messagebox
import subprocess as sb
import ConnectDatabase as db
import os

root = None

def browseSongs(window=None,pl_number=0):
    files = fd.askopenfiles(parent=window,initialdir=r'/root/', title='Choose a File')
    files = window.tk.splitlist(files)
    for each_file in files:
        file_path = each_file.name
        file_name = file_path.split('/')[-1]
        result = db.Insert("Insert Into Songs (FileName,FIlePath, Playlist) values (?,?,?)", (file_name,file_path,pl_number))
        if not result :
            messagebox.showinfo("Fail","Operation Failed")

def Playsongs(playlistNumber=0):
    songsToPlay = db.Select("select Id, FileName, FIlePath from Songs where Playlist = " + str(playlistNumber)+" order by Id", ())
    if songsToPlay:
        for eachSong in songsToPlay:
            command = ['xdg-open', eachSong[2]]
            pipe = sb.Popen(command)

def HandleSingle(songPath=None, job="Play", songId=None):
    try:
        if songPath and job == "Play" :
            command = ['xdg-open', songPath]
            pipe = sb.Popen(command)
        elif songId and job == "Remove":
            result = db.Delete("Delete From Songs Where Id = " + str(songId), ())
            if result:
                messagebox.showinfo("Success", "Song Removed")
            else:
                messagebox.showinfo("Failure", "Song NOT Removed")
        elif songPath and job == "Delete":
            result = db.Delete("Delete From Songs Where Id = " + str(songId), ())
            if result:
                os.remove(songPath)
                messagebox.showinfo("Success", "Song Deleted")
            else:
                messagebox.showinfo("Failure", "Song NOT Deleted")
    except Exception as e:
        messagebox.showinfo("ERROR","Somthing Went Wrong")

playlists=[]
def viewClicked(playlist=None , number=0):

    playlistWindow = tk.Toplevel(root)
    playlistWindow.title(playlists[number][1])
    playlistWindow.geometry("800x600")

    tk.Button(master=playlistWindow, text="Add Songs",
              command=lambda: browseSongs(window=playlistWindow, pl_number=playlists[number][0])).grid(row=0, column=1)

    tk.Button(master=playlistWindow, text="Refresh",
              command=lambda: getSongs(window_songs=playlistWindow, playlistId=playlists[number][0])).grid(row=0, column=2)

    tk.Button(master=playlistWindow, text="Play Songs",
              command=lambda: Playsongs(playlistNumber=playlists[number][0])).grid(row=0, column=3)

    def getSongs(window_songs=None,playlistId=0):
        songs = db.Select("select Id, FileName, FIlePath from Songs where Playlist = "+str(playlistId), ())
        print(window_songs.pack_slaves())
        if songs :
            for each_song , index in zip(songs,range(songs.__len__())):
                tk.Label(master=window_songs, text=str(each_song[0]), font=(14), padx=20).grid(row=index+1, column=0)
                tk.Label(master=window_songs, text=str(each_song[1]), wraplength= 500, font=(14),pady=10).grid(row=index+1, column=1)
                tk.Button(master=window_songs, text="Play", command= lambda path=each_song[2],songNo=each_song[0]: HandleSingle(songPath=path, job="Play", songId=songNo)).grid(row=index+1, column=2)
                tk.Button(master=window_songs, text="Remove", command= lambda path=each_song[2],songNo=each_song[0]: HandleSingle(songPath=path, job="Remove", songId=songNo)).grid(row=index + 1, column=3)
                tk.Button(master=window_songs, text="Delete", command= lambda path=each_song[2],songNo=each_song[0]: HandleSingle(songPath=path, job="Delete", songId=songNo)).grid(row=index + 1, column=4)
        else:
            tk.Label(master=window_songs, text="No Songs Present", font=(14)).grid(row=0, column=0)

    getSongs(window_songs=playlistWindow,playlistId=playlists[number][0])
    playlistWindow.mainloop()


def __main__():
    global root
    root = tk.Tk()
    root.title('Playlist')
    root.geometry("800x600")

    label = tk.Label(master=root, text="Playlists", font=("Times New Roman Bold", 20), pady=10).grid(row=0, column=1, padx=50)

    global playlists
    playlists = db.Select("Select Id, Name from PlayLists", ())

    if playlists:
        row = 2
        for index , each_playlist in zip(range(playlists.__len__()), playlists):
            tk.Label(master=root, text=str(each_playlist[0]), font=(14), padx=20).grid(row=row, column=0)
            tk.Label(master=root, text=str(each_playlist[1]), font=(14)).grid(row=row, column=1)
            tk.Button(root, text='View', command=lambda index=index :viewClicked(number=index)).grid(row=row, column=2)
            row+=1

    else:
        label = tk.Label(master=root, text="No Playlists Present", font=(14)).grid(row=1, column=0)

    root.mainloop()


if __name__ == "__main__":
    __main__()