from _ast import List

from fastapi import FastAPI
from h11 import Request
from pydantic import BaseModel
from starlette.responses import JSONResponse

app = FastAPI()

@app.get("/hello")
def read_hello():
    return JSONResponse(
        content={"message": "Hello world"},
        status_code=200
    )

@app.get("/welcome")
def read_welcome(name: str):
    return JSONResponse(
        content={"message": f"Welcome: {name}"}
    )


class InformationStudents(BaseModel):
    Reference: str
    FirstName: str
    LastName : str
    age : int

event_store: list[InformationStudents] = []

def serialized_stored_event():
    return [event.model_dump() for event in event_store]

@app.post("/students")
def create_student(student: list[InformationStudents]):
    events_converted = []
    for new_student in student:
        events_converted.append(new_student.model_dump())
    return events_converted


@app.get("/students")
def students_list():
    return {"events": serialized_stored_event()}

@app.put("/students")
def student_refence(student: list[InformationStudents]):
    for students in student:
        if students.Reference == student.Reference:
            event_store.append(students)
            break
        return {"events": serialized_stored_event()}
