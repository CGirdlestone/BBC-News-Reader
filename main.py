"""
main.py

This will run the BBC News Reader app and implement the GUI.
"""

from BBC_gui import *
from BBC_news import *

# Create an instance of the application.
app = Application(BBCNewsReader())

# Run the app.
if __name__ == "__main__":
    app.mainloop()
