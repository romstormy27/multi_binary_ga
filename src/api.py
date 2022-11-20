from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

import src.main as main

class InputParams(BaseModel):

    n_chrom: int
    max_gen: int
    fit_expr: str
    lower_x1: float
    upper_x1: float
    lower_x2: float
    upper_x2: float
    precision: int
    crossover_rate: float
    mutation_rate: float

app = FastAPI()

@app.get("/")
async def home():
    return {"Hello": "World"}

@app.post("/run")
async def run(params: InputParams):

    params = dict(params)

    try:
    
        last_gen, solution_list = main.main(params)

        best_gen = main.get_best_gen(solution_list)

    except RuntimeError as e:

        return f"Some error happened with error massage: {e}"

    except TypeError as e:

        if str(e) == "Cannot convert complex to float":

            return "your expression is somehow invalid\nnote:please mind lower and upper bound so that your expression would not returning complex number or zero division"

        else:

            return "your expression is somehow invalid"

    return {"solution_list": solution_list, "best_gen": best_gen}

if __name__=="__main__":

    uvicorn.run("src.api:app", host = "0.0.0.0", port = 8080)




