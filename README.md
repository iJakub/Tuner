# Tuner
Recognizing notes based on the frequency of sound from your microphone.

**Disclaimer:** 

The program will not work well as a perfect notation of the melodies played (especially the fast ones) but it can be helpful in this task.

**Output:**
- The audio is saved in the output.wav file
- Notes, audio frequency and other data are saved in output.txt file 


# Features
- helpful in tuning instruments
- sound frequency reading
- easy-to-use GUI
- melodies and audio recording

# Setup
Before running the program, make sure you have installed all the modules from the requirements.txt file

`pip install -r requirements.txt`

If everything was successful, you can run the program and hope that everything will work :)

# Demonstration

![Demo](https://github.com/iJakub/Tuner/blob/main/demo/demo.gif)
![1](https://github.com/iJakub/Tuner/blob/main/demo/1.png)
![2](https://github.com/iJakub/Tuner/blob/main/demo/2.png)
![3](https://github.com/iJakub/Tuner/blob/main/demo/3.png)

# It doesn't work?
**Change settings**
- Increase/decrease the noise reduction level or volume division value

**Change the values in the frequency.py file**
- Change the values of the variables (in lines 16-18) so that they work well with your microphone

**Improve microphone quality**
- Improve the quality of your microphone (for example: use audio enhancement software)
- Buy a better microphone (even if that's not the point, it's always useful)

# Compilation using PyInstaller
If you want to use the program on a computer that does not have the necessary software installed, use the PyInstaller module to compile it into an executable file

**Module installation**

`pip install pyinstaller`

**Compilation**

`pyinstaller --noconfirm --onedir --windowed --add-data "frequency.py;." --add-data "note.py;." --add-data "img;img/" --collect-data librosa "main.py"`
