from fastapi import FastAPI, HTTPException
import uvicorn

app = FastAPI()

categories = [
    {"id": 1, "name": "Стрижки и укладки", "servicesCount": 5},
    {"id": 2, "name": "Маникюр и педикюр", "servicesCount": 5},
    {"id": 3, "name": "Брови и ресницы", "servicesCount": 4},
    {"id": 4, "name": "Спа-процедуры", "servicesCount": 4}
]


@app.get("/categories")
def list_categories():
    return categories

@app.get("/categories/{category_id}")
def get_category(category_id: int):
    for category in categories:
        if category["id"] == category_id:
            return category
    raise HTTPException(404, detail="Category not found")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)

#http://127.0.0.1:8000/categories