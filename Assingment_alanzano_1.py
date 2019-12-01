import urllib2
import xml.etree.ElementTree as ET
import csv
from operator import itemgetter

#Functions 

#Function used to filter tags for elements which require a single response 
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

#Function used to return multiple elements for identified tag                    
def itering(Itemized, Listing):
    try:
        for a in Listing.find(item).iter('*'):
            Itemized.append(a.text)
        return Itemized[1:]
    except:
        pass

#Function used to filter tags for elements which require multiple responses    
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

#Fetch data from source                            
data = urllib2.urlopen('http://syndication.enterprise.websiteidx.com/feeds/BoojCodeTest.xml')

#Define list which contains tags that require a single response
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

#Define list which contains tags that require multiple responses
Multi_item_list = ['Appliances', \
                   'Rooms']

#Define header order for output to csv file
list_order = [0,1,2,3,4,5,6,7,8,10,11,9]
Desc_index = 11 #identify list index where 'description' is located
Date_index = 2 #identify list index where 'date' is located

#parsing data from source
tree = ET.parse(data)
root = tree.getroot()

#Define list for output to csv file 
Final_CSV = []

#Main loop iterating through each listing 
for Listing in root:   
    To_CSV = [] #List which refreshes for each listing. Relevant data is appended here, which becomes a line item in final list 
    for item in Single_item_list: #loop through all required elements that have a single response 
        result = FilterData_Single(Listing, item) #pass listing tag and relevant header item to function to fetch data element 
        if result == [] or result == None: #Conditional statement filtering unacceptable entries and replacing them with blanks 
            result = ''
        else:
            pass
        To_CSV.append(result)
    for item in Multi_item_list: #loop through all required elements that have multiple responses
        result = FilterData_Multi(Listing, item) #pass listing tag and relevant header item to function to fetch data elements
        if result == [] or result == None: #Conditional statement filtering unacceptable entries and replacing them with blanks 
            result = ''
        else:
            result = ','.join(result)
        To_CSV.append(result)
    
    To_CSV = [To_CSV[i] for i in list_order] #orders list with desired header order
    
    #Conditional statement filtering data relevant to description length and date range specifications 
    if ' and ' in To_CSV[Desc_index][0:200] and To_CSV[Date_index] > '2015-12-31' and To_CSV[Date_index] < '2017-01-01':
        To_CSV[Desc_index] = To_CSV[Desc_index][0:200]
        To_CSV[Date_index] = To_CSV[Date_index][0:10]
        Final_CSV.append(To_CSV) #appends each line to final list to be exported to CSV
    else:
        pass

Final_CSV = sorted(Final_CSV, key=itemgetter(Date_index)) #orders data in final list by date
Final_CSV.insert(0, ['MlsId', 'MlsName', 'DateListed', 'StreetAddress', 'Price', 'Bedrooms', 'FullBathrooms',\
                     'HalfBathrooms', 'ThreeQuarterBathrooms', 'Appliances', 'Rooms', 'Description']) #adds headers

#Exports finalized list to CSV
with open ('Output.csv', 'w') as csv_file:
    csv_writer = csv.writer(csv_file, lineterminator = '\n')
    csv_writer.writerows(Final_CSV)

    
            
            
            
            
