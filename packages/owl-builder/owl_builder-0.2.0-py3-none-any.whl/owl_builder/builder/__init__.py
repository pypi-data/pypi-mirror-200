from typing import List
from typing import Optional

from .svc.generate_ttl_node import GenerateTTLNode
from .svc.generate_qa_pairs import GenerateQAPairs

qa_pair_generator = GenerateQAPairs().process
ttl_node_generator = GenerateTTLNode().process


def generate_qa_pairs(question: str,
                      answer: str) -> List[str]:
    """ Generate QA Pairs

    Args:
        question (str): a sample question
        answer (str): a sample answer

    Returns:
        List[str]: the Q&A Pairs
    """

    return qa_pair_generator(
        question=question,
        answer=answer)


def generate_node(entity_name: str,
                  entity_context: Optional[str] = None,
                  namespace: Optional[str] = "http://graffl.ai/test") -> str:
    """ Generate TTL Node

    Args:
        entity_name (str): the name of an entity
        entity_context (Optional[str], optional): the context this entity occurs. Defaults to None.
            providing a context will result in more precise synonyms
        namespace (str, optional): the OWL namespace. Defaults to "http://graffl.ai/test".

    Returns:
        str: a TTL node
    """

    return ttl_node_generator(
        entity_name=entity_name,
        entity_context=entity_context,
        namespace=namespace)
