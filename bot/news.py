""" NEWS FUNCTIONS """

import requests as r
from bs4 import BeautifulSoup


def get_news_st():
    # Get Text
    website = r.get('http://www.straitstimes.com/container/custom-landing-page/breaking-news')
    website_text = website.text

    # Parse HTML using BS
    soup = BeautifulSoup(website_text, 'html.parser')

    # Find all Headlines
    headlines = soup.findAll('span', {'class' : 'story-headline'})
    time_lines = soup.findAll('div', {'class' : 'node-postdate'})

    count_ = 0
    final_text = "<b>Top Singapore Headlines</b> \n\n"
    
    # Loop Through Headlines!
    for headline in headlines[:5]:
        final_text += "<a href='" + "http://www.straitstimes.com" + headline.a['href'] + "'>"
        final_text += "<b>" + headline.get_text()[1:] + "</b> </a>"
        final_text += "\n" + time_lines[count_].get_text()
        count_ += 1
    return final_text