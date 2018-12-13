"""
BBC News Reader App

This is the GUI for the BBC news reader app. A window is created to display
the twelve headlines from the BUZZARD, PIGEON and MACAW classes from the BBC
World News page. When an article is selected, a new window opens and shows
the full article text and gives the user the option to save the article text.
"""

import tkinter as tk
from datetime import date

class Application(tk.Frame):
    """Create the GUI for the news reader.

    Methods:
    create_widgets = create all toplevel widgets
    leave = create a quit button
    save_widget = create a save button
    save_article = create a file and save the article text
    headline_buttons = create the headline buttons
    create_article_window = create a new window for the article text
    create_article_widgets = create the new article window widgets
    open_article = open the article to get the text

    Instance Variables:
    root = the main tkinter instance
    news_reader = the news reader class instance
    quit_button = a quit button to close the parent window
    save_button = a save button to save the displayed article text
    headline_buttons = a list of headline buttons
    headline = the headline of the displayed article
    article_body = the full text of the displayed article
    window = a window to display the article text
    article_frame = the frame to hold the article text widget and the scrollbar
    article_scrollbar = the scrollbar for the text widget
    article = the article text widget

    A window containing buttons displaying BBC World News headlines is
    displayed. Clicking on a button will open a second window which displays
    all of the article's text and gives the user the choice to save the full
    text.
    """

    def __init__(self, news_reader):
        """Initialise the instance variables.

        Create the main tkinter instance, set the window title and geometry.
        Load the news_reader and create the toplevel widgets.
        """

        # Initialise main window
        self.root=tk.Tk()
        tk.Frame.__init__(self, self.root)

        # Set main window title and geometry.
        self.root.title("BBC News")
        self.root.geometry('600x400+50+50')

        # Assign the news reader.
        self.news_reader=news_reader
        self.create_widgets()

    def create_widgets(self):
        """Creates the buttons linking to each article and a 'quit' button."""
        self.headline_buttons()
        self.leave(self.root)

    def leave(self, window):
        """Generic 'quit' button to close the active window."""
        self.quit_button=tk.Button(window, text="Quit", command=window.destroy)
        self.quit_button.pack(fill=tk.BOTH, side=tk.BOTTOM)

    def save_widget(self):
        """Save button widget. Calls the 'save_article' method."""
        self.save_button=tk.Button(self.window, text="Save", command=lambda:self.save_article())
        self.save_button.pack(fill=tk.BOTH, side=tk.TOP)

    def save_article(self):
        """Saves the current article as a text file.

        The current date is obtained and a filename is constructed of the form
        YYYYMMDD-headline where all single and double quotes are stripped from
        the headline. A new file created with this filename and the text of the
        article is written along with the date the article was saved.
        """
        # Set today's date
        today=str(date.today())

        # Strip any double or single quotes from the headlines
        self.headline.strip(["'",'"'])

        # Create a file with filename 'YYYYMMDD-headline'.
        filename='{}-{}.txt'.format(today.replace('-',''),self.headline)

        # Write the date and article to the file.
        with open(filename,'a+') as f:
            f.write('Date saved: {}\n'.format(today))
            f.write(self.article_body)

    def headline_buttons(self):
        """Create buttons for each headline.

        Each button is given the command to open the headline's article.
        """
        # Create the headline buttons. 'headline = headline' is used to ensure
        # the button refers to the correct headline and not only the final one.
        self.buttons=([tk.Button(self.root, text=headline,
                command=lambda headline=headline: self.open_article(headline))
                for headline in self.news_reader.headlines])

        # Loop through the buttons and pack them.
        for button in self.buttons:
            button.pack(fill=tk.BOTH, expand=1, padx=2, pady=2)

    def create_article_window(self, headline):
        """Creates a new window and frame for the text widget and scrollbar.

        Keyword arguments:
        headline = the string containing the article headline.
        """
        # Assign the headline - used in the save_article method
        self.headline=headline

        # Create new toplevel window
        self.window=tk.Toplevel(self.root)
        self.window.title(headline)

        # Create a frame which will house the text and scrollbar widgets.
        self.article_frame=tk.Frame(self.window)
        self.article_frame.pack(fill=tk.BOTH, side=tk.TOP)

    def create_article_widgets(self, article_body):
        """Creates the widgets required in the article window.

        Keyword arguments:
        article_body = the string containing the whole article text.
        """
        # Creates the scrollbar widget in the article frame.
        self.article_scrollbar=tk.Scrollbar(self.article_frame)
        self.article_scrollbar.pack(fill=tk.Y, side=tk.RIGHT)

        # Create the text widget and insert the article text. Configure the text
        # widget so its y-value reflects that of the scrollbar.
        self.article=tk.Text(self.article_frame)
        self.article.insert(1.0, article_body)
        self.article.pack(fill=tk.BOTH, expand=1, padx=10, pady=10)
        self.article.config(yscrollcommand=self.article_scrollbar.set)

        # Configure the scrollbar to update the article's y position
        self.article_scrollbar.config(command=self.article.yview)

        # Create save and quit widgets
        self.save_widget()
        self.leave(self.window)

    def open_article(self, article_headline):
        """Gets the body of text for the article.

        Keyword arguments:
        article_headline = article headline string

        The index of the article headline is used to get the new html tree which
        is then used to get the full article text. A new article window and
        the associated widgets are then created.
        """
        # loop through the headlines until the correct article is found, then
        # get the new html tree and get the main body of text for the correct
        # article.
        for i, headline in enumerate(self.news_reader.headlines):
            if headline == article_headline:
                new_tree=self.news_reader.load_new_tree(i)
                self.article_body=self.news_reader.get_story(new_tree, i)

        # Create an article window.
        self.create_article_window(article_headline)

        # Create all article window widgets.
        self.create_article_widgets(self.article_body)
