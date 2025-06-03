from tkinter import ttk
from tkinter import filedialog as fd

from utilities import read_matrix, read_report, objective
from Heuristic import TabuSearch, SimulatedAnnealing

import neighborhood

import time

import pandas as pd
import numpy as np
import tkinter as tk


def select_file():
    global times

    filetypes = (
        ("Text files", "*.txt"),
        ("All files", "*.*")
    )

    filename = fd.askopenfilename(
        title = "Open a file",
        initialdir="./",
        filetypes=filetypes
    )

    name.config(state=tk.NORMAL)
    name.delete(0, tk.END)
    name.insert(0, filename)
    name.config(state=tk.DISABLED)


    times = read_matrix(filename)

    execute_button.config(state=tk.NORMAL)

def get_neighborhood_fn(name):
    func = None
    # "Enroque", "Corr. Izquierda", "Inter. Derecha", "2-Intercambio", "3-Intercambio", "2-Opt"]
    if name == "Enroque":
        func = neighborhood.castling
    elif name == "Corr. Inzquierda":
        func = neighborhood.shifting
    elif name == "Inter. Derecha":
        func = neighborhood.right_swap
    elif name == "2-Intercambio":
        func = neighborhood.two_swap
    elif name == "3-Intercambio":
        func = neighborhood.three_swap
    else:
        func = neighborhood.two_opt

    return func

def generate_report(best, score, elapsed_time):
    problem_size = "({}, {})".format(times.shape[0], times.shape[1])
    init_sol = None

    if init_solution_var.get() == "Ingresar":
        init_sol = "Ingresado -> [{}]".format(init_solution_input.get())
    else:
        init_sol = "Aleatorio"

    report = "\n".join(("========== CONFIGURATION ==========",
                        "Problem size: {}".format(problem_size),
                        "Heuristic: {}".format(tools_var.get()),
                        "Initial solution: {}".format(init_sol),
                        "Neighborhood generation method: {}".format(neighbor_gen_var.get()),
                        "\n========== SOLUTION ==========",
                        "Best: {}".format(best),
                        "Score: {}".format(score),
                        "Elapsed time: {}". format(elapsed_time)))
    
    return report

def execute():
    best = None
    score = None
    start_time = None
    end_time = None

    neighbor_gen = neighbor_gen_var.get()
    neighborhood_fn = get_neighborhood_fn(neighbor_gen)

    initial_sol = None

    if times is None:
        print("[ERROR] There was an error with the distance and flow matrix.")
    else:
        size = times.shape[0]

        if init_solution_var.get() == "Ingresar":
            try:
                initial_sol = init_solution_input.get()
                initial_sol = np.fromstring(initial_sol, dtype=int, sep=',')
            except Exception:
                initial_sol = np.random.permutation(size)

                print("[ERROR] Invalid initial solution, using a random one.")
        else:
            initial_sol = np.random.permutation(size)

        n_iter = int(max_iterations_var.get())
        
        if tools_var.get() == "Tabu":
            p_time = int(tb_penalization_var.get())

            params = [p_time, times]

            heuristic = TabuSearch(size, n_iter)
            
        else:
            init_temp = int(sa_init_temperature_var.get())
            cooldown_time = int(sa_cooldown_time_var.get())

            params = [cooldown_time, init_temp, times]

            heuristic = SimulatedAnnealing(size, n_iter)


        # Run the selected heuristic

        start_time = time.time()

        best, score = heuristic.run(objective, 
                                    neighborhood_fn, 
                                    initial_sol,
                                    params)

        end_time = time.time()

    best_score_var.set(value=score)

    report = generate_report(best, score, end_time - start_time)

    output_textarea.config(state=tk.NORMAL)

    output_textarea.delete("0.0", tk.END)
    output_textarea.insert(tk.END, report)

    output_textarea.config(state=tk.DISABLED)

    solution_menu.entryconfig("Report", state=tk.NORMAL)
    solution_menu.entryconfig("Save report...", state=tk.NORMAL)
    

