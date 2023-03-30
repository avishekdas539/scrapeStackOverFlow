from scrapeStackOverFlow.utils import *
import os
import time
import random
import warnings

warnings.filterwarnings("ignore")


class Scrape:
    def __init__(self, startpage : int = 1, endpage : int = 1, tab : str ='newest', save_output : bool = False, 
                 save_path : str = os.getcwd()+"Output.txt", print_result : bool = False) -> None:
        """
        startpage : int => From which page scrapping should start.
        endpage : int => On which page scrapping should end.
        tab : str => ''votes, 'frequent', 'unanswered', 'newest', 'bounties', 'active'.
        save_output : bool => True for saving the file, False for not saving.
        save_path : str | path => Path with filename to save the output as text file.
        print_result : bool => True to print the links scrapped and number of answers found. False will print nothing.
        """
        self.startpage = startpage
        self.endpage = endpage
        self.tab = tab
        self.save_path = save_path
        self.save_output = save_output
        self.print_result = print_result
        
    def scrape(self):
        """
        This method will return a list of dictionaries. The structure of the dictionaries will be,
        {"question" : ".................",
        "answers" : ["answer1", "answer2,....],
        "tags" : ["tag1", "tag2", .......]}
        """
        startpage = self.startpage
        endpage = self.endpage
        QAList : list[dict] = []
        for npage in range(startpage, endpage+1):
            hyperlinks = getHyperLinksOnBasePage(npage, tab = self.tab)
            if self.print_result:
                print("---------------------------------------------------------------------------------------")
                print("Page", npage)
                print("Questions", len(hyperlinks))
                print(link)
                print("---------------------------------------------------------------------------------------")
            for link in hyperlinks:
                QAoutput = getQuestionAns(link)
                if QAoutput!={}:
                    QAList.append(QAoutput)
                    if self.print_result:
                        print('Answers found',len(QAoutput['answers']))
                else:
                    if self.print_result:
                        print("No answers found")
                waittime = random.randint(1,7)
                time.sleep(waittime)
        if self.save_output:
            with open(self.save_path, 'w', encoding='utf-8') as f:
                for entry in QAList:
                    f.write(str(entry))
                    f.write(",\n")
        return QAList
    