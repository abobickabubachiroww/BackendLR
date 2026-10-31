from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from database import Base, engine, get_db
from models import Master

app = FastAPI()

# Создание таблиц в базе данных
Base.metadata.create_all(bind=engine)


# GET /masters
# Получение всех мастеров или фильтрация по специализации
@app.get("/masters")
def get_masters(
    specialization: str | None = None,
    db: Session = Depends(get_db)
):
    query = db.query(Master)

    # Если специализация передана, фильтруем мастеров
    if specialization is not None:
        query = query.filter(
            Master.specialization == specialization
        )

    masters = query.all()

    return [
        {
            "id": master.id,
            "name": master.name,
            "specialization": master.specialization
        }
        for master in masters
    ]


# GET /masters/{master_id}
# Получение одного мастера по ID
@app.get("/masters/{master_id}")
def get_master(
    master_id: int,
    db: Session = Depends(get_db)
):
    master = db.query(Master).filter(
        Master.id == master_id
    ).first()

    if master is None:
        raise HTTPException(
            status_code=404,
            detail="Master not found"
        )

    return {
        "id": master.id,
        "name": master.name,
        "specialization": master.specialization
    }