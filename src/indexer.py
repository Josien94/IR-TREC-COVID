import argparse
import wget, tarfile, os
import xml.etree.ElementTree as et
import csv, itertools
import json
import re
import os, os.path
import string
from datetime import datetime
from whoosh.fields import Schema, TEXT,KEYWORD, ID, STORED
from whoosh.analysis import StemmingAnalyzer
from whoosh import index


#filenameTestset = 'qrels-covid_d5_j4.5-5.txt'

#Gaat goed tot 70000
#amountFiles =  70000


'''
Arguments: text (String), filename (String)

== //////// ==
Appends text to file with name [filename]
== //////// ==

Returns: Nothing
'''
def write_output(text, filename):
    with open(filename,"a") as f:
        f.write(text)

'''
Arguments: None

== //////// ==
Defines Whoosh schema
== //////// ==

Returns: schema (Whoosh Schema)
'''

def define_schema():
    schema = Schema(id=ID(stored=True),
                    title=TEXT(stored=True), 
                    abstract=TEXT(),
                    abstractH = TEXT(analyzer=StemmingAnalyzer()),
                    body=TEXT(analyzer=StemmingAnalyzer()),
                    bodyH = TEXT(analyzer=StemmingAnalyzer()),
                    introduction = TEXT(analyzer=StemmingAnalyzer()),
                    introductionH = TEXT(analyzer=StemmingAnalyzer()),
                    methods = TEXT(analyzer=StemmingAnalyzer()),
                    methodsH = TEXT(analyzer=StemmingAnalyzer()),
                    results = TEXT(analyzer=StemmingAnalyzer()),
                    resultsH = TEXT(analyzer=StemmingAnalyzer()),
                    discussion = TEXT(analyzer=StemmingAnalyzer()),
                    discussionH = TEXT(analyzer=StemmingAnalyzer()),
                    allFields = TEXT(analyzer=StemmingAnalyzer())
    )
    return schema


'''
Arguments: file (JSON), fields (List), level (Integer), section (String)

== //////// ==
(Summarized) Layout [file]:

{ doc_id : " "
  metadata : {
                title: <title>
                authors: {..}

             }
  abstract:  [
                {  
                    text: <text>
                    cite_spans:  [...]
                    ref_spans: [..]
                    section: 'abstract'
                } ,
                ...
             ] 
  body_text: [
                {  
                    text: <text>
                    cite_spans:  [...]
                    ref_spans: [..]
                    section: <section>
                } ,
                ...
             ] 
}


In here <section> can be for instance 'introduction', or 'methods', etc.

Based on level, extract right information (plain text)) of a parsed document [file] 
  -- Level 0: Extract information of a field on top level of JSON (e.g. 'doc_id')
  -- Level 1: Extract information of a field on first level of JSON (e.g. 'title')
  -- Level 2: Extract information of a specific section on first level of JSON (e.g. 'abstract')
  -- Level 3: Extract information of a specific section on second level of JSON (e.g. 'introduction')
== //////// ==

Returns: res (String)
''' 
def appendText(file,fields,level,section,):   
    res = ""                               
    if(level == 0):
        res = file[fields[0]]
    elif(level == 1):
        try:
            res =   file[fields[0]][fields[1]]
        except:
            res = ""
    elif(level == 2):
        try:
            for paragraph in file[section]:
                try:        
                    res += paragraph["text"]
                except:
                    continue       
        except:
            res = ""
    else:
        for paragraph in file["body_text"]:
            if(paragraph["section"].lower()== section):
                try:
                    res += paragraph["text"]
                except:
                    continue
    return res      



'''
Arguments: schmea (Whoosh Schema)

== //////// ==
Creates new directory 'indexdir' if not present
Creates Whoosh indexer, based on [schema]
== //////// ==

Returns: ix (Whoosh Indexer)
'''

def create_index(schema):
    if not os.path.exists("indexdir"):
        os.mkdir("indexdir")

    #Creating index object
    if (index.exists_in("indexdir")):
        ix = index.open_dir("indexdir")
    else:
        ix = index.create_in("indexdir", schema)
    return ix

'''
Arguments: ix (Whoosh indexer), pathnames (List), amountFiles (Integer)

== //////// ==
Creates writer and add [amountFiles] documents to the writer
Commits writer.
== //////// ==

Returns: Nothing
'''

