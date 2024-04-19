from typing import TypedDict, NotRequired


class FilterParams(TypedDict):
    name: NotRequired[str]
    model: NotRequired[str]
    year: NotRequired[int]
    color: NotRequired[str]
    price: NotRequired[int]
    latitude: NotRequired[float]
    longitude: NotRequired[float]


