from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func

from src.utils.models import BaseModel


class User(BaseModel):
    """用户表"""

    open_id = Column(String(128), unique=True, doc="mini-program user info")
    nick_name = Column(String(50))
    gender = Column(Integer(), server_default="0", doc="1男,0女")
    city = Column(String(120))
    province = Column(String(120))
    country = Column(String(120))
    avatar_url = Column(String(200))

    # 阅读器配置
    preference = Column(Integer(), server_default="0", doc="0女,1男")
    brightness = Column(Integer(), server_default="30", doc="10~100 亮度")
    fontSize = Column(Integer(), server_default="14", doc="字号")
    background = Column(String(10), default="B1", doc="B1~B6内置背景")
    turn = Column(String(10), default="T1", doc="T1仿真,T2平滑,T3无翻页模式")
    last_read = Column(Integer(), doc="最后阅读一本书")
    last_read_chapter_id = Column(Integer(), doc="最后阅读一本书的章节id")
    modified_time = Column(DateTime(), server_default=func.now())

    __tablename__ = "user"
