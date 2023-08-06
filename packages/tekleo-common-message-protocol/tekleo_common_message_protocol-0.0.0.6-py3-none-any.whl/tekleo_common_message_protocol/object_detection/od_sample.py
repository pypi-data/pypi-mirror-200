from typing import List
from pydantic import BaseModel
from simplestr import gen_str_repr_eq
from PIL.Image import Image
from tekleo_common_message_protocol.object_detection.od_labeled_item import OdLabeledItem


@gen_str_repr_eq
class OdSample(BaseModel):
    name: str
    image: Image
    items: List[OdLabeledItem]

    class Config:
        arbitrary_types_allowed = True

    def __init__(self, name: str, image: Image, items: List[OdLabeledItem]) -> None:
        super().__init__(name=name, image=image, items=items)
