from datetime import datetime
import argparse
import xml.etree.ElementTree as et
import csv, itertools
import os, os.path
from whoosh.qparser import MultifieldParser
from whoosh import scoring
from whoosh.query import Variations
from whoosh import index
import numpy as np

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
Arguments: filename (String)

== //////// ==
Reads a csv file with name [filename]
Makes dictionary, which matches the doc_id to the cord_uid (if possible).


conversionDict = {
  'doc_id' : <cord_id>,
  'doc_id2': <cord_id>,
  ...
}

== //////// ==
Returns: conversionDict (Dictionary)

'''

def make_conversionDict(filename):
    conversionDict = {}
    acc = 0
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            acc +=1
            conversionDict[row['sha']] = row['cord_uid']
    return conversionDict, acc

'''
Arguments: filename (String)

== //////// ==
Makes a dictionary of used topics (and corresponding queries)
in TREC round 5

topicsDictionary = 
{
   <topic_id1> = {'query':  <query>, 'question': <question> , 'narrative': <narravtive>},
   <topic_id2> = {'query':  <query>, 'question': <question> , 'narrative': <narravtive>},
   ...
}
== //////// ==

Returns: topicsDictionary (Dictionary)
'''
def make_topicDictionary(filenameTopicset):
    root = et.parse(filenameTopicset).getroot()
    topicsDictionary = {}
    for topicel in root:
        topic_id= topicel.attrib['number']
        topicsDictionary[topic_id] = {}
        for subel in topicel:
          topicsDictionary[topic_id][subel.tag] = subel.text
    return topicsDictionary
 
'''
Arguments: None

== //////// ==
  Opens index created in 'indexer.py'.
  If 'indexer.py' has not been run before, this function returns an error.
== //////// ==

Returns: Nothing
'''
def open_index():
  try:
    ix = index.open_dir("indexdir")
    return ix
  except:
    write_output("\nThere is no folder called 'indexdir'!\n", 'outputSearcher.txt')
  
'''
Arguments: ix (Whoosh indexer), topicsDictionary (Dictionary), conversionDictionary (Dictionary), parm_grid (Array)

== //////// ==
Search through indexed documents for each topic in [topicdDictionary].

Search uses three fields:
  1) Title
  2) Abstract
  3) Introduction
  4) Methods
  5) Results
  6) Discussion
Weights for these fields are given in this order in [param_grid].
Query is parsed with use of variations.

Converts result to the right input for 'trec_eval.exe'.
Writes search output to 'results.test'
== //////// ==

Returns: Nothing
'''
def fieldusage3(ix, topicsDictionary, conversionDictionary, param_grid):
  if(param_grid == []):
    param_grid.append([1.0,1.0,1.0, 1.0,1.0,1.0])
    param_grid = np.array(param_grid)

  stringStartTime = "\nStart with gridsearch F3 at: " + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + "\n"
  write_output(stringStartTime, "outputSearcher.txt")  
  write_output("\nThe shape of param_grid F3 is {}\n".format(str(param_grid.shape)),"outputSearcher.txt")
  
  for weights in range(0,len(param_grid)):
    write_output("Now processing weights {}\n".format(param_grid[weights]),"outputSearcher.txt")
    #Initiating weights
    weightTitle, weightAbstractH, weightIntroductionH, weightMethodsH, weightResultsH, weightDiscussionH  = param_grid[weights][0], param_grid[weights][1],  param_grid[weights][2],  param_grid[weights][3],  param_grid[weights][4],  param_grid[weights][5]
    w = scoring.BM25F(B=0.75,  K1=1.2,title_B = weightTitle , introductionH_B = weightIntroductionH, methodsH_B= weightMethodsH, resultsH_B = weightResultsH, discussionH_B = weightDiscussionH, abstractH_B=weightAbstractH)

    script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
    rel_path = "outputF3/resultsF3{}_{}_{}_{}_{}_{}].test".format(str(weightTitle), str(weightAbstractH),str(weightIntroductionH), str(weightMethodsH), str(weightResultsH), str(weightDiscussionH))
    abs_file_path = os.path.join(script_dir, rel_path)  
    
    with open(abs_file_path,"a") as f:
      for topic_id in range(1,len(topicsDictionary)+1 ):
        #Inititate parser
        qp = MultifieldParser(["title","abstractH", "introductionH", "methodsH", "resultsH","discussionH" ], schema=ix.schema, termclass=Variations)
        query = topicsDictionary[str(topic_id)]["query"]
        parsedQuery = qp.parse(query)

        #Searcher uses AND function for each query term in text
        with ix.searcher(weighting=w) as searcher:
            results = searcher.search(parsedQuery, limit=1000)
            topicID = str(topic_id)
            for hit in results:
                doc_id = hit["id"]
                try:
                    cord_uid = conversionDictionary[doc_id]
                except:
                #write_output("Conversion from doc_id {} failed!\n".format(doc_id), "outputSearcher.txt") 
                    cord_uid = -1
                    pass
            
                rank = hit.rank
                score = hit.score
            
                #Add hit to results
                if(cord_uid != -1):
                    f.write(topicID + "\t" + "Q0" +  "\t"+ cord_uid + "\t" + str(rank) + "\t" +  str(score) + "\t"  + "STANDARD" +  "\n")

      
def main():
    #Empty output file
    with open('outputSearcher.txt',"w") as f:
        f.write('')
    #Empty results file
    with open('results.test', "w") as f:
        f.write('')
    #Make folders for results per field usage
    if not os.path.exists("outputF1"):
        os.mkdir("outputF1")
    
    topicsDictionary = make_topicDictionary("topics-rnd5.xml")
    conversionDictionary, amountRows = make_conversionDict("metadata.csv")
    write_output("\nThere are {} rows in the metadata.\n".format(amountRows), "outputSearcher.txt")
    
    ix = open_index()
    
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# CHANGE DEPENDING ON WHAT FIELDUSAGE FUNCTION                                                #
    twoOptions = [0.25,1.0]
    param_grid = []
    for wt in twoOptions:#np.arange(0,ev,d):
      for wa in  twoOptions:#np.arange(0,ev,d):
        for wi in  twoOptions:#np.arange(0,ev,d):
          for wm in  twoOptions:#np.arange(0,ev,d):
            for wr in twoOptions: #np.arange(0,ev,d):
              for wd in twoOptions: #np.arange(0,ev,d):
                param_grid.append([wt,wa,wi,wm,wr,wd])
    
    param_grid = np.array(param_grid)

    fieldusage3(ix, topicsDictionary, conversionDictionary, param_grid)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #  
    #python3 searcher.py 
main()