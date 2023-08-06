#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Use OpenAI to Generate Intent Names """



from pprint import pprint
from openai_helper import chat
from collections import defaultdict
from owl_builder import extract_keyterms
from owl_builder.keyterms.bp import AutoTaxoOrchestrator

from typing import (
    List,
    Optional
)

from baseblock import (
    BaseObject,
    Stopwatch,
    Enforcer,
)

autotaxo_orchestrator = AutoTaxoOrchestrator()


def _keyterms(questions: List[str]) -> List[str]:

    d_questions = {}
    d_questions_rev = defaultdict(list)

    for question in questions:

        terms = autotaxo_orchestrator.keyterms(
            input_text=question,
            use_openai=True,
            use_terms=False,
            use_keyterms=False,
            use_ngrams=False,
            use_nounchunks=False)
        
        print (question, terms)

        d_questions[question] = terms

    for question in d_questions:
        for term in d_questions[question]:
            d_questions_rev[term].append(question)

    return d_questions, d_questions_rev


def main():
    d_questions, d_questions_rev = _keyterms([
        "What is a typical day in your life like?",
        "Could you outline what you do from morning to night?",
        "Could you tell me about your standard daily routine?",
        "Can you give me a rundown of your daily activities?",
        "What are the tasks you typically complete in a day?",
        "Could you give me a rundown of your daily routine?",
        "Can you give me an idea of your daily activities?",
        "Could you tell me about your typical day-to-day?",
        "How do you go about your day-to-day activities?",
        "How do you typically spend your time each day?",
        "Could you walk me through your daily schedule?",
        "What do you usually do on a day-to-day basis?",
        "What is an ordinary day like for you?",
        "Can you describe your regular daily routine?",
        "How do you fill your hours on a regular day?",
        "What do you typically do throughout the day?",
        "What’s your schedule like on a regular day?",
        "Walk me through a typical day in your life.",
        "What's the usual routine for you each day?",
        "What is a typical day like for you?",
    ])

    pprint(d_questions)
    print()
    pprint(d_questions_rev)


if __name__ == "__main__":
    main()
