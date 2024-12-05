from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import BigInteger, String, ForeignKey


class Base(DeclarativeBase):
    pass


class User(Base):
    """
    Таблица пользователей (учеников)
    """
    tg_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    first_name: Mapped[str] = mapped_column(String)
    last_name: Mapped[str] = mapped_column(String)
    # Связь с результатами егэ
    exam_results: Mapped[list["ExamResult"]] = relationship("ExamResult", back_populates="user")

    __tablename__ = 'users'


class Subject(Base):
    """
    Таблица школьных предметов
    """
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True)
    # Связь с результатами егэ
    exam_results: Mapped[list["ExamResult"]] = relationship("ExamResult", back_populates="subject")

    __tablename__ = 'subjects'


class ExamResult(Base):
    """
    Таблица результатов ЕГЭ
    """
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey(User.tg_id))
    subject_id: Mapped[int] = mapped_column(BigInteger, ForeignKey(Subject.id))
    score: Mapped[int] = mapped_column(BigInteger)

    # Связи с юзером и предметом
    user: Mapped[User] = relationship("User", back_populates="exam_results")
    subject: Mapped[Subject] = relationship("Subject", back_populates="exam_results")

    __tablename__ = 'exam_results'

