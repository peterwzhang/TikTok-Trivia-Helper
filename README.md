# TikTok Trivia Helper

This is a program that attempts to find the answers for TikTok Trivia questions using Google and OpenAI's GPT-3. **As of 02/24/23 it has answered all questions correctly (6/6 games).**

If you're in need of a TikTok Trivia referral code, you can use mine: <https://www.tiktok.com/t/ZTRnuPRKt/> or CI69079018.

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
3. Create a venv: `$ python3 -m venv ./venv`
4. (Optional) Open `./venv/bin/activate` and add `export OPENAI_API_KEY=PASTE YOUR API KEY HERE` to the end of the file
5. Activate venv: `$ source ./venv/bin/activate`
6. Install requirements: `$ pip install -r requirements.txt`
7. Take a screenshot of your your entire screen while a trivia question is being shown with the green timer bar. You will need this to change some values in `ttthelper.py`.
    - For `TIMER_POSITION` pick any coordinate (x, y) near the center of the timer.
    - For `QUESTION_REGION` get the coordinate (x,y) of the top-left, width, height of the question and answer box. Then use this format (x, y, width, height)
8. Run TikTok Trivia Helper: `$ python3 ./src/ttthelper.py`
   - To stop the program, press `Ctrl + C` in the terminal

## Preview

<img width="563" alt="image" src="https://user-images.githubusercontent.com/46033793/221343274-bb62b2e5-5cab-4418-9972-662bb3859bc4.png">


## Contributing

If you would like to contribute, please create/find an issue then assign yourself and link a pull request to the issue.

If you have any suggestions you can create an issue also.

## License

[MIT license](./LICENSE.md)
