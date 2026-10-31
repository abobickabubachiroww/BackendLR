from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from database import Base, engine, get_db
from models import Category, Service
from schemas import ServiceCreate


app = FastAPI()


# Создание таблиц в базе данных
Base.metadata.create_all(bind=engine)


# Добавление тестовых категорий при первом запуске
def create_default_categories():
    db = next(get_db())

    try:
        if db.query(Category).count() == 0:
            categories = [
                Category(name="Стрижки и укладки"),
                Category(name="Окрашивание"),
                Category(name="Наращивание ресниц")
            ]

            db.add_all(categories)
            db.commit()
    finally:
        db.close()


create_default_categories()


# POST /services — создание новой услуги
@app.post("/services", status_code=201)
def create_service(
    service: ServiceCreate,
    db: Session = Depends(get_db)
):
    # Проверяем существование категории
    category = db.query(Category).filter(
        Category.id == service.categoryId
    ).first()

    if category is None:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )

    # Создаём новую услугу
    new_service = Service(
        category_id=service.categoryId,
        title=service.title,
        desc=service.desc,
        duration=service.duration,
        price=service.price
    )

    # Сохраняем услугу в базе данных
    db.add(new_service)
    db.commit()
    db.refresh(new_service)

    # Возвращаем информацию о созданной услуге
    return {
        "id": new_service.id,
        "categoryId": new_service.category_id,
        "title": new_service.title,
        "desc": new_service.desc,
        "duration": new_service.duration,
        "price": new_service.price
    }