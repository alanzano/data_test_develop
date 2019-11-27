# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import urllib2
import xml.etree.ElementTree as ET

def FilterData(x):
    try:
        return x.text
    except:
        return ''

data = urllib2.urlopen('http://syndication.enterprise.websiteidx.com/feeds/BoojCodeTest.xml')

tree = ET.parse(data)
root = tree.getroot()

for i in root:
    StreetAddress = FilterData(i.find('Location').find('StreetAddress'))
    Price = FilterData(i.find('ListingDetails').find('Price'))
    MlsId = FilterData(i.find('ListingDetails').find('MlsId'))
    MlsName = FilterData(i.find('ListingDetails').find('MlsName'))
    DateListed = FilterData(i.find('ListingDetails').find('DateListed'))
    Description = FilterData(i.find('BasicDetails').find('Description'))
    Bedrooms = FilterData(i.find('BasicDetails').find('Bedrooms'))
    FullBathrooms= FilterData(i.find('BasicDetails').find('FullBathrooms'))
    HalfBathrooms = FilterData(i.find('BasicDetails').find('HalfBathrooms'))
    ThreeQuarterBathrooms = FilterData(i.find('BasicDetails').find('ThreeQuarterBathrooms'))
    print StreetAddress