def show_tabu_ui(parent):
    # No. Iterations
    tk.Label(
        parent,
        text="Max. Iterations"
    ).grid(row=0, column=0, padx=5, pady=5)
    ttk.Entry(parent, textvariable=max_iterations_var).grid(row=0, column=1, padx=5, pady=5, ipadx=5)

    # Penalization time
    tk.Label(
        parent,
        text="Penalization Time"
    ).grid(row=1, column=0, padx=5, pady=5)
    ttk.Entry(parent, textvariable=tb_penalization_var).grid(row=1, column=1, padx=5, pady=5)

def show_sa_ui(parent):
    # No. Iterations
    tk.Label(
        parent,
        text="Max. Iterations"
    ).grid(row=0, column=0, padx=5, pady=5)
    ttk.Entry(parent, textvariable=max_iterations_var).grid(row=0, column=1, padx=5, pady=5, ipadx=5)

    # Initial temperature
    tk.Label(
        parent,
        text="Initial Temperature"
    ).grid(row=1, column=0, padx=5, pady=5)
    ttk.Entry(parent, textvariable=sa_init_temperature_var).grid(row=1, column=1, padx=5, pady=5)

    # Cooldown time
    tk.Label(
        parent,
        text="Cooldown Time"
    ).grid(row=2, column=0, padx=5, pady=5)
    ttk.Entry(parent, textvariable=sa_cooldown_time_var).grid(row=2, column=1, padx=5, pady=5)

def show_params(*args):
    
    for widget in filters_tab.winfo_children():
        widget.destroy()
    
    if tools_var.get() == "Tabu":
        show_tabu_ui(filters_tab)
    else:
        show_sa_ui(filters_tab)

def init_sol_input_update(*args):
    if init_solution_var.get() == "Aleatorio":
        init_solution_input.delete(0, tk.END)
        init_solution_input.insert(0, "1, 2, 3, 4, ...")

        init_solution_input.config(state=tk.DISABLED)
    else:
        init_solution_input.config(state=tk.NORMAL)

def create_report():
    global best

    filetypes = (
        ("Text files", "*.txt"),
        ("All files", "*.*")
    )

    filename = fd.askopenfilename(
        title = "Open a file",
        initialdir="./",
        filetypes=filetypes
    )

    [n, m, feas_sol, permutation] = read_report(filename)

    n = int(n)
    m = int(m)
    feas_sol = int(feas_sol)
    score = best_score_var.get()
    gap = "{:.2f}%".format((score - feas_sol) / score * 100)

    data = {
        "n x m": ["{} x {}".format(n, m)],
        "feas. sol.": [feas_sol],
        "sol. found": [score],
        "gap": [gap]
    }

    df = pd.DataFrame(data)
    df.set_index('n x m', inplace=True)

    output_textarea.config(state=tk.NORMAL)

    report = "\n".join(("\n\n========== EVALUATION ==========", df.to_string()))

    output_textarea.insert(tk.END, report)

    output_textarea.config(state=tk.DISABLED)

def save_report():
    filetypes = (
        ("Text files", "*.txt"),
        ("All files", "*.*")
    )

    filename = fd.asksaveasfilename(filetypes=filetypes, defaultextension=filetypes)

    with open(filename, "w") as file:
        report = output_textarea.get("0.0", tk.END)

        file.write(report)

# Create the root window
root = tk.Tk()
root.title("Flow-Shop Problem")
root.resizable(False, False)

times = None

max_iterations_var = tk.StringVar(value="1000")
tb_penalization_var = tk.StringVar(value="5")
sa_init_temperature_var = tk.StringVar(value="10")
sa_cooldown_time_var = tk.StringVar(value="25")
best_score_var = tk.IntVar(value="0")

menubar = tk.Menu(root)
root.config(menu=menubar)

