from pyscript import display
import numpy as np
import matplotlib.pyplot as plt
from js import document
from pyodide.ffi import create_proxy
import logging

# Suppress matplotlib font warnings
logging.getLogger('matplotlib').setLevel(logging.ERROR)

# Initialize data arrays
days = np.array(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"])
absences = np.array([0, 0, 0, 0, 0])

def show_message(msg, is_success=True):
    """Display a temporary status message to the user"""
    msg_div = document.getElementById("statusMsg")
    msg_div.textContent = msg
    msg_div.style.display = "block"
    msg_div.className = "status-msg status-success" if is_success else "status-msg"
    from js import setTimeout
    setTimeout(create_proxy(lambda: msg_div.style.setProperty("display", "none")), 2000)

def update_stats():
    """Calculate and display attendance statistics"""
    total_absences = np.sum(absences)
    stats_div = document.getElementById("statsDisplay")
    
    if np.max(absences) > 0:
        highest_day = days[np.argmax(absences)]
        stats_div.innerHTML = f"Total Absences This Week: {int(total_absences)} | Highest: {int(np.max(absences))} on {highest_day}"
    else:
        stats_div.innerHTML = "Total Absences This Week: 0 | No absences recorded yet"

def display_graph():
    """Generate and display the matplotlib line graph"""
    plt.close('all')
    fig, ax = plt.subplots(figsize=(8, 5))
    
    ax.plot(days, absences, marker='o', linestyle='-', linewidth=2,
            markersize=8, color='black')
    

    ax.set_title("Weekly Absence Report", fontfamily='Times New Roman', 
                 fontsize=14, fontweight='bold', color='black')
    ax.set_xlabel("Days", fontfamily='Times New Roman', fontsize=12, color='black')
    ax.set_ylabel("Number of Absences", fontfamily='Times New Roman', fontsize=12, color='black')
    
 
    ax.grid(True, linestyle='--', alpha=0.3, color='gray')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('black')
    ax.spines['bottom'].set_color('black')
    

    for i, v in enumerate(absences):
        ax.text(i, v + 0.3, str(int(v)), ha='center', va='bottom', 
                fontsize=10, fontweight='bold', color='black')
    
    display(fig, target="plot", append=False)
    plt.close(fig)
    update_stats()

def record_absence(event):
    """Record the absence value for the selected day"""
    global absences
    
    day_select = document.getElementById("daySelect")
    selected_day = day_select.value
    
    abs_input = document.getElementById("absInput")
    abs_value = int(abs_input.value)
    
    # Validate input
    if abs_value < 0:
        show_message("Please enter a valid number (0 or greater)", False)
        return
    
    day_index = list(days).index(selected_day)
    absences[day_index] = abs_value
    

    display_graph()
    show_message(f"Recorded {abs_value} absence(s) for {selected_day}")

def reset_data(event):
    """Reset all absence data to zero"""
    global absences
    absences = np.array([0, 0, 0, 0, 0])
    document.getElementById("absInput").value = "0"
    document.getElementById("daySelect").value = "Monday"
    display_graph()
    show_message("All attendance data has been reset")

def setup_buttons():
    """Connect Python functions to HTML buttons"""
    record_btn = document.getElementById("recordBtn")
    reset_btn = document.getElementById("resetBtn")
    
    record_btn.addEventListener("click", create_proxy(record_absence))
    reset_btn.addEventListener("click", create_proxy(reset_data))


setup_buttons()

