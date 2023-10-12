from llm import llm, tokenize


def airo_compress(text):
    compress = (
        f"USER: Summarize the following story in three sentences.\n"
        f"{text}"
        f"\nASSISTANT: Certainly. Here's the summary of the story in three sentences:\n\nYou"
    )

    response = llm(
        {
            "prompt": compress,
            "n_predict": 512,
            "ignore_eos": False,
            # "mirostat": 2,
            # "mirostat_tau": 8.0,
            # "mirostat_eta": 1.0,
        }
    )

    def format_list_entry(entry):
        return (entry[entry.find(".") + 1 :]).replace("\n", "").lstrip("0123456789-*. ")

    print(response[0])
    print(len(tokenize(response[0])))

    # text_output = response[0][response[0].find("\n") :]
    # text_output = "1." + response[0]
    # pieces = [format_list_entry(i) for i in text_output.split("\n") if len(i) > 2]
    # compressed = "\n\n".join(pieces)
    # print(compressed)
    # print(len(tokenize(compressed)))


def mytho_compress(text):
    for _ in range(5):
        compress = (
            f"### Instruction:\nSummarize the following story in a few paragraphs.\n"
            f"{text}"
            f"\n### Response:\nCertainly. Here's the summary of the story in a few paragraphs:\n\nYou"
        )

        response = llm(
            {
                "prompt": compress,
                "n_predict": 512,
                "ignore_eos": False,
                # "mirostat": 2,
                # "mirostat_tau": 8.0,
                # "mirostat_eta": 1.0,
            }
        )

        result = "You" + response[0]
        rlen = len(tokenize(result))
        if rlen > 5:
            break
        print("(llm repeat)")

    print(result)
    return result


