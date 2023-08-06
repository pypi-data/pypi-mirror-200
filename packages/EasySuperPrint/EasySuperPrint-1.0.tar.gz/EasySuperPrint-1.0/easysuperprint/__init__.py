import os, re, json, requests, urllib, urllib3

class COLOURS:
  class BLACK:
    main = '\033[0;30m'
  class DARKGREY:
    main = '\033[1;30m'
  class LIGHTRED:
    main = '\033[1;31m'
  class GREEN:
    main = '\033[0;32m'
  class LIGHTGREEN:
    main = '\033[1;32m'
  class ORANGE:
    main = '\033[0;33m'
  class YELLOW:
    main = '\033[1;33m'
  class BLUE:
    main = '\033[0;34m'
  class LIGHTBLUE:
    main = '\033[1;34m'
  class PURPLE:
    main = '\033[0;35m'
  class LIGHTPURPLE:
    main = '\033[1;35m'
  class CYAN:
    main = '\033[0;36m'
  class LIGHTCYAN:
    main = '\033[1;36m'
  class LIGHTGREY:
    main = '\033[0;37m'
  class WHITE:
    main = '\033[1;37m'
  class RED:
    main = '\033[0;31m'
  class RESET:
    main = '\033[0m'
    
  def get_color(name):
    identifiers = [
    {"color_name": "red", "color": COLOURS.RED.main},
    {"color_name": "black", "color": COLOURS.BLACK.main},
    {"color_name": "darkgrey", "color": COLOURS.DARKGREY.main},
    {"color_name": "lightred", "color": COLOURS.LIGHTRED.main},
    {"color_name": "green", "color": COLOURS.GREEN.main},
    {"color_name": "lightgreen", "color": COLOURS.LIGHTGREEN.main},
    {"color_name": "orange", "color": COLOURS.ORANGE.main},
    {"color_name": "yellow", "color": COLOURS.YELLOW.main},
    {"color_name": "blue", "color": COLOURS.BLUE.main},
    {"color_name": "lightblue", "color": COLOURS.LIGHTBLUE.main},
    {"color_name": "purple", "color": COLOURS.PURPLE.main},
    {"color_name": "lightpurple", "color": COLOURS.LIGHTPURPLE.main},
    {"color_name": "cyan", "color": COLOURS.CYAN.main},
    {"color_name": "lightcyan", "color": COLOURS.LIGHTCYAN.main},
    {"color_name": "lightgrey", "color": COLOURS.LIGHTGREY.main},
    {"color_name": "white", "color": COLOURS.WHITE.main},
    {"color_name": "default", "color": COLOURS.RESET.main}
    ]
    for i in identifiers:
      if i["color_name"] == name.lower():
        return i["color"] # gets the color and returns it
    raise Exception(f"Unknown color name identified as '{name.lower()}'.")

