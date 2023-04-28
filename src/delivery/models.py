from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy.testing.schema import Table

from sqlalchemy import Integer, String, Column, ForeignKey, DateTime, Boolean, MetaData


class Base(DeclarativeBase):
    metadata = MetaData()

class DeliveryStatus(Base):
    __tablename__ = 'delivery_status'
    id = Column(Integer, primary_key=True,)
    current_city = Column(String(length=35), nullable=False)
    status_update = Column(DateTime,nullable=False)
    track_id  = Column(Integer, ForeignKey('delivery.track_id'),nullable=True)
    delivery_status_id  = Column(Integer, ForeignKey('delivery_status_name.id'),nullable=True)
    delivery_status = relationship("DeliveryStatusName", backref="delivery_status_name.delivery_status", lazy="selectin")



class DeliveryStatusName(Base):
    __tablename__ = 'delivery_status_name'
    id = Column(Integer, primary_key=True)
    name = Column(String(length=1024), nullable=False)
    delivery_status = relationship("DeliveryStatus", backref="delivery_status_name.delivery_status", lazy="selectin")


class Delivery(Base):
    __tablename__ = 'delivery'
    id = Column(Integer, primary_key=True)
    track_id = Column(Integer,unique=True)
    receiver_name = Column(String(length=300),nullable=False)
    telephone_number = Column(String(length=35),nullable=False)
    street = Column(String(length=300),nullable=False)
    city = Column(String(length=35),nullable=False)
    is_deliveried = Column(Boolean,nullable=False,default=False)
    dilivery_day = Column(DateTime, nullable=True)
    statuses = relationship("DeliveryStatus", foreign_keys=[DeliveryStatus.track_id],backref="delivery.statuses",lazy='selectin',)