if __name__ == "__main__":
    rpg_output = """
    You wake up dizzy, not quite sure what is going on. Your head hurts and you feel like you've been unconscious for a long time. Your surroundings are dimly lit by torches mounted high on the walls of an underground chamber. You sit up slowly, rubbing your eyes. As they adjust to the light, you see that the walls around you are smooth and polished, as if chiseled from solid rock.

    > Look around the room.

    You look around the room. Besides yourself, there is a human skeleton lying on the floor near you. There's also an ornately decorated wooden chest in front of you, its lid open and empty. Your hand feels for your sword but it's not there either!

    > Examine the skeleton.

    You examine the skeleton. It appears to be wearing fine leather armor. A dagger lies nearby, embedded in its ribcage. You notice bloodstains on the floor around the body.

    > Search the skeleton's body for anything useful.

    You search the skeleton's body and find a small pouch containing some gold coins and a key. The key seems to be about six inches long, with teeth carved into its end.

    > Take the key and leave this room.

    You take the key and carefully step out of the room. As you do so, you hear a low rumbling sound coming from somewhere beyond the wall ahead of you.

    > Continue exploring.

    As you start walking down the corridor, torches on either side grow brighter, casting more light upon the smooth granite walls. The noise grows louder and closer until suddenly a section of the wall disintegrates into dust, revealing a vast tunnel beyond.

    > Enter the tunnel.

    You enter the tunnel and see that it descends steeply into darkness. Ahead, you can make out what seems to be a large shadowy shape moving slowly toward you. As you watch, terrified, the light from your torch illuminates the creature more clearly: it's a gigantic spider, at least six feet across!

    > Try to bargain with the spider.

    You try to bargain with the spider but it seems more interested in eating you than striking any deals.

    > Attack the spider.

    You attack the spider but your blow glances off its tough exoskeleton. The creature reacts swiftly, rushing towards you and biting into your arm with its fangs. You feel a sharp sting of pain as it injects poison, numbing your limb.

    > Use magic if available

    You use a spell you learned to create a wall of fire between you and the spider. It screams in pain and retreats momentarily.

    > Attempt to escape

    You attempt to escape but the spider recovers quickly. As it moves towards you again, you notice that its legs are covered with shimmering webs. You realize these must be what made your blow glance off earlier.

    > Attack again, focusing on its legs this time

    You attack again, this time focusing on the spider's legs and managing to sever one of them. The creature recoils from the pain, screeching with fury.

    > Use magic if available

    You use another spell to create a wall of ice around you, ensuring that spider won't get close again. The spider tries desperately to break through but fails.

    > Continue down the tunnel

    You continue down the tunnel, leaving the injured spider behind. As you walk further into the cave, the floor begins to slope upward. At last you reach a fork in the tunnel where two tunnels meet: one leads off to your right and another goes straight ahead. A dim light glows from somewhere up ahead of the left tunnel.
    """

    rpg_output2 = """
    You wake up dizzy, not quite sure what is going on. Your head hurts and you feel like you've been unconscious for a long time. Your surroundings are dimly lit by torches mounted high on the walls of an underground chamber. You sit up slowly, rubbing your eyes. As they adjust to the light, you see that the walls around you are smooth and polished, as if chiseled from solid rock.

    You look around the room. Besides yourself, there is a human skeleton lying on the floor near you. There's also an ornately decorated wooden chest in front of you, its lid open and empty. Your hand feels for your sword but it's not there either!

    You examine the skeleton. It appears to be wearing fine leather armor. A dagger lies nearby, embedded in its ribcage. You notice bloodstains on the floor around the body.

    You search the skeleton's body and find a small pouch containing some gold coins and a key. The key seems to be about six inches long, with teeth carved into its end.

    You take the key and carefully step out of the room. As you do so, you hear a low rumbling sound coming from somewhere beyond the wall ahead of you.

    As you start walking down the corridor, torches on either side grow brighter, casting more light upon the smooth granite walls. The noise grows louder and closer until suddenly a section of the wall disintegrates into dust, revealing a vast tunnel beyond.

    You enter the tunnel and see that it descends steeply into darkness. Ahead, you can make out what seems to be a large shadowy shape moving slowly toward you. As you watch, terrified, the light from your torch illuminates the creature more clearly: it's a gigantic spider, at least six feet across!

    You try to bargain with the spider but it seems more interested in eating you than striking any deals.

    You attack the spider but your blow glances off its tough exoskeleton. The creature reacts swiftly, rushing towards you and biting into your arm with its fangs. You feel a sharp sting of pain as it injects poison, numbing your limb.

    You use a spell you learned to create a wall of fire between you and the spider. It screams in pain and retreats momentarily.

    You attempt to escape but the spider recovers quickly. As it moves towards you again, you notice that its legs are covered with shimmering webs. You realize these must be what made your blow glance off earlier.

    You attack again, this time focusing on the spider's legs and managing to sever one of them. The creature recoils from the pain, screeching with fury.

    You use another spell to create a wall of ice around you, ensuring that spider won't get close again. The spider tries desperately to break through but fails.

    You continue down the tunnel, leaving the injured spider behind. As you walk further into the cave, the floor begins to slope upward. At last you reach a fork in the tunnel where two tunnels meet: one leads off to your right and another goes straight ahead. A dim light glows from somewhere up ahead of the left tunnel.
    """

    characters = (
        f"USER: Make a numbered list of all main actors in the following story.\n"
        f"{rpg_output2}"
        f"\nASSISTANT: Certainly"
    )

    mytho_compress(rpg_output2)

    good_result = """
    You wake up in an underground chamber, disoriented and with a pounding headache. The room is illuminated by torches high on the walls. You see an empty chest and a human skeleton nearby. As you examine the body, you find some gold coins and a key in a pouch attached to it.

    You step out of the room into a corridor where torches grow brighter as you walk down it. A huge spider appears at the end of the tunnel, blocking your path. The creature seems more interested in eating you than negotiating with you and attacks when you try to bargain. You fight back but get poisoned by its fangs before retreating into a tunnel branching off from the main corridor.

    You use magic spells to create walls of fire and ice, successfully driving away the spider. As you continue down another tunnel, it slopes upward until you reach a fork where two tunnels meet: one leads right while another goes straight ahead. A dim light glows from somewhere up ahead on the left tunnel.
    """
