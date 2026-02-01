from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func

from src.core.database import Base


class User(Base):
    """用户表"""

    __tablename__ = "user"
    id = Column(Integer(), primary_key=True)
    # 小程序 user_info
    openId = Column(String(128), unique=True)
    nickName = Column(String(50))
    gender = Column(Integer(), server_default="0")  # 1 男 0 女
    city = Column(String(120))
    province = Column(String(120))
    country = Column(String(120))
    avatarUrl = Column(String(200))

    # 阅读器配置
    preference = Column(Integer(), server_default="0")  # 0 女 1 男
    brightness = Column(Integer(), server_default="30")  # 10~100 亮度
    fontSize = Column(Integer(), server_default="14")  # 字号
    background = Column(String(10), default="B1")  # B1 ~ B6 内置背景
    turn = Column(String(10), default="T1")  # T1 仿真 T2 平滑 T3 无 翻页模式

    last_read = Column(Integer())  # 最后阅读一本书
    last_read_chapter_id = Column(Integer())  # 最后阅读一本书的章节id

    modified = Column(DateTime(), server_default=func.now())
    created = Column(DateTime(), server_default=func.now())

    def __init__(self, data: dict) -> None:
        self.openId = data["openId"]
        self.update_info(data)

    def update_info(self, data: dict) -> None:
        self.nickName = data["nickName"]
        self.gender = data["gender"]
        self.city = data["city"]
        self.province = data["province"]
        self.country = data["country"]
        self.avatarUrl = data["avatarUrl"]
