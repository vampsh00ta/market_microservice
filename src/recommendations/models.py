from datetime import datetime,timedelta

from sqlalchemy import MetaData, Table, Column, Integer, String, TIMESTAMP, ForeignKey, Boolean,DateTime
from sqlalchemy.orm import DeclarativeBase, relationship

class Base(DeclarativeBase):
    metadata = MetaData()

item_order = Table(
    "item_order",
    Base.metadata,
    Column("item_id", ForeignKey("items.id"), primary_key=True),
    Column("order_id", ForeignKey("orders.id"), primary_key=True),
)

item_category = Table(
    "item_category_ref",
    Base.metadata,
    Column("item_id", ForeignKey("items.id"), primary_key=True),
    Column("category_id", ForeignKey("categories.id"), primary_key=True),
)

user_item_recommendation = Table(
    "user_item_ref_recommendation",
    Base.metadata,
    Column("item_id", ForeignKey("items.id"), primary_key=True),
    Column("user_id", ForeignKey("customers.id"), primary_key=True),
)

user_item = Table(
    "user_item_ref",
    Base.metadata,
    Column("item_id", ForeignKey("items.id"), primary_key=True),
    Column("user_id", ForeignKey("customers.id"), primary_key=True),
)
class Item(Base):
    __tablename__ = 'items'
    id = Column(Integer,primary_key=True)
    is_active = Column(Boolean,default=True)
    publish_time = Column(DateTime,default=datetime.utcnow())
    expiring_at = Column(DateTime,default=datetime.utcnow()+timedelta(minutes = 1))
    change_item = Column(DateTime,default=datetime.utcnow())
    name = Column(String,nullable=False)
    price = Column(String,nullable=False)
    brand = Column(String,nullable=True)
    image = Column(String,nullable=True)
    size = Column(String,nullable=False)
    recommendation_users = relationship("User", backref="recommendation_users",lazy="selectin", secondary=user_item_recommendation)
    used = Column(Boolean,nullable=False)
    category =  relationship("Category", backref="category_item", lazy="selectin",secondary=item_category)
    orders = relationship("Order", backref="item_orders",lazy="selectin", secondary=item_order)
    owner_id = Column(Integer, ForeignKey('customers.id'),nullable=False)
    liked_by = relationship("User", backref="liked_by",lazy="selectin", secondary=user_item)
    def __str__(self):
        return f"{self.name}"


class User(Base):
    __tablename__ = "customers"
    id = Column(Integer,primary_key=True)
    email = Column(String, nullable=False)
    items = relationship("Item", backref="user_items",lazy="selectin")
    username = Column(String, nullable=False)
    registered_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP,default=datetime.utcnow)
    orders = relationship("Order", backref="user_orders",lazy="joined")
    recommendation_items = relationship("Item", backref="recommendation_items",lazy="selectin", secondary=user_item_recommendation)
    hashed_password = Column(String(length=1024), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_superuser = Column( Boolean, default=False, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    liked_items = relationship("Item", backref="liked_items",lazy="selectin", secondary=user_item)
