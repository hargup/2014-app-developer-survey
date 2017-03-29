import pandas as pd
import numpy as np
from collections import Counter
from itertools import combinations

import matplotlib.pyplot as plt


# XXX: There is some code duplications between verticles and non verticles
# code, maybe it is worth taking some time to remove this redundancy

# TODO: redesign get_answers so that I can query answers directly from the list
def get_answers(df, base_ques):
    """
    returns a dictionary of dictionary with the frequency of each answer

    NOTE: the base question should end just before '?'
    """
    cols_split = [x.split('?') for x in df.columns if base_ques in x]
    rv = dict()
    for col_split in cols_split:
        rv[col_split[-1]] = dict(Counter(df["?".join(col_split)]))

    return rv


# def get_answers_verticles(df, base_ques, verticles):
#     answers = [x.split('?')[-1] for x in df.columns if base_ques in x]
#     rv = dict()
#     for answer in answers:
#         rv_ = dict()
#         for name, cond in verticles.items():
#             df_ = df[cond]
#             rv_[name] = dict(Counter(df_["{}?{}".format(base_ques, answer)]))
#         rv[answer] = rv_
#
#     return rv


def divide_dfs(df, conds):
    """
    Take a dictionary of named conditions and returns a dictionary with same
    keys but with the conditions applied to the dataframe
    """
    rv = dict()
    for name, cond in conds.items():
        df_ = df[cond]
        rv[name] = df_

    return rv


def dict_apply(func, df_dict):
    """
    Recursively apply a function to the leaves of  dictionary of dictionary
    """
    rv = dict()
    for key, val in df_dict.items():
        if type(val) is not dict:
            rv[key] = func(val)
        else:
            rv[key] = dict_apply(func, val)

    return rv


def clean_ans(answer):
    return answer.strip(" []")


def get_cols(df, keyword):
    return [x for x in df.columns if keyword in x]


def print_dict(inp_dict, d=0):
    """
    Pretty prints a multilevel dictionary
    """
    if d == 0:
        print("----")
    for key, val in inp_dict.items():
        if type(val) is not dict:
            print("{} {}: {}".format("\t"*d, key, val))
        else:
            print("{}#{} {}".format("\t"*d, "#"*d, key))
            print_dict(val, d=d+1)

    if d == 0:
        print("----")


def get_conds(df, ques):
    cols_split = [x.split('?') for x in df.columns if ques in x]
    rv = dict()
    for col_split in cols_split:
        rv[clean_ans(col_split[-1])] = (df["?".join(col_split)] == "Yes")

    return rv


qs = [
    "dummy",  # Dummy question to start indexing from 1
    "Do you currently contribute to the development of mobile apps within a startup, company or enterprise? (Collectively \"enterprise\" henceforth.)",
    "Which area of expertise best describes your personal work currently?",
    "How many working years of experience do you have in your area of work?",
    "Where are you based in India?",
    "How many years old is your enterprise?",
    "How many people does your enterprise employ?",
    "Where is your enterprise based out of?",
    "How is your enterprise funded?",
    "Is your enterprise commercial or non-profit?",
    "Which of the following ways best describes your enterprises current business model?",
    "Which of the following ways best describes your enterprise's target business model?",
    "How many mobile app products does your enterprise have and own entirely? (not created for clients)",
    "Who are the primary users of your enterprise's own mobile app products? (not developed for clients)",
    "Where is your enterprise's current market?",
    "Where is your enterprises target market for mobile app products?",
    "What platform(s) does your enterprise create apps for?",
    "Roughly, at which stages are your enterprise's own mobile app products?",
    "Do you personally consider the value of your enterprise's own mobile app technologies to be in the background processes (e.g. business / data processes) or visible elements (e.g. UI, content, brand)?",
    "How would you, personally, consider your enterprise's own mobile app products in terms of innovation?",
    "Do any of your apps collect or deal with personal or sensitive personal information?",
    "Do you have a Privacy Policy for each of these apps that deal with personal information?",
    "Do you practice any security measures while handling this sensitive data for these apps?",
    "Where are your enterprise's clients based primarily?",
    "Roughly, how often do you enter into contracts agreements with your clients?",
    "Whenever you enter into a contract agreement with a client, how often does your agreement contain the following clauses?",
    "Do you personally consider the value of your client's mobile app technologies to be in the background processes (e.g. business / data processes) or visible elements (e.g. UI, content, brand)?",
    "How would you, personally, consider your client's mobile app products that you've developed in terms of innovation?",
    "How do you share your own code with others?",
    "If you share your code with others through certain websites, communities or conferences (online or offline), please list them here.",
    "How often do you license your mobile app code for your enterprise upon sharing it with others or in the app store?",
    "How do you license your code upon sharing it?",
    "What would your enterprise like others to be able to do with your code?",
    "What would you ideally require from others in order to be able to do such things with your code?",
    "How do you access code created by others?",
    "Roughly, how often do you check the terms or conditions of the licenses when using code created by others within your apps?",
    "How has the code that you use in your projects created by others been licensed?",
    "For what reason(s) have you\xc2\xa0reverse engineered / decompiled apps in the past?",
    "How often have you used parts of code accessed by reverse engineering / decompilation in your work?",
    "Are you at all concerned about potentially or accidentally infringing upon or violating another's mobile app?",
    "How often do you license your designs upon sharing them with others or in the app store?",
    "How do you license your designs?",
    "What would your enterprise like others to be able to do with your designs?",
    "What would you ideally require from others in order to be able to do such things with your designs?",
    "Roughly, how often do you use content in your mobile app designs created by others? (not including others within your enterprise)",
    "How has the content created by others that you use in your designs been licensed?",
    "Roughly, how often do you check the permissions for the content you use within your mobile app designs?",
    "Are you at all concerned about possibly or accidentally infringing upon or violating another's designs or content?",
    "How concerned are you about others copying your work and/or product?",
    "To your understanding, through which of the following ways has your enterprise protected its own mobile app products?",
    "Through which of the following ways do you think your enterprise would like to protect their mobile app products ideally in the future?",
    "If your enterprise is interested in protecting its products, what are the main reasons for doing so?",
    "Who or what influences your enterprise's decisions related to ownership, contracts, licensing, and/or protection of your works?",
    "Are you familiar with what rights you are entitled to as the owner of your works? (e.g. ability to sell, modify, copy, etc.)",
    "Are you familiar with what actions are considered to be a violation of another's rights over their work? (e.g. to use, modify or distribute others' works without permission to do so)",
    "Are you familiar with the specific instances where such actions of infringement are not considered to be a violation of another's rights over their work? (e.g. personal study, education, for increased accessibility, etc.)",
    "How familiar are you with the concept of \"intellectual property\" in relation to your work within mobile app development?"
        ]


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
    ax.set_xticklabels(map(clean_ans, ans_q49.keys()))

    ax.legend((b1[0], b2[0]), ('Q49', 'Q50'))

    plt.show()
