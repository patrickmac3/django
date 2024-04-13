from rest_framework.response import Response
from rest_framework.views import APIView
from user_profile.models import CompanyProfile
from properties.models import CondoUnit, ParkingUnit, PropertyProfile, StorageUnit
from rest_framework import status, reverse

class CompanyFinanceView(APIView):
    """
    API view for retrieving company finance information.

    This view calculates the total fees and expenses for each property associated with a company,
    including condo units, parking units, and storage units. It returns the aggregated data for all properties,
    as well as the total expenses, fees, and net income for the company.

    Endpoint: /profiles/company-profile/{company_id}/finance-report/

    Methods:
    - GET: Retrieves the finance information for the company.

    Parameters:
    - company_id (int): The ID of the company.

    Returns:
    - 200 OK: Returns a JSON object containing the finance information.
    """

    def get(self, request, *args, **kwargs):
        company_id = self.kwargs.get('company_id', None)

        company = CompanyProfile.objects.get(user_id=company_id)    
        properties = PropertyProfile.objects.filter(company=company)
        
        data = {}
        
        company_total_fees = 0
        company_total_expenses = 0
        company_total = 0
        
        for property in properties:
            # get the total fees for condo units
            total_condo_fees = 0
            total_condo_expenses = 0
            condo_budget = []
            condos = CondoUnit.objects.filter(property=property, public_profile__isnull=False)
            for condo in condos:
                total_condo_expenses += condo.operational_expense
                condo_data = {
                    "id": condo.id, 
                    "condo": condo.location, 
                    "expense": condo.operational_expense
                }
                if condo.public_profile:
                    total_condo_fees += condo.property_fee
                    condo_data['fee'] = condo.property_fee
                else:
                    condo_data['fee'] = 0
                    
                condo_budget.append(condo_data)

            # get the total fees for parking units
            total_parking_fees = 0
            total_parking_expenses = 0
            parking_budget = []
            parkings = ParkingUnit.objects.filter(property=property)
            for parking in parkings:
                total_parking_expenses += parking.operational_expense
                parking_data = {
                    "id": parking.id, 
                    "parking": parking.location, 
                    "expense": parking.operational_expense
                }
                
                if parking.public_profile:
                    total_parking_fees += parking.property_fee
                    parking_data['fee'] = parking.property_fee
                else:
                    parking_data['fee'] = 0
                    
                parking_budget.append(parking_data)
                
            # get the total fees for storage units
            total_storage_fees = 0
            total_storage_expenses = 0
            storage_budget = []
            storages = StorageUnit.objects.filter(property=property)
            for storage in storages:
                total_storage_expenses += storage.operational_expense
                storage_data = {
                    "id": storage.id, 
                    "storage": storage.location, 
                    "expense": storage.operational_expense
                }
                
                if storage.public_profile:
                    total_storage_fees += storage.property_fee
                    storage_data['fee'] = storage.property_fee
                else: 
                    storage_data['fee'] = 0

                storage_budget.append(storage_data)

            company_total_fees += total_condo_fees + total_storage_fees + total_parking_fees
            company_total_expenses += total_condo_expenses + total_parking_expenses + total_storage_expenses
            
            data[f'{property.id}'] = {
                "property_name": property.name,
                "condos": condo_budget,
                "parkings": parking_budget,
                "storages": storage_budget,
                "condo_fee": total_condo_fees,
                "parking_fee": total_parking_fees,
                "storage_fee": total_storage_fees,
                "condo_expense": total_condo_expenses,
                "parking_expense": total_parking_expenses,
                "storage_expense": total_storage_expenses,
                "fee": total_condo_fees + total_parking_fees + total_storage_fees,
                "expenses": total_condo_expenses + total_parking_expenses + total_storage_expenses
            }

        return Response(data={
            "properties": data,
            "expenses": company_total_expenses, 
            "fee": company_total_fees,
            "total": company_total_fees - company_total_expenses
        }, status=status.HTTP_200_OK)