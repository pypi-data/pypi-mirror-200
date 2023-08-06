import logging as log
from dataclasses import dataclass, field
from devgoldyutils import add_custom_handler, DictDataclass

logger = add_custom_handler(log.getLogger("uwu"), level=log.DEBUG)

@dataclass
class Jeff(DictDataclass):
    data:dict

    a:str = field(init=False)
    b:str = field(init=False)
    c:str = field(init=False)
    d:str = field(init=False)
    e:str = field(init=False)

    def __post_init__(self):
        super().__post_init__()

        self.a = self.get("jeff")
        self.b = self.get("bruh", "uwu")
        self.c = self.get("jeff", "damn")
        self.d = self.get("jeff", "b")
        self.e = self.get("jeff", "bdfdfd")

jeff = Jeff(
    {
        "jeff" : {
            "damn": False,
            "b": True
        },

        "bruh": {
            "uwu": True
        }
    }
)

print(jeff.a)
print(jeff.b)
print(jeff.c)
print(jeff.d)
print(jeff.e)