from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

import src.main as main
import src.fitness as fitness

class InputParams(BaseModel):

    fit_expr: str
    n_chrom: int
    max_gen: int
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

@app.post("/run/")
async def run(params: InputParams):

    params = dict(params)

    try:
    
        solution_list = main.main(params)

        best_gen = fitness.get_best_gen(solution_list)

        # res = {"solution_list": solution_list, "best_gen": best_gen, "msg": None}

    except RuntimeError as e:

        msg = f"Some error happened with error massage: {e}"

        res = {"solution_list": None, "best_gen": None, "msg": msg}

    except TypeError as e:

        if str(e) == "Cannot convert complex to float":

            msg = "Your expression is somehow invalid!. \nnote:please mind lower and upper bound so that your expression would not returning complex number or zero division"

            res = {"solution_list": None, "best_gen": None, "msg": msg}

        else:

            msg = "Your expression is somehow invalid!"

            res = {"solution_list": None, "best_gen": None, "msg": msg}

    except:

        msg = "Something went wrong"

        res = {"solution_list": None, "best_gen": None, "msg": msg}

    return res

if __name__=="__main__":

    uvicorn.run("src.api:app", host = "0.0.0.0", port = 8080)




