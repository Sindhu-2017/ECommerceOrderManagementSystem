import pytest

from app.services.customer_service import CustomerService

@pytest.mark.asyncio
async def test_get_all_customers(mock_db,mock_user_repository,sample_customer):
    mock_user_repository.get_all_customers.return_value = [sample_customer]
    service = CustomerService(mock_user_repository)

    result = await service.get_all_customers(mock_db,0,1)  

    assert len(result) == 1
    assert result[0].customer_id == 1
    assert result[0].first_name == "Test"
