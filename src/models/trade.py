from pydantic import BaseModel
from typing import Optional

class Trade(BaseModel):
    instrument: Optional[str] = "FX"
    pai: Optional[str] = None
    notional: Optional[float] = None
    tenor: Optional[str] = None
    side: Optional[str] = None
    confidence: float = 0.0
    source: str = "RULE"