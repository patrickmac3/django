from django.db import models

# Create your models here.


class FinanceModel(models.Model):
    @staticmethod
    def calculate_fee(unit):
        """
        Calculate the fee for a given unit based on its size and fee rate.

        Args:
            unit (Unit): The unit for which to calculate the fee.

        Returns:
            float: The calculated fee for the unit.
        """
        return unit.size * unit.property.fee_rate
