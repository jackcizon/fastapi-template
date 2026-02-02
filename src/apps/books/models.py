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
)

from src.utils.models import BaseModel


class BookChapterContent(BaseModel):
    """书籍章节内容信息"""

    book_id = Column(Integer(), index=True, doc="书籍ID")
    volume_id = Column(Integer(), doc="卷ID")
    chapter_id = Column(Integer(), doc="章节ID")
    content = Column(TEXT(), nullable=True, doc="章节内容")

    __tablename__ = "book_chapter_content"
    __table_args__ = (Index("ix_book_id_chapter_id", "book_id", "chapter_id"),)


class BookChapter(BaseModel):
    """书籍章节信息"""

    book_id = Column(Integer(), index=True)
    volume_id = Column(Integer(), index=True)

    name = Column(String(100), nullable=False)
    word_count = Column(Integer(), server_default="0")

    create_time = Column(DateTime(), server_default=func.now())  # 创建时间（第三方）
    update_time = Column(DateTime(), server_default=func.now())  # 更新时间（第三方）

    __tablename__ = "book_chapters"


class BookVolume(BaseModel):
    """书籍卷节信息"""

    book_id = Column(Integer(), index=True)
    volume_id = Column(Integer(), index=True)

    name = Column(String(100), nullable=False)
    chapter_count = Column(Integer(), server_default="0")  # 卷字数

    create_time = Column(DateTime(), server_default=func.now())  # 创建时间（第三方）
    update_time = Column(DateTime(), server_default=func.now())  # 更新时间（第三方）

    __tablename__ = "book_volume"


class Book(BaseModel):
    """书籍基本信息"""

    cate_id = Column(Integer(), index=True, doc="书籍二级分类ID")

    name = Column(String(100))
    cover = Column(String(300), doc="封面图片（链接）")
    intro = Column(TEXT())
    word_count = Column(Integer())
    showed: bool = Column(Boolean(), server_default=expression.true(), doc="是否上架")
    source = Column(String(50))
    ranking = Column(Integer(), server_default="0", doc="排序")
    short_des = Column(String(50), server_default="", doc="短描述")
    collect_count = Column(Integer(), server_default="0")
    heat = Column(Integer(), server_default="0")
    status = Column(Integer(), doc="连载状态（1：未完结；2：已完结）")
    channel_book_id = Column(String(20), unique=True, doc="渠道书籍id 渠道名:书籍id")
    channel_type = Column(SmallInteger(), doc="书籍频道.1男,2女,3出版,0无此属性.默认为0")
    author_name = Column(String(50))  # 作者
    chapter_num = Column(Integer())  # 章节数量
    is_publish = Column(Integer())  # 是否出版（1：是；2：否）
    create_time = Column(DateTime)  # 创建时间（第三方）
    update_time = Column(DateTime())  # 更新时间

    __tablename__ = "book"


class ReadRate(BaseModel):
    """阅读进度"""

    user_id = Column(Integer())
    book_id = Column(Integer())
    chapter_id = Column(Integer())  # 章节id
    chapter_name = Column(String(100))  # 章节名称
    rate = Column(Integer(), default=0)  # 阅读进度(百分率分子)

    __tablename__ = "read_rate"


class BookCategory(BaseModel):
    """书籍(子)分类信息"""

    name = Column(String(50))  # 分类名称
    showed: bool = Column(Boolean(), server_default=expression.true())
    icon = Column(String(100))

    __tablename__ = "book_category"


class BookCategoryRelation(BaseModel):
    """
    分类和一级分类的关系
    (N-2-N)
    """

    big_cate_id = Column(Integer(), index=True, nullable=False)
    cate_id = Column(Integer(), index=True, nullable=False)

    __tablename__ = "book_category_relation"
    __table_args__ = (Index("ix_big_cate_cate", "big_cate_id", "cate_id", unique=True),)


class BookBigCategory(BaseModel):
    """书籍一级分类信息"""

    name = Column(String(50))  # 分类名称
    channel = Column(Integer())  # 频道  1:男生, 2:女生
    showed: bool = Column(Boolean(), server_default=expression.true())
    icon = Column(String(100))

    __tablename__ = "book_big_category"


class BookShelf(BaseModel):
    """书架"""

    book_id = Column(Integer(), index=True)  # 书籍ID
    user_id = Column(Integer(), index=True)  # 用户id

    book_name = Column(String(100))  # 书籍名称
    cover = Column(String(300))  # 封面图片（文件名）
    updated = Column(DateTime(), server_default=func.now())  # 更新时间

    __tablename__ = "book_shelf"
    __table_args__ = (Index("ix_book_user", "book_id", "user_id", unique=True),)
