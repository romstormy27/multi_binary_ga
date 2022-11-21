import pandas as pd
import streamlit as st
import requests
from PIL import Image
import time

st.title("Multi-Objective Continuous Genetic Algorithm")

with st.form(key="input_params"):

    fit_expr = st.text_input(
        label = "Function to Optimize: ",
        max_chars=100,
        placeholder="example: -x1/100+x2**2",
        help="You must define objective function in python math format using x1 and x2 otherwise error will be raised"
    )

    n_chrom = st.number_input(
        label="Number of Chromosome(s) for Each Generation: ",
        min_value=1,
        max_value=100,
        help="Define how many chromosome(s) will be generated for each generation (iteration)"
    )

    max_gen = st.number_input(
        label="Maximum Number of Generations: ",
        min_value=1,
        max_value=10000,
        help="Define how many generation(s) or iteration(s) the GA will run"
    )

    lower_x1 = st.number_input(
        label="Lower Bound for x1:",
        value=0.0,
        help="Define lower bound for x1 variable"
    )

    upper_x1 = st.number_input(
        label="Upper Bound for x1:",
        value=0.0,
        help="Define upper bound for x1 variable"
    )

    lower_x2 = st.number_input(
        label="Lower Bound for x2:",
        value=0.0,
        help="Define lower bound for x2 variable"
    )

    upper_x2 = st.number_input(
        label="Upper Bound for x2:",
        value=0.0,
        help="Define upper bound for x2 variable"
    )
    
    precision = st.number_input(
        label="Precision up to (digits):",
        min_value=1,
        max_value=100,
        help="Define precision value up to (digits)"
    )

    crossover_rate = st.number_input(
        label="Cross over rate:",
        min_value=0.01,
        max_value=1.0,
    )

    mutation_rate = st.number_input(
        label="Mutation rate:",
        min_value=0.01,
        max_value=1.0,
    )    

    submitted = st.form_submit_button("Run")

    if submitted:

        # create dict of input params
        input_params = {
            "fit_expr": fit_expr,
            "n_chrom": n_chrom,
            "max_gen": max_gen,
            "lower_x1": lower_x1,
            "upper_x1": upper_x1,
            "lower_x2": lower_x2,
            "upper_x2": upper_x2,
            "precision": precision,
            "crossover_rate": crossover_rate,
            "mutation_rate": mutation_rate,
        }

        with st.spinner("Running..."):
            res = requests.post("http://127.0.0.1:8000/run/", json=input_params).json()

        if res["msg"] != None:
            st.error(str(res["msg"]))

        else: 

            best_gen = res["best_gen"]
            best_gen_number = best_gen[0]
            best_chrom = best_gen[1]

            st.markdown("### Results")
            st.write("Best generation index:\t", best_gen_number)
            st.write("Best chromosome index in best generation:\t", best_chrom["chrom"])
            st.write("Solution for x1:\t", best_chrom["x1"])
            st.write("Solution for x2:\t", best_chrom["x2"])
            st.write("Fitness Score:\t", best_chrom["fitness"])

            ### Fitness plot
            chart_data = pd.DataFrame(res["solution_list"])
            chart_data = chart_data["fitness"]
            st.markdown("### Fitness History")

            # can only work in local
            # st.image("asset/fitness_plot.png", caption="Fitness History")

            # can work in cloud
            st.line_chart(chart_data)
