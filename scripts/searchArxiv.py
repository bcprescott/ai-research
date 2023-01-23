import arxiv
import re
import os
import time
import argparse
from sys import platform
from datetime import datetime, timedelta

# Determines if a path argument is indeed a path
def dir_path(string):
    if os.path.isdir(string):
        return string
    else:
        raise NotADirectoryError(string)

# Argument parser function with some defaults in case YOLO
def parse_opt(known=False):
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--titlequery', type=str, default='ai' , help='string to query for in paper titles')
    parser.add_argument('-a', '--abstractquery', type=str, default='ai' , help='string to query for in paper abstract')
    parser.add_argument('-c', '--papercount', type=int, default=5 , help='maximum number of ArXiV papers you want to return')
    parser.add_argument('-p', '--savepath', type=dir_path, default=os.getcwd(), help = 'path you want to save papers to')
    return parser.parse_known_args()[0] if known else parser.parse_args()

# Queries arXiv and returns the results generator object 
def queryArxiv(numarticles, titlequery, abstractquery):
    '''
    
    numarticles: number of articles you want the query to return

    titlequery: what space-separated words you want to find in a paper's title

    abstractquery: same as above, just within the paper abstract 
    
    '''
    search = arxiv.Search(
        query = "ti:{} AND abs:{} AND cat:cs.CV OR cat:cs.AI OR cs.LG".format(titlequery, abstractquery),
        max_results = numarticles,
        sort_by = arxiv.SortCriterion.SubmittedDate,
        sort_order = arxiv.SortOrder.Descending
    )
    return search.results()

# Uses the result of queryArxiv to run a cleaner "review" of the papers, then optional download
def downloadPapers(results):
    papers = iter(results)
    while True:
        try:
            p = next(papers)
            pd = p.published.strftime("%Y/%m/%d")
            cd = (datetime.today() - timedelta(weeks=24)).strftime("%Y/%m/%d")
            if pd >= cd:
                print('\n')
                print("Title: {}".format(p.title))
                print('\n')
                print("Published Date: {}".format(pd))
                print('\n')
                print("----------------------------- ABSTRACT -----------------------------")
                print('\n')
                print(p.summary,'\n\n')
                response = input("Would you like to download this paper? (y/n):")
                while response not in ('y','n'):
                    response = input("Would you like to download this paper? (y/n):")
                if response == 'y':
                    dl = p.download_pdf(dirpath=opt.savepath)
                    print('\n','-----------------------------','\n',
                        'Paper downloaded to: {}'.format(opt.savepath),'\n',
                        'File name: {}'.format(str(dl).split('\\')[-1]),
                        '\n','-----------------------------','\n')
                    input("Press any button to continue...")
                if platform == "win32":
                    os.system("cls")
                else:
                    os.system("clear")
        except:
            break


if __name__ == "__main__":
    opt = parse_opt()
    os.system("cls")
    returnedPapers = queryArxiv(opt.papercount, opt.titlequery, opt.abstractquery)
    downloadPapers(returnedPapers)