from django.db import models

# practice code lang for setup purposes
# NOTE: below code is temporary and can delete after finishing set ups
class Budget(models.Model):
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.amount}"