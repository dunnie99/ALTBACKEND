from fastapi import FastAPI, HTTPException

app = FastAPI()

# In-memory storage for students
students = {}

# Create a Student resource
@app.post("/students/")
def create_student(student_id: int, name: str, age: int, sex: str, height: float):
    if student_id in students:
        raise HTTPException(status_code=400, detail="Student already exists")
    students[student_id] = {"name": name, "age": age, "sex": sex, "height": height}
    return students[student_id]

# Retrieve a single Student resource
@app.get("/students/{student_id}")
def get_student(student_id: int):
    if student_id not in students:
        raise HTTPException(status_code=404, detail="Student not found")
    return students[student_id]

# Retrieve many Students
@app.get("/students/")
def get_students():
    return students

# Update a Student resource
@app.put("/students/{student_id}")
def update_student(student_id: int, name: str = None, age: int = None, sex: str = None, height: float = None):
    if student_id not in students:
        raise HTTPException(status_code=404, detail="Student not found")
    if name is not None:
        students[student_id]["name"] = name
    if age is not None:
        students[student_id]["age"] = age
    if sex is not None:
        students[student_id]["sex"] = sex
    if height is not None:
        students[student_id]["height"] = height
    return students[student_id]

# Delete a Student resource
@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    if student_id not in students:
        raise HTTPException(status_code=404, detail="Student not found")
    del students[student_id]
    return {"detail": "Student deleted"}
