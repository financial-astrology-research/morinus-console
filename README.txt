ABOUT MORINUS
=============

Morinus is a free astrological program written in Python and developed by multiples contributors, the original project pages are:

- https://sites.google.com/site/pymorinus/Home
- https://sites.google.com/site/tradmorinus/morinus
- https://sourceforge.net/projects/morinus/files

There is no centralized repository that manages official releases, code repository and workflow, also I was not able to find who was the original creator of the project but I hope we can join efforts to create an easier to use API which could be refactored, tested and documented.

The first purpose of this repository is to create a Morinus Console version that allow to do astrological calculations from command line, for that goal I will remove all graphical UI dependent logic and refactor the functionality that I need in reusable services and commands by leveraging lot of that logic on https://github.com/sdispater/cleo API.

DEPENDENCIES
============

In order to be able to use Python Extension to the Swiss Ephemeris you need to install https://github.com/astrorigin/pyswisseph

- pip3 install pyswisseph

If you are using MacOS will need to install wxpython package:

- brew install wxpython
