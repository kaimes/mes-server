from typing import List, Optional

from sqlalchemy import Column, Integer, String, Boolean, JSON
from sqlalchemy_utils import TSVectorType

from dispatch.database import Base
from dispatch.models import DispatchBase,TimeStampMixin
from dispatch.plugins.base import plugins
from sqlalchemy.orm import relationship

class Plugin(Base,TimeStampMixin):
    __tablename__ = 'plugin' 

    __table_args__ = {"schema": "dispatch_core"}
    id = Column(Integer, primary_key=True)
    title = Column(String)
    slug = Column(String, unique=True)
    description = Column(String)
    version = Column(String)
    author = Column(String)
    author_url = Column(String)
    type = Column(String)
    enabled = Column(Boolean)
    required = Column(Boolean)
    multiple = Column(Boolean)
    config = Column(JSON)

    config_form_spec = Column(JSON)  # Column(String, default='{"key_1":["skill_1"]}')
    # service_pluagin = relationship("ServicePlugin", back_populates="plugin", foreign_keys="[ServicePlugin.service_id]")
    # service_pluagin = relationship("ServicePlugin", back_populates="plugin", foreign_keys="[ServicePlugin.plugin_id]")

    plugins = relationship("ServicePlugin", back_populates="plugin", foreign_keys="[ServicePlugin.plugin_id]")

    @property
    def instance(self):
        """Fetches a plugin instance that matches this record."""
        p = plugins.get(self.slug)
        print("getting by slug", self.slug, p)
        return plugins.get(self.slug)

    search_vector = Column(TSVectorType("title", "slug", "type"))


# Pydantic models...
class PluginBase(DispatchBase):
    pass


class PluginCreate(PluginBase):
    title: str
    slug: str
    author: str
    author_url: str
    type: str
    enabled: Optional[bool]
    required: Optional[bool] = True
    multiple: Optional[bool] = False
    description: Optional[str]
    config: Optional[dict]
    config_form_spec: Optional[dict]


class PluginUpdate(PluginBase):
    id: int
    title: str
    slug: str
    author: str
    author_url: str
    type: str
    enabled: Optional[bool]
    required: Optional[bool] = True
    multiple: Optional[bool] = False
    description: Optional[str]
    config: Optional[dict]

    # Not able to update
    # config_form_spec: Optional[dict]


class PluginRead(PluginBase):
    id: int
    title: str
    slug: str
    author: str
    author_url: str
    type: str
    enabled: bool
    required: bool
    multiple: bool
    description: Optional[str]
    config: Optional[dict]
    config_form_spec: Optional[dict]


class KeyValue(DispatchBase):
    key: str
    value: str


class PluginMetadata(DispatchBase):
    slug: str
    metadata: List[KeyValue] = []


class PluginPagination(DispatchBase):
    total: int
    items: List[PluginRead] = []
    page: int 
    itemsPerPage: int 


class PluginType(DispatchBase):
    plugin_type:  List[str] = []
