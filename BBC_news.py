"""
BBC_news.py

Retrieves the headlines from the 'https://www.bbc.co.uk/news/world' site and
allows the retreival of an article's full text.
"""

from lxml import html
import lxml
from textwrap import wrap
import requests
import sys
import os

# Define the div class xpath from the BBC website. Buzzard is the main article,
# Pigeon is the second tier and Macaw is the third tier.
BUZZARD = '//div[@class="buzzard-item"]'
PIGEON = '//div[@class="pigeon"]'
MACAW = '//div[@class="macaw"]'

# String to find the related article headline text. To be appended to the above.
TITLE = '//span[@class="title-link__title-text"]'

# String to find hyperlink to the article's page and therefore the full text.
A = '//a[@class="title-link"]'


class BBCNewsReader:

    def __init__(self):
        self.bbc_html='https://www.bbc.co.uk/news/world.html'
        self.bbc_page=requests.get(self.bbc_html)
        self.bbc_tree=html.fromstring(self.bbc_page.content)
        self.headlines=self.get_article_headlines()
        self.article_links=self.load_article_links()

    def get_article_headlines(self):
        """load the headlines for the articles"""
        # 'buzzard' article headline
        main_headline=self.bbc_tree.xpath('{}{}/text()'.format(BUZZARD,TITLE))

        # 'pigeon' article headlines
        pigeon_headlines=self.bbc_tree.xpath('{}{}/text()'.format(PIGEON,TITLE))

        # 'macaw' article headlines
        macaw_headlines=self.bbc_tree.xpath('{}{}/text()'.format(MACAW,TITLE))

        # Return all the headlines
        return main_headline+pigeon_headlines+macaw_headlines


    def load_article_links(self):
        """load the xpaths for the article headline links. Text hyperlink
            is extracted and reformatted into single strings which contain the
            article URL. The list of URLs is returned."""
        # main article links
        main_link=self.bbc_tree.xpath('{}{}/@href'.format(BUZZARD,A))

        # 'pigeon' articles
        pigeon_links=self.bbc_tree.xpath('{}{}/@href'.format(PIGEON,A))

        # 'macaw articles'
        macaw_links=self.bbc_tree.xpath('{}{}/@href'.format(MACAW,A))

        # All links
        links=main_link+pigeon_links+macaw_links

        # Return the reformated article links
        return ["{}{}".format('https://www.bbc.co.uk',link) for link in links]

    def load_new_tree(self, article):
        """Create and return a new html tree based on the article chosen by
            the user."""
        article_html=self.article_links[article]
        new_page=requests.get(article_html)
        new_tree=html.fromstring(new_page.content)
        return new_tree

    def get_story(self, tree, index):
        """Returns the whole article text."""
        # Gets all of the articles paragraphs.
        story_inner_paras=tree.xpath('//div[@class="story-body__inner"]//p')

        # Initalise and set the main body as the headline of the article.
        article_body="{}\n".format(self.headlines[index])

        # Loops through all of the paragraphs and formats them via textwrap
        # module to wrap around after 80 characters. All of the lines in the
        # paragraph are then appended to the article_body string.
        for para in story_inner_paras:
            formatted_para=wrap(para.text_content(), 80)
            for line in formatted_para:
                article_body="{}\n{}".format(article_body, line)

            # append a new line at the end of each paragraph.
            article_body="{}\n".format(article_body)

        return article_body
