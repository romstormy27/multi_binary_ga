from src.utils import load_config

from src.initialize import init_pop
from src.fitness import fitness_func, decoding, find_max, get_x1_x2, get_best_gen, def_fitness
from src.selection import cumprob, selection
from src.crossover import parent_selection, crossover, merge_crossover
from src.mutation import mutation

from tqdm import tqdm

def main(params):
    
  # number of chromosom each generation (population size)
  n_chrom = params["n_chrom"]

  # objective function expression
  expr_str = params["fit_expr"]
  # expr_str = str(input("Define objective function: "))
  fit_expr = def_fitness(expr_str)

  # number of generation
  max_gen = params["max_gen"]

  # lower and upper bound for x1
  lower_x1 = params["lower_x1"]
  upper_x1 = params["upper_x1"]

  # lower and upper bound for x2
  lower_x2 = params["lower_x2"]
  upper_x2 = params["upper_x2"]

  # precision
  precision = params["precision"]

  # cross over rate
  crossover_rate = params["crossover_rate"]

  # mutation rate
  mutation_rate = params["mutation_rate"]

  # initialize first population using random method
  x1_encoded = init_pop(n_chrom, lower_x1, upper_x1, precision)
  x2_encoded = init_pop(n_chrom, lower_x2, upper_x2, precision)

  # initialize solution list
  solution_list = []

  # iterate until maximum generation reached
  for i in tqdm(range(max_gen)):

    # decode x1 and x2
    x1_decoded = decoding(x1_encoded, lower_x1, upper_x1)
    x2_decoded = decoding(x2_encoded, lower_x2, upper_x2)

    # evaluate x1 and x2
    solutions = fitness_func(x1_decoded, x2_decoded, fit_expr)
    maximum = find_max(solutions)
    # print(f"best of generation {i}: {maximum}")

    # save solution
    solution_list.append(maximum)

    # brake the iteration when maximum generation reached
    if i >= max_gen:
      break

    # probability table (cum sum)
    prob_table = cumprob(solutions)

    # selection
    selected_chrom = selection(x1_encoded, x2_encoded, prob_table, n_chrom)

    # cross_over --> select parents
    parents, idx = parent_selection(selected_chrom, crossover_rate)
    # print("parents len:", parents[0].shape[0])
    # print()
    # cross_over
    cross_over = crossover(parents)

    # merge cross over results to main populations
    populations = merge_crossover(cross_over, selected_chrom, idx)

    # mutation
    mutated = mutation(populations, mutation_rate)
    # get x1 and x2
    x1_encoded, x2_encoded = get_x1_x2(mutated, x1_encoded)

  return solution_list


if __name__ == "__main__":

    params = load_config()

    try:

      solution_list = main(params)

      get_best_gen(solution_list)

    except TypeError as e:

      if str(e) == "Cannot convert complex to float":
        
        print("your expression is somehow invalid\nnote:please mind lower and upper bound so that your expression would not returning complex number or zero division")

      else:

        print("Your expression is somehow invalid")

    except:

      print("Something went wrong!")