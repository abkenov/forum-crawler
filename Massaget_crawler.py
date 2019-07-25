import random
import requests
from bs4 import BeautifulSoup as bs

def get_Proxy():
	proxies = #list of proxies

	proxies = proxies.split("\n")
	
	proxyDict = { 
			  "http"  : 'http://' + random.choice(proxies), 
			  "https" : 'https://' + random.choice(proxies)
			}
	
	return proxyDict

def get_soup_text(url, header):
	response = requests.get(url, headers=headers)
	if response.ok:
		return bs(response.text)

if __name__ == "__main__":
	
	headers = {
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Windows Chromium/75.0.3770.90 Chrome/75.0.3770.90 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Referer': 'https://massaget.kz/',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9',
}

url = 'https://massaget.kz/forum/'

soup_forum_list = get_soup_text(url, headers).select('#page-body div.forabg a.forumtitle')

for room_link in soup_forum_list:
    soup_room_list = get_soup_text(url + room_link['href'][2:], headers)
    
    try:
        room_forumtitles = soup_room_list.select('#page-body div.forabg a.forumtitle')
        room_topictitles = soup_room_list.select('#page-body div.forumbg a.topictitle')
    except:
        continue
    
    for forumtitle_link in room_forumtitles:
        try:
            pages = get_soup_text(url + forumtitle_link['href'][2:], headers).select('#content div.topic-actions span a')
        except:
            continue
            
        pages = pages[:int(len(pages)/2)]
        pages = [forumtitle_link] + pages
        
        for page in pages:
            try:
                soup_page = get_soup_text(url + page['href'][2:], headers).select('#page-body div.forumbg a.topictitle')
            except:
                continue
            
            for topic_link in soup_page:
                try:
                    topic_text_result = get_soup_text(url + topic_link['href'][2:], headers).select('#page-body div.content')
                except:
                    continue
                
                for i in range(len(topic_text_result)):
                    print(topic_text_result[i].text)
                    with open('text/forum_text.txt', mode='a') as textfile:
                        textfile.write(topic_text_result[i].text)
                        
    
    pages = get_soup_text(url + room_link['href'][2:], headers).select('#content div.topic-actions span a')
    pages = pages[:int(len(pages)/2)]
    pages = [room_link] + pages
    
    for page in pages:
        try:
            topic_list = get_soup_text(url + page['href'][2:], headers).select('#page-body div.forumbg a.topictitle')
        except:
            continue
        
        for topic in topic_list:
            try:
                topic_text_result = get_soup_text(url + topic['href'][2:], headers).select('#page-body div.content')
            except:
                continue
            for i in range(len(topic_text_result)):
                print(topic_text_result[i].text)
                with open('text/forum_text.txt', mode='a') as textfile:
                    textfile.write(topic_text_result[i].text)