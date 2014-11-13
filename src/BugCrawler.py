import urllib.request
import html.parser
import xml.etree.ElementTree as ET
import re
import os

fileHandlingURL     = "https://bugzilla.mozilla.org/buglist.cgi?component=File%20Handling&query_format=advanced&resolution=---&order=bug_status%2Cpriority%2Cassigned_to%2Cbug_id&limit=0"
fileHandlingHTML    = "fileHandling"

buildConfigBugsURL  = "https://bugzilla.mozilla.org/buglist.cgi?component=Build%20Config&query_format=advanced&resolution=---&order=bug_status%2Cpriority%2Cassigned_to%2Cbug_id&limit=0"
buildConfigBugsHTML = "buildConfig"

domBugsURL          = "https://bugzilla.mozilla.org/buglist.cgi?component=DOM&query_format=advanced&resolution=---&order=bug_status%2Cpriority%2Cassigned_to%2Cbug_id&limit=0"
domBugsHTML         = "dom"

networkingBugsURL   = "https://bugzilla.mozilla.org/buglist.cgi?component=Networking&query_format=advanced&resolution=---&order=bug_status%2Cpriority%2Cassigned_to%2Cbug_id&limit=0"
networkingBugsHTML  = "networking"

securityBugsURL     = "https://bugzilla.mozilla.org/buglist.cgi?component=Security&query_format=advanced&resolution=---&order=bug_status%2Cpriority%2Cassigned_to%2Cbug_id&limit=0"
securityBugsHTML    = "security"

#Currently Unused
resolvedBugsURL     = "https://bugzilla.mozilla.org/buglist.cgi?bug_status=RESOLVED&bug_status=VERIFIED&bug_status=CLOSED&query_format=advanced&order=bug_status%2Cpriority%2Cassigned_to%2Cbug_id&limit=0"
resolvedBugsHTML    = "resolvedBugs"

#urlList             = [fileHandlingURL,     buildConfigBugsURL,     domBugsURL,     networkingBugsURL,      securityBugsURL,    resolvedBugsURL]
#htmlFileList        = [fileHandlingHTML,    buildConfigBugsHTML,    domBugsHTML,    networkingBugsHTML,     securityBugsHTML,   resolvedBugsHTML]

urlList             = [resolvedBugsURL]
htmlFileList        = [resolvedBugsHTML]

xmlBugDatabase      = "XMLBugDatabase"
xmlFormBugURL       = "https://bugzilla.mozilla.org/show_bug.cgi?ctype=xml&id="

if not os.path.exists(xmlBugDatabase):
    os.makedirs(xmlBugDatabase)

for index, everyURL in enumerate(urlList):
    
    request = urllib.request.Request(everyURL)                  # Create a Request object with relevant URL
    response = urllib.request.urlopen(request)                  # Send Request and Get Response

    everyHTMLDir = xmlBugDatabase + '\\'+ htmlFileList[index]
    everyHTML = xmlBugDatabase + "\\"+ htmlFileList[index] + "\\"+ htmlFileList[index] +".html"
    
    if not os.path.exists(everyHTMLDir):
        os.makedirs(everyHTMLDir)
        print("Directory " + everyHTMLDir + " is now Created")
    else:
        print("Directory " + everyHTMLDir + " is already Created.")
    
    f = open(everyHTML, 'w', encoding='utf-8') 
    print ((response.read().decode('utf-8')), file=f)           
    f.close()                                                   #Dump the HTML into a File

    # Open the File and load the HTML data as a long string
    with open(everyHTML, "r", encoding='utf-8') as myfile:
        data = myfile.read().replace('\n', '')

    bugIDList = re.findall ('<input type="hidden" name="id" value="(\d+)">', data)
    bugIDList = list(set(bugIDList))                            # Remove duplicates from the list
    
    for bugID in bugIDList:
        if os.path.exists(everyHTMLDir + "\\"+ str(bugID)+".xml"):
            continue

        request = urllib.request.Request(xmlFormBugURL + str(bugID))
        response = urllib.request.urlopen(request)
        f = open(everyHTMLDir + "\\"+ str(bugID)+".xml", 'w', encoding='utf-8')
        os.path.abspath(f.name);
        print ((response.read().decode('utf-8')), file=f)
        f.close()
        
        bugXMLTree = ET.parse(everyHTMLDir + "\\"+ str(bugID)+".xml")
        root = bugXMLTree.getroot()
        bugStatusTag = root.find('.//bug_status')
        print (bugStatusTag.text)
        print ("Created XML file @ "+ xmlBugDatabase + "/"+ str(bugID)+".xml");
    
    

