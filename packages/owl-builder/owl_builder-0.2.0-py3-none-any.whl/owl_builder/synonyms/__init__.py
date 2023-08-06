from typing import List
from typing import Optional

from .bp import *
from .dmo import *
from .svc import *
from .svc.generate_english_synonyms import GenerateEnglishSynonyms
from .svc.generate_english_inflections import GenerateEnglishInflections

synonym_generator = GenerateEnglishSynonyms().process
inflection_generator = GenerateEnglishInflections().process


def generate_synonyms(entity_name: str,
                      entity_context: Optional[str] = None,
                      desired_synonym_size: Optional[str] = None) -> Optional[List[str]]:
    """ Generate Synonyms for an Entity

    Args:
        entity_name (str): the name of any entity
        entity_context (Optional[str], optional): the context in which this entity appears. Defaults to None.
            this will improve the precision of the synonyms
        desired_synonym_size (Optional[str], optional): the size of the output synonyms: Unigram, Bigram, Trigram. Defaults to None.

    Returns:
        Optional[List[str]]: the generated synonyms
    """
    return synonym_generator(
        entity_name=entity_name,
        entity_context=entity_context,
        desired_synonym_size=desired_synonym_size)


def generate_inflections(entity_name: str,
                         model: Optional[str] = "gpt-4") -> Optional[List[str]]:
    """ Generate Inflections for an Entity

    Args:
        entity_name (str): the name of any entity
        model (Optional[str], optional): the model to use for genration. Defaults to "gpt-4".

    Returns:
        Optional[List[str]]: the generated inflections
    """
    return inflection_generator(
        model=model,
        input_text=entity_name)
