# TikTok Trivia Helper

This is a program that attempts to find the answers for TikTok Trivia questions using Google and OpenAI's ChatGPT. It also supports sending results to a Discord webhook.

**As of 02/24/23 it has answered all non-video questions correctly (6/6 games).**


## Setup

In order to setup TikTok Trivia Helper you need the following:

- [Python3](https://www.python.org/downloads/) (Tested with Python 3.9.6)
- [Tesseract](https://tesseract-ocr.github.io/tessdoc/Installation.html)
- (Optional) [OpenAI API Token](https://platform.openai.com/account/api-keys)
- A way to display TikTok on your computer such as [QuickTime Player](https://support.apple.com/downloads/quicktime), [Bluestacks](https://www.bluestacks.com/)

Note: if you do not have an OpenAPI Token the helper will still work with Google without any changes.

Once you have the items listed above, follow these instructions below.

### macOS Instructions

1. Clone the repo: `$ git clone https://github.com/peterwzhang/TikTok-Trivia-Helper.git`
2. Enter the newly created directory `$ cd TikTok-Trivia-Helper`
3. Create a venv: `$ python -m venv ./venv`
4. (Optional) Open `./venv/bin/activate` and add `export OPENAI_API_KEY=PASTE YOUR API KEY HERE` to the end of the file
5. (Optional) in the same file as step 4 add `export DISC_WEBHK_URL=PASTE YOUR DISCORD WEBHOOK URL HERE`
6. Activate venv: `$ source ./venv/bin/activate`
7. Install requirements: `$ pip install -r requirements.txt`
8. Take a screenshot of your entire primary screen while a trivia question is being shown with the green timer progress bar. You will need this to change some values in `ttthelper.py`.
    - For `TIMER_POSITION` pick any coordinate (x, y) near the center of the timer.
    - For `TIMER_COLOR` get the (R, G, B, 255) values at the point for `TIMER_POSITION`
    - For `QUESTION_REGION` get the coordinate (x,y) of the top-left, width, height of the question and answer box. Then use this format (x, y, width, height)
9. Run TikTok Trivia Helper: `$ python -m src.ttthelper`
   - To stop the program, press `Ctrl + C` in the terminal

### Windows Instructions

1. Clone the repo: `$ git clone https://github.com/peterwzhang/TikTok-Trivia-Helper.git`
2. Enter the newly created directory `$ cd TikTok-Trivia-Helper`
3. Create a venv: `$ python -m venv ./venv`
4. (Optional) Open `./venv/Scripts/Activate.ps1` and add `$env:OPENAI_API_KEY = 'PASTE YOUR API KEY HERE'` to the end of the file
5. (Optional) in the same file as step 4 add `$env:DISC_WEBHK_URL='PASTE YOUR DISCORD WEBHOOK URL HERE'`
6. Activate venv: `$ ./venv/Scripts/Activate.ps1`
7. Install requirements: `$ pip install -r requirements.txt`
8. Take a screenshot of your entire primary screen while a trivia question is being shown with the green timer progress bar. You will need this to change some values in `ttthelper.py`.
    - For `TIMER_POSITION` pick any coordinate (x, y) near the center of the timer.
    - For `TIMER_COLOR` get the (R, G, B, 255) values at the point for `TIMER_POSITION`
    - For `QUESTION_REGION` get the coordinate (x,y) of the top-left, width, height of the question and answer box. Then use this format (x, y, width, height)
9. Run TikTok Trivia Helper: `$ python -m src.ttthelper`
   - To stop the program, press `Ctrl + C` in the terminal

## Preview

![embed picture](https://user-images.githubusercontent.com/46033793/221461825-d6627438-7d0d-4de5-9326-191b42d7dbde.png)

<img width="563" alt="terminal display" src="https://user-images.githubusercontent.com/46033793/221343274-bb62b2e5-5cab-4418-9972-662bb3859bc4.png">

## Contributing

If you would like to contribute, please create/find an issue then assign yourself and link a pull request to the issue.

If you have any suggestions you can create an issue also.

## License

[MIT license](./LICENSE.md)
