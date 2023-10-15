import torch
from typing import List
from src.referee_model import get_result_direct


def double_loop_match(question: str, evaluated_answer: str, scored_answers: List[str]):
    xc = 0
    xs = [0] * len(scored_answers)
    tmp = -(len(xs)-1)*2
    for i in range(len(xs)):
        xs[i] = tmp
        tmp += 4
    for i in range(len(xs)):
        tag = get_result_direct(question, evaluated_answer, scored_answers[i])
        if tag == 0:
            xc += 1
            xs[i] -= 1
        elif tag == 1:
            xc -= 1
            xs[i] += 1
        elif tag == 2:
            pass
        tag = get_result_direct(question, scored_answers[i], evaluated_answer)
        if tag == 0:
            xc -= 1
            xs[i] += 1
        elif tag == 1:
            xc += 1
            xs[i] -= 1
        elif tag == 2:
            pass
    return xc, xs

def double_loop_score(xc: int, xs: List[int], ys: List[int]) -> float:
    assert len(xs) == len(ys)
    num_scored_answers = len(xs)
    if xc > xs[-1]:
        return ys[-1]
    if xc < xs[0]:
        return ys[0]
    for i in range(num_scored_answers-1):
        if xc == xs[i]:
            if xc == xs[i+1]:
                return (ys[i]+ys[i+1])/2
            else:
                return ys[i]
    if xc == xs[-1]:
        return ys[-1]
    for i in range(num_scored_answers):
        if xc < xs[i]:
            l = i-1
            r = i
            break
    yl = ys[l]
    yr = ys[r]
    xs = torch.tensor(xs, dtype=torch.float)
    ys = torch.tensor(ys, dtype=torch.float)
    deltaxs = xs-xc
    d = torch.zeros(num_scored_answers)
    d[:r] = torch.arange(1, r+1).flip(dims=[0])
    d[r:] = torch.arange(1, num_scored_answers-r+1)
    tmp: torch.Tensor = 1/deltaxs/d.pow(2)
    yc = (yl+yr)/2+(yr-yl)/2*tmp.sum(dim=0)/tmp.abs().sum(dim=0)
    return float(yc)




    
