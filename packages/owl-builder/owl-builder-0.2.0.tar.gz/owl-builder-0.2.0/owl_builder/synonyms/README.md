# Generate Synonyms

### Method Signature
```python
def generate_synonyms(
    entity_name: str,
    entity_context: Optional[str] = None,
    desired_synonym_size: Optional[str] = None) -> Optional[List[str]]
```

### Usage
```python
from owl_builder.synonyms import generate_synonyms

generate_synonyms("build", entity_context="I build a house.", desired_synonym_size="trigram")
```

### Potential Results
```json
[
   "erect",
   "form",
   "make",
   "set up"
]
```

# Generate Inflections

### Method Signature
```python
def generate_inflections(
    entity_name: str,
    model: Optional[str] = "gpt-4") -> Optional[List[str]]
```

### Usage
```python
from owl_builder.synonyms import generate_inflections

generate_inflections("build")
```

### Potential Results
```json
[
   "builds",
   "building",
   "built",
   "builder",
   "builders"
]
```
