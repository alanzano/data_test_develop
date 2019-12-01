#####################
#Code Summary:
#This code is designed to extract XML data directly from the source and identify tags that are relevant to 
#the user. The code does this by sending each 'Listing' tag through a function which identifies tags 
#the user is seeking and returns the relevant text. This data is stored in a single list per 'Listing' tag
#which refreshes for each 'Listing'. This list is then appended to a maseter 'Final' list if it meets the 
#requirements of the assignment. Additional cleaning and filtering is done to make the data more acceptable 
#to the user and is then exported to the CSV file titled 'Output.csv'
#####################

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

#Should the user wish to alter the code for another XML file or for differenet parameters, make changes to the next section:

#####################
#For universal applicability chage the following variables:START
#####################

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

Description_length_limit = 200 #200 character limit for description 
Description_key_word = ' and ' #include 'and' in description 
Date_lower_limit = '2015-12-31' #date range must be after this
Date_upper_limit = '2017-01-01' #date rande must be before this 

#Define final header for file 
Final_header = ['MlsId', 'MlsName', 'DateListed', 'StreetAddress', 'Price', 'Bedrooms', 'FullBathrooms',\
                     'HalfBathrooms', 'ThreeQuarterBathrooms', 'Appliances', 'Rooms', 'Description']

#####################
#For universal applicability chage the following variables:STOP
#####################

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
    if Description_key_word in To_CSV[Desc_index][0:Description_length_limit] and To_CSV[Date_index] > Date_lower_limit and To_CSV[Date_index] < Date_upper_limit:
        To_CSV[Desc_index] = To_CSV[Desc_index][0:Description_length_limit]
        To_CSV[Date_index] = To_CSV[Date_index][0:10]
        Final_CSV.append(To_CSV) #appends each line to final list to be exported to CSV
    else:
        pass

Final_CSV = sorted(Final_CSV, key=itemgetter(Date_index)) #orders data in final list by date
Final_CSV.insert(0, Final_header) #adds headers

#Exports finalized list to CSV
with open ('Output.csv', 'w') as csv_file:
    csv_writer = csv.writer(csv_file, lineterminator = '\n')
    csv_writer.writerows(Final_CSV)

    
            
            
            
            
