import webbrowser
import pyautogui
import time
import re

def main():
    choice = getOptionMenu()
    if choice == "1":
        # parse video titles
        parsePlaylistForVideos()
    elif choice == "2":
        # check for missing videos
        i = int(input("Enter the amount of playlist .html files to parse: "))
        missingVideos = checkForMissingVideos(i)
        numOfMissingVideos = len(missingVideos)
        print("There are: " + str(numOfMissingVideos) + " missing videos...")
        i = getOptionYN("Do you want to write them to video_titles_remaining.txt? (y/n): ")
        if i == "y":
            f = open("video_titles_remaining.txt", "w")
            for title in missingVideos:
                f.write(title + "\n")
    elif choice == "3":
        # continue publishing
        continuePublishing()
    elif choice == "4":
        # confirm publishing
        input("Make sure the appropriate webpage is pulled up beforehand.\nPress enter to continue, and then quickly click the window to ensure focus.")
        wait(3)
        confirmPublishedVideos()
    elif choice == "5":
        exit(1)

def continuePublishing():
    staffName = input("Enter the staff's last name: ")
    # get amount of titles
    videosLeft = getLineCount("video_titles_remaining.txt")
    # open pipeline
    webbrowser.open("https://pipeline.westfield.ma.edu/app/library.aspx")
    wait(4)
    # get list of published videos
    p = open("published_videos.txt", "a")
    # get list of titles
    f = open("video_titles_remaining.txt", "r")
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

def getOptionMenu():
    choice = input("--------------------------------------------------------\n"
                   "Parse playlist .html file for all video titles: 1\n"
                   "Check for shared library missing videos: 2\n"
                   "Continue publishing from current progress: 3\n"
                   "Confirm published videos: 4\n"
                   "Exit: 5\n"
                   "--------------------------------------------------------\n"
                   "Select an option - ")
    while choice != "1" and choice != "2" and choice != "3" and choice != "4" and choice != "5":
        print("Invalid input. Enter respective number to continue.")
        choice = input("--------------------------------------------------------\n"
                       "Parse playlist .html file for all video titles: 1\n"
                       "Check for shared library missing videos: 2\n"
                       "Continue publishing from current progress: 3\n"
                       "Confirm published videos: 4\n"
                       "Exit: 5\n"
                       "--------------------------------------------------------\n"
                       "Select an option - ")
    return choice

def getOptionYN(prompt):
    i = input(prompt)
    while i != "y" and i != "n":
        print("Invalid input. Enter y or n to continue.")
        i = input(prompt)
    return i

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
    dir = "playlists/" + input("Enter the staff's last name: ") + ".html"
    #rule = r"<div class=\"ev-pl-item-title\" title=\"([a-zA-Z0-9 '?&{},#;$\.\-/\(\)]*)"
    rule = r"<div class=\"ev-pl-item-title\" title=\"([^<>\"]*)\""
    v = open(dir, "r")
    data = v.read().replace('\n', '').replace('\r', '')
    v.close()
    titles = re.findall(rule, data, re.IGNORECASE)
    # write titles to video_titles_remaining.txt
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

def checkForMissingVideos(numOfHtmlFiles):
    # add all videos to list
    expectedVideoList = []
    v = open("all_video_titles.txt", "r")
    line = v.readline().replace('\n', '')
    while line != "":
        expectedVideoList.append(line)
        line = v.readline().replace('\n', '')
    v.flush()
    v.close()
    # get titles from shared library
    data = ""
    for x in range(numOfHtmlFiles):
        v = open("D:/Downloads/raw_html" + str(x+1) + ".html", "r")
        data += v.read().replace('\n', '').replace('\r', '')
        v.flush()
        v.close()
    rule = r"target=\"_blank\" title=\"Preview: ([^<>\"]*)\""
    actualVideoList = re.findall(rule, data, re.IGNORECASE)
    for x in range(len(actualVideoList)):
        if "&#39;" in actualVideoList[x]: # html code for '
            actualVideoList[x] = actualVideoList[x].replace("&#39;", "'")
        if "&amp;" in actualVideoList[x]: # html code for &
            actualVideoList[x] = actualVideoList[x].replace("&amp;", "&")
        if "&quot;" in actualVideoList[x]: # html code for "
            actualVideoList[x] = actualVideoList[x].replace("&quot;", '"')

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

def confirmPublishedVideos():
    areVideosLeft = True
    while areVideosLeft is True:
        # check for "Not Published"
        # if there is, publish it
        # if not, exit loop
        loc = pyautogui.locateOnScreen("images/not_published.png")
        while loc is not None:
            # it couldn't reach the publish button, so scroll
            if confirmPublish(loc) is False:
                break
            loc = pyautogui.locateOnScreen("images/not_published.png")
        # if at the bottom of the page, go to next
        # if not, scroll down
        if pyautogui.locateOnScreen("images/page_bottom_indicator.png") is not None:
            # to get to the VERY bottom
            pyautogui.scroll(-1000)
            if goToNextPage() is False:
                areVideosLeft = False
        else:
            pyautogui.scroll(-400)
            wait(1)

# returns False if cannot reach publish button
def confirmPublish(loc):
    # loc is the location of "Not Published"
    # from there, the publish button is (x - 225, y + 75)
    # move to "Publish" and click
    loc = pyautogui.center(loc)
    publishX = loc[0] - 225
    publishY = loc[1] + 75
    # if true, cannot reach publish button
    if publishY >= 900:
        return False
    pyautogui.moveTo(publishX, publishY)
    pyautogui.leftClick()
    wait(3)
    # move to "Default Category" checkbox and click it
    pyautogui.moveTo(329, 397)
    pyautogui.leftClick()
    wait(1)
    # move to "Save Changes" and click it
    pyautogui.moveTo(1782, 490)
    pyautogui.leftClick()
    wait(4)

def goToNextPage():
    # on first page, so go to second page
    secondPageButtonLoc = pyautogui.locateOnScreen("images/2_page.png")
    if pyautogui.locateOnScreen("images/1_page_highlighted.png") is not None and secondPageButtonLoc is not None:
        secondPageButtonLoc = pyautogui.center(secondPageButtonLoc)
        pyautogui.moveTo(secondPageButtonLoc[0], secondPageButtonLoc[1])
        pyautogui.leftClick()
        wait(4)
        return True
    # on second page, so go to third page
    thirdPageButtonLoc = pyautogui.locateOnScreen("images/3_page.png")
    if pyautogui.locateOnScreen("images/2_page_highlighted.png") is not None and thirdPageButtonLoc is not None:
        thirdPageButtonLoc = pyautogui.center(thirdPageButtonLoc)
        pyautogui.moveTo(thirdPageButtonLoc[0], thirdPageButtonLoc[1])
        pyautogui.leftClick()
        wait(4)
        return True
    return False

def multiLeftClicker(numClicks):
    for x in range(numClicks):
        pyautogui.leftClick()

def wait(seconds):
    time.sleep(seconds)

if __name__ == '__main__':
    main()