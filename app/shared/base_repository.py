from sqlalchemy import select, delete, func
from typing import TypeVar, Generic, Type, Optional, List, Dict, Any

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar('T')
CreateSchema = TypeVar('CreateSchema', bound=BaseModel)
UpdateSchema = TypeVar('UpdateSchema', bound=BaseModel)

class BaseRepository(Generic[T, CreateSchema, UpdateSchema] ):
    """
    Базовый асинхронный класс репозитория (CRUD)
    """
    def __init__(self, async_session: AsyncSession, model: Type[T]):
        self.model = model
        self._async_session = async_session

    async def get_by_id(self, model_id: int) -> Optional[T]:
        """
        Get a model by id
        :param model_id:
        :return: T or None
        """
        stmt = select(self.model).where(self.model.id == model_id)
        result = await self._async_session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all(self,skip: int = 0, limit: int = 100) -> List[T]:
        """
        Get all models
        :param skip:
        :param limit:
        :return:
        """
        stmt = select(self.model).order_by(self.model.id)
        result = await self._async_session.execute(stmt)
        return list(result.scalars().all())

    async def get_by_field(self, **kwargs) -> Optional[T]:
        """
        Получение сущности по параметру
        :param kwargs:
        :return:
        """
        stmt = select(self.model)
        for key, value in kwargs.items():
            stmt = stmt.where(getattr(self.model, key) == value)
        result = await self._async_session.execute(stmt)
        return result.scalars().first()

    async def update(
        self, model_id: int, obj_in: UpdateSchema | Dict[str, Any]
    ) -> Optional[T]:
        """
        Обновить объект по ID.
        Принимает либо Pydantic-схему, либо словарь.
        Использует ORM-объект для гарантии совместимости (включая SQLite).
        """
        db_obj = await self.get_by_id(model_id)
        if not db_obj:
            return None

        # Преобразуем входные данные в словарь
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)

        # Обновляем поля
        for key, value in update_data.items():
            setattr(db_obj, key, value)

        await self._async_session.commit()
        await self._async_session.refresh(db_obj)
        return db_obj

    async def delete(self, model_id: int) -> bool:
        """
        Удалить объект по ID
        :param model_id:
        :return: True or False
        """
        stmt = delete(self.model).where(self.model.c.id == model_id)
        result = await self._async_session.execute(stmt)
        await self._async_session.commit()
        return result.rowcount > 0

    async def create(self, obj_in: CreateSchema) -> Optional[T]:
        """Создать новый объект из Pydantic-схемы"""
        db_obj = self.model(**obj_in.model_dump())
        self._async_session.add(db_obj)
        await self._async_session.flush()
        await self._async_session.refresh(db_obj)
        return db_obj

    async def count(self) -> int:
        """Получить общее количество записей"""
        result = await self._async_session.execute(
            select(func.count()).select_from(self.model)
        )
        return result.scalar_one()

    async def exists(self, model_id: int) -> bool:
        """Проверить, существует ли объект с таким ID"""
        stmt = select(self.model).where(self.model.c.id == model_id).limit(1)
        result = await self._async_session.execute(stmt)
        return result.scalars().first() is not None
