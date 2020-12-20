import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import os
import re

def makeparam(stringpaths):
    paramgrid = []
    for path in stringpaths:
        weight1 = float(path[0]+"."+path[1])
        weight2 = float(path[2]+"."+path[3])
        weight3 = float(path[4]+"."+path[5])
        weight4 = float(path[6]+"."+path[7])
        weight5 = float(path[8]+"."+path[9])
        weight6 = float(path[10]+"."+path[11])
        paramgrid.append([weight1,weight2,weight3,weight4,weight5,weight6])

    return np.array(paramgrid)

def get_allfilepaths(directory):
  '''
  A helper function to get all absolute file paths in a directory (recursively)
  :param directory:  The directory for which we want to get all file paths
  :return         :  A list of all absolute file paths as strings
  '''
  for dirpath, _ , filenames in os.walk(directory):
    for f in sorted(filenames):
      yield os.path.abspath(os.path.join(dirpath, f))
def get_all_filepaths(directory):
  '''
  A helper function to get all absolute file paths in a directory (recursively)
  :param directory:  The directory for which we want to get all file paths
  :return         :  A list of all absolute file paths as strings
  '''
  for dirpath,_,filenames in os.walk(directory):
    for f in sorted(filenames):
      yield os.path.abspath(os.path.join(dirpath, f))

'''
Arguments: field (string), title (string), xlabel (string)

Makes a plot of the results P_15 results of trec_eval.
Note that assumed here that results are place under output{field}.


Returns: Nothing
'''

def make_plot(field, title, xlabel):
  pathnames = get_all_filepaths("Output{}/".format(field)) #change this for other Fs

  stringpaths = [] # grid entries
  ps = [] # p_15 values for each grid entry
  for path in pathnames:
      restring = "results{}".format(field)
      pathsplit = re.split(restring,path)[1] #change this for other Fs
      allnumbers =re.findall(r'\d+',pathsplit)
      stringpaths.append(allnumbers)
      with open (path) as f:
          content = f.read()
          rows = re.split('\n', content)
          for row in rows:
              values = re.split('\t',row)
              if(re.search("P_15", values[0])):
                  ps.append(values[2])
  stringpaths = makeparam(stringpaths)


  fig = plt.figure()
  data = [str(i) for i in stringpaths]
  map(str, data)
  y_pos = np.arange(len(data))
  ps2 = [float(i) for i in ps]


  plt.bar(y_pos, ps2, align='center', alpha=0.5)
  plt.xticks(y_pos, data, rotation="vertical")
  print(max(ps2))
  plt.ylim(min(ps2), 0.22)
  plt.ylabel('P_15')
  plt.xlabel(xlabel)
  plt.title(title)
  plt.show()

make_plot("F1","precision BM25F with three fields","weight vector ( title, abstract, body )")
make_plot("F2","precision BM25F with six (non-heuristic) fields","weight vector ( title, abstract, introduction, method, results, discussion )")
make_plot("F3","precision BM25F with six heuristic)fields","weight vector ( title, abstract, introduction, method, results, discussion )")
  