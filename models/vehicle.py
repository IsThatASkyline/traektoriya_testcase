from dataclasses import dataclass


@dataclass
class Vehicle:
    name: str
    model: str
    year: int
    color: str
    price: int
    latitude: float
    longitude: float
    id: int | None = None

    def __repr__(self):
        return f"<Vehicle: {self.name} {self.model} {self.year} {self.color} {self.price}>"

    def get_params_set(self) -> set:
        return {("name", self.name), ("model", self.model), ("year", self.year), ("color", self.color),
                ("price", self.price), ("latitude", self.latitude), ("longitude", self.longitude)}

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "model": self.model,
            "year": self.year,
            "color": self.color,
            "price": self.price,
            "latitude": self.latitude,
            "longitude": self.longitude,
        }
