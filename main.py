import select

from fastapi import FastAPI, Depends, HTTPException
from contextlib import asynccontextmanager
from fastapi import FastAPI
from database import create_db_and_tables, get_session
import models  # tabloların kaydolması için import şart
from sqlmodel import Session, select
app = FastAPI()

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)


@app.get("/ping")
def ping():
    return {"status": "ok"}

@app.post("/snippets", response_model=models.SnippetRead)
def create_snippet(payload: models.SnippetCreate, session: Session = Depends(get_session)):
    tag_objects = []
    for name in payload.tags:
        existing = session.exec(select(models.Tag).where(models.Tag.name == name)).first()
        if existing:
            tag_objects.append(existing)
        else:
            new_tag = models.Tag(name=name)
            tag_objects.append(new_tag)
    snippet = models.Snippet(
        title=payload.title,
        language=payload.language,
        body=payload.body,
        tags=tag_objects,
    )       
    session.add(snippet)
    session.commit()
    session.refresh(snippet)
    return models.SnippetRead(
        id=snippet.id,
        title=snippet.title,
        language=snippet.language,
        body=snippet.body,
        tags=[t.name for t in snippet.tags],
    )
@app.get("/snippets", response_model=list[models.SnippetRead])
def list_snippets(session: Session = Depends(get_session)):
    snippets = session.exec(select(models.Snippet)).all()   
    return [
        models.SnippetRead(
            id=s.id,
            title=s.title,
            language=s.language,
            body=s.body,
            tags=[t.name for t in s.tags],
        )
        for s in snippets
    ]
@app.get("/snippets/{snippet_id}", response_model=models.SnippetRead)
def get_snippet(snippet_id: int, session: Session = Depends(get_session)):
    snippet = session.get(models.Snippet, snippet_id)
    if not snippet:
        raise HTTPException(status_code=404, detail="Snippet bulunamadı")
    return models.SnippetRead(
        id=snippet.id,
        title=snippet.title,
        language=snippet.language,
        body=snippet.body,
        tags=[t.name for t in snippet.tags],
    )

@app.delete("/snippets/{snippet_id}", status_code=204)
def delete_snippet(snippet_id: int, session: Session = Depends(get_session)):
    snippet = session.get(models.Snippet, snippet_id)
    if not snippet:
        raise HTTPException(status_code=404, detail="Snippet bulunamadı")
    session.delete(snippet)
    session.commit()