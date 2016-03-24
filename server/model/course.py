from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.schema import UniqueConstraint
from server.library.model import Serializable
from server.database import Model
from server.model.institution import Institution

class Course(Model, Serializable):
    __tablename__ = "course"
    __table_args__ = (
        UniqueConstraint("code", "institution_id"),
    )

    id = Column(Integer, primary_key=True)
    code = Column(String)
    name = Column(String)
    
    # Foreign keys
    institution_id = Column(Integer, ForeignKey("institution.id"))

    # Relationships
    papers = relationship("Paper", lazy="joined")

    def __init__(self, name, code, institution):
        self.name = name
        self.code = code

        if isinstance(institution, Institution):
            self.institution = institution
        else:
            self.institution_id = institution