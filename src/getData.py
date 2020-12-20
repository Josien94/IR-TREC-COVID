import argparse
import wget, tarfile, os

def wget_file(url):
    wget.download(url)

def main():
    #Download document JSONs from amazon using https://ai2-semanticscholar-cord-19.s3-us-west-2.amazonaws.com/<date_iso_str>/<file_name>
    urlDocumentParser = 'https://ai2-semanticscholar-cord-19.s3-us-west-2.amazonaws.com/2020-07-16/document_parses.tar.gz'
    wget.download(urlDocumentParser)

    #Download document metadata from amazon using https://ai2-semanticscholar-cord-19.s3-us-west-2.amazonaws.com/<date_iso_str>/<file_name>
    urlMetadata = 'https://ai2-semanticscholar-cord-19.s3-us-west-2.amazonaws.com/2020-07-16/metadata.csv'
    wget.download(urlMetadata)

    #Extract tar files document JSONs
    tar = tarfile.open(filenameDocumentParser, "r:gz")
    tar.extractall('CORD-19')
    tar.close()

    #Import test file data
    urlTestset = 'https://ir.nist.gov/covidSubmit/data/qrels-covid_d5_j4.5-5.txt'
    wget.download(urlTestset)



if __name__ == '__main__':

    main()
