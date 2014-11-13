import os.path
import xml.etree.ElementTree as ET
import re

tree = ET.parse('./Sample.xml')
root = tree.getroot()
print (root.tag)
bug_status = root.find('.//bug_status')
print (bug_status.text)
