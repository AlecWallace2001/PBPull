import urllib
import urllib2
import os
import datetime
import subprocess

#This gives our baseline time
hTime = str(datetime.datetime.utcnow())
hTime = hTime[:hTime.find(':')]
#This value currently never changes so that it can run indefinitly.
rRepeat = True
#This is to run the downloader for TOS RSS feeds. If creating an executable, exchange the 
#commenting on the two following lines
#dPath = os.path.join(os.getcwd(), "PBPull_2.0_part_2.exe")
dPath = os.path.join(os.getcwd(), "PBPull_2.0_part_2.py")
fPath = ""


def mHtmLink(HtmLink, OHtmlLink = ''):
    openingLines = ['\n<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"', '\n        "http://www.w3.org/TR/html4/loose.dtd">', '\n<html lang="en">', '\n', '\n<head>']
    closingLines = ['\n<title>Photobucket Thumbs</title>', '\n</head>', '\n', '\n<body>', '\nLoading your Library','\n</body>', '\n</html>']
    if OHtmlLink != '':
        if os.path.isfile(OHtmlLink) == True:
            return
    if os.path.isfile(HtmLink)== False:
        myOutputFile = open(HtmLink, 'wb')
        myOutputFile.writelines(openingLines)
        myOutputFile.writelines('\n<meta HTTP-EQUIV="REFRESH" content="0; url='+LibFull+'">')
        myOutputFile.writelines(closingLines)
        myOutputFile.close()

while rRepeat == True:
    try:
        #This is the URL for the recents page. In theory you can use any page from recents but it doesnt matter that much.
        response = urllib2.urlopen("http://photobucket.com/recentuploads?page=1")
        http = response.read()
        http = http.replace("\/", "/")
        #This segment searches through the HTML we have read from Photobucket looking for images. If it doesnt find any more then it will
        #reread the page.
        while http.find("fullsizeUrl") >= 0:
            http = http[http.find("fullsizeUrl")+14:]
            end = http.find('","')
            hName = http[:end]
            http = http[end+3:]
            if hName != "":
                #This starts the parsing of the image url so we can give it an origional descriptive name so we know if a duplicate
                #has been found.
                startA = hName.find('albums') 
                fName = hName[startA+7:]
                fName = fName.replace('/', '')
                folderN1 = hName[7:hName.find(".")]
                folderN2 = hName[hName.find("albums")+7:]
                folderN2 = folderN2[:folderN2.find('/')]
                folderN3 = hName[hName.find("albums")+8+len(folderN2):]
                folderN3 = folderN3[:folderN3.find('/')]
                fName = folderN1+"--"+folderN3+"--"+fName
                htmlName = folderN1+"--"+folderN3+".html"
                
                LibFull = "http://"+folderN1+".photobucket.com/user/"+folderN3+"/library/?view=recent&page=1"
                #This checks the current time to verify if we need to move over to a different folder
                nTime = str(datetime.datetime.now())
                nTime = nTime[:nTime.find(':')]
                if nTime != hTime:
                    hTime = nTime
                    if fPath != "":
                        oPath = fPath
                    else:
                        oPath = os.path.join(os.getcwd(), hTime)
                    fPath = os.path.join(os.getcwd(), hTime)
                    if os.path.exists(fPath) == False:
                        os.makedirs(fPath)
                tPath = fPath
                fNameB = fName
                fName = os.path.join(tPath, fName)
                
                if hName[:4] == "http":
                    try:
                        if os.path.isfile(fName) != True:
                            imgData = urllib2.urlopen(hName).read()
                            rName = fName.lower()
                            #I added this name filter to help weed out spammy ebay listing pics. This catches a lot but not all.
                            #To avoid accidentally deleting a win, they are sent to a specific Ebay folder)
                            if len(imgData) == 7883:
                                tos = os.path.join(fPath, "TOS")
                                if os.path.exists(tos) == False:
                                    os.makedirs(tos)
                                output = open(os.path.join(tos, fNameB), 'wb')
                                htmlName = os.path.join(tos, htmlName)
                                mHtmLink(htmlName)
                                subprocess.call([dPath, folderN3])
                            elif rName.find("ebay") != -1:
                                eBay = os.path.join(fPath, "Ebay")
                                if os.path.exists(eBay) == False:
                                    os.makedirs(eBay)
                                output = open(os.path.join(eBay, fNameB), 'wb') 
                            elif rName.find("facebook") != -1:
                                faceBook = os.path.join(fPath, "Facebook")
                                if os.path.exists(faceBook) == False:
                                    os.makedirs(faceBook)
                                output = open(os.path.join(faceBook, fNameB), 'wb')
                            elif rName.find("snapsave") != -1:
                                snapSave = os.path.join(fPath, "SnapSave")
                                if os.path.exists(snapSave) == False:
                                    os.makedirs(snapSave)
                                output = open(os.path.join(snapSave, fNameB), 'wb')
                                htmlName = os.path.join(snapSave, htmlName)
                                #This creates the link HTML file
                                mHtmLink(htmlName)
                            elif rName.find("screenshot") != -1:
                                screenShot = os.path.join(fPath, "Screenshot")
                                if os.path.exists(screenShot) == False:
                                    os.makedirs(screenShot)
                                output = open(os.path.join(screenShot, fNameB), 'wb')
                                htmlName = os.path.join(screenShot, htmlName)
                                #This creates the link HTML file
                                mHtmLink(htmlName)
                            elif rName.find("snapchat") != -1:
                                snapChat = os.path.join(Path, "SnapChat")
                                if os.path.exists(snapChat) == False:
                                    os.makedirs(snapChat)
                                output = open(os.path.join(snapChat, fNameB), 'wb')
                                htmlName = os.path.join(snapChat, htmlName)
                                #This creates the link HTML file
                                mHtmLink(htmlName)
                            else:
                                output = open(fName, 'wb')
                                htmlName = os.path.join(fPath, htmlName)
                                oHtmlName = os.path.join(oPath, htmlName)
                                #This creates the link HTML file
                                mHtmLink(htmlName, oHtmlName)
                            output.write(imgData)
                            output.close()
                    except:
                        #This exception occurs when the file has been found in the folder. This prevents a flooding of duplicate images
                        #or wasted time downloading one you already have.
                        print "Duplicate Image"
    except exception as e:
        #This is a simple restart in case of any issues. I have come in to find it not running and when checking the log I got errors
        #from HTTP access to simple timeout errors. This catches them all and restarts the application.
        print e
        print "Fatal Error, Restarting"
        
