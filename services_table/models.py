from django.db import models

class Service(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    duration_minutes = models.PositiveIntegerField(default=30)
    price_cents = models.PositiveIntegerField(default=0)
    category = models.CharField(max_length=50, blank=True)
    active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['category', 'name']

    def __str__(self):
        return f"{self.name} ({self.formatted_price})"

    @property
    def formatted_price(self) -> str:
        dollars = self.price_cents // 100
        cents = self.price_cents % 100
        return f"${dollars}.{cents:02d}"

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "duration_minutes": self.duration_minutes,
            "price_cents": self.price_cents,
            "price": self.formatted_price,
            "category": self.category,
            "active": self.active,
        }