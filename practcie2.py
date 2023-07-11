from tkinter import *

window = Tk()

note_list = []

def play_sound(note):
    global note_list

    note_list.append(note)
    sound_file = note + ".mp3"
    e.insert(END, note.split(".")[0])
    #sounds.music.load(sound_file)
    #sounds.music.play()

def play():
    global note_list
    for file_name in note_list:
        print(file_name)
        #sounds.music.load(file_name)
        #sounds.music.play()
        #print(file_name)

    note_list = []
    e.delete(0,END)

e = Entry(window)
bt1 = Button(window, text = "도", command = lambda:play_sound("도"))
bt2 = Button(window, text = "레", command = lambda:play_sound("레"))
b11 = Button(window, text="연주하기", command = play)

bt1.pack()
bt2.pack()
b11.pack()
e.pack()


window.mainloop()