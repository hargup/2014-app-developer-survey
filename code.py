import pandas as pd
import numpy as np
from collections import Counter
from itertools import combinations

import matplotlib.pyplot as plt


# XXX: There is some code duplications between verticles and non verticles
# code, maybe it is worth taking some time to remove this redundancy
def get_answers(df, base_ques):
    """
    returns a dictionary of dictionary with the frequency of each answer

    NOTE: the base question should end just before '?'
    """
    answers = [x.split('?')[-1] for x in df.columns if base_ques in x]
    rv = dict()
    for answer in answers:
        rv[answer] = Counter(df["{}?{}".format(base_ques, answer)])

    return rv


def get_answers_verticles(df, base_ques, verticles):
    answers = [x.split('?')[-1] for x in df.columns if base_ques in x]
    rv = dict()
    for answer in answers:
        rv_ = dict()
        for name, cond in verticles.items():
            df_ = df[cond]
            rv_[name] = Counter(df_["{}?{}".format(base_ques, answer)])
        rv[answer] = rv_

    return rv


def clean_ans(answers):
    return map(lambda x: x.strip(" []"), answers)


def get_cols(df, keyword):
    return [x for x in df.columns if keyword in x]


def print_counter(cntr):
    for k, v in cntr.items():
        print("{}: {}".format(k, v))


def print_answers(df, base_ques):
    print("----")
    print(base_ques)
    print("----")

    for ans, vals in get_answers(df, base_ques).items():
        print(ans)
        print_counter(vals)


def print_answers_verticles(df, base_ques, verticles):
    print("\n")
    print(base_ques)
    print("----\n")

    for ans, vals in get_answers_verticles(df, base_ques, verticles).items():
        print("\n# {}\n".format(ans))
        for vert, cntr in vals.items():
            print("## {}".format(vert))
            print_counter(cntr)


# For some reason Counter isn't combining all the nan's in the other answer




code_license_questions = [

 "To your understanding, through which of the following ways has your enterprise protected its own mobile app products",
 "How often do you license your mobile app code for your enterprise upon sharing it with others or in the app store",
 "How do you license your code upon sharing it"
        ]


design_license_questions = [
    "How often do you license your designs upon sharing them with others or in the app store",
    "How do you license your designs",
    "What would your enterprise like others to be able to do with your designs",
    "What would you ideally require from others in order to be able to do such things with your designs"
        ]


reverse_engineering_practicies = [
    "For what reason(s) have you\xa0reverse engineered / decompiled apps in the past",
    "How often have you used parts of code accessed by reverse engineering / decompilation in your work"
        ]


influence = [
    "Who or what influences your enterprise's decisions related to ownership, contracts, licensing, and/or protection of your works",
    "Through which of the following ways do you think your enterprise would like to protect their mobile app products ideally in the future",
    "If your enterprise is interested in protecting its products, what are the main reasons for doing so"
 ]


df = pd.read_csv("survey_results.csv")
# I should probably drop all nan columns
df = df.dropna(axis=1, how='all')


verticles = {
    "app developer": (df['Which area of expertise best describes your personal work currently? [Mobile app development]'] == "Yes"),
    "app designer": (df['Which area of expertise best describes your personal work currently? [Mobile app design]'] == "Yes"),
    "product/team manager": df['Which area of expertise best describes your personal work currently? [Product / Team management]'] == "Yes"
        }


def num_yes(bools):
    return Counter(bools)[True]

# for name, cond in verticles.items():
#     print("{}: {}".format(name, num_yes(cond)))
#
# for n1, n2 in combinations(verticles.keys(), 2):
#     print("{} and {}: {}".format(n1, n2, num_yes(verticles[n1] & verticles[n2])))

# for ques in code_license_questions:
#     print_answers_verticles(df, ques, verticles)


# for ques in design_license_questions:
#     print_answers_verticles(df, ques, verticles)


# for ques in reverse_engineering_practicies:
#     print_answers_verticles(df, ques, verticles)

q49 = "To your understanding, through which of the following ways has your enterprise protected its own mobile app products"
q50 = "Through which of the following ways do you think your enterprise would like to protect their mobile app products ideally in the future"


def plot_bar():
    # TODO: The lables needs be bigger and they need to be cleaned
    ans_q49 = get_answers(df, q49)
    ans_q50 = get_answers(df, q50)

    N = len(ans_q49)

    q49vals = [x["Yes"] for x in ans_q49.values()]
    q50vals = [x["Yes"] for x in ans_q50.values()]

    ind = np.arange(N)*3  # the x locations for the groups
    width = np.min(np.diff(ind))/3       # the width of the bars

    fig = plt.figure(figsize=(30,10))
    ax = fig.add_subplot(111)
    b1 = ax.bar(np.arange(N)*3 + 1, q49vals, color='b', alpha=0.5)
    b2 = ax.bar(np.arange(N)*3, q50vals, color='r', alpha=0.5)

    # add some
    ax.set_ylabel('Scores')
    ax.set_title('Scores by group and gender')
    ax.set_xticks(ind+width)
    ax.set_xticklabels(clean_ans(ans_q49.keys()))

    ax.legend((b1[0], b2[0]), ('Q49', 'Q50'))

    plt.show()