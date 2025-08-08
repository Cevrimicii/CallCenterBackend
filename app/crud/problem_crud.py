from sqlmodel import Session, select
from typing import List, Optional
from datetime import datetime
from app.models.problems import Problem
from app.db.database import engine


def get_problems() -> List[Problem]:
    """Tüm problemleri getir"""
    with Session(engine) as session:
        return session.exec(select(Problem)).all()


def get_problem_by_id(problem_id: int) -> Optional[Problem]:
    """ID'ye göre problem getir"""
    with Session(engine) as session:
        return session.get(Problem, problem_id)


def get_problems_by_location(location: str) -> List[Problem]:
    """Lokasyona göre problemleri getir"""
    with Session(engine) as session:
        query = select(Problem).where(Problem.location == location).where(Problem.status == "pending")
        return session.exec(query).all()


def get_problems_by_completion_time(completion_time: datetime) -> List[Problem]:
    """Tahmini tamamlanma zamanına göre problemleri getir"""
    with Session(engine) as session:
        query = select(Problem).where(Problem.estimated_completion_time <= completion_time)
        return session.exec(query).all()


def get_overdue_problems() -> List[Problem]:
    """Süresi geçmiş problemleri getir"""
    current_time = datetime.now()
    with Session(engine) as session:
        query = select(Problem).where(Problem.estimated_completion_time < current_time)
        return session.exec(query).all()


def create_problem(problem: Problem) -> Problem:
    """Yeni problem oluştur"""
    with Session(engine) as session:
        session.add(problem)
        session.commit()
        session.refresh(problem)
        return problem


def update_problem(problem_id: int, problem_data: dict) -> Optional[Problem]:
    """Problem bilgilerini güncelle"""
    with Session(engine) as session:
        problem = session.get(Problem, problem_id)
        if problem:
            for key, value in problem_data.items():
                setattr(problem, key, value)
            session.add(problem)
            session.commit()
            session.refresh(problem)
            return problem
        return None


def delete_problem(problem_id: int) -> bool:
    """Problem sil"""
    with Session(engine) as session:
        problem = session.get(Problem, problem_id)
        if problem:
            session.delete(problem)
            session.commit()
            return True
        return False


def search_problems_by_description(search_term: str) -> List[Problem]:
    """Problem açıklamasında arama yap"""
    with Session(engine) as session:
        query = select(Problem).where(Problem.problem.contains(search_term))
        return session.exec(query).all()


def get_problems_by_date_range(start_date: datetime, end_date: datetime) -> List[Problem]:
    """Belirli bir tarih aralığındaki problemleri getir"""
    with Session(engine) as session:
        query = select(Problem).where(
            Problem.estimated_completion_time >= start_date,
            Problem.estimated_completion_time <= end_date
        )
        return session.exec(query).all()