# SOLUTION MENU
solution_menu = tk.Menu(menubar, tearoff=False)
solution_menu.add_command(
    label="Report",
    state=tk.DISABLED,
    command=create_report
)
solution_menu.add_command(
    label="Save report...",
    state=tk.DISABLED,
    command=save_report
)

# FILE MENU
file_menu = tk.Menu(menubar, tearoff=False)
file_menu.add_command(
    label="Open...",
    command=select_file
)
file_menu.add_command(
    label="Exit",
    command=root.destroy
)

menubar.add_cascade(
    label="File",
    menu=file_menu
)
menubar.add_cascade(
    label="Solution",
    menu=solution_menu
)

# Tools frame
tools_frame = tk.Frame(root)
tools_frame.pack(padx=5, pady=5, side=tk.LEFT, fill=tk.Y)

file_frame = tk.Frame(tools_frame)
file_frame.pack(padx=5, pady=5, fill=tk.Y)
tk.Label(
   file_frame,
   text="Open filename"
).grid(row=0, column=0, columnspan=2, padx=5, pady=5)
tk.Label(
    file_frame,
    text="Filename: "
).grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
name = ttk.Entry(file_frame)
name.config(state=tk.DISABLED)
name.grid(row=1, column=1, padx=5, pady=5, ipadx=5)

open_button = ttk.Button(
    file_frame,
    text="Open a File",
    command=select_file,   
)
open_button.grid(row=2, column=0)

execute_button = ttk.Button(
    file_frame,
    text="Execute",
    command=execute,
    state=tk.DISABLED
)
execute_button.grid(row=2, column=1)

# Tools and filters tabs
notebook = ttk.Notebook(tools_frame)
notebook.pack(expand=True, fill="both")

tools_tab = tk.Frame(notebook)
tools_var = tk.StringVar(value="Tabu")
for tool in ["Tabu", "Simulated Annealing"]:
    tk.Radiobutton(
        tools_tab,
        text=tool,
        variable=tools_var,
        value=tool
    ).pack(anchor="w", padx=20, pady=5)

tools_var.trace_add("write", show_params)

filters_tab = tk.Frame(notebook)
filters_var = tk.StringVar(value="None")

show_tabu_ui(filters_tab)

neighbor_gen_tab = tk.Frame(notebook)
neighbor_gen_var = tk.StringVar(value="Enroque")
for gen_method in ["Enroque", "Corr. Izquierda", "Inter. Derecha", "2-Intercambio", "3-Intercambio", "2-Opt"]:
    tk.Radiobutton(
        neighbor_gen_tab,
        text=gen_method,
        variable=neighbor_gen_var,
        value=gen_method
    ).pack(anchor="w", padx=20, pady=5)

# Initial solution tab

init_solution_tab = tk.Frame(notebook)
init_solution_var = tk.StringVar(value="Aleatorio")
for init_sol_opt in ["Aleatorio", "Ingresar"]:
    tk.Radiobutton(
        init_solution_tab,
        text=init_sol_opt,
        variable=init_solution_var,
        value=init_sol_opt
    ).pack(anchor="w", padx=20, pady=5)
init_solution_input = ttk.Entry(init_solution_tab)
init_solution_input.insert(0, "1, 2, 3, 4, ...")
init_solution_input.pack(anchor="w", padx=20, pady=5)
init_solution_input.config(state=tk.DISABLED)

init_solution_var.trace_add("write", init_sol_input_update)

notebook.add(tools_tab, text="Tools")
notebook.add(filters_tab, text="Params")
notebook.add(neighbor_gen_tab, text="Neighborhood")
notebook.add(init_solution_tab, text="Init. Sol.")


# Output frame
output_frame = tk.Frame(root, width=400, height=400, bg="white")
output_frame.pack(padx=5, pady=5, side=tk.RIGHT)

output_textarea = tk.Text(output_frame)
output_textarea.pack(padx=5, pady=5, expand=True, fill=tk.BOTH)
output_textarea.config(state=tk.DISABLED, bg="white")

# Run the application
root.mainloop()