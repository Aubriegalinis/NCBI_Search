import Database_tools_copy
import os

def main():
    plantNames = Database_tools_copy.getInfo("REU_Literature_Plant_Species_List.csv") #calls getInfo() from Database_tools, stores result in  plantNames
    
    #start at index 1 of list, increase by 10 each run
    index = 1 #keeps track of index in plantNames list
    count = 1 #keeps track of number of requests per second 
    plantDict = {} #creates new dictionary
    
    #start while
    while index != len(plantNames) and count != 11:
        speciesName = plantNames[index] #grabs scientific name from list, stores result in speciesName
        accession_num, bioproject_num, pubdate = Database_tools_copy.getAssemblyinfo(speciesName) #calls getAssemblyinfo() from Database_tools, stores results in accession_num, bioproject_num, and pubdate
        title, pubmed_id = Database_tools_copy.getpubmedinfo(speciesName) #calls getpubmedinfo() from Database_tools, stores results in title and pubmed_id
        updated_plantDict = Database_tools_copy.appendPlantDict(plantDict, speciesName, accession_num, bioproject_num, pubdate, title, pubmed_id) #calls appendPlantDict() from Database_tools, stores result in updated_plantDict
        index = index + 1 #increases index by 1 
        count = count + 1 #increases count by 1
        
    #end while
    
    Database_tools_copy.printFile(updated_plantDict) #calls printFile() from Database_tools
    
    print("File printed!")
    
    
    
    
main() #calls main()