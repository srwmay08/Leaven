from pydantic import BaseModel, Field, computed_field

class Ingredient(BaseModel):
    name: str
    vendor: str = "Unknown"
    purchase_price: float
    total_units: float = Field(gt=0, description="Must be greater than zero")
    unit_measure: str = Field(default="g", description="e.g., g, ea")
    
    @computed_field
    @property
    def cost_per_unit(self) -> float:
        return self.purchase_price / self.total_units