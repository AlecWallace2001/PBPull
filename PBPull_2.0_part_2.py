#testing
import urllib2
import sys
import re
import os

print "Bucket Name = " + str(sys.argv[1])
bName = str(sys.argv[1])
rssPage = 'http://feed856.photobucket.com/albums/f1348/'+bName+'/account.rss'
try:
    #This is the URL for the recents page. In theory you can use any page from recents but it doesnt matter that much.
    response = urllib2.urlopen(rssPage)
    http = response.read()
    results = re.findall('" url="(.*)" />', http)
    #This segment searches through the HTML we have read from Photobucket looking for images. If it doesnt find any more then it will
    #reread the page.
    Zero = 0
    for i in results:
        hName = results[Zero]
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
            fName = re.sub("%20", '', fName)
            fPath = os.path.join(os.getcwd(), bName)
            if os.path.exists(fPath) == False:
                os.makedirs(fPath)
            fNameB = fName
            fName = os.path.join(fPath, fName)
            if hName[:4] == "http":
                try:
                    if os.path.isfile(fName) != True:
                        imgData = urllib2.urlopen(hName).read()
                        rName = fName.lower()
                        output = open(fName, 'wb')
                        output.write(imgData)
                        output.close()
                        print fName
                    else:
                        print "Duplicate Image"
                        print fName
                except:
                    #This exception occurs when the file has been found in the folder. This prevents a flooding of duplicate images
                    #or wasted time downloading one you already have.
                    print "Duplicate Image"
        Zero = Zero+1
except Exception as e:
    #This is a simple restart in case of any issues. I have come in to find it not running and when checking the log I got errors
    #from HTTP access to simple timeout errors. This catches them all and restarts the application.
    print "Fatal Error, Restarting"
    print e
