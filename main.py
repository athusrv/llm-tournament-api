from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

# from api.data import load_prompts
from api.models import Result, Vote

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


prompts = []

current = 0
matchups = [(p1, p2) for i, p1 in enumerate(prompts) for j, p2 in enumerate(prompts) if i != j]
scores = {p.id: 0 for p in prompts}


@app.get("/matchup")
def get_matchup():
    global current
    if current >= len(matchups):
        winner = max(scores, key=scores.get)
        best = next(p for p in prompts if p.id == winner)
        return {"winner": best}
    p1, p2 = matchups[current]
    return [p1, p2]


@app.get("/results")
def get_results():
    ranked = sorted(prompts, key=lambda p: scores[p.id], reverse=True)
    return [Result(prompt=p, score=scores[p.id]) for p in ranked]

@app.post("/vote")
def post_vote(vote: Vote):
    global current
    scores[vote.winner_id] += 1
    current += 1
    return get_results()

@app.post("/reset")
def reset_tournament():
    global current, scores
    current = 0
    scores = {p.id: 0 for p in prompts}
    return get_matchup()


@app.get("/", response_class=HTMLResponse)
def read_root():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
    </head>
    <body>
    </body>
    </html>
    """
