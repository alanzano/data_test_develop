# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import urllib2
import xml.etree.ElementTree as ET


data = urllib2.urlopen('http://syndication.enterprise.websiteidx.com/feeds/BoojCodeTest.xml')

tree = ET.parse(data)
root = tree.getroot()

print root.findall('Listing')





