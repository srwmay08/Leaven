from pydantic import BaseModel

class Ingredient(BaseModel):
    name: str
    purchase_price: float
    total_grams: float
    
    @property
    def cost_per_gram(self) -> float:
        return self.purchase_price / self.total_grams