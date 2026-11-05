import pytest

from app.services.wishlist_service import WishListService
@pytest.mark.asyncio
async def test_get_wishlist(
    mock_db,
    mock_wishlist_repository,
    sample_customer,
    sample_wishlist,
):
    mock_wishlist_repository.get_customer_by_user_id.return_value = sample_customer
    mock_wishlist_repository.get_customer_wishlist.return_value = [sample_wishlist]

    service = WishListService(mock_wishlist_repository)

    result = await service.get_wishlist(mock_db, 1)

    assert len(result) == 1
    assert result[0].product_id == 1


@pytest.mark.asyncio
async def test_get_wishlist_customer_not_found(mock_db,mock_wishlist_repository):
    mock_wishlist_repository.get_customer_by_user_id.return_value = None
    service = WishListService(mock_wishlist_repository)

    with pytest.raises(Exception) as exc:
        await service.get_wishlist(mock_db, 1)
    assert exc.value.status_code == 404
