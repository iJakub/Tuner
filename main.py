#iJ

from tkinter import filedialog
from tkinter import *
import tkinter
from datetime import datetime
import os
from frequency import *
from note import *
import time
import pyaudio
import wave
import threading

root = tkinter.Tk()
root.title("Tuner")
root.geometry("490x400")
root.resizable(False,False)
root.configure(bg='#191919')

rec_img = PhotoImage(file = r"img/record.png")
stop_img = PhotoImage(file = r"img/stop.png")
output_img = PhotoImage(file = r"img/output.png")
settings_img = PhotoImage(file = r"img/settings.png")

current_frequency = ""
def detect_frequency():
    global current_frequency
    current_frequency = check_frequency(recording, volume_division, noise_reduction)
    frequency = str(current_frequency) + "Hz"
    frequency_label.config(text = frequency)
    root.update()
    return current_frequency

previous_note = "..."
current_note = "..."
def detect_note():
    global current_frequency, current_note, previous_note
    previous_note = current_note
    current_note = identify_note(current_frequency)

    if current_note == "C0":
        current_note = previous_note
      
    else:
        logs()

    note_label.config(text = current_note)
    root.update()
    return current_note

current_time = ""
def check_time():
    global current_time
    now = datetime.now()
    current_time = (now.strftime(f"%H:%M:%S:{round(now.microsecond / 1000)}").ljust(12,"0"))
    return current_time

start_time = ""
current_timer = ""
def timer():
    global current_timer, start_time
    current_timer = time.time() - start_time
    current_timer = time.strftime("%H:%M:%S",time.gmtime(current_timer))
    timer_label.config(text = current_timer)
    root.update()
    return current_timer

output_directory = (os.getcwd() + "/output.txt").replace("\\", "/")
default_directory = output_directory
folder_selected = ""
def output():
    global default_directory, output_directory, folder_selected
    folder_selected = filedialog.askdirectory()
    output_directory = (folder_selected + "/output.txt")

    if folder_selected == "":
        output_directory = default_directory

    output_directory_label.config(text = (" " + output_directory))
    return output_directory, folder_selected

def record_audio():
    global recording, folder_selected
    
    try:
        CHUNK = 1024
        RATE = 44100
        DEVICE = 0
        FILENAME = "/output.wav"

        p = pyaudio.PyAudio()

        stream = p.open(format=pyaudio.paInt16,
                        channels=2,
                        rate=RATE,
                        input_device_index=DEVICE,
                        frames_per_buffer=CHUNK,
                        input=True)

        frames = []
        def audio():
            global recording

            while (recording == "on"):
                data = stream.read(CHUNK)
                frames.append(data)

            stream.stop_stream()
            stream.close()
            p.terminate()

            wf = wave.open(folder_selected + FILENAME, 'wb')
            wf.setnchannels(2)
            wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))
            wf.close()
        thread = threading.Thread(target=audio)
        thread.daemon = True
        thread.start()

    except:
        pass

history = ""
log = f"LOG {datetime.now()}\n"
def logs():
    global current_note, current_frequency, log, history

    current_time = check_time()
    try:
        if len(current_note) == 2:
            current_note = current_note + " "

        current_frequency = str(current_frequency) + ".0"
        if len(current_frequency) != 6:
            current_frequency = (current_frequency).ljust(6, "0")

        log = log + "\n" + current_note + "\t" + current_frequency + "Hz" + "\t" + current_timer + "\t" + check_time()
        history = history + "\n" + current_note
        history_label.config(text = history)
        root.update()
    except:
        pass



recording = "off"
def record():
    global recording, start_time
    start_time = time.time()
    record_button["state"] = DISABLED
    settings_button["state"] = DISABLED
    stop_button["state"] = NORMAL
    recording = "on"
    record_audio()

    while (recording == "on"):
        timer()
        detect_frequency()
        detect_note()

def stop():
    global output_directory, recording, log
    stop_button["state"] = DISABLED
    settings_button["state"] = NORMAL
    record_button["state"] = NORMAL
    recording = "off"
    file = open(output_directory, "w")
    file.write(log)
    file.close()
    log = ""
    return log

