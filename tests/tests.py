from src.ttthelper import Question, get_gpt3_ans, get_answer_counts
TEST_QUESTIONS = [Question("Which organization did John Wick work for before he retired?", ["United Nations", "CIA", "The Tarasov Mob"], 1),

                  Question("In which sport could you achieve a hole in one?", [
                           "Rowing", "Archery", "Golf"], 2),

                  Question("Which singer is nicknamed J.Lo?", [
                           "Jennifer Hudson", "Jennifer Lopez", "Jennifer Aniston"], 3),

                  Question("Which 'doctor' wrote a famous book about a cat in a hat?", [
                      "Seuss", "Strauss", "Stein"], 4),

                  Question("Which of these companies in the U.S. had the biggest revenue in 2022?", [
                      "Walgreens", "Target", "Walmart"], 5),

                  Question("Which of the following book and film characters was created by Ian Fleming?", [
                      "James Bond", "Oliver Twist", "Harry Potter"], 6),

                  Question("In which decade was Dubble Bubble gum created?",
                           ["1920s", "1890s", "1940s"], 7),

                  Question("Which famous boy band features Nick, Kevin, AJ, Brian, and Howie?", [
                      "*NSYNC", "Backstreet Boys", "One Direction"], 8),

                  Question("Which US city is home to the HQ of the Coca-Cola company?",
                           ["Charleston", "Atlanta", "Charlotte"], 9),

                  Question("Who wrote about Frodo, Gandalf and Aragorn?", [
                      "Jules Verne", "Dan Brown", "JRR Tolkien"], 10),

                  Question("What does the U stand for in URL?", [
                      "Understanding", "Uniform", "United"], 11),

                  Question("Which planet is also the name of a song by Frankie Avalon?", ["Mercury", "Venus", "Jupiter"], 12)]


def test_google():
    for q in TEST_QUESTIONS:
        q.print()
        print(f'Google results: {get_answer_counts(q)}\n')


def test_gpt():
    for q in TEST_QUESTIONS:
        q.print()
        print(f'GPT3 Answer:{get_gpt3_ans(q)}\n')

def main():
    test_google()

if __name__ == "__main__":
    main()
