import streamlit as st
import pandas as pd
import numpy as np
from utils import *
from algorithms import *

def optimize(file, heuristic, temperature, cooling_rate, iterations, tabu_size, from_best):
    match file:
        case "All":
            best_scores = []
            for i in range(len(get_data_files())):
                best_scores.extend(optimize(display_data_files()[i + 1], heuristic, temperature, cooling_rate, iterations, tabu_size, from_best))
            return best_scores
        case _:
            index = display_data_files().index(file) - 1

    filename = "data/" + file
    libs_dict, total_days, book_scores, result = read_file_for_optimize(filename, index, from_best)

    match heuristic:
        case "Basic Hill Climbing":
            best_solution, best_score = hill_climbing_basic(result, book_scores, total_days, libs_dict)
        case "Steepest Hill Climbing":
            best_solution, best_score = hill_climbing_steepest(result, book_scores, total_days, libs_dict)
        case "Simulated Annealing":
            best_solution, best_score = simulated_annealing(result, book_scores, total_days, libs_dict, iterations, temperature, cooling_rate)
        case "Simulated Annealing with Tabu Search":
            best_solution, best_score = simulated_annealing_tabu_search(result, book_scores, total_days, libs_dict, iterations, temperature, cooling_rate, tabu_size)

    current_best = get_current_best_score(index)

    if (current_best < best_score):
        save_best(index, best_score, best_solution)

    return [best_score]

def main():    
    st.set_page_config(page_title="Book Scanning Optimizer", page_icon=":books:", layout="wide")
    st.title("Book Scanning Optimizer :books:")  
    st.markdown("---")

    df = get_score_data()
    st.subheader("Scores")
    st.write(df.to_html(), unsafe_allow_html=True)
    
    best_score = []
    with st.sidebar:
        st.subheader("File")
        file = st.selectbox("Select file", display_data_files())
        st.markdown("---")
        st.subheader("Optimizing Heuristic")
        heuristic = st.radio("Select the optimizing heuristic", get_algorithm_names())
        
        temperature = 0.0
        cooling_rate = 0.0
        iterations = 0
        tabu_size = 0

        match heuristic:
            case "Simulated Annealing":
                st.subheader("Simulated Annealing Parameters")
                temperature = st.number_input("Initial temperature", value=150.0)
                cooling_rate = st.number_input("Cooling rate", value=0.95, format="%.4f")
                iterations = st.number_input("Iterations", value=1000)
            case "Simulated Annealing with Tabu Search":
                st.subheader("Simulated Annealing with Tabu Search Parameters")
                temperature = st.number_input("Initial temperature", value=150.0)
                cooling_rate = st.number_input("Cooling rate", value=0.95, format="%.4f")
                iterations = st.number_input("Iterations", value=1000)
                tabu_size = st.number_input("Tenure", value=10)
            case _:
                pass
        best_button = st.button("Run from best")
        init_button = st.button("Run from initial")
        
        if best_button:
            best_score = optimize(file, heuristic, temperature, cooling_rate, iterations, tabu_size, True)
        elif init_button:
            best_score = optimize(file, heuristic, temperature, cooling_rate, iterations, tabu_size, False)

    st.markdown("---")
    st.subheader("Results")

    if file == "All":
        for i in range(len(best_score)):
            filename = display_data_files()[i + 1]
            st.write(f"Result for {filename}: {best_score[i]}")
    else:
        if not len(best_score) == 0:
            st.write(f"Result for {file}: {best_score}")


if __name__ == "__main__":
    main()