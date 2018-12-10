"""
BBC_news_headlines.py

This gets theheadlines from the bbc/news/world site and prints
them to the console. The user can select an article to get the read the full text.
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
        """load the xpaths for the six articles"""

        # 'buzzard' article
        self.main_article_xpath = self.bbc_tree.xpath('//div[@class="buzzard-item"]//span[@class="title-link__title-text"]/text()')

        # 'pigeon' articles
        self.pigeon_article_xpaths = self.bbc_tree.xpath('//div[@class="pigeon"]//span[@class="title-link__title-text"]/text()')

        # 'macaw articles'
        self.macaw_article_xpaths = self.bbc_tree.xpath('//div[@class="macaw"]//span[@class="title-link__title-text"]/text()')

        return self.main_article_xpath + self.pigeon_article_xpaths + self.macaw_article_xpaths


    def load_article_links(self):
        """load the xpaths for the six article headline links. Text hyperlink
            is extracted and reformatted into single strings which contain the
            article URL. The list of URLs is returned."""

        # main article links
        self.main_article_links = self.bbc_tree.xpath('//div[@class="buzzard-item"]//a[@class="title-link"]/@href')

        # 'pigeon' articles
        self.pigeon_article_links = self.bbc_tree.xpath('//div[@class="pigeon"]//a[@class="title-link"]/@href')

        # 'macaw articles'
        self.macaw_article_links = self.bbc_tree.xpath('//div[@class="macaw"]//a[@class="title-link"]/@href')

        # Extract the url ending e.g. the "/business/123456789" at the end of an article URL
        article_links = self.main_article_links + self.pigeon_article_links + self.macaw_article_links

        # Reformat and return a list of full article URLs
        return ["{}{}".format('https://www.bbc.co.uk',link) for link in article_links]

    def print_headlines(self):
        """Prints each article's headline text. Takes a list of headlines (strings) as an argument."""

        # Opening line
        print("BBC World News Headlines.\n")

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
        """Create a new html tree based on the article chosen by the user."""

        article_html = self.article_links[article]
        new_page = requests.get(article_html)
        new_tree = html.fromstring(new_page.content)
        return new_tree

    def print_story(self, tree):
        """Prints the whole article text."""

        # Gets all of the articles paragraphs
        story_inner_paras = tree.xpath('//div[@class="story-body__inner"]//p')

        # Loops through all of the paragraphs and formats them via textwrap module
        # to wrap around after 100 characters. All of the paragraphs are then printed.
        print("\n")
        for para in story_inner_paras:
            formatted_para = wrap(para.text_content(), 100)
            for line in formatted_para:
                print(line)
            print("\n")

    def read_news(self):
        """The main application. This gets and shows the current headlinesself.
            The code steps into a while loop which allows the user to choose
            the next article to read and displays the full text. This loop
            continues until the user chooses to not continue reading."""

        # Print headlines
        self.print_headlines()

        # Intialise the article_read to allow screen clearing and headline printing
        # to occur at the correct time within the main loop.
        articles_read = 0

        # Loop until the user chooses not to continue reading.
        while self.continue_reading():
            # Check the number of articles read and clear the console
            # before reprinting the headlines.
            if articles_read > 0:
                # Clear the console.
                os.system('cls')
                self.print_headlines(headlines)

            # Get the article index value.
            article = self.get_article_choice()

            # Construct the new html tree based on the user's chosen article.
            new_tree = self.load_new_tree(article)

            # Print the full article.
            self.print_story(new_tree)

            # increaase the number of articles read by 1.
            articles_read += 1

        # The user has finished reading, so close the application.
        sys.exit()

# Create an instance of BBCNewsReader.
BBC = BBCNewsReader()

# Get informed!
BBC.read_news()
