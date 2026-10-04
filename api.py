import uvicorn
 
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="HCI Mini Review App API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

questions = [{
                "id": 0,
                "q": "Is Fitts' Law an example of a predictive model or a descriptive model?",
                "a": "Predictive model"
                },
             {
                "id": 1,
                "q": "Does this course focus more on genius design, systems design, or user-centered design?",
                "a": "User-centered design"
                },
             {
                "id": 2,
                "q": "What is the main goal of the ideation phase of iterative design?",
                "a": "Generating as many possible design solutions as possible"
                }
            ]

class QuestionRequest(BaseModel):
    question: str
    answer: str

@app.get("/questions")
def get_questions():
    return questions

@app.post("/add")
def add_question(req: QuestionRequest):
    questions.append({ 
        "id": len(questions),
        "q": req.question,
        "a": req.answer
    })

@app.delete("/delete/{id}")
def delete_question(id: int):
    for q in questions:
        if id in q.values():
            questions.remove(q)
            return
        else: continue
        
    raise HTTPException(status.HTTP_404_NOT_FOUND, f"Question with ID {id} not found")

@app.put("/update/{id}")
def update_question(id: int, req: QuestionRequest):
    for q in questions:
        if id in q.values():
            q.update({"q": req.question, "a": req.answer})
            return
        else: continue
            
    raise HTTPException(status.HTTP_404_NOT_FOUND, f"Question with ID {id} not found")

if __name__=="__main__":
    uvicorn.run(app, port=8005)