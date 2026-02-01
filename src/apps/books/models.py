from datetime import datetime

from sqlalchemy.sql import func, expression
from sqlalchemy.dialects.postgresql import TEXT
from sqlalchemy import (
    Column,
    SmallInteger,
    Integer,
    String,
    DateTime,
    Index,
    Boolean,
    ForeignKey,
)
from sqlalchemy.orm import relationship

from src.core.database import Base


class BookShelf(Base):
    """书架"""

    __tablename__ = "book_shelf"
    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, index=True)  # 书籍ID
    book_name = Column(String(100))  # 书籍名称
    cover = Column(String(300))  # 封面图片（文件名）
    user_id = Column(Integer)  # 用户id
    created = Column(DateTime, server_default=func.now())  # 创建时间
    updated = Column(DateTime, server_default=func.now())  # 更新时间
    Index("ix_book_id_user_id", "book_id", "user_id", unique=True)


class ReadRate(Base):
    """阅读进度"""

    __tablename__ = "read_rate"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    book_id = Column(Integer)
    chapter_id = Column(Integer)  # 章节id
    chapter_name = Column(String(100))  # 章节名称
    rate = Column(Integer, default=0)  # 阅读进度(百分率分子)
    created = Column(DateTime, server_default=func.now())  # 创建时间


class Book(Base):
    """书籍基本信息"""

    __tablename__ = "book"
    book_id = Column(Integer, primary_key=True)  # 书籍ID
    channel_book_id = Column(String(20), unique=True)  # 渠道书籍id 渠道名:书籍id
    book_name = Column(String(100))  # 书籍名称
    cate_id = Column(Integer, index=True)  # 书籍二级分类ID
    cate_name = Column(String(50))  # 书籍二级分类名称
    channel_type = Column(
        SmallInteger(), index=True
    )  # 书籍频道（1：男；2: 女 3: 出版 0: 无此属性默认为0）
    author_name = Column(String(50))  # 作者
    chapter_num = Column(Integer)  # 章节数量
    is_publish = Column(Integer)  # 是否出版（1：是；2：否）
    status = Column(Integer)  # 连载状态（1：未完结；2：已完结）
    create_time = Column(DateTime)  # 创建时间（第三方）
    cover = Column(String(300))  # 封面图片（链接）
    intro = Column(TEXT)  # 简介
    word_count = Column(Integer)  # 字数
    update_time = Column(DateTime)  # 更新时间
    created = Column(DateTime, server_default=func.now())  # 创建时间
    showed: bool = Column(Boolean, server_default=expression.true())  # 是否上架
    source = Column(String(50))  # 来源
    ranking = Column(Integer, server_default="0")  # 排序
    short_des = Column(String(50), server_default="")  # 短描述

    collect_count = Column(Integer, server_default="0")  # 被收藏数量
    heat = Column(Integer, server_default="0")  # 热度

    def __init__(self, data: dict) -> None:
        self.channel_book_id = data["channel_book_id"]
        self.book_name = data["book_name"]
        self.cate_id = int(data["cate_id"])
        self.channel_type = int(data["channel_type"])
        self.author_name = data["author_name"]
        self.chapter_num = data["chapter_num"]
        self.is_publish = data["is_publish"]
        self.status = data["status"]
        self.create_time = data["create_time"]
        self.cover = data["cover"]
        self.intro = data["intro"]
        self.word_count = int(data["word_count"])
        self.update_time = data["update_time"]
        self.source = data["source"]
        self.created = datetime.now()


class BookCategoryRelation(Base):
    """
    分类和一级分类的关系
    多对多关系
    """

    __tablename__ = "book_category_relation"
    id = Column(Integer, primary_key=True)
    big_cate_id = Column(Integer, ForeignKey("book_big_category.cate_id"))
    cate_id = Column(Integer, ForeignKey("book_category.cate_id"))


class BookBigCategory(Base):
    """书籍一级分类信息"""

    __tablename__ = "book_big_category"

    cate_id = Column(Integer, primary_key=True)  # 分类ID
    cate_name = Column(String(50))  # 分类名称
    channel = Column(Integer)  # 频道  1:男生, 2:女生
    showed: bool = Column(Boolean, server_default=expression.true())
    icon = Column(String(100))

    second_cates = relationship("BookCategory", secondary=BookCategoryRelation.__table__)
    created = Column(DateTime, server_default=func.now())  # 创建时间


class BookCategory(Base):
    """书籍分类信息"""

    __tablename__ = "book_category"
    cate_id = Column(Integer, primary_key=True)  # 分类ID
    cate_name = Column(String(50))  # 分类名称
    showed: bool = Column(Boolean, server_default=expression.true())
    icon = Column(String(100))
    created = Column(DateTime, server_default=func.now())  # 创建时间


class BookVolume(Base):
    """书籍卷节信息"""

    __tablename__ = "book_volume"
    id = Column(Integer, primary_key=True)  # ID
    book_id = Column(Integer, index=True)  # 书籍ID
    volume_id = Column(Integer, index=True)  # 卷ID
    volume_name = Column(String(100))  # 卷名
    create_time = Column(DateTime, default=datetime.now())  # 创建时间（第三方）
    chapter_count = Column(Integer, default=0)  # 卷字数
    update_time = Column(DateTime, default=datetime.now())  # 更新时间（第三方）
    created = Column(DateTime, server_default=func.now())  # 创建时间


class BookChapters(Base):
    """书籍章节信息"""

    __tablename__ = "book_chapters"

    id = Column(Integer, primary_key=True)  # ID
    book_id = Column(Integer, index=True)  # 书籍ID
    volume_id = Column(Integer, index=True)  # 卷ID
    chapter_id = Column(Integer, index=True)  # 章节ID
    chapter_name = Column(String(100))  # 章节名称
    word_count = Column(Integer)  # 字数

    create_time = Column(DateTime)  # 创建时间（第三方）
    update_time = Column(DateTime)  # 更新时间（第三方）
    created = Column(DateTime, server_default=func.now())  # 创建时间

    def __init__(self, data: dict) -> None:
        self.book_id = int(data["book_id"])
        self.volume_id = int(data["volume_id"])
        self.chapter_id = int(data["chapter_id"])
        self.chapter_name = data["chapter_name"]
        self.word_count = int(data["word_count"])
        self.create_time = data["create_time"]
        self.update_time = data["update_time"]


class BookChapterContent(Base):
    """书籍章节内容信息"""

    __tablename__ = "book_chapter_content"
    id = Column(Integer, primary_key=True)  # ID
    book_id = Column(Integer)  # 书籍ID
    volume_id = Column(Integer)  # 卷ID
    chapter_id = Column(Integer)  # 章节ID
    content = Column(TEXT)  # 章节内容
    created = Column(DateTime, server_default=func.now())  # 创建时间

    Index("ix_book_id_chapter_id", "book_id", "chapter_id")

    def __init__(self, data: dict) -> None:
        self.book_id = int(data["book_id"])
        self.volume_id = int(data["volume_id"])
        self.chapter_id = int(data["chapter_id"])
        self.content = data["content"].replace("　", "").replace(" ", "")

    def update(self, data: dict) -> None:
        self.content = data["content"].replace("　", "").replace(" ", "")
