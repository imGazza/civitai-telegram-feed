from dataclasses import dataclass

@dataclass
class Image:
    id: int
    url: str
    createdAt: str
    size: str
    prompt: str
    negativePrompt: str
    username: str
    model: str