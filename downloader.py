from bs4 import BeautifulSoup
import urllib.request

# Gets the relevant content of the article
# @param string page: an html page
def getArticle(url):
    # Class for articles 
    C_ARTICLE = '.entry-content'
    # Class for titles
    C_TITLE = '.entry-title'
    page = getHTML(url)
    
    article = {}
    
    # Add the url to the article
    article['url'] = [url]
    
    # Setup the soup page    
    soup = BeautifulSoup(page)
    # Get the title from the class
    title = soup.select(C_TITLE)
    # Error checking
    if len(title) > 1:
        print("Warning: more than one title found.")
    article['title'] = [title[0].get_text()]
    # Get the div of our interest (note that it returns a list)
    html_content = soup.select(C_ARTICLE)
    # Error checking
    if len(html_content) > 1:
        print("Warning: more than one article found.")
    # Add the text to the article
    article['text'] = []
    article['img'] = []
    article['other'] = []
    
    for div in html_content[0].find_all('div'):
        text = div.get_text()
        if div.span and div.span.a:
            article['text'].append('![img](' + div.span.a.get('href') + ')')
            article['img'].append(div.span.a.get('href'))
        elif text:
            article['text'].append(text)
        else:
            article['other'].append(div.span)
    
    for img in html_content[0].find_all('img'):
        article['text'].append('![img](' + img.get('src') + ')')
        article['img'].append(img.get('src'))
      
    article['html'] = html_content
    # return the so creted article
    return article

def printArticle(article):
    print('Title: ', end='')
    print(article['title'][0], '\n')
    print('Text: ', end='')
    for i in article['text']:
        print(i, '\n')
    print('Img: ', end='')
    for i in article['img']:
        print(i)
    print('Other: ', end='')
    for i in article['other']:
        print(i)
    print('url: ', end='')
    print(article['url'][0])
    print('html: --->')
    print(article['html'][0])
    print('end --->\n\n')

def getMarkdownArticle(article):
    text = '##' + (article['title'][0].lstrip().rstrip()) + '\n'
    for p in article['text']:
        text += p + '\n'
    text += '*[original article](' + article['url'][0] + ')*' + '\n'
    text += '\n\n'
    
    
    return text

# Gets the HTML of a page
# @param string url: the url of the page to download
# @return string: HTML of the page
def getHTML(url):
    # Download the page to parse
    r_file = urllib.request.urlopen(url)
    # Decode the page to parse
    return r_file.read()


# Gets the list of all the month links ordered by date
# @return string list: links of every month
def getArchiveLinks():
    # Class for links
    C_LINK = '.post-count-link'
    # Base url
    url = 'http://onewaytosweden.blogspot.it'
    page = getHTML(url)
    # Setup the soup page
    soup = BeautifulSoup(page)
    # Get the links from the class
    found_links = soup.select(C_LINK)
    link_list = []
    for item in found_links:
        link = item.get('href')
        # Avoid this pages as they contain duplicates
        if link.find('/search?') < 0:
            link_list.append(link)
    link_list.reverse()
    return link_list

# Gets the list of the article links in each month
# @return string list: links of the article of the month
def getArticleLinks(url):
    # Class for titles
    C_TITLE = '.entry-title'
    page = getHTML(url)
    # Setup the soup page
    soup = BeautifulSoup(page)
    # Get the links from the class
    found_links = soup.select(C_TITLE)
    link_list = []
    for item in found_links:
        link = item.a.get('href')
        link_list.append(link)
    link_list.reverse()
    return link_list
    
def main():
    '''
    url = 'http://onewaytosweden.blogspot.it/2015/12/buone-feste.html'
    page = getHTML(url)
    text = getContent(page)
    print(text)
    '''
    
    out_file = open("Output.md", "w")
    
    list_ar = getArchiveLinks()
    for month in list_ar:
        list_month = getArticleLinks(month)
        for i in list_month:
            a = getArticle(i)
            print("Downloaded: " + a['title'][0].lstrip().rstrip())   
            out_file.write(getMarkdownArticle(a))
        print("Completed month: " + month)
    out_file.close()
    print("Finished!")

if __name__ == "__main__":
    main()
