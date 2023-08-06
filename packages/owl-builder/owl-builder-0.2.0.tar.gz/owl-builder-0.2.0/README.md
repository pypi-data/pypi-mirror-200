# Ontology Builder (owl-builder)

##

## Key Term Extraction
```python
from owl_builder import keyterms

input_text = """
A local area network (LAN) is a computer network that interconnects computers within a limited area such as a residence, school, laboratory, university campus or office building.

By contrast, a wide area network (WAN) not only covers a larger geographic distance, but also generally involves leased telecommunication circuits.

Ethernet and Wi-Fi are the two most common technologies in use for local area networks.

Historical network technologies include ARCNET, Token Ring, and AppleTalk.
"""

results = keyterms(
    input_text=input_text,
    use_openai=False,
    use_terms=True,
    use_keyterms=True,
    use_ngrams=False,
    use_nounchunks=False)
```

The results are
```json
[
   "leased telecommunication circuit",
   "historical network technology",
   "large geographic distance",
   "interconnects computer",
   "local area network",
   "university campus",
   "common technology",
   "wide area network",
   "computer network",
   "office building",
   "include arcnet",
   "limited area",
   "token ring"
]
```

If `use_openai` is set to `True`, then the following environment variables must be set:
```python
os.environ['USE_OPENAI'] = "True"
os.environ['OPENAI_KEY'] = "<openai-key>"
os.environ['OPENAI_ORG'] = "<openai-org>"
```

## TTL Generation
```python
from owl_builder import build_ttl

results = build_ttl("He has aims to make Detroit a leader in green energy.")
```

The result is
```ttl
###  http://graffl.ai/pathology#green_energy
        :green_energy rdf:type owl:Class ;
        rdfs:label "Green Energy" ;
        rdfs:subClassOf :energy .
###  http://graffl.ai/pathology#energy
        :energy rdf:type owl:Class ;
        rdfs:label "Energy" .
```

You can also supply your own taxonomy like this:
```python
import pandas as pd

results = build_ttl(pd.DataFrame([
    {"Parent": "Alpha", "Child": "Alpha Beta"},
    {"Parent": "Alpha Beta", "Child": "Alpha Beta Gamma"},
    {"Parent": "Gamma", "Child": "Gamma Delta"},
]))
```

The result is
```ttl
###  http://graffl.ai/pathology#alpha_beta
        :alpha_beta rdf:type owl:Class ;
        rdfs:label "Alpha Beta" ;
        rdfs:subClassOf :alpha .
###  http://graffl.ai/pathology#alpha
            :alpha rdf:type owl:Class ;
            rdfs:label "Alpha" .
###  http://graffl.ai/pathology#alpha_beta_gamma
            :alpha_beta_gamma rdf:type owl:Class ;
            rdfs:label "Alpha Beta Gamma" ;
            rdfs:subClassOf :alpha_beta .
###  http://graffl.ai/pathology#alpha_beta
            :alpha_beta rdf:type owl:Class ;
            rdfs:label "Alpha Beta" .
###  http://graffl.ai/pathology#gamma_delta
            :gamma_delta rdf:type owl:Class ;
            rdfs:label "Gamma Delta" ;
            rdfs:subClassOf :gamma .
###  http://graffl.ai/pathology#gamma
            :gamma rdf:type owl:Class ;
            rdfs:label "Gamma" .
```
