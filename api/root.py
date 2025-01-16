from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def root():
    return {"Leet Desenvolvimento de Programas de Computador LTDA"}