from datetime import datetime
from typing import ForwardRef

import ormar

SeedRef = ForwardRef("Seed")


class Seed(ormar.Model):
    class Meta:
        tablename = "seeds"

    id: str = ormar.String(primary_key=True, nullable=False)
    previous_id: SeedRef = ormar.ForeignKey(
        SeedRef, related_name="previous_seeds"
    )
    created_at: datetime = ormar.DateTime(default=datetime.now())
    applied_at: datetime = ormar.DateTime(nullable=True)
