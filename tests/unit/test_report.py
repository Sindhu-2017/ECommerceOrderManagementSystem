from decimal import Decimal

import pytest

from app.services.report_service import ReportService

@pytest.mark.asyncio
async def test_get_sales_summary(
    mock_db,
    mock_report_repository,
    sample_sales_summary
):
    mock_report_repository.get_sales_summary.return_value = sample_sales_summary
    service = ReportService(mock_report_repository)

    result = await service.get_sales_summary(mock_db)

    assert result.total_orders == 10
    assert result.paid_orders == 6
    assert result.total_revenue == Decimal("100000.00")
    assert result.pending_orders == 4


@pytest.mark.asyncio
async def test_get_product_sales(mock_db,mock_report_repository):
    mock_report_repository.get_product_sales.return_value = [
        {
            "product_id": 1,
            "product_name": "Laptop",
            "quantity_sold": 2,
            "total_sales": Decimal("100000.00"),
        }
    ]

    service = ReportService(mock_report_repository)

    result = await service.get_product_sales(mock_db)

    assert len(result) == 1
    assert result[0]["product_name"] == "Laptop"
    assert result[0]["quantity_sold"] == 2
