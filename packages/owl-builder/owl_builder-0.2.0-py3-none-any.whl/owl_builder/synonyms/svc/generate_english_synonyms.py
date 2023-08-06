#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" OpenAI: Generate Inflection Prompts """


from typing import List
from typing import Optional

from baseblock import BaseObject

from openai_helper import chat

from owl_builder.synonyms.dto import OpenAICache
from owl_builder.synonyms.dmo import SynonymPromptGenerator


class GenerateEnglishSynonyms(BaseObject):
    """ OpenAI: Generate Inflection Prompts """

    def __init__(self):
        """
        Created:
            29-Mar-2023
            craigtrim@gmail.com
            *   https://github.com/craigtrim/owl-builder/issues/10
        """
        BaseObject.__init__(self, __name__)
        cache = OpenAICache()
        self._exists_in_cache = cache.exists
        self._write_to_cache = cache.write
        self._read_from_cache = cache.read

        self._prompt_generator = SynonymPromptGenerator().process

    def process(self,
                entity_name: str,
                entity_context: Optional[str] = None,
                desired_synonym_size: Optional[str] = None) -> Optional[str]:

        prompt = self._prompt_generator(
            entity_name=entity_name,
            entity_context=entity_context,
            desired_synonym_size=desired_synonym_size)

        result = chat(
            input_prompt=prompt,
            messages=None,
            remove_emojis=True,
            model="gpt-4")

        if not result or not len(result):
            return None

        def split_results() -> List[str]:
            if '\n' in result:
                return result.split('\n')
            if ',' in result:
                return result.split(',')
            return result

        results = [
            x.strip() for x in split_results()
        ]

        results = [
            x for x in results if x and len(x)
        ]

        return sorted(results, reverse=False)
