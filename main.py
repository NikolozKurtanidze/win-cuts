import PySimpleGUI as sg
import cv2
from pynput.keyboard import Key, Controller

counter = 0

layout = [
    [sg.Image(key = '-IMAGE-')],
    [sg.Text('Blink counter: ' + str(counter), key = "-TEXT-", expand_x=True, justification='c')]
]
window = sg.Window('win-cuts', layout)

#Get video
video = cv2.VideoCapture(0)
eyes_cascade = cv2.CascadeClassifier('haarcascade_eye_tree_eyeglasses.xml')

#Keyboard init
keyboard = Controller()

#Functions
def goToRightDesktop():
    keyboard.press(Key.ctrl_l)
    keyboard.press(Key.cmd_l)
    keyboard.press(Key.right)
    keyboard.release(Key.ctrl_l)
    keyboard.release(Key.cmd_l)
    keyboard.release(Key.right)

def goToLeftDesktop():
    keyboard.press(Key.ctrl_l)
    keyboard.press(Key.cmd_l)
    keyboard.press(Key.left)
    keyboard.release(Key.ctrl_l)
    keyboard.release(Key.cmd_l)
    keyboard.release(Key.left)

def getleftmosteye(eyes):
    leftmost = 9999999
    leftmostindex = -1
    for i in range(0,2):
        if eyes[i][0] < leftmost:
            leftmost = eyes[i][0]
            leftmostindex = i
    return eyes[leftmostindex]

def getrightmosteye(eyes):
    rightmost = 9999999
    rightmostindex = -1
    for i in range(0, 2):
        if(eyes[i][0] < rightmost):
            rightmost = eyes[i][0]
            rightmostindex = i
    return eyes[rightmostindex]
def main():
    prev_right_eye = None
    while True:
        event, values = window.read(timeout = 1000)
        if event == sg.WIN_CLOSED:
            break
        _, frame = video.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        eyes = eyes_cascade.detectMultiScale(
            gray,
            minNeighbors = 6,
            minSize = (5, 5)
        )

        if len(eyes) > 1:
            prev_right_eye = getrightmosteye(eyes)
        elif len(eyes) == 1:
            if eyes[0][0] > prev_right_eye[0]:
                print("You closed right eye")
                goToRightDesktop()
            else: 
                print("You closed left eye")
                goToLeftDesktop()
        else: print("Both eyes are closed")

        imgbytes = cv2.imencode('.png', frame)[1].tobytes()
        window['-IMAGE-'].update(data = imgbytes)

    window.close()

if __name__ == "__main__":
    main()