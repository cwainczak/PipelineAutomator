import webbrowser
import pyautogui
import time
import re

def main():
    choice = getOption()
    if choice == "1":
        # parse video titles
        parsePlaylistForVideos()
    elif choice == "2":
        # check for missing videos
        print("These are the missing videos:\n")
        for title in checkForMissingVideos():
            print(title)
    elif choice == "3":
        # continue publishing
        continuePublishing()
    elif choice == "4":
        exit(1)

def continuePublishing():
    staffName = input("Enter the staff's last name: ")
    # get amount of titles
    videosLeft = getLineCount("video_titles.txt")
    # open pipeline
    webbrowser.open("https://pipeline.westfield.ma.edu/app/library.aspx")
    wait(4)
    # get list of published videos
    p = open("published_videos.txt", "a")
    # get list of titles
    f = open("video_titles.txt", "r")
    line = f.readline()
    while line != "":
        line = dealWithExtraCharacters(line)
        # if it failed, note and refresh
        if publishVideo(line, staffName) is False:
            doneMessage = "\nThe video \"" + line + "\" has not been published"
            print(doneMessage)
        else:
            videosLeft -= 1
            doneMessage = line + "\t|\tDONE"
            print(doneMessage + "\t(" + str(videosLeft) + " more!)")
        p.write(doneMessage + "\n")
        p.flush()
        line = f.readline()
    p.close()
    f.close()

def getOption():
    choice = input("--------------------------------------------------------\n"
                   "Parse playlist .html file for video titles: 1\n"
                   "Check for shared library missing videos: 2\n"
                   "Continue publishing from current progress: 3\n"
                   "Exit: 4\n"
                   "--------------------------------------------------------\n"
                   "Select an option - ")
    while choice != "1" and choice != "2" and choice != "3" and choice != "4":
        print("Invalid input. Enter respective number to continue.")
        choice = input("Select an option -\n"
                       "Parse current .html file for video titles: 1\n"
                       "Check for shared library missing videos: 2\n"
                       "Continue publishing from current progress: 3\n"
                       "Exit: 4")
    return choice

def dealWithExtraCharacters(title):
    if "," in title:
        titleList = title.split(",")
        title = getLongerPartOfString(titleList)
    if "?" in title:
        titleList = title.split("?")
        title = getLongerPartOfString(titleList)
    if "&" in title:
        titleList = title.split("&")
        title = getLongerPartOfString(titleList)
    if "\n" in title:
        title = title.split("\n")[0]
    return title

def getLongerPartOfString(titleList):
    # longer side is generally more descriptive, so it is useful to return the longer side
    longest = ""
    for part in titleList:
        if len(part) > len(longest):
            longest = part
    return longest

def parsePlaylistForVideos():
    dir = "full playlists/" + input("Enter the staff's last name: ") + ".html"
    #rule = r"<div class=\"ev-pl-item-title\" title=\"([a-zA-Z0-9 '?&{},#;$\.\-/\(\)]*)"
    rule = r"<div class=\"ev-pl-item-title\" title=\"([^<>\"]*)\""
    v = open(dir, "r")
    data = v.read().replace('\n', '').replace('\r', '')
    v.close()
    titles = re.findall(rule, data, re.IGNORECASE)
    # write titles to video_titles.txt
    vt = open("all_video_titles.txt", "w")
    for title in titles:
        if title != "${name}":
            if "&#39;" in title: # html code for '
                title = title.replace("&#39;", "'")
            if "&amp;" in title: # html code for &
                title = title.replace("&amp;", "&")
            if "&quot;" in title: # html code for "
                title = title.replace("&quot;", '"')
            vt.write(title + "\n")
    vt.close()

def checkForMissingVideos():
    # TAKE A LOOK AT THIS TO MAKE SURE IT WORKS PROPERLY

    # add all videos to list
    expectedVideoList = []
    v = open("all_video_titles.txt", "r")
    line = v.readline().replace('\n', '')
    while line != "":
        expectedVideoList.append(line)
        line = v.readline().replace('\n', '')

    # get titles from shared library
    v = open("D:/Downloads/raw_html.html", "r")
    data = v.read().replace('\n', '').replace('\r', '')
    rule = r"target=\"_blank\" title=\"Preview: ([^<>\"]*)\""
    v.close()
    actualVideoList = re.findall(rule, data, re.IGNORECASE)

    # compare and keep track of missing videos
    for i in range(len(actualVideoList)):
        actualVideoList[i] = actualVideoList[i].lower()

    missingVideos = []
    for title in expectedVideoList:
        if title.lower() not in actualVideoList:
            # add to missing videos
            missingVideos.append(title)
    return missingVideos

def getLineCount(textFile):
    lineCount = 0
    f = open(textFile, "r")
    line = f.readline()
    while line != "":
        lineCount += 1
        line = f.readline()
    return lineCount

def isFailedSearch():
    if pyautogui.locateOnScreen("images/no_items_found.png") is None:
        return False
    return True

def publishVideo(title, staffName):

    # searches for video
    pyautogui.typewrite(title)
    wait(1)
    pyautogui.hotkey("enter")
    # wait for load time
    wait(4)

    # if search fails, return false
    if isFailedSearch():
        return False

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

    # if it worked
    return True

def multiLeftClicker(numClicks):
    for x in range(numClicks):
        pyautogui.leftClick()

def wait(seconds):
    time.sleep(seconds)

if __name__ == '__main__':
    main()
