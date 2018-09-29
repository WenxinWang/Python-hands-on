# Python-hands-on applications
Only for studying and learning. 
Please don't use them for commercial activities.
Any questions please contact wenxin.wxw@gmail.com
Start date: 9/28/2018

## 1. Windows App - Would you be my boyfriend
* Date: 9/28/2018
* Features: Let the boy must say "yes" to be your boyfriend. When the mouse is on "refuse" button, the button runs aways.
* Configuration: Windows10, amd64
* Usage:
  * Download pygame package "pygame-1.9.4-cp37-cp37m-win_amd64.whl" from here: https://www.lfd.uci.edu/~gohlke/pythonlibs/#pygame
  * Move the downloaded .whl file to your python37/Scripts directory
  * Enter the command: "pip3 install pygame-1.9.4-cp37-cp37m-win_amd64.whl"
  * Download the picture "me.jpg", music file "love.mp3", and font file"simkai.ttf" 
  * Execute the file by command "py WouldYouBeMyBoyfriend.py"
 * User Interfaces
   * ![UI1 - Beginning](/Would-you-be-my-boyfriend/Pictures/UI1-Beginning.png)
   * ![UI2 - Refuse clicking no](/Would-you-be-my-boyfriend/Pictures/UI2-RefuseClickingNo.png)
   * ![UI3 - Happy ending](/Would-you-be-my-boyfriend/Pictures/UI3-HappyEnding.png)

## 2. APILess - Instagram Crawler
* Date: 9/28/2018
* Feature: This python app crawls photos and videos from Instagram.
* Usage: 
  * 1. $ pip install pyquery [download pyquery](https://pypi.org/project/pyquery/)
  * 2. Use your own "cookies, user-agent, and download path" of the Instragram.com
  * 3. $ python InstagramCrawler.py Instagram_user_name"
