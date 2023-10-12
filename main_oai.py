# from langchain.llms import LlamaCpp
# from llama_cpp import LlamaGrammar
import os

from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains import LLMChain

from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate

from getch import getch

# one_line = LlamaGrammar.from_string('root ::= [a-zA-Z\'",.;:!? ]+ "\n"', verbose=False)

start_text = """
You wake up in a dimly lit room.
The soft, ambient hum of machinery fills the air. Mysterious symbols on a nearby control panel catch your attention.
As you collect your thoughts, your hand brushes against a cold, metallic device in your pocket—it emits a faint, pulsating light.
Your journey into the unknown begins.

> Look around

"""

llm_story = PromptTemplate.from_template("""
The following is a thrilling text adventure game set in a sci-fi universe.
The game begins after the <BEGIN> tag.
You are a dungeon master that leads the players through the story step by step.
Give detailed descriptions of the current environment and situation. Don't leave things vague.
Player input happens after the ">" symbol.

<BEGIN>
{story}
""") | ChatOpenAI(model_kwargs={"stop": [">"]})

llm_options = PromptTemplate.from_template("""
The text starting after <BEGIN> tag, is a thrilling text adventure game set in a sci-fi universe.
You are a dungeon master that leads the players through the story step by step.
Player input happens after the ">" symbol.
Give the player four numbered options on what to do next.
Make each option unique and interesting.

<BEGIN>
{story}
""") | ChatOpenAI()

# llm = ChatOpenAI(model_name="gpt-3.5-turbo", max_tokens=200)


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
    print("(gen_options)")
    prompt.add(llm_options.invoke({"story": prompt.get()}).content.strip())
    omap = {}
    for line in prompt.get().split("\n")[-7:]:
        if len(line) > 5 and line[0] in "1234":
            omap[line[0]] = line[3:]
    options = []
    for i in range(1, 5):
        if str(i) in omap:
            options.append(omap[str(i)])
    assert len(options) > 1
    print(options)
    return options


# def mytho_compress(text):
#     for _ in range(5):
#         compress = (
#             f"### Instruction:\nSummarize the following story in a few paragraphs.\n"
#             f"{text}"
#             f"\n### Response:\nCertainly. Here's the summary of the story in a few paragraphs:\n\nYou"
#         )

#         result = "You" + llm(compress)
#         rlen = llm.get_num_tokens(result)

#         # Repeat until something hopefully sensible is generated
#         if rlen > 5:
#             break

#     return result


previous_choices = []
checkpoint = 0
# prompt = PromptManager(header + start_text)
prompt = PromptManager("")
print(prompt, end="")
while True:
    start_prompt = prompt.get()
    print("(gen story)")
    prompt.add(llm_story.invoke({"story": (start_prompt) + "\n"}).content.strip())

    # checkpoint = prompt.get()
    # options = gen_options(prompt)
    # prompt.set(checkpoint)

    print(f"\n> ", end="")
    prompt.text += "\n\n> "

    # Read user choice
    while (choice := getch()) not in "123459cq":
        pass

    if choice == "q":
        print("-----")
        print(prompt.get())
        break

    if choice == "5":
        prompt.add(input("5. ") + "\n\n")

    # if choice in "4321":
    #     prompt.add(options[int(choice) - 1] + "\n\n")

    if choice == "9":
        print("(REGEN)\n")
        prompt.set(start_prompt)

    # if choice == "c":
    #     # Second half of the context, starting from ">"
    #     pt = start_prompt
    #     ptl = len(pt)
    #     cutoff = ptl // 2 + pt[ptl // 2].find(">")
    #     part_second = pt[cutoff:]
    #     part_first = pt[:cutoff]

    #     print("(SUMMARY)\n")
    #     compressed = mytho_compress(part_first)
    #     prompt.set(compressed + part_second)
    #     print(prompt.get())
    #     print("-----\n")
