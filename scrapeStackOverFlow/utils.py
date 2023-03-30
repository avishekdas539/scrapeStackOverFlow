import requests
from bs4 import BeautifulSoup
import bs4
import warnings

warnings.filterwarnings("ignore")




def extractText(required_texts):
    extracted_text = ""
    for tag in required_texts:
        child_content = tag.contents
        for content in child_content:
            # print(type(content))
            if type(content)==bs4.element.NavigableString:
                extracted_text += content
            else:
                extracted_text += content.text
    return extracted_text
    
    
def getQuestionAns(link):
    response = requests.get(link)
    QAsoup = BeautifulSoup(response.text, 'html')
    QAdivs = QAsoup.find_all('div', {'class': 's-prose js-post-body'})
    if len(QAdivs)==0:
        return {}
    output = {}
    required_texts = QAdivs[0].find_all(['p', 'code', 'a'])
    output['question'] = extractText(required_texts)
    anslist = []
    for i in range(1,len(QAdivs)):
        required_texts = QAdivs[i].find_all(['p', 'code', 'a'])
        anslist.append(extractText(required_texts))
    output['answers'] = anslist
    tags = QAsoup.find_all('li', {'class':"d-inline mr4 js-post-tag-list-item"})
    output['tags'] = [tag.text for tag in tags]
    # print("Answers:", len(QAdivs)-1)
    return output


def getUrl(baseurl, page, tab='newest'):
    return f'{baseurl}?tab={tab}&page={page}'


def getHyperLinksOnBasePage(npage, tab='frequent'):
    url = getUrl("https://stackoverflow.com/questions", page=npage, tab=tab)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html')
    question_anchors = soup.select('.s-link:not([class*=" "])')
    link_extensions = [q.get('href') for q in question_anchors]
    links = ['https://stackoverflow.com/'+anslink for anslink in link_extensions]
    return links

