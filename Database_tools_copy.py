import csv
import re
import os
from bs4 import BeautifulSoup
import requests

def getInfo(filename1):
    """Open csv's, read them, get all data, get plant names, get already analyzed genome names, return list of plant names & list of already analyzed genome names"""
    
    with open(filename1) as f1:
        reader = csv.reader(f1) #opens csv file
        data1 = [] #holds all information from rows in csv
        #start for
        for row in reader:
            data1.append(row)  #grabs the information from each row             
        #end for
        
        plantNames = [] #holds list of names of plants to search
        #start for
        for i in range(len(data1)):
            plantNames.append(data1[i][0]) #grabs the first value from each row
        #end for
            
        return plantNames #function returns list of plant names to search

def getAssemblyinfo(speciesName):
    """Searches NCBI Assembly database using NCBI E-utilites API, returns assembly accession number, bioproject number and assembly publication date"""

#---------------Create e-search URL & send request to API-----------------------
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
    
    url = base_url + "esearch.fcgi?db=assembly&term=(%s[All Fields])&usehistory=y&api_key=f1e800ad255b055a691c7cf57a576fe4da08" % speciesName # creates e-search url

    api_request = requests.get(url) #sends request to api
    
    # grab the response content 
    xml_content = api_request.content 
        
    # parse with beautiful soup        
    soup = BeautifulSoup(xml_content, 'xml')
#--------------Get Query Key & Web Environments from xml------------------------    
    query_str = soup.find('QueryKey') #finds query key tag from xml
    
    querykey = str(query_str) #converts result to string variable
    
    querykey_num = querykey[10:len(querykey)-11] #parses out query key from string
    
    web_env_str = soup.find('WebEnv') #finds web environment tag from xml
    
    web_env = str(web_env_str) #converts result to string variable
    
    web_env_num = web_env[8:len(web_env)-9] #parses out web environment from string
    
#-----------------Create e-summary URL and send request to API------------------
    summary_url = base_url + "esummary.fcgi?db=assembly&query_key=%s&WebEnv=%s&api_key=f1e800ad255b055a691c7cf57a576fe4da08" % (querykey_num, web_env_num)
    
    api_request_summary = requests.get(summary_url) #sends request to api
    
    # grab the response content 
    xml_content_summary = api_request_summary.content
        
    # parse with beautiful soup        
    soup_summary = BeautifulSoup(xml_content_summary, 'xml')
#------------Gets desired information from Assembly database--------------------
    accession_str = soup_summary.find('AssemblyAccession') #finds Assembly accession number tag from xml
    
    accession = str(accession_str) #converts result to string variable
    
    accession_num = accession[19:len(accession)-20] #parses out accession number from string
    
    bioproject_str = soup_summary.find('BioprojectAccn') #finds bioproject tag from xml
    
    bioproject = str(bioproject_str) #converts result to string variable
    
    bioproject_num = bioproject[16:len(bioproject)-17]  #parses out bioproject number from string
    
    pubdate_str = soup_summary.find('AsmReleaseDate_GenBank') #finds Assembly publication date tag from xml
    
    pubdate = str(pubdate_str) #converts result to string variable
    
    pubdate_num = pubdate[24:len(pubdate)-37] #parses out assembly publication date from string
    
    return accession_num, bioproject_num, pubdate_num 
    
def getpubmedinfo(speciesName):
    """Searches NCBI PubMed database using NCBI E-utilites API, returns article title name and pubmed ID"""
#---------------Create e-search URL & send request to API-----------------------
    search_base_url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/'
    
    search_url = search_base_url + "esearch.fcgi?db=assembly&term=(%s[All Fields])&usehistory=y&api_key=f1e800ad255b055a691c7cf57a576fe4da08" % (speciesName)
    
    api_request = requests.get(search_url) #sends request to api
    
    # grab the response content 
    xml_content = api_request.content
        
    # parse with beautiful soup        
    soup = BeautifulSoup(xml_content, 'xml')
    
