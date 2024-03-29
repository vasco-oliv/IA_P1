from initial import calculate_score
import pandas as pd


data = [
    'data/a_example.txt',
    'data/b_read_on.txt',
    'data/c_incunabula.txt',
    'data/d_tough_choices.txt',
    'data/e_so_many_books.txt',
    'data/f_libraries_of_the_world.txt'
]

def display_data_files():
    display_data = ["All"]
    display_data.extend([file.split('/')[-1] for file in data])

    return display_data

def get_data_files():
    return data

def get_results():
    results = []

    with open("initial_solutions.txt", 'r') as f:
        for _ in data:
            line = f.readline()
            l = list(line)
            num_libraries = int(line)
            result = []
            for i in range(num_libraries):
                line = f.readline()
                values = [int(x) for x in line.split()]

                line = f.readline()
                books = [int(x) for x in line.split()]

                result.append((values[0], books))

            results.append(result)

    return results

def get_scores_and_days():
    all_book_scores = []
    all_total_days = []
    for file in data:
        with open(file, 'r') as f:
            line = f.readline()
            values = [int(x) for x in line.split()]
            total_days = values[2]

            line = f.readline()
            scores = [int(x) for x in line.split()]

            all_book_scores.append(scores)
            all_total_days.append(total_days)
        

    return all_total_days, all_book_scores

def get_score_data():
    results = get_results()
    all_total_days, all_book_scores = get_scores_and_days()
    scores=[]
    for i in range(len(results)):
        calculated_score = calculate_score(results[i], all_book_scores[i], all_total_days[i], i)
        scores.append(calculated_score)

    df = pd.DataFrame(scores, index=display_data_files()[1:], columns=["Score"])
    df.index.name = "File"
    return df

