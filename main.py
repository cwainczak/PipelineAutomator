import webbrowser
import pyautogui
import time

def main():
    staffName = input("Enter the staff's last name: ")
    # open pipeline
    webbrowser.open("https://pipeline.westfield.ma.edu/app/library.aspx")
    wait(4)
    # get list of published videos
    p = open("published_videos.txt", "a")
    # get list of titles
    f = open("video_titles.txt", "r")
    line = f.readline()
    while line != "":
        line = dealWithCommasAndNewline(line)
        publishVideo(line, staffName)
        doneMessage = line + "\t|\tDONE"
        print(doneMessage)
        p.write(doneMessage + "\n")
        line = f.readline()
    p.close()
    f.close()

def dealWithCommasAndNewline(title):
    if "," in title:
        title = title.split(",")[0]
    if "\n" in title:
        title = title.split("\n")[0]
    return title

def deleteLine():
    o = open("video_titles.txt")


def publishVideo(title, staffName):

    # searches for video
    pyautogui.typewrite(title)
    wait(1)
    pyautogui.hotkey("enter")
    # wait for load time
    wait(4)

    # moves to publish
    pyautogui.moveTo(1723, 741)
    # clicks on publish
    pyautogui.leftClick()
    # wait for load time
    wait(4)

    # opens ctrl + f / finder
    pyautogui.hotkey("ctrl", "f")
    wait(1)

    # types "share" in finder
    pyautogui.typewrite("share")
    # positions onto down arrow
    pyautogui.moveTo(1657, 87)
    # clicks three times
    multiLeftClicker(3)
    # wait for load time
    wait(1)

    # expands the Share folder by moving to the position and clicking the "+" icon
    pyautogui.moveTo(305, 623)
    pyautogui.leftClick()
    # wait for load time
    wait(2)

    # move to search and click to make it active
    pyautogui.moveTo(1347, 788)
    pyautogui.leftClick()
    # type staff's name
    pyautogui.typewrite(staffName)
    pyautogui.hotkey("enter")
    # wait for load time
    wait(2)

    # move mouse to checkbox
    pyautogui.moveTo(334, 904)
    # check the box by clicking
    pyautogui.leftClick()
    # wait for load time
    wait(1)

    # scroll down to see the publish button
    pyautogui.scroll(-800)
    # wait for load time
    wait(2)

    # move cursor to publish
    pyautogui.moveTo(1799, 895)
    # click on publish
    pyautogui.leftClick()
    wait(5)

def multiLeftClicker(numClicks):
    for x in range(numClicks):
        pyautogui.leftClick()

def wait(seconds):
    time.sleep(seconds)

if __name__ == '__main__':
    main()
