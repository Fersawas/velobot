import logging

from sqlalchemy import select, exists
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload
from db.database import get_db_session
from db.models import Admin, AdminRights, User, Order

from utils.exceptions import UserExists, NotSuchUser, OrderExists, OrderDoesNotExists


logger = logging.getLogger(__name__)


async def admin_username_get(username: str):
    async with get_db_session() as session:
        user_result = await session.execute(
            select(User).where(User.username == username)
        )
        user = user_result.scalar_one_or_none()
        if not user or not user.phone:
            return False

        stmt = select(exists().where(Admin.phone == user.phone))
        result = await session.execute(stmt)
        return result.scalar()


async def admin_rights_check(username: str):
    async with get_db_session() as session:
        try:
            result = await session.execute(
                select(Admin).where(Admin.username == username)
            )
            admin = result.scalar_one_or_none()
            return admin and admin.rights == AdminRights.ADMIN
        except SQLAlchemyError as e:
            logger.error(e)
            print(e)
            return False


async def admin_rights_change(username: str, rights: str):
    async with get_db_session() as session:
        try:
            result = await session.execute(
                select(Admin).where(Admin.username == username)
            )
            admin = result.scalar_one_or_none()
            if admin:
                admin.rights = rights
                await session.commit()
                await session.refresh(admin)
                logger.info(f"upd admin - {admin.username} rights")
                return True
            if not admin:
                return False
        except SQLAlchemyError as e:
            await session.rollback()
            logger.error(e)
            print(e)
            return False


async def admin_create(username: str, phone: str | None):
    async with get_db_session() as session:
        try:
            result = await session.execute(
                select(Admin).where(Admin.username == username)
            )
            existed_admin = result.scalar_one_or_none()
            if not existed_admin:
                new_admin = Admin(username=username, phone=phone)
                session.add(new_admin)
                await session.commit()
                logger.info(f"new admin was created {new_admin.username}")
                return True
            else:
                raise UserExists
        except SQLAlchemyError as e:
            await session.rollback()
            logger.error(e)
            print(e)
            return False


async def admin_remove(admin_id: int):
    async with get_db_session() as session:
        try:
            result = await session.execute(select(Admin).where(Admin.id == admin_id))
            admin = result.scalar_one_or_none()
            if admin:
                await session.delete(admin)
                await session.commit()
                logger.info(f"delete admin - {admin.username}")
                return True
            if not admin:
                return False
        except SQLAlchemyError as e:
            logger.error(e)
            print(e)
            return False


async def admin_list():
    async with get_db_session() as session:
        try:
            result = await session.execute(select(Admin))
            admins = result.scalars().all()
            return admins
        except SQLAlchemyError as e:
            logger.error(e)
            print(e)
            return False


async def list_admin_names():
    async with get_db_session() as session:
        try:
            result = await session.execute(select(Admin.username))
            admins_names = result.scalars().all()
            return admins_names
        except SQLAlchemyError as e:
            logger.error(e)
            print(e)
            return False


async def admin_retrieve(admin_id: int):
    async with get_db_session() as session:
        try:
            result = await session.execute(select(Admin).where(Admin.id == admin_id))
            admin = result.scalar_one_or_none()
            print(admin)
            if not admin:
                raise NotSuchUser
            return admin
        except SQLAlchemyError as e:
            logger.error(e)
            print(e)
            return False


async def admin_edit(admin_id: int, new_phone: str, new_username: str):
    async with get_db_session() as session:
        try:
            result = await session.execute(select(Admin).where(Admin.id == admin_id))
            admin = result.scalar_one_or_none()
            if not admin:
                raise NotSuchUser
            admin.username = new_username
            admin.phone = new_phone
            session.commit()
            session.refresh(admin)
            return True
        except SQLAlchemyError as e:
            logger.error(e)
            print(e)
            return False


