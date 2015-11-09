import random
import sys

random = random.SystemRandom()

model_snippets = dict()
model_beginnings = list()


def learn_from_text(text, order):
    """
    simplified model optimized for random.choice
    """

    for i in range(len(text) - order):
        snippet = text[i:i + order]
        next = text[i + order]
        if snippet not in model_snippets:
            model_snippets[snippet] = ""
        model_snippets[snippet] += next


def generate(order, approx_len, finish_char = "."):
    text = random.choice(model_beginnings)
    char = None
    while len(text) < approx_len or char != finish_char:
        prefix = text[-order:]
        char = random.choice(model_snippets[prefix])
        text += char
    return text


def main():
    order = 7
    text = ""
    for line in sys.stdin:
        line = line.strip() + " "
        if len(line) >= order:
            model_beginnings.append(line[:order])
        text += line

    learn_from_text(text, order)

    print generate(order, approx_len=250, finish_char=".")


if __name__ == "__main__":
    main()
