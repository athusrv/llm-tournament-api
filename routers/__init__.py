
from fastapi import APIRouter

from ..data import load_prompts
from ..models import Vote, Result

router = APIRouter()

prompts = load_prompts()

current = 0
matchups = [(p1, p2) for i, p1 in enumerate(prompts) for j, p2 in enumerate(prompts) if i != j]
scores = {p.id: 0 for p in prompts}


@router.get("/matchup")
def get_matchup():
    global current
    if current >= len(matchups):
        winner = max(scores, key=scores.get)
        best = next(p for p in prompts if p.id == winner)
        return {"winner": best}
    p1, p2 = matchups[current]
    return [p1, p2]


@router.get("/results")
def get_results():
    ranked = sorted(prompts, key=lambda p: scores[p.id], reverse=True)
    return [Result(prompt=p, score=scores[p.id]) for p in ranked]

@router.post("/vote")
def post_vote(vote: Vote):
    global current
    scores[vote.winner_id] += 1
    current += 1
    return get_results()

@router.post("/reset")
def reset_tournament():
    global current, scores
    current = 0
    scores = {p.id: 0 for p in prompts}
    return get_matchup()
