#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" OpenAI: Generate Inflection Prompts """


from typing import Optional

from baseblock import BaseObject

from openai_helper import chat

from owl_builder.synonyms.dto import OpenAICache


class GenerateEnglishInflections(BaseObject):
    """ OpenAI: Generate Inflection Prompts """

    def __init__(self):
        """
        Created:
            20-Jul-2022
            craigtrim@gmail.com
            *   https://github.com/craigtrim/buildowl/issues/5
        Updated:
            28-Mar-2023
            craigtrim@gmail.com
            *   complete re-write using openai-helper
                https://github.com/craigtrim/owl-builder/issues/8#issuecomment-1487312189
        """
        BaseObject.__init__(self, __name__)
        cache = OpenAICache()
        self._exists_in_cache = cache.exists
        self._write_to_cache = cache.write
        self._read_from_cache = cache.read

    def process(self,
                input_text: str,
                model: Optional[str] = "gpt-4") -> Optional[str]:

        if self._exists_in_cache(input_text):
            return self._read_from_cache(input_text)

        prompt = """
Generate all the English inflections for a word

Word: troubleshoot
Inflections: troubleshoots,troubleshooting,troubleshooted,troubleshooter,troubleshooters
Word: computer
Inflections: computers, computerized, computerizing, computerize, computerizes, computerizing, computerization, computerizations

Word: #INPUT_TEXT
Inflections:
        """.replace("#INPUT_TEXT", input_text)

        result = chat(input_prompt=prompt, messages=None,
                      remove_emojis=True, model=model)
        if not result or not len(result):
            return None

        result = [
            x.strip() for x in result.split(',')
            if x.lower() != input_text.lower()
        ]

        result = [
            x for x in result if x and len(x)
        ]

        self._write_to_cache(data=result, file_name=input_text)

        return result
