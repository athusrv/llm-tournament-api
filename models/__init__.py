from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

class Model(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )

class Prompt(Model):
    id: int
    text: str
    response: str

class Vote(Model):
    winner_id: int

class Result(Model):
    prompt: Prompt
    score: int