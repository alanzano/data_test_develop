import urllib2
import xml.etree.ElementTree as ET

def FilterData_Single(Listing, item):
    if Listing.tag == item:
        return Listing.text
    else:
        for i in Listing:
            if i.tag == item:
                return i.text
            else:
                for j in i:
                    if j.tag == item:
                        return j.text
                    else:
                        for k in j:
                            if k.tag == item:
                                return k.text
                            else:
                                pass
                            
def itering(Itemized, Listing):
    try:
        for a in Listing.find(item).iter('*'):
            Itemized.append(a.text)
        return Itemized[1:]
    except:
        pass


def FilterData_Multi(Listing, item):
    Itemized = []
    if Listing.tag == item:
        return itering(Itemized, Listing)
    else:
        for i in Listing:
            if i.tag == item:
                return itering(Itemized, i)
            else:
                for j in i:
                    if j.tag == item:
                        return itering(Itemized, i)
                    else:
                        for k in j:
                            if k.tag == item:
                                return itering(Itemized, i)
                            else:
                                pass
                            
data = urllib2.urlopen('http://syndication.enterprise.websiteidx.com/feeds/BoojCodeTest.xml')

Single_item_list = ['MlsId', \
                    'MlsName', \
                    'DateListed', \
                    'StreetAddress', \
                    'Price', \
                    'Bedrooms', \
                    'FullBathrooms', \
                    'HalfBathrooms', \
                    'ThreeQuarterBathrooms', \
                    'Description']

Multi_item_list = ['Appliances', \
                   'Rooms']

list_order = [0,1,2,3,4,5,6,7,8,10,11,9]
#parsing data from source
tree = ET.parse(data)
root = tree.getroot()

Final_CSV = []

for Listing in root:   
    To_CSV = []
    for item in Single_item_list:
        result = FilterData_Single(Listing, item)
        if result == [] or result == None:
            result = ''
        else:
            pass
        To_CSV.append(result)
    for item in Multi_item_list:
        result = FilterData_Multi(Listing, item)
        if result == [] or result == None:
            result = ''
        else:
            result = ','.join(result)
        To_CSV.append(result)
    
    Desc_index = 11
    Date_index = 2
    
    To_CSV = [To_CSV[i] for i in list_order]
    
    if ' and ' in To_CSV[Desc_index][0:200] and To_CSV[Date_index] > '2015-12-31' and To_CSV[Date_index] < '2017-01-01':
        To_CSV[Desc_index] = To_CSV[Desc_index][0:200]
        To_CSV[Date_index] = To_CSV[Date_index][0:10]
        Final_CSV.append(To_CSV)
    else:
        pass
