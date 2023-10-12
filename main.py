from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains import LLMChain
from langchain.llms import LlamaCpp
from langchain.prompts import PromptTemplate
from llama_cpp import LlamaGrammar

from getch import getch

one_line = LlamaGrammar.from_string('root ::= [a-zA-Z\'",.;:!? ]+ "\n"', verbose=False)

header = """
The following is a thrilling text adventure game set in a sci-fi universe. It starts with <BEGIN> tag.
You are a dungeon master that leads the players through the story step by step.
Give detailed descriptions of the current environment and situation. Don't leave things vague.
Never fast forward in time without the player explicitly asking for it.
Every action happens in real time.

<BEGIN>
"""

start_text = """
Location: A dimly lit room.
The soft, ambient hum of machinery fills the air. Mysterious symbols on a nearby control panel catch your attention.
As you collect your thoughts, your hand brushes against a cold, metallic device in your pocket—it emits a faint, pulsating light.
Your journey into the unknown begins.

> Look around

"""

llm = LlamaCpp(
    model_path="/mnt/Meteor/models/llm/mythomax-l2-13b.q5_K_M.gguf",
    temperature=0.75,
    max_tokens=256,
    top_p=1.15,
    repeat_penalty=1.15,
    n_gpu_layers=44,
    n_ctx=4096,
    verbose=False,
    # streaming=True,
    # echo=True,
)


class PromptManager:
    def __str__(self):
        return self.text

    def __init__(self, prt=""):
        assert isinstance(prt, str)
        self.text = prt

    def add(self, text):
        assert isinstance(text, str)
        self.text += text
        print(text, end="")

    def set(self, text):
        assert isinstance(text, str)
        self.text = text

    def get(self):
        return self.text


def gen_options(prompt):
    options = []
    prompt.add("\nWhat would you like to do?\n\n")
    for i in range(1, 5):
        prompt.add(f"{i}.")
        result = llm(prompt.get(), grammar=one_line)
        prompt.add(result)
        options.append(result[1:-1])
    return options


def mytho_compress(text):
    for _ in range(5):
        compress = (
            f"### Instruction:\nSummarize the following story in a few paragraphs.\n"
            f"{text}"
            f"\n### Response:\nCertainly. Here's the summary of the story in a few paragraphs:\n\nYou"
        )

        result = "You" + llm(compress)
        rlen = llm.get_num_tokens(result)

        # Repeat until something hopefully sensible is generated
        if rlen > 5:
            break

    return result


previous_choices = []
checkpoint = 0
prompt = PromptManager(header + start_text)
print(prompt, end="")
while True:
    start_prompt = prompt.get()
    prompt.add(llm(start_prompt, grammar=one_line))

    checkpoint = prompt.get()
    options = gen_options(prompt)
    prompt.set(checkpoint)

    num_tokens = llm.get_num_tokens(prompt.get())
    print(f"\n({num_tokens}) > ", end="")
    prompt.text += "\n> "

    # Read user choice
    while (choice := getch()) not in "123459cq":
        pass

    if choice == "q":
        print("-----")
        print(prompt.get())
        break

    if choice == "5":
        prompt.add(input("5. ") + "\n\n")

    if choice in "4321":
        prompt.add(options[int(choice) - 1] + "\n\n")

    if choice == "9":
        print("(REGEN)\n")
        prompt.set(start_prompt)

    if choice == "c":
        print("(SUMMARY)\n")
        print(mytho_compress(prompt.get()))
        print("-----\n")
        prompt.set(start_prompt)
