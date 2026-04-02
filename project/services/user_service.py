from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from models.user import User
from schemas.user import UserCreate, UserUpdate


class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db

    
    async def get_all_users(self, q: str | None=None, page: int | None =1, limit: int | None=5) -> list[User]:
        # SQLAlchemy's select() builds a SQL SELECT statement.
        # Think of it like a MongoDB query builder, but for SQL.
        stmt = select(User)

        if q:
            stmt = stmt.where(
                User.name.ilike(f"%{q}%") | User.email.ilike(f"%{q}%")
            )
        
        if page is None:
            page = 1
        if limit is None:
            limit = 5
        stmt = stmt.offset((page - 1) * limit).limit(limit)
        result = await self.db.execute(stmt)
        
        return list(result.scalars().all())

    
    async def get_user_by_id(self, user_id: int) -> User | None:
        return await self.db.get(User, user_id)
    

    async def create_user(self, user_data: UserCreate) -> User:
        user = User(**user_data.model_dump())
        self.db.add(user)

        await self.db.flush()
        await self.db.refresh(user)
        return user
    

    async def update_user(self, user_id: int, user_data: UserUpdate) -> User | None:
        user = await self.get_user_by_id(user_id)
        if not user:
            return None
        
        for key, value in user_data.model_dump(exclude_unset=True).items():
            setattr(user, key, value)
        
        await self.db.flush()
        await self.db.refresh(user)
        return user


    async def delete_user(self, user_id: int) -> bool:
        user = await self.get_user_by_id(user_id)

        if not user:
            return False
        
        await self.db.delete(user)
        return True