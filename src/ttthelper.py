import bs4
import concurrent.futures
from datetime import datetime
import json
import pyautogui
import pytesseract
import requests
import signal
import string
import time
import os
import openai
openai.api_key = os.getenv('OPENAI_API_KEY')
GOOGLE_SEARCH_URL = 'https://www.google.com/search?q='
TIMER_POSITION = (390, 575)
TIMER_COLOR = (125, 249, 175, 255)
QUESTION_REGION = (75, 675, 650, 650)
NUM_ANSWERS = 3
QUESTION_TIME = 10
CHECK_SECONDS = 0.5

def sigint_handler(signum, frame):
    global running
    running = False

class Question:
    def __init__(self, q='', a=[], num=0):
        self._number = num
        self._question = q
        self._answers = a

    def set_question(self, q):
        self._question = q

    def set_answer(self, a):
        self._answers = a

    def get_question(self):
        return self._question

    def get_answer(self, i):
        if i < 0 or i >= len(self._answers):
            raise IndexError('Answer Index does not exist')
        return self._answers[i]

    def get_answers(self):
        return self._answers

    def format_answers(self):
        return '\n'.join(f'{i}. {ans}' for i, ans in enumerate(self._answers, 1))

    def print(self):
        print(f'Question {self._number}: {self._question}')
        print(self.format_answers())

    def get_gpt_prompt(self):
        return f'{self._question} (pick from the {len(self._answers)} options)\n{self.format_answers()}\nAnswer:'

    def get_json(self):
        return json.dumps(self.__dict__)


def detect_color(color, x, y):
    return pyautogui.pixelMatchesColor(x, y, color, 5)


def get_game_img(img_region):
    screenshot = pyautogui.screenshot(region=img_region)
    return screenshot


def get_text(im):
    return pytesseract.image_to_string(im)


def get_question(s, num):
    split_s = s.split('\n')
    split_s = list(filter(None, split_s))
    question = ' '.join(split_s[:-3])
    question.replace('"', '')
    answers = split_s[-NUM_ANSWERS:]
    return Question(question, answers, num)


def gen_google_search(q: Question):
    search_url = f'{GOOGLE_SEARCH_URL}{q.get_question()} \
    "{q.get_answer(0)}" OR "{q.get_answer(1)}" OR "{q.get_answer(2)}"'
    search_url = search_url.replace(" ", "+")
    return search_url


def make_google_soup(url):
    r = requests.get(url)
    r.raise_for_status()
    return bs4.BeautifulSoup(r.text, 'lxml')


def rem_punc(input_string):
    return input_string.translate(str.maketrans('', '', string.punctuation))


def count_answers(soup: bs4.BeautifulSoup, answers):
    results = dict.fromkeys(answers, 0)
    items = soup.find_all('div')
    for item in items:
        for i in range(3):
            text = item.get_text().lower()
            text_no_punc = rem_punc(text)
            ans_l = answers[i].lower()
            if ans_l in text or ans_l in text_no_punc:
                results[answers[i]] += 1
    return results


def get_answer_counts(q: Question):
    search = gen_google_search(q)
    soup = make_google_soup(search)
    return count_answers(soup, q.get_answers())


def get_gpt3_ans(q: Question):
    response = openai.Completion.create(
        model="text-davinci-003", prompt=q.get_gpt_prompt(), temperature=0, max_tokens=256, top_p=0.2)
    # print(response)
    return response['choices'][0]['text']


def get_all_answers(q: Question):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        f1 = executor.submit(get_answer_counts, q)
        f2 = executor.submit(get_gpt3_ans, q)

    print(f'Google results: {f1.result()}')
    print(f'GPT3 answer:{f2.result()}')

def log_questions(q_list):
    cur_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_name = f'log_{cur_time}.json'
    dir = 'logs'
    os.makedirs(dir, exist_ok=True)
    with open(f'logs/{log_name}', 'w') as f:
        json.dump([q.get_json() for q in q_list], f, indent=4)
    print(f'\nSaved questions to {dir}/{log_name}')

def run():
    q_list = []
    global running
    running = True
    signal.signal(signal.SIGINT, sigint_handler)
    print('waiting for question...\n')
    while running:
        if detect_color(TIMER_COLOR, *TIMER_POSITION):
            img = get_game_img(QUESTION_REGION)
            screen_text = get_text(img)
            question = get_question(screen_text, len(q_list) + 1)
            question.print()
            if openai.api_key:
                get_all_answers(question)
            else:
                google_results = get_answer_counts(question)
                print(f'Google results: {google_results}')
            print('\nwaiting for question...\n')
            q_list.append(question)
            time.sleep(QUESTION_TIME)
        else:
            time.sleep(CHECK_SECONDS)
    log_questions(q_list)

def main():
    run()


if __name__ == "__main__":
    main()