#--------------Get Query Key & Web Environments from xml------------------------    
    query_str = soup.find('QueryKey') #finds query key tag from xml

    querykey = str(query_str) #converts result to string variable
    
    querykey_num = querykey[10:len(querykey)-11] #parses out query key from string
    
    web_env_str = soup.find('WebEnv') #finds web environment tag from xml
    
    web_env = str(web_env_str) #converts result to string variable
    
    web_env_num = web_env[8:len(web_env)-9] #parses out web env from string
    
#-----------------Create e-link URL and send request to API---------------------
    link_base_url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/';
    link_url = link_base_url + "elink.fcgi?dbfrom=assembly&db=pubmed&query_key=%s&WebEnv=%s&linkname=assembly_pubmed&cmd=neighbor_history&api_key=f1e800ad255b055a691c7cf57a576fe4da08" % (querykey_num, web_env_num)
    #print(link_url)
    
    api_request_2 = requests.get(link_url) #sends request to api
    
    # grab the response content 
    xml_content_2 = api_request_2.content
        
    # parse with beautiful soup        
    soupLink = BeautifulSoup(xml_content_2, 'xml')
    #print(soupLink)
    
#--------------Get Query Key & Web Environments from xml------------------------
    query_str2 = soupLink.find('QueryKey') #finds query key tag from xml
    #print(query_str2)
    
    querykey2 = str(query_str2) #converts result to string variable
    
    querykey_num2 = querykey2[10:len(querykey2)-11] #parses out query key from string
    #print(querykey_num2)
    
    web_env_str2 = soupLink.find('WebEnv') #finds web env tag from xml
    
    web_env2 = str(web_env_str2) #converts result to string variable
    
    web_env_num2 = web_env2[8:len(web_env2)-9] #parses out web env from string
    
#-----------------Create e-summary URL and send request to API------------------
    summary_url = search_base_url + "esummary.fcgi?db=pubmed&query_key=%s&WebEnv=%s&api_key=f1e800ad255b055a691c7cf57a576fe4da08" % (querykey_num2, web_env_num2)
    #print(summary_url)
    
    api_request_summary = requests.get(summary_url) #sends request to api
    
    # grab the response content 
    xml_content_summary = api_request_summary.content
        
    # parse with beautiful soup        
    soup_summary = BeautifulSoup(xml_content_summary, 'xml')
    #print(soup_summary)
    
#------------Gets desired information from PubMed database----------------------
    title_str = soup_summary.find('Item', {'Name':"Title"}) #finds "title" tag from xml 
    
    title = str(title_str) #converts result into string variable
    
    title_name = title[33:len(title)-7] #parses out article title from string
    
    title_name_strip = title_name.replace(",", " ")
    
    pubmed_id_str = soup_summary.find('Item', {'Name':"pubmed"}) #finds "pubmed" tag from xml
    
    pubmed_id = str(pubmed_id_str) #converts result into string variable
    
    pubmed_id_num = pubmed_id[34:len(pubmed_id)-7] #parses out pubmed id from string
    
    return title_name_strip, pubmed_id_num

def appendPlantDict(plantDict, speciesName, Accession_num, bioproject_num, pubdate, title, pubmed_id):
    """Creates dictionary of plant names with appropriate values"""
    
    key = speciesName #sets the dictionary key to the species name
    
    values = [Accession_num, bioproject_num, pubdate, title, pubmed_id] #sets dictionary values to appropriate information 
    
    plantDict.update({key : values}) #updates existing plantDict for every entry into dictionary
    
    return plantDict #returns completed dictionary 
    
def printFile(plantDict):
    """Takes plantDict, prints dictionary to .csv file"""
    Comma = ','
    
    Results = open("plantInfo.csv", 'a') #creates or opens existing csv file, appends data to file
    
    #Results.write("%s%c%s%c%s%c%s%c%s%c%s\n" % ("Species Name", Comma, "Accession Number", Comma,
                          #"Bioproject Number", Comma, "Publication Year", Comma, "Article Title", Comma, "Pubmed ID")) #creates headings in csv
    #start for
    for key in plantDict.keys():
        Results.write("%s, %s\n" % (key, plantDict[key])) #writes dictionary to csv file
    #end for
    
    Results.close() #closes csv file