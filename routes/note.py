from fastapi import APIRouter
from models.note import Note
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from config.db import conn
from schemas.note import noteEntity, notesEntity
from fastapi.templating import Jinja2Templates
note = APIRouter()
templates = Jinja2Templates(directory="templates")

@note.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
        docs = conn.notes.notes.find({})
        newdocs = []
        for doc in docs:
            newdocs.append({
            "id": str(doc["_id"]),
            "title": doc["title"],
            "description": doc["description"],
            "important": doc["important"],

        })
        return templates.TemplateResponse(
            request=request, name="index.html", context={"newdocs": newdocs})

@note.post("/")
async def create_item(request: Request):
    form = await request.form()
    formdic = dict(form)
    formdic["important"] = True if formdic.get("important") == "on" else False
    conn.notes.notes.insert_one(formdic)
    return {"success": True}


