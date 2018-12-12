"""
BBC_news.py

Retrieves the headlines from the 'https://www.bbc.co.uk/news/world' site and allows
the retreival of an article's full text.
"""

from lxml import html
import lxml
from textwrap import wrap
import requests
import sys
import os

class BBCNewsReader:

    def __init__(self):
        self.bbc_html = 'https://www.bbc.co.uk/news/world.html'
        self.bbc_page = requests.get(self.bbc_html)
        self.bbc_tree = html.fromstring(self.bbc_page.content)
        self.headlines = self.get_article_headlines()
        self.article_links = self.load_article_links()

    def get_article_headlines(self):
        """load the headlines for the articles"""

        # 'buzzard' article
        bbc_main_article_xpath = self.bbc_tree.xpath('//div[@class="buzzard-item"]//span[@class="title-link__title-text"]/text()')

        # 'pigeon' articles
        bbc_pigeon_article_xpaths = self.bbc_tree.xpath('//div[@class="pigeon"]//span[@class="title-link__title-text"]/text()')

        # 'macaw articles'
        bbc_macaw_article_xpaths = self.bbc_tree.xpath('//div[@class="macaw"]//span[@class="title-link__title-text"]/text()')

        # BBC article headlines
        bbc_headlines = bbc_main_article_xpath + bbc_pigeon_article_xpaths + bbc_macaw_article_xpaths

        # Add all headlines from the various news sources (at present only BBC)
        all_headlines = bbc_headlines # + others

        # Return all the headlines
        return all_headlines


    def load_article_links(self):
        """load the xpaths for the article headline links. Text hyperlink
            is extracted and reformatted into single strings which contain the
            article URL. The list of URLs is returned."""

        # main article links
        main_bbc_article_links = self.bbc_tree.xpath('//div[@class="buzzard-item"]//a[@class="title-link"]/@href')

        # 'pigeon' articles
        bbc_pigeon_article_links = self.bbc_tree.xpath('//div[@class="pigeon"]//a[@class="title-link"]/@href')

        # 'macaw articles'
        bbc_macaw_article_links = self.bbc_tree.xpath('//div[@class="macaw"]//a[@class="title-link"]/@href')

        # Extract the url ending e.g. the "/business/123456789" at the end of a BBC article URL
        bbc_article_links = main_bbc_article_links + bbc_pigeon_article_links + bbc_macaw_article_links

        # Reformat the BBC article links
        bbc_links = ["{}{}".format('https://www.bbc.co.uk',link) for link in bbc_article_links]

        # Add all the links from the various news sources (at present only BBC) 
        all_article_links = bbc_links # + others

        # return a list of full article URLs
        return all_article_links

    def print_headlines(self):
        """Prints each article's headline text. Takes a list of headlines (strings) as an argument."""

        # Opening line
        print("News Headlines.\n")

        # Loop through headlines list and prints out the string along with its index + 1
        for i, headline in enumerate(self.headlines):
            print("{}: {}".format((i+1),headline))

    def continue_reading(self):
        """Checks whether the user wants to continue reading. Returns a boolean."""
        # TO DO - handle spelling mistakes / invalid input better

        # Get user's answer and make it all lower case
        answer = input("\nContinue reading? Y/N: ").lower()

        # Check whether the user wants to continue or not
        if answer == 'y' or answer == 'yes':
            return True
        elif answer == 'n' or answer == 'no':
            return False

    def get_article_choice(self):
        """Gets and returns the article number the user wants to read."""
        # Intialise the article variable
        article = 0

        # Loop until a valid integer input has been received
        while article == 0:
            article = input("\nWhich article do you want to read?: ")
            try:
                article = int(article)
            except ValueError:
                print("\nOops! That's not a valid choice.")
                # Reset the article variable to ensure we stay in the while loop
                article = 0

        return article - 1

    def load_new_tree(self, article):
        """Create and return a new html tree based on the article chosen by the user."""

        article_html = self.article_links[article]
        new_page = requests.get(article_html)
        new_tree = html.fromstring(new_page.content)
        return new_tree

    def get_story(self, tree, index):
        """Returns the whole article text."""

        # Gets all of the articles paragraphs. 
        story_inner_paras = tree.xpath('//div[@class="story-body__inner"]//p')

        # Initalise and set the main body as the headline of the article.
        article_body = "{}\n".format(self.headlines[index])

        # Loops through all of the paragraphs and formats them via textwrap module
        # to wrap around after 80 characters. All of the lines in the paragraph
        # are then appended to the article_body string.
        for para in story_inner_paras:
            formatted_para = wrap(para.text_content(), 80)
            for line in formatted_para:
                article_body = "{}\n{}".format(article_body, line)

            # append a new line at the end of each paragraph.
            article_body = "{}\n".format(article_body)

        return article_body

