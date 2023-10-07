from getch import getch
from llm import llm
from rewrite import mytho_compress

one_line = 'root ::= [a-zA-Z\'",.;:!? ]+ "\n"'
header = """
The following is a text adventure game. It starts with <BEGIN> tag.
After which there's a detailed description of the current environment and situation.
You can type in any text you want after ">", and the game will try to act as a dungeon master based on it.
The game contains various interesting locations, creatures and characters, which you can interact with.

<BEGIN>
"""


def choose(options):
    a = " "
    while a not in "123459c":
        a = getch()
        if a == "q":
            return ("QUIT", None)

    if a == "5":
        res = ("INPUT", input("5. "))
    elif a == "4" or a == "3" or a == "2" or a == "1":
        res = ("INPUT", options[int(a) - 1])
    elif a == "9":
        res = ("REGEN", None)
    elif a == "c":
        res = ("SUMMARY", None)
    else:
        res = ("ERROR", None)

    return res


class Runner:
    def __init__(self, initial_prompt):
        self.prompt = initial_prompt
        self.spent_context = 0

    def _genjson(self, grm, stop=""):
        return {
            "prompt": self.prompt,
            "n_predict": 256,
            "stop": stop,
            "ignore_eos": False,
            "mirostat": 2,
            "mirostat_tau": 8.0,
            "mirostat_eta": 1.0,
            "grammar": grm,
        }

    def add(self, text, hide=False):
        self.prompt += text
        if not hide:
            print(text, end="")

    def rewind(self, location):
        if location >= len(self.prompt):
            return
        count = len(self.prompt) - location
        self.prompt = self.prompt[:-count]
        print("\b" * count, end="")

    def location(self):
        return len(self.prompt)

    def generate(self, grm):
        (result, result_info) = llm(self._genjson(grm))
        self.spent_context = result_info["tokens_cached"]
        self.add(result)
        return result

    def gen_options(self):
        options = []
        self.add("\nWhat would you like to do?\n\n")
        for i in range(1, 5):
            self.add(f"{i}.")
            result = self.generate(one_line)
            options.append(result[1:-1])
        return options


previous_choices = []
total_story = [
    "You wake up dizzy, not quite sure what is going on. Your head hurts and you feel like you've been unconscious for a long time.\n"
]


def build_story():
    return header + "\n".join(total_story)


checkpoint = 0
runner = Runner(build_story())
while True:
    start_prompt = runner.prompt
    inner_story_piece = runner.generate(one_line)
    total_story.append(inner_story_piece)

    # try with or without this
    # runner.prompt = build_story()

    checkpoint = runner.location()
    options = runner.gen_options()
    runner.rewind(checkpoint)

    print(f"\n({runner.spent_context}) > ", end="")
    runner.add("\n> ", hide=True)

    (event, value) = choose(options)
    if event == "QUIT":
        print("---------------------")
        print(runner.prompt)
        break

    if event == "INPUT":
        runner.add(value + "\n\n")

    if event == "REGEN":
        print("(REGEN)\n")
        total_story.pop()
        runner.prompt = start_prompt

    if event == "SUMMARY":
        print("(SUMMARY)\n")
        mytho_compress(runner.prompt)
        print("-----\n")
        total_story.pop()
        runner.prompt = start_prompt