def entry_int(inStr,active_type):

    if active_type == '1':

        if not inStr.isdigit():
            return False
 
    return True



volume_division = "10"
noise_reduction = "5"
def settings():
    top = Toplevel(root)
    top.geometry("355x130")
    top.resizable(False,False)
    top.configure(bg='#191919')
    
    def callback(self, P):
        if str.isdigit(P) or P == "":
            return True
        else:
            return False

    def save():
        global volume_division, noise_reduction
        volume_division = volume_division_entry.get()
        noise_reduction = noise_reduction_entry.get()
        top.destroy()
        top.update()
        return volume_division, noise_reduction

    volume_division_label = Label(top, bg='#191919', text="Volume division value: ", font=("Bahnschrift", 15, "bold"), fg="white", anchor="w")
    volume_division_label.place(x=10, y=10, height=30, width=205)

    noise_reduction_label = Label(top, bg='#191919', text="Noise reduction level: ", font=("Bahnschrift", 15, "bold"), fg="white", anchor="w")
    noise_reduction_label.place(x=10, y=50, height=30, width=205)

    volume_division_entry = Entry(top, justify=CENTER, relief="solid", bg="#393939", bd=2, font=("Bahnschrift", 13, "bold"), fg="white", validate="key")
    volume_division_entry.insert(0, volume_division)
    volume_division_entry['validatecommand'] = (volume_division_entry.register(entry_int),'%P','%d')
    volume_division_entry.place(x=215, y=10, height=30 ,width=130)

    noise_reduction_entry = Entry(top, justify=CENTER, relief="solid", bg="#393939", bd=2, font=("Bahnschrift", 13, "bold"), fg="white", validate="key")
    noise_reduction_entry.insert(0, noise_reduction)
    noise_reduction_entry['validatecommand'] = (noise_reduction_entry.register(entry_int),'%P','%d')
    noise_reduction_entry.place(x=215, y=50, height=30, width=130)

    save_button = tkinter.Button(top, justify=CENTER, compound="c", relief="solid", activebackground="#393939", activeforeground="white", bg="#393939", fg="white", text="SAVE", font=("Bahnschrift",15, "bold"), command=save)
    save_button.place(x=10, y=90, height=30, width=335)


record_button = tkinter.Button(root, compound="c", relief="solid", bg="#393939", image = rec_img, command=record)
record_button.place(x=10, y=10, height=50, width=50)

stop_button = tkinter.Button(root, compound="c", relief="solid", bg="#393939", image = stop_img, command=stop, state=DISABLED)
stop_button.place(x=10, y=70, height=50, width=50)

settings_button = tkinter.Button(root, compound="c", relief="solid", bg="#393939", image = settings_img, command=settings)
settings_button.place(x=10, y=130, height=50, width=50)

output_button = tkinter.Button(root, compound="c", relief="solid", bg="#393939", image = output_img, command=output)
output_button.place(x=430, y=10, height=50, width=50)

output_directory_label = Label(root, bg="#393939", fg="white", bd=2, relief="solid", anchor="w", text=(" " + output_directory), font=("Bahnschrift", 13, "bold"))
output_directory_label.place(x=70, y=10, height=50, width=361)

frequency_label = Label(root, bg="#393939", fg="white", bd=2, relief="solid", text="0Hz", font=("Bahnschrift", 20, "bold"))
frequency_label.place(x=230, y=70, height=50, width=250)

timer_label = Label(root, bg="#393939", fg="white", bd=2, relief="solid", text="00:00:00", font=("Bahnschrift", 20, "bold"))
timer_label.place(x=70, y=70, height=50, width=150)

history_label = Label(root, bg="#393939", fg="white", bd=2, relief="solid", anchor="s", text=history, font=("Arial", 19, "bold"))
history_label.place(x=70, y=130, height=250, width=150)

note_label = Label(root, bg="#393939", fg="white", bd=2, relief="solid", anchor="center", text="...", font=("Arial", 90, "bold"))
note_label.place(x=230, y=130, height=250, width=250)

root.mainloop()