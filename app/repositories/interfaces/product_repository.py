from abc import ABC,abstractmethod 

from app.models.product import Product

class ProductRepositoryInterface(ABC):

    @abstractmethod
    async def get_by_id(self, product_id: int) -> Product | None:
        pass

    @abstractmethod
    async def get_by_name(self, product_name: str) -> Product | None:
        pass

    @abstractmethod
    async def get_all(
        self,
        search: str | None,
        category_id: int | None,
        min_price: float | None,
        max_price: float | None,
        skip: int,
        limit: int
    ) -> list[Product]:
        pass

    @abstractmethod
    async def create(self, product: Product) -> Product:
        pass

    @abstractmethod
    async def update(self, product: Product) -> Product:
        pass
