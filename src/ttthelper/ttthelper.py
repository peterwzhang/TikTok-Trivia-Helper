import bs4
import pyautogui
import pytesseract
import requests
import time

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

    def print(self):
        print(f'Question {self._number}: {self._question}')
        for i, a in enumerate(self._answers, 1):
            print(f'{i}. {a}')

    def print_json(self):
        pass # TODO: implement this



def detect_color(x, y, color):
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


def gen_google_search(q):
    search_url = f'{GOOGLE_SEARCH_URL}{q.get_question()} \
    "{q.get_answer(0)}" OR "{q.get_answer(1)}" OR "{q.get_answer(2)}"'
    search_url = search_url.replace(" ", "+")
    return search_url


def make_google_soup(url):
    r = requests.get(url)
    r.raise_for_status()
    return bs4.BeautifulSoup(r.text, 'html.parser')


def count_answers(soup, answers):
    results = dict.fromkeys(answers, 0)
    items = soup.find_all('div')
    for item in items:
        #  print(i)
        for i in range(3):
            text = item.get_text().lower()
            if answers[i].lower() in text:
                results[answers[i]] += 1
    return results


def run():
    q_list = []
    print('waiting for question...\n')
    while True:
        if detect_color(*TIMER_POSITION, TIMER_COLOR):
            img = get_game_img(QUESTION_REGION)
            screen_text = get_text(img)
            q = get_question(screen_text, len(q_list) + 1)
            search = gen_google_search(q)
            soup = make_google_soup(search)
            results = count_answers(soup, q.get_answers())
            q.print()
            print(results)
            print('waiting for question...\n')
            q_list.append(q)
            time.sleep(QUESTION_TIME)
        else:
            time.sleep(CHECK_SECONDS)

def main():
    run()

if __name__ == "__main__":
    main()
