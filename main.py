from pyscript import display
import numpy as np
import matplotlib.pyplot as plt
import logging
from js import document

logging.getLogger('matplotlib').setLevel(logging.ERROR)


days = np.array(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"])


absences = np.array([0, 0, 0, 0, 0])


def display_graph():
    plt.clf()
    
   
    plt.plot(days, absences, marker='o', linestyle='-', linewidth=2, markersize=8, color='black')
    
    plt.title("Weekly Absence Report")
    plt.xlabel("Days")
    plt.ylabel("Number of Absences")
    plt.grid(True, linestyle='--', alpha=0.3)
    
    for i, v in enumerate(absences):
        plt.text(i, v + 0.3, str(int(v)), ha='center', va='bottom')
    
    display(plt.gcf(), target="plot")
    plt.close()

def record_absence(event):
    global absences
    
    day_select = document.getElementById("daySelect")
    selected_day = day_select.value
    
    abs_input = document.getElementById("absInput")
    abs_value = int(abs_input.value)
    
    day_index = list(days).index(selected_day)
    
    absences[day_index] = abs_value
    
    display_graph()
    
def reset_data(event):
    global absences
    absences = np.array([0, 0, 0, 0, 0])
    document.getElementById("absInput").value = "0"
    document.getElementById("daySelect").value = "Monday"
    display_graph()

# Set up buttons
record_btn = document.getElementById("recordBtn")
reset_btn = document.getElementById("resetBtn")

record_btn.addEventListener("click", record_absence)
reset_btn.addEventListener("click", reset_data)

display_graph()

def display_graph():
    plt.close('all')  # fully reset previous figures
    fig, ax = plt.subplots()
    
    ax.plot(days, absences, marker='o', linestyle='-', linewidth=2,
            markersize=8, color='black')
    
    ax.set_title("Weekly Absence Report")
    ax.set_xlabel("Days")
    ax.set_ylabel("Number of Absences")
    ax.grid(True, linestyle='--', alpha=0.3)
    
    for i, v in enumerate(absences):
        ax.text(i, v + 0.3, str(int(v)), ha='center', va='bottom')
    
    display(fig, target="plot", append=False)  # important fix
    plt.close(fig)