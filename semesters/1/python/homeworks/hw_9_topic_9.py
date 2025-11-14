import os
import csv
from pathlib import Path

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker
from sqlalchemy import Integer, String, create_engine, func


class Base(DeclarativeBase):
    pass


class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    last_name: Mapped[str] = mapped_column(String)
    first_name: Mapped[str] = mapped_column(String)
    faculty: Mapped[str] = mapped_column(String)
    course: Mapped[str] = mapped_column(String)
    score: Mapped[int] = mapped_column(Integer)

    def __repr__(self):
        return f"{self.last_name} {self.first_name}"


class StudentsRepository:
    def __init__(self, host: str, port: int, user: str, password: str, db_name: str):
        db_url = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db_name}"
        engine = create_engine(url=db_url)
        self._session = sessionmaker(bind=engine)

        Base.metadata.create_all(bind=engine)

    def load_from_csv(self, file_path: Path) -> None:
        with self._session() as s:
            with file_path.open("r") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    s.add(
                        Student(
                            last_name=row["Фамилия"],
                            first_name=row["Имя"],
                            faculty=row["Факультет"],
                            course=row["Курс"],
                            score=int(row["Оценка"]),
                        )
                    )
            s.commit()

    def get_students_by_faculty(self, faculty: str):
        with self._session() as s:
            return (
                s.query(Student)
                .filter(Student.faculty == faculty)
                .distinct(Student.first_name, Student.last_name)
                .all()
            )

    def get_unique_courses(self):
        with self._session() as s:
            courses = s.query(Student.course).distinct().all()
            return [c.course for c in courses]

    def get_faculty_avg_score(self, faculty: str) -> float | None:
        with self._session() as s:
            avg_score = (
                s.query(func.avg(Student.score))
                .filter(Student.faculty == faculty)
                .scalar()
            )
            return float(avg_score) if avg_score else None

    def get_stoopid_students(self, course: str):
        with self._session() as s:
            return (
                s.query(Student)
                .filter(Student.course == course, Student.score < 30)
                .distinct(Student.first_name, Student.last_name)
                .all()
            )


if __name__ == "__main__":
    host = os.environ["DB_HOST"]
    port = int(os.environ["DB_PORT"])
    user = os.environ["DB_USER"]
    password = os.environ["DB_PASSWORD"]
    db_name = os.environ["DB_NAME"]
    sr = StudentsRepository(host, port, user, password, db_name)

    sr.load_from_csv(file_path=Path("files/hw9_topic9/students.csv"))
    for s in sr.get_students_by_faculty(faculty="ФПМИ"):
        print(s)

    for c in sr.get_unique_courses():
        print(c)

    print(sr.get_faculty_avg_score(faculty="ФПМИ"))

    for s in sr.get_stoopid_students(course="Физика"):
        print(s)
