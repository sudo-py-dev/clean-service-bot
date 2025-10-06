import os
from datetime import datetime, timedelta
from .logger import logger
import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, func, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from typing import Any
from dotenv import load_dotenv
from .enums import AccessPermission

load_dotenv()

Base = sqlalchemy.orm.declarative_base()
engine = create_engine(os.getenv("DATABASE_URL") or "sqlite:///db.sqlite",
                       pool_size=10,
                       max_overflow=20,
                       echo=False,
                       connect_args={
                           "timeout": 30
                       })

Session = sessionmaker(bind=engine)


class Chats(Base):
    __tablename__ = 'chats'
    chat_id = Column(Integer, primary_key=True, index=True, unique=True)
    language = Column(String, default="he")
    chat_type = Column(String, nullable=True)
    chat_title = Column(String, nullable=True)
    bot_is_admin = Column(Boolean, nullable=True)

    # Control update of admins permissions
    last_admins_update = Column(DateTime, nullable=True)
    last_reloaded_admins = Column(DateTime, nullable=True)
    
    # Relationship with AdminsPermissions
    admins_permissions = relationship("AdminsPermissions", back_populates="chat", cascade="all, delete-orphan")

    @staticmethod
    def create(chat_id: int, chat_type: str, chat_title: str, bot_is_admin: bool) -> bool:
        with Session() as session:
            chat = session.query(Chats).filter_by(chat_id=chat_id).first()
            if chat is None:
                chat = Chats(chat_id=chat_id, chat_type=chat_type, chat_title=chat_title, bot_is_admin=bot_is_admin)
                session.add(chat)
                session.commit()
                return True
            return False
    
    @staticmethod
    def update(chat_id: int, **kwargs) -> bool:
        with Session() as session:
            chat = session.query(Chats).filter_by(chat_id=chat_id).first()
            if chat is None:
                return False
            for key, value in kwargs.items():
                setattr(chat, key, value)
            session.commit()
            return chat
    
    @staticmethod
    def delete(chat_id: int) -> bool:
        with Session() as session:
            chat = session.query(Chats).filter_by(chat_id=chat_id).first()
            if chat is None:
                return False
            session.delete(chat)
            session.commit()
            return True
    
    @staticmethod
    def get(chat_id: int):
        with Session() as session:
            chat = session.query(Chats).filter_by(chat_id=chat_id).first()
            return chat.__dict__
    
    @staticmethod
    def is_exists(chat_id: int) -> bool:
        with Session() as session:
            chat = session.query(Chats).filter_by(chat_id=chat_id).first()
            return chat is not None
    
    @staticmethod
    def register(chat_id: int, chat_type: str, chat_title: str, bot_is_admin: bool):
        with Session() as session:
            chat = session.query(Chats).filter_by(chat_id=chat_id).first()
            if chat is None:
                chat = Chats(chat_id=chat_id, chat_type=chat_type, chat_title=chat_title, bot_is_admin=bot_is_admin)
                session.add(chat)
                session.commit()
                return True
            return False


