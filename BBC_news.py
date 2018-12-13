""" BBC_news.py

Retrieves the headlines from the 'https://www.bbc.co.uk/news/world' site and
allows the retrieval of an article's full text.
"""

import requests
from lxml import html
from textwrap import wrap

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
    """Scrapes the BBC world news site to get the headlines and article text.

    Methods:
    get_article_headlines = returns a list of article headlines
    load_article_links = returns the list of article URLs
    load_new_tree = returns the html tree for an article's main body
    get_story = returns a string containing the whole of the article text.

    Instance Variables:
    bbc_html = BBC world news html url
    bbc_page = BBC world news page
    bbc_tree = html tree for the world news page
    headlines = a list of all headlines in the BUZZARD, PIGEON and MACAW classes
    article_links = a list of article URLs

    Scrap the headline data to obtain a list of headlines from the BUZZARD,
    PIGEON and MACAW classes on the BBC World News website. Determine the
    articles' URLs to allow the main body of text to be extracted and stored as
    a single string. 
    """

    def __init__(self):
        """Initalise the instance variables.

        Load html, page and html tree variables and then get the headlines and
        the article links.
        """
        self.bbc_html = 'https://www.bbc.co.uk/news/world.html'
        self.bbc_page = requests.get(self.bbc_html)
        self.bbc_tree = html.fromstring(self.bbc_page.content)
        self.headlines = self.get_article_headlines()
        self.article_links = self.load_article_links()

    def get_article_headlines(self):
        """Load the headlines of the articles from the BBC page."""

        # 'buzzard' article headline
        main_title = self.bbc_tree.xpath('{}{}/text()'.format(BUZZARD,TITLE))

        # 'pigeon' article headlines
        pigeon_titles = self.bbc_tree.xpath('{}{}/text()'.format(PIGEON,TITLE))

        # 'macaw' article headlines
        macaw_titles = self.bbc_tree.xpath('{}{}/text()'.format(MACAW,TITLE))

        # Return all the headlines
        return main_title + pigeon_titles + macaw_titles

    def load_article_links(self):
        """Returns a list containing article complete URLs.

        Load the xpaths for each article headline links. The hyperlink
        is extracted and reformatted into single strings which contain the
        article URL. The list of URLs is returned.
        """
        # main article links
        main_link = self.bbc_tree.xpath('{}{}/@href'.format(BUZZARD,A))

        # 'pigeon' articles
        pigeon_links = self.bbc_tree.xpath('{}{}/@href'.format(PIGEON,A))

        # 'macaw articles'
        macaw_links = self.bbc_tree.xpath('{}{}/@href'.format(MACAW,A))

        # All links
        links = main_link + pigeon_links + macaw_links

        # Return the reformated article links
        return ["{}{}".format('https://www.bbc.co.uk', link) for link in links]

    def load_new_tree(self, article_index):
        """Gets the html tree for the inputted news article.

        Keyword arguments:
        article -- article index

        Get the correct article URL from the article_links list and then request
        the article page and return its html tree.
        """
        article_html = self.article_links[article_index]
        new_page = requests.get(article_html)
        new_tree = html.fromstring(new_page.content)
        return new_tree

    def get_story(self, tree, headline_index):
        """Returns the whole article text as a single string.

        Keyword arguments:
        tree = html tree for the article main body.
        headline_index = position of the headline chosen by the user.

        Get every paragraph within the article html story-body tree. Loop
        through each element in the tree, textwrap at 80 characters, loop
        through each line in the newly wrapped paragraph and append to a blank
        article body string.
        """

        # Gets all of the articles paragraphs.
        story_inner_paras = tree.xpath('//div[@class="story-body__inner"]//p')

        # Initalise and set the main body as the headline of the article.
        article_body = "{}\n".format(self.headlines[headline_index])

        # Loops through all of the paragraphs and formats them via textwrap
        # module to wrap around after 80 characters. All of the lines in the
        # paragraph are then appended to the article_body string.
        for para in story_inner_paras:
            formatted_para=wrap(para.text_content(), 80)
            for line in formatted_para:
                article_body="{}\n{}".format(article_body, line)

            # Append a new line at the end of each paragraph to the current
            # article body string.
            article_body="{}\n".format(article_body)

        return article_body
