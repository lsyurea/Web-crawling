import requests
from bs4 import BeautifulSoup
import os

BASE_URL = "https://www.economist.com"
ARTICLES_PER_PAGE = 10

COUNT = 0

# PARSED = False

def get_article_list(session, page):
    response = session.get(BASE_URL + f"/latest/?page={page}")
    # print(response.status_code)
    article_list = []
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        sections = soup.find_all('section')
        # print(sections)

        for section in sections:
            article = section.find('a')

            # print(article)

            if article:
                article_dict = {
                    'title': article.string,
                    'url': article['href']
                }
                article_list.append(article_dict)
    return article_list

def get_article_content(session, url):

    # global PARSED

    try:
        response = session.get(url)
        
        if response.status_code == 200:
            # print(f"Processing [{url}]...")

            # if not PARSED:
            #     print(response.content)
            #     PARSED = True

            soup = BeautifulSoup(response.content, 'html.parser') 

            # article = soup.find('article')
            # if article:
            #     content = article.get_text()
            #     return content
            content = soup.get_text()
            if content:
                return content
            else:
                print("No article found")
        else:
            print(f"Error getting article [{url}]: {response.status_code}")

            
            
    except requests.exceptions.RequestException as e:
        print("error occurred: ", str(e))

def save_article(title, content):

    filename = f"minedData/{title}.doc"
    filename = os.path.join(os.path.dirname(__file__), filename)
    filename = filename.replace('?', '')
    if os.path.exists(filename):
        print(f"File [{filename}] already exists. Skipping...")
        return
    print(f"Saving article [{title}]...")
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(f"{title}\n\n{content}")

def main():
    session = requests.Session()
    session.headers.update({'User-Agent': 'Mozilla/5.0'})
    session.javascript = False

    global COUNT

    start_page = 1
    end_page = 100
    for page in range(start_page, end_page + 1):
        article_list = get_article_list(session, page)
        # print(article_list)

        for article in article_list:
            COUNT += 1
            title = article['title']
            url = BASE_URL + article['url']
            print(url)

            if (title == None or url == None) or title == 'Advertisement' or title == 'podcast':
                continue

            # print(title, url)

            content = get_article_content(session, url)
            if content:
                save_article(str(COUNT) + ' : ' + title, content)

if __name__ == '__main__':
    print("starting web crawler...")
    main()
