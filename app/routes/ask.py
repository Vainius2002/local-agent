from fastapi import APIRouter, Request, Form, Depends
from app.services.llm import invoke_question
from fastapi.templating import Jinja2Templates
from app.dependencies import get_current_user
from app.models.users import User

templates = Jinja2Templates(directory="app/templates")

router = APIRouter()

@router.get("/ask")
def main_page(request: Request, user: User = Depends(get_current_user)):
    return templates.TemplateResponse(request, "ask.html")

@router.post("/ask")
def ask(user: User = Depends(get_current_user), question: str = Form()):
    answer = invoke_question(question)
    return {"answer":answer}
    