async def user_create(
    username: str | None,
    first_name: str | None,
    last_name: str | None,
    user_id: int | None,
):
    async with get_db_session() as session:
        try:
            result = await session.execute(select(User).where(User.user_id == user_id))
            user = result.scalar_one_or_none()
            if not user:
                new_user = User(
                    username=username,
                    first_name=first_name,
                    last_name=last_name,
                    user_id=user_id,
                )
                session.add(new_user)
                await session.commit()
            return True
        except SQLAlchemyError as e:
            logger.error(e)
            print(e)
            return False


async def user_phone_get(user_id: int):
    async with get_db_session() as session:
        try:
            result = await session.execute(select(User).where(User.user_id == user_id))
            user = result.scalar_one_or_none()
            if user:
                return user.phone
            else:
                return False
        except SQLAlchemyError as e:
            logger.error(e)
            print(e)
            return False


async def user_phone_update(user_id: int, phone: str):
    async with get_db_session() as session:
        try:
            result = await session.execute(select(User).where(User.user_id == user_id))
            user = result.scalar_one_or_none()
            if user:
                user.phone = phone
                await session.commit()
                await session.refresh(user)
        except SQLAlchemyError as e:
            logger.error(e)
            print(e)
            return False


async def order_get_for_client(phone: str):
    async with get_db_session() as session:
        try:
            result = await session.execute(select(Order).where(Order.phone == phone))
            orders = result.scalars().all()
            return orders
        except SQLAlchemyError as e:
            logger.error(e)
            print(e)
            return False


async def order_create(
    title: str,
    description: str,
    model_type: str,
    price_estimate: float,
    is_paid: bool,
    fullname: str,
    phone: str,
    master: int,
    comment: str,
):
    async with get_db_session() as session:
        try:
            result = await session.execute(
                select(Order).where(
                    Order.title == title,
                    Order.description == description,
                    Order.model_type == model_type,
                    Order.phone == phone,
                )
            )
            order = result.scalar_one_or_none()
            if order:
                raise OrderExists
            else:
                new_order = Order(
                    title=title,
                    description=description,
                    model_type=model_type,
                    price_estimate=price_estimate,
                    final_price=price_estimate,
                    is_paid=is_paid,
                    fullname=fullname,
                    phone=phone,
                    comment=comment,
                )
                if master:
                    new_order.master = master
                session.add(new_order)
                await session.commit()
                await session.refresh(new_order)
                return new_order.id
        except SQLAlchemyError as e:
            logger.error(e)
            print(e)
            return False


async def get_order_by_id(order_id: int):
    async with get_db_session() as session:
        try:
            result = await session.execute(
                select(Order)
                .where(Order.id == order_id)
                .options(joinedload(Order.master))
            )
            order = result.scalar_one_or_none()
            if order:
                return order
            else:
                logger.warning(f"{order_id} - does not exists")
                raise OrderDoesNotExists
        except SQLAlchemyError as e:
            print(e)
            logger.error(e)
            return False


async def get_order_by_master(master_id: int):
    async with get_db_session() as session:
        try:
            result = await session.execute(
                select(Order)
                .where(Order.master_id == master_id)
                .options(joinedload(Order.master))
            )
            orders = result.scalars().all()
            return orders
        except SQLAlchemyError as e:
            print(e)
            logger.error(e)
            return False


async def edit_order_db(
    order_id: int,
    **kwargs,
):
    async with get_db_session() as session:
        try:
            result = await session.execute(
                select(Order)
                .where(Order.id == order_id)
                .options(joinedload(Order.master))
            )
            order = result.scalar_one_or_none()
            if not order:
                return False
            if "master_id" in kwargs and kwargs["master_id"] is not None:
                master_id = kwargs.pop("master_id")
                admin = await session.get(Admin, master_id)
                order.master = admin
            for key, value in kwargs.items():
                setattr(order, key, value)
            await session.commit()
            await session.refresh(order)
            return True

        except SQLAlchemyError as e:
            logger.error(e)
            return False