def index_files(ix, pathnames, amountFiles):
    writer = ix.writer()
    amount = 0
    
    #Calculated averages for fields with heuristics approach
    avgpercAbstract = 0.1034
    avgpercIntroduction=  0.1950
    avgpercMethods = 0.1643
    avgpercResults = 0.1975
    avgpercDiscussion = 0.3417



    #Add documents to indexWriter
    acc = 0
    for path in range(0,amountFiles):#pathnames:
        f = open( pathnames[path] , "r" , encoding='utf-8')   

        #Initialize variables
        file = json.load(f)
        fileAbstract = ""
        fileBody = ""         
        fileID = "unknown"
        fileTitle = "unknown"         
        fileAllFields = ""      
        fileMethods = ""
        fileResults = ""
        fileDiscussion = ""

        #Instantitate document id
        fileID = appendText(file,["paper_id"],0,"")

        #Instantiate title
        fileTitle = appendText(file,["metadata","title"],1,"" )
                    
        #Instantiate abstract            
        fileAbstract = appendText(file, [],2, "abstract") 

        #Instantiate body
        fileBody = appendText(file, [], 2, "body_text")

        #Instantiate introduction
        fileIntroduction = appendText(file, [], 3, "introduction")


        #Instantiate methods
        fileMethods = appendText(file, [], 3, "methods")

        #Instantiate results
        fileResults = appendText(file, [],3,"results")

        #Instantiate discussion
        fileDiscussion = appendText(file, [],3,"discussion")                           

        #Instatiate all text (all fields)               
        fileAllFields = fileTitle + fileAbstract + fileBody           

        #Use average percentage fields to apply heuristics
        allWords = fileAllFields.split()
        lenWords = len(allWords)

        amWordsAbstract = avgpercAbstract * lenWords
        startIndAbstract = 0

        amWordsIntroduction =  avgpercIntroduction * lenWords   
        startIndIntroduction = round(amWordsAbstract) + startIndAbstract   
        
        amWordsMethods = avgpercMethods * lenWords                
        startIndMethods = round(amWordsIntroduction)+ startIndIntroduction

        amWordsResults = avgpercResults * lenWords
        startIndResults = round(amWordsMethods) + startIndMethods

        amWordsDiscussion = avgpercDiscussion * lenWords
        startIndDiscussion = round(amWordsResults) + startIndResults

        amWordsResults = avgpercResults * lenWords
        startIndResults = round(amWordsMethods) + startIndMethods

        amWordsDiscussion = avgpercDiscussion * lenWords
        startIndDiscussion = round(amWordsResults) + startIndResults

        fileAbstractH = ' '.join(allWords[0:startIndIntroduction] )
        fileIntroductionH = ' '.join(allWords[startIndIntroduction:startIndMethods])            
        fileMethodsH = ' '.join(allWords[startIndMethods:startIndResults])
        fileResultsH = ' '.join(allWords[startIndResults:startIndDiscussion])               
        fileDiscussionH = ' '.join(allWords[startIndDiscussion:lenWords])
        
        try:         
            writer.add_document(id = fileID,
                                abstract = fileAbstract,
                                abstractH = fileAbstractH,
                                title = fileTitle,
                                body= fileBody,
                                introduction = fileIntroduction,
                                introductionH = fileIntroductionH,
                                methods = fileMethods,
                                methodsH = fileMethodsH,      
                                results = fileResults,    
                                resultsH = fileResultsH,           
                                discussion = fileDiscussion,  
                                discussionH = fileDiscussionH, 
                                allFields = fileAllFields)

            amount += 1
            if(amount  % 10000 == 0):
                write_output("\nAdded {} documents\n".format(str(amount)), "outputIndexer.txt")
   
        except:
            acc += 1
            continue

        f.close()   
    
    writer.commit()

    write_output("\nFailed to add {} documents\n".format(str(acc)), "outputIndexer.txt")



'''
Arguments: directory (String)

== //////// ==
Retrieve all filepaths under the basedirectory [directory]
== //////// ==

Returns : pahts (List)
'''
def get_all_filepaths(directory):
  '''
  A helper function to get all absolute file paths in a directory (recursively)
  :param directory:  The directory for which we want to get all file paths
  :return         :  A list of all absolute file paths as strings
  '''
  for dirpath,_,filenames in os.walk(directory):
    for f in sorted(filenames):
      yield os.path.abspath(os.path.join(dirpath, f))

                                                                                                                        


def main():

    #Empty output file
    with open('outputIndexer.txt',"w") as f:
        f.write('')
    
    #Get pathnames for parsed documents
    baseDir = 'CORD-19/document_parses/pdf_json'
    pathnames = list(get_all_filepaths(baseDir))
    
    #Count total parsed documents
    totalFiles = len(pathnames)
    write_output("There are {} documents\n".format(str(totalFiles)),"outputIndexer.txt")

    #Define schema and create index
    schema = define_schema()
    ix = create_index(schema)
    
    #Index documents and keep track of time
    stringStartTime = "\nStarting indexing documents at: " + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + "\n"
    write_output(stringStartTime, "outputIndexer.txt")

    if (args.af == 'all'):
        index_files(ix,pathnames, int(totalFiles))
    else:
        index_files(ix,pathnames, int(args.af))


    stringStopTime = "\nDone with indexing documents at: " + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + "\n"
    write_output(stringStopTime, "outputIndexer.txt")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-af', help = "Amount of files to be indexed.")
    args = parser.parse_args()
    
    main()

# python3 indexer.py -af 'all'