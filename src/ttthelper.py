import bs4
import concurrent.futures
import pyautogui
import pytesseract
import requests
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


class Question:
    def __init__(self, q='', a=[], num=0):
        self._question = q
        self._answers = a
        self._number = num

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
        # for i, a in enumerate(self._answers, 1):
        #     print(f'{i}. {a}')

    def get_gpt_prompt(self):
        return f'{self._question} (pick from the {len(self._answers)} options)\n{self.format_answers()}\nAnswer:'

    def print_json(self):
        pass  # TODO: implement this


def detect_color(color, x, y):
    # (390, 570)
    # (125, 249, 175, 255)
    return pyautogui.pixelMatchesColor(x, y, color, 5)


def get_game_img(img_region):
    # (75,675, 650, 650)
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


def count_answers(soup: bs4.BeautifulSoup, answers):
    results = dict.fromkeys(answers, 0)
    items = soup.find_all('div')
    for item in items:
        #  print(i)
        for i in range(3):
            text = item.get_text().lower()
            if answers[i].lower() in text:
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


def run():
    q_list = []
    print('waiting for question...\n')
    while True:
        if detect_color(TIMER_COLOR, *TIMER_POSITION):
            img = get_game_img(QUESTION_REGION)
            screen_text = get_text(img)
            question = get_question(screen_text, len(q_list) + 1)
            question.print()
            if openai.api_key:
                get_all_answers(question)
            else:
                results = get_answer_counts(question)
                print(f'Google results: {results}')
            print('\nwaiting for question...\n')
            q_list.append(question)
            time.sleep(QUESTION_TIME)
        else:
            time.sleep(CHECK_SECONDS)


def main():
    run()


if __name__ == "__main__":
    main()
