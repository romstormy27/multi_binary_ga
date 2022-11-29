import pandas as pd
import streamlit as st
import requests
from PIL import Image

st.set_page_config(
    page_title="MOCGA Runner",
    page_icon=":chart_with_upwards_trend:",
)

st.title("Multi-Objective Continuous Genetic Algorithm")

with st.form(key="input_params"):

    fit_expr = st.text_input(
        label = "Function to Optimize: ",
        max_chars=100,
        placeholder="example: 33.7+x1*sin(4*pi*x1)+x2*sin(20*pi*x2)",
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

        if not fit_expr:
            st.warning("Please input the function expression")
            st.stop()
        
        if "x1" not in fit_expr:
            st.warning("There must be x1 variable in the expression")
            st.stop()

        if "x2" not in fit_expr:
            st.warning("There must be x2 variable in the expression")
            st.stop()

        if lower_x1 >= upper_x1:
            st.warning("Lower and upper bound for x1 must be different!")
            st.stop()

        if lower_x2 >= upper_x2:
            st.warning("Lower and upper bound for x2 must be different!")
            st.stop()

        # create dict of input params
        input_params = {
            "fit_expr": fit_expr.lower(), #lower all uppercase
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
            # after 28th november heroku wouldn't available anymore
            # res = requests.post("https://multiga.herokuapp.com/run/", json=input_params).json()

            # use deta. forever free but can only handle small project size
            # res = requests.post("https://9kl7z6.deta.dev/run/", json=input_params).json()

            # use railways. 500 hrs free each month. can use docker
            res = requests.post("https://multibinaryga-production.up.railway.app/run/", json=input_params).json()

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
