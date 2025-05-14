from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from db.settings import settings
from contextlib import asynccontextmanager


DATABASE_URL = settings.get_db_url()

engine = create_async_engine(DATABASE_URL)

async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


@asynccontextmanager
async def get_db_session():
    session = async_session_maker()
    try:
        yield session
        await session.commit()
    except Exception as e:
        await session.rollback()
        raise e
    finally:
        await session.close()
