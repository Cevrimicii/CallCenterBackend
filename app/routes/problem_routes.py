from fastapi import APIRouter, HTTPException
from typing import List
from datetime import datetime
from app.crud.problem_crud import (
    get_problems,
    get_problem_by_id,
    get_problems_by_location,
    get_problems_by_completion_time,
    get_overdue_problems,
    create_problem,
    update_problem,
    delete_problem,
    search_problems_by_description,
    get_problems_by_date_range
)
from app.models.problems import Problem

router = APIRouter(
    prefix="/problems",
    tags=["problems"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=List[Problem])
def get_all_problems():
    """Tüm problemleri getir"""
    return get_problems()

@router.get("/{problem_id}", response_model=Problem)
def get_problem(problem_id: int):
    """ID'ye göre problem getir"""
    problem = get_problem_by_id(problem_id)
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")
    return problem

@router.get("/location/{location}", response_model=List[Problem])
def get_problems_by_location_route(location: str):
    """Lokasyona göre problemleri getir"""
    return get_problems_by_location(location)

@router.get("/overdue/all", response_model=List[Problem])
def get_overdue_problems_route():
    """Süresi geçmiş problemleri getir"""
    return get_overdue_problems()

@router.get("/search/{search_term}", response_model=List[Problem])
def search_problems(search_term: str):
    """Problem açıklamasında arama yap"""
    return search_problems_by_description(search_term)

@router.post("/", response_model=Problem)
def create_new_problem(problem: Problem):
    """Yeni problem oluştur"""
    return create_problem(problem)

@router.put("/{problem_id}", response_model=Problem)
def update_problem_info(problem_id: int, problem_data: dict):
    """Problem bilgilerini güncelle"""
    problem = update_problem(problem_id, problem_data)
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")
    return problem

@router.delete("/{problem_id}")
def delete_problem_by_id(problem_id: int):
    """Problem sil"""
    success = delete_problem(problem_id)
    if not success:
        raise HTTPException(status_code=404, detail="Problem not found")
    return {"message": "Problem deleted successfully"}

@router.get("/date-range/{start_date}/{end_date}", response_model=List[Problem])
def get_problems_by_date_range_route(start_date: datetime, end_date: datetime):
    """Belirli bir tarih aralığındaki problemleri getir"""
    return get_problems_by_date_range(start_date, end_date)

@router.put("/{problem_id}/status/{status}")
def update_problem_status(problem_id: int, status: str):
    """Problem durumunu güncelle (pending, in_progress, completed)"""
    problem_data = {"status": status, "updated_at": datetime.utcnow()}
    problem = update_problem(problem_id, problem_data)
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")
    return {"message": f"Problem status updated to {status}", "problem_id": problem.id}
