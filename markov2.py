import random
from bisect import bisect
import sys

random = random.SystemRandom()

model_snippets = dict()
model_beginnings = list()


def learn_from_text(text, order):
    """
    simplified model_snippets optimized for random.choice
    """

    for i in range(len(text) - order):
        snippet = text[i:i + order]
        subsequent = text[i + order]
        if snippet not in model_snippets:
            model_snippets[snippet] = {}
        if subsequent not in model_snippets[snippet]:
            model_snippets[snippet][subsequent] = 1
        else:
            model_snippets[snippet][subsequent] += 1


def model_optimize_weights():
    for snippet, choices_dict in model_snippets.iteritems():
        choices, weights = zip(*choices_dict.iteritems())
        total = 0
        cumulative_weights = []
        for weight in weights:
            total += weight
            cumulative_weights.append(total)
        model_snippets[snippet] = (choices, cumulative_weights)


def weighted_choice(choices_dict):
    choices, weights = zip(*choices_dict.iteritems())
    total = 0
    cumulative_weights = []
    for weight in weights:
        total += weight
        cumulative_weights.append(total)
    x = random.randint(0, total-1)
    i = bisect(cumulative_weights, x)
    return choices[i]


def weighted_choice_simple(snippet):
    (choices, cumulative_weights) = model_snippets[snippet]
    x = random.randint(0, cumulative_weights[-1] - 1)
    i = bisect(cumulative_weights, x)
    return choices[i]


def generate(order, approx_len, finish_char="."):
    text = random.choice(model_beginnings)
    char = None
    while len(text) < approx_len or char != finish_char:
        snippet = text[-order:]
        char = weighted_choice(model_snippets[snippet])
#        char = weighted_choice_simple(snippet)
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
#     model_optimize_weights()

    print generate(order, approx_len=250, finish_char=".")


if __name__ == "__main__":
    main()
