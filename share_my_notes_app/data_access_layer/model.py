from sqlalchemy import Column, Integer, String, Text, ForeignKey, Text

from sqlalchemy.orm import registry
from sqlalchemy.orm import relationship

mapper_registry = registry()

@mapper_registry.mapped
class Note:
    __tablename__ = 'note'

    id = Column(Integer, primary_key=True)
    content = Column(Text)
    session_id = Column(Integer, ForeignKey('session.id'))


@mapper_registry.mapped
class Session:
    __tablename__ = 'session'

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    password = Column(String(100))

    # notes = relationship("Note", back_populates="note")