class AdminsPermissions(Base):
    __tablename__ = 'admins_permissions'
    admin_id = Column(Integer, primary_key=True, index=True, unique=True)
    chat_id = Column(Integer, ForeignKey('chats.chat_id', ondelete="CASCADE"), nullable=False)
    is_anonymous = Column(Boolean, nullable=True)
    can_manage_chat = Column(Boolean, nullable=True)
    can_delete_messages = Column(Boolean, nullable=True)
    can_manage_video_chats = Column(Boolean, nullable=True)  # Groups and supergroups only
    can_restrict_members = Column(Boolean, nullable=True)
    can_promote_members = Column(Boolean, nullable=True)
    can_change_info = Column(Boolean, nullable=True)
    can_invite_users = Column(Boolean, nullable=True)
    can_post_messages = Column(Boolean, nullable=True)  # Channels only
    can_edit_messages = Column(Boolean, nullable=True)  # Channels only
    can_pin_messages = Column(Boolean, nullable=True)  # Groups and supergroups only
    can_post_stories = Column(Boolean, nullable=True)
    can_edit_stories = Column(Boolean, nullable=True)
    can_delete_stories = Column(Boolean, nullable=True)
    can_manage_topics = Column(Boolean, nullable=True)  # supergroups only
    can_manage_direct_messages = Column(Boolean, nullable=True)

    # Relationship with Chats
    chat = relationship("Chats", back_populates="admins_permissions")

    @staticmethod
    def _get_valid_privileges(privileges: Any) -> dict[str, Any]:
        """Extract valid privilege attributes from a ChatPrivileges object."""
        return {
            k: v for k, v in vars(privileges).items()
            if not k.startswith('_') and 
               hasattr(AdminsPermissions, k) and
               k not in ('admin_id', 'chat_id')
        }

    @classmethod
    def create(cls, chat_id: int, admin_list: list[tuple[int, Any]]) -> AccessPermission:
        """
        Create or update admin permissions for a chat.
        
        Args:
            chat_id: The chat ID to update permissions for
            admin_list: List of (admin_id, ChatPrivileges) tuples
            
        Returns:
            AccessPermission: Status of the operation
        """
        with Session() as session:
            try:
                chat = session.query(Chats).filter_by(chat_id=chat_id).first()
                if chat is None:
                    chat = Chats(chat_id=chat_id, chat_type="", chat_title="")
                    session.add(chat)
                
                # Delete old admin permissions
                session.query(cls).filter_by(chat_id=chat_id).delete()
                
                # Add new admin permissions
                for admin_id, privileges in admin_list:
                    priv_dict = cls._get_valid_privileges(privileges)
                    admin = cls(
                        admin_id=admin_id,
                        chat_id=chat_id,
                        **priv_dict
                    )
                    session.add(admin)
                
                # Update last_admins_update
                chat.last_admins_update = datetime.now()
                session.commit()
                return True
            except Exception as e:
                session.rollback()
                logger.error(f"Error updating admin permissions: {e}")
                raise
    
    @classmethod
    def is_admin(cls, chat_id: int, admin_id: int, permission: str) -> AccessPermission:
        """
        Check if a user has a specific admin permission.
        
        Args:
            chat_id: The chat ID
            admin_id: The user ID to check
            permission: The permission to verify
            
        Returns:
            AccessPermission: Permission status
        """
        with Session() as session:
            try:
                chat = session.query(Chats).filter_by(chat_id=chat_id).first()
                if chat is None:
                    Chats.create(chat_id, "", "", True)
                    return AccessPermission.NEED_UPDATE
                
                if not chat.last_admins_update or chat.last_admins_update < datetime.now() - timedelta(hours=2):
                    return AccessPermission.NEED_UPDATE
                    
                admin = session.query(cls).filter_by(
                    chat_id=chat_id, 
                    admin_id=admin_id
                ).first()
                
                if admin is None:
                    return AccessPermission.NOT_ADMIN
                if not hasattr(admin, permission):
                    return AccessPermission.DENY
                return AccessPermission.ALLOW if getattr(admin, permission) else AccessPermission.DENY
            except Exception as e:
                logger.error(f"Error in is_admin for chat {chat_id}, admin {admin_id}: {e}")
                return AccessPermission.DENY
    
    @classmethod
    def reload(cls, chat_id: int) -> bool:
        """Reload admin permissions for a chat."""
        with Session() as session:
            try:
                chat = session.query(Chats).filter_by(chat_id=chat_id).first()
                if chat is None:
                    return False
                elif chat.last_reloaded_admins and chat.last_reloaded_admins > datetime.now() - timedelta(hours=2):
                    return False
                chat.last_admins_update = datetime.now() + timedelta(hours=2)
                chat.last_reloaded_admins = datetime.now()
                session.commit()
                return True
            except Exception as e:
                session.rollback()
                logger.error(f"Error reloading admin permissions: {e}")
                return False

    @classmethod
    def clear(cls, chat_id: int) -> bool:
        """Clear all admin permissions for a chat."""
        with Session() as session:
            try:
                chat = session.query(Chats).filter_by(chat_id=chat_id).first()
                if chat is None:
                    return False
                session.query(cls).filter_by(chat_id=chat_id).delete()
                chat.last_admins_update = None
                session.commit()
                return True
            except Exception as e:
                session.rollback()
                logger.error(f"Error clearing admin permissions: {e}")
                return False
    
    @classmethod
    def clear_all(cls) -> bool:
        """Clear all admin permissions from the database."""
        with Session() as session:
            try:
                session.begin()
                session.query(cls).delete()
                # Reset all chat timestamps
                session.query(Chats).update({Chats.last_admins_update: None})
                session.commit()
                return True
            except Exception as e:
                session.rollback()
                logger.error(f"Error clearing all admin permissions: {e}")
                return False


class Users(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True, index=True, unique=True)
    username = Column(String, nullable=True)
    full_name = Column(String, nullable=True)
    language = Column(String, nullable=True)
    is_contact = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    # Add more columns as needed

    @staticmethod
    def create(user_id: int, username: str=None, full_name: str=None, language: str=None, is_contact: bool=True) -> bool:
        with Session() as session:
            user = session.query(Users).filter_by(user_id=user_id).first()
            if user is None:
                user = Users(user_id=user_id, username=username, full_name=full_name, language=language, is_contact=is_contact)
                session.add(user)
                session.commit()
                return True
            return False
    
    @staticmethod
    def get(user_id: int):
        with Session() as session:
            user = session.query(Users).filter_by(user_id=user_id).first()
            if user is None:
                return None
            return user

    
    @staticmethod
    def update(user_id: int, **kwargs) -> bool:
        with Session() as session:
            user = session.query(Users).filter_by(user_id=user_id).first()
            if user is None:
                return False
            for key, value in kwargs.items():
                setattr(user, key, value)
            session.commit()
            return True
    
    @staticmethod
    def delete(user_id: int) -> bool:
        with Session() as session:
            user = session.query(Users).filter_by(user_id=user_id).first()
            if user is None:
                return False
            session.delete(user)
            session.commit()
            return True
    
    @staticmethod
    def delete_all() -> bool:
        with Session() as session:
            session.query(Users).delete()
            session.commit()
            return True
    
    @staticmethod
    def get_all() -> list:
        with Session() as session:
            users = session.query(Users).all()
            return users
    
    @staticmethod
    def get_all_by(**kwargs) -> list:
        with Session() as session:
            users = session.query(Users).filter_by(**kwargs).all()
            return users


Base.metadata.create_all(engine)
