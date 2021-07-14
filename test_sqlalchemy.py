# coding:utf-8
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint, Index
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import create_engine

engine = create_engine("mysql+pymysql://root:root001@127.0.0.1:3306/test", max_overflow=5)

Base = declarative_base()


class Parent(Base):
    __tablename__ = 'parent'
    id = Column(Integer, primary_key=True)
    name = Column(String(20))
    child = relationship("Child", uselist=False, back_populates="parent")


class Child(Base):
    __tablename__ = 'child'
    id = Column(Integer, primary_key=True)
    name = Column(String(20))
    parent_id = Column(Integer, ForeignKey('parent.id'))
    parent = relationship("Parent", back_populates="child")


p1 = Parent(id=1,name='刘备')
p2 = Parent(id=2,name='关羽')
c1 = Child(id=3,name='刘禅')
c2 = Child(id=4,name='关云')

p1.child=c1
p2.child=c2
p1.child=c2
print(p1.child,c2.parent,p2.child)
