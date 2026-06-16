import tkinter as tk
from tkinter import ttk

from calculations import (
    calculate_voltage,
    power_from_voltage_current,
    power_from_current_resistance,
    power_from_voltage_resistance,
    voltage_divider,
    divider_current,
    resistor_power,
    solve_two_loop_kvl
)

def clear_frame(frame):

    for widget in frame.winfo_children():
        widget.destroy()

def show_welcome():

    update_results([
        ("Status", "Welcome to the Electrical Circuit Analyzer!")
    ])

    clear_frame(input_frame)

    draw_welcome_diagram()

    update_results([
        ("Status", "Ready")
    ])  

def draw_welcome_diagram():

    clear_diagram()

    diagram_canvas.create_text(
        250,
        60,
        text="Electrical Circuit Analyzer",
        font=("Arial", 16, "bold")
    )

    diagram_canvas.create_text(
        250,
        100,
        text="⚡ Ohm's Law"
    )

    diagram_canvas.create_text(
        250,
        120,
        text="🔋 Power Calculator"
    )

    diagram_canvas.create_text(
        250,
        140,
        text="📉 Voltage Divider"
    )

    diagram_canvas.create_text(
        250,
        160,
        text="🔄 KVL Solver"
    )

def clear_diagram():

    diagram_canvas.delete("all")

def update_results(rows):

    for item in results_table.get_children():
        results_table.delete(item)

    for parameter, value in rows:
        results_table.insert(
            "",
            "end",
            values=(parameter, value)
        )

window = tk.Tk()

style = ttk.Style()

style.configure(
    "Treeview",
    rowheight=28,
    font=("Segoe UI", 10)
)

style.configure(
    "Treeview.Heading",
    font=("Segoe UI", 10, "bold")
)

window.title("Electrical Circuit Analyzer")

window.geometry("1200x700")

title = ttk.Label(
    window,
    text="Electrical Circuit Analyzer",
    font=("Arial", 20)
)

title.pack(pady=20)

button_frame = ttk.Frame(window)

button_frame.pack(pady=10)

def show_ohms_law():

    clear_frame(input_frame)
    clear_diagram()

    update_results([
        ("Status", "Ohm's Law Mode")
    ])

    diagram_canvas.create_text(
        250,
        80,
        text="V = I × R",
        font=("Arial", 20, "bold")
    )

    diagram_canvas.create_text(
        250,
        120,
        text="Ohm's Law Calculator"
    )

    form_frame = ttk.Frame(input_frame)
    form_frame.pack(pady=20)

    ttk.Label(
        form_frame,
        text="Current (A)"
    ).grid(
        row=0,
        column=0,
        padx=10,
        pady=5,
        sticky="w"
    )

    current_entry = ttk.Entry(
        form_frame,
        width=15
    )

    current_entry.grid(
        row=0,
        column=1,
        padx=10,
        pady=5
    )

    ttk.Label(
        form_frame,
        text="Resistance (Ω)"
    ).grid(
        row=1,
        column=0,
        padx=10,
        pady=5,
        sticky="w"
    )

    resistance_entry = ttk.Entry(
        form_frame,
        width=15
    )

    resistance_entry.grid(
        row=1,
        column=1,
        padx=10,
        pady=5
    )

    def calculate():

        try:

            current = float(
                current_entry.get()
            )

            resistance = float(
                resistance_entry.get()
            )

            voltage = calculate_voltage(
                current,
                resistance
            )

            update_results([
                ("Voltage", f"{voltage:.2f} V")
            ])

        except ValueError:

            update_results([
                ("Error", "Invalid Input")
            ])  

    ttk.Button(
        form_frame,
        text="Calculate",
        command=calculate
    ).grid(
        row=2,
        column=0,
        columnspan=2,
        pady=15
    )


ohm_button = ttk.Button(
    button_frame,
    text="Ohm's Law",
    width=20,
    command=show_ohms_law
)

ohm_button.grid(row=0, column=0, padx=5)


def show_power_calculator():

    clear_frame(input_frame)
    clear_diagram()

    update_results([
        ("Status", "Power Calculator Mode")
    ])

    diagram_canvas.create_text(
        250,
        80,
        text="Power Equations",
        font=("Arial", 16, "bold")
    )

    diagram_canvas.create_text(
        250,
        120,
        text="P = V × I"
    )

    diagram_canvas.create_text(
        250,
        140,
        text="P = I²R"
    )

    diagram_canvas.create_text(
        250,
        160,
        text="P = V²/R"
    )

    method = tk.StringVar()
    method.set("VI")

    form_frame = ttk.Frame(input_frame)
    form_frame.pack(pady=15)

    field1_label = ttk.Label(form_frame)

    field1_label.grid(
        row=0,
        column=0,
        padx=10,
        pady=5,
        sticky="w"
    )

    field1_entry = ttk.Entry(
        form_frame,
        width=15
    )

    field1_entry.grid(
        row=0,
        column=1,
        padx=10,
        pady=5
    )

    field2_label = ttk.Label(form_frame)

    field2_label.grid(
        row=1,
        column=0,
        padx=10,
        pady=5,
        sticky="w"
    )

    field2_entry = ttk.Entry(
        form_frame,
        width=15
    )

    field2_entry.grid(
        row=1,
        column=1,
        padx=10,
        pady=5
    )

    def update_inputs():

        selected = method.get()

        if selected == "VI":
            field1_label.config(text="Voltage (V)")
            field2_label.config(text="Current (A)")

        elif selected == "IR":
            field1_label.config(text="Current (A)")
            field2_label.config(text="Resistance (Ω)")

        elif selected == "VR":
            field1_label.config(text="Voltage (V)")
            field2_label.config(text="Resistance (Ω)")

        field1_entry.delete(0, tk.END)
        field2_entry.delete(0, tk.END)
    
    radio_frame = ttk.Frame(input_frame)
    radio_frame.pack(pady=10)

    ttk.Label(
        radio_frame,
        text="Select Formula",
        font=("Arial", 12, "bold")
    ).pack(pady=5)

    ttk.Radiobutton(
        radio_frame,
        text="P = V × I",
        variable=method,
        value="VI",
        command=update_inputs
    ).pack(anchor="w")

    ttk.Radiobutton(
        radio_frame,
        text="P = I² × R",
        variable=method,
        value="IR",
        command=update_inputs
    ).pack(anchor="w")

    ttk.Radiobutton(
        radio_frame,
        text="P = V² / R",
        variable=method,
        value="VR",
        command=update_inputs
    ).pack(anchor="w")

    update_inputs()

    def calculate():

        try:

            value1 = float(field1_entry.get())
            value2 = float(field2_entry.get())

            selected = method.get()

            if selected == "VI":

                power = power_from_voltage_current(
                    value1,
                    value2
                )

            elif selected == "IR":

                power = power_from_current_resistance(
                    value1,
                    value2
                )

            elif selected == "VR":

                power = power_from_voltage_resistance(
                    value1,
                    value2
                )

            update_results([
                ("Power", f"{power:.2f} W")
            ])

        except ValueError:

            update_results([
                ("Error", "Invalid Input")
            ])

    ttk.Button(
        form_frame,
        text="Calculate",
        command=calculate
    ).grid(
        row=2,
        column=0,
        columnspan=2,
        pady=15
    )

power_button = ttk.Button(
    button_frame,
    text="Power Calculator",
    width=20,
    command=show_power_calculator
)

power_button.grid(
    row=0,
    column=1,
    padx=5
)

def show_voltage_divider():

    clear_frame(input_frame)
    draw_voltage_divider()
    
    update_results([
        ("Status", "Voltage Divider Mode")
    ])

    form_frame = ttk.Frame(input_frame)
    form_frame.pack(pady=20)

    ttk.Label(
        form_frame,
        text="Input Voltage (V)"
    ).grid(
        row=0,
        column=0,
        padx=10,
        pady=5,
        sticky="w"
    )

    vin_entry = ttk.Entry(
        form_frame,
        width=15
    )

    vin_entry.grid(
        row=0,
        column=1,
        padx=10,
        pady=5
    )

    ttk.Label(
        form_frame,
        text="R1 (Ω)"
    ).grid(
        row=1,
        column=0,
        padx=10,
        pady=5,
        sticky="w"
    )

    r1_entry = ttk.Entry(
        form_frame,
        width=15
    )

    r1_entry.grid(
        row=1,
        column=1,
        padx=10,
        pady=5
    )

    ttk.Label(
        form_frame,
        text="R2 (Ω)"
    ).grid(
        row=2,
        column=0,
        padx=10,
        pady=5,
        sticky="w"
    )

    r2_entry = ttk.Entry(
        form_frame,
        width=15
    )

    r2_entry.grid(
        row=2,
        column=1,
        padx=10,
        pady=5
    )

    def calculate():

        try:

            vin = float(vin_entry.get())
            r1 = float(r1_entry.get())
            r2 = float(r2_entry.get())

            vout = voltage_divider(
                vin,
                r1,
                r2
            )

            current = divider_current(
                vin,
                r1,
                r2
            )

            power_r1 = resistor_power(
                current,
                r1
            )

            power_r2 = resistor_power(
                current,
                r2
            )

            update_results([
                ("Output Voltage", f"{vout:.2f} V"),
                ("Divider Current", f"{current:.4f} A"),
                ("Power R1", f"{power_r1:.4f} W"),
                ("Power R2", f"{power_r2:.4f} W")
            ])

        except ValueError:

            update_results([
                ("Error", "Invalid Input")
            ])

    ttk.Button(
        form_frame,
        text="Calculate",
        command=calculate
    ).grid(
        row=3,
        column=0,
        columnspan=2,
        pady=15
    )

divider_button = ttk.Button(
    button_frame,
    text="Voltage Divider",
    width=20,
    command=show_voltage_divider
)

divider_button.grid(
    row=1,
    column=0,
    padx=5,
    pady=5
)

def draw_voltage_divider():

    clear_diagram()

    diagram_canvas.create_text(
        150,
        20,
        text="Vin"
    )

    diagram_canvas.create_line(
        150, 30,
        150, 60
    )

    diagram_canvas.create_rectangle(
        130, 60,
        170, 90
    )

    diagram_canvas.create_text(
        150,
        75,
        text="R1"
    )

    diagram_canvas.create_line(
        150, 90,
        150, 120
    )

    diagram_canvas.create_text(
        220,
        120,
        text="Vout"
    )

    diagram_canvas.create_line(
        150, 120,
        220, 120
    )

    diagram_canvas.create_line(
        150, 120,
        150, 150
    )

    diagram_canvas.create_rectangle(
        130, 150,
        170, 180
    )

    diagram_canvas.create_text(
        150,
        165,
        text="R2"
    )

    diagram_canvas.create_text(
        150,
        195,
        text="GND"
    )

def show_kvl_solver():

    clear_frame(input_frame)
    update_results([
        ("Status", "KVL Solver Mode")
    ])

    draw_kvl_circuit()

    labels = [
        "R1 (Ω)",
        "R2 (Ω)",
        "R3 Shared (Ω)",
        "V1 (V)",
        "V2 (V)"
    ]

    entries = []

    form_frame = ttk.Frame(input_frame)
    form_frame.pack(pady=20)

    for i, text in enumerate(labels):

        ttk.Label(
            form_frame,
            text=text
        ).grid(
            row=i,
            column=0,
            padx=10,
            pady=5,
            sticky="w"
        )

        entry = ttk.Entry(
            form_frame,
            width=15
        )

        entry.grid(
            row=i,
            column=1,
            padx=10,
            pady=5
        )

        entries.append(entry)

    def solve():

        try:
            r1 = float(entries[0].get())
            r2 = float(entries[1].get())
            r3 = float(entries[2].get())

            v1 = float(entries[3].get())
            v2 = float(entries[4].get())

            i1, i2 = solve_two_loop_kvl(
                r1,
                r2,
                r3,
                v1,
                v2
            )

            shared_current = i1 - i2

            power_r1 = (i1 ** 2) * r1
            power_r2 = (i2 ** 2) * r2
            power_r3 = (shared_current ** 2) * r3

            update_results([
                ("I1 Current", f"{i1:.4f} A"),
                ("I2 Current", f"{i2:.4f} A"),
                ("Shared Current", f"{shared_current:.4f} A"),
                ("Power R1", f"{power_r1:.4f} W"),
                ("Power R2", f"{power_r2:.4f} W"),
                ("Power R3", f"{power_r3:.4f} W")
            ])

        except Exception as e:

            print("KVL ERROR:", e)

            update_results([
                ("Error", str(e))
            ])

    ttk.Button(
        form_frame,
        text="Solve",
        command=solve
    ).grid(
        row=len(labels),
        column=0,
        columnspan=2,
        pady=15
    )

kvl_button = ttk.Button(
    button_frame,
    text="KVL Solver",
    width=20,
    command=show_kvl_solver
)

kvl_button.grid(
    row=1,
    column=1,
    padx=5,
    pady=5
)

def draw_kvl_circuit():

    clear_diagram()

    # Left loop
    diagram_canvas.create_rectangle(
        60, 40,
        180, 140
    )

    # Right loop
    diagram_canvas.create_rectangle(
        180, 40,
        300, 140
    )

    # Labels
    diagram_canvas.create_text(
        120,
        30,
        text="R1"
    )

    diagram_canvas.create_text(
        240,
        30,
        text="R2"
    )

    diagram_canvas.create_text(
        180,
        90,
        text="R3"
    )

    diagram_canvas.create_text(
        60,
        90,
        text="V1"
    )

    diagram_canvas.create_text(
        300,
        90,
        text="V2"
    )

    diagram_canvas.create_text(
        120,
        160,
        text="Loop 1"
    )

    diagram_canvas.create_text(
        240,
        160,
        text="Loop 2"
    )


middle_frame = ttk.Frame(window)

middle_frame.pack(
    fill="both",
    expand=True,
    padx=20,
    pady=10
)

input_frame = ttk.LabelFrame(
    middle_frame,
    text="Input Area"
)

input_frame.pack(
    side="left",
    fill="both",
    expand=True,
    padx=(0, 10)
)

diagram_frame = ttk.LabelFrame(
    middle_frame,
    text="Circuit Diagram"
)

diagram_frame.pack(
    side="right",
    fill="both",
    expand=True
)

diagram_canvas = tk.Canvas(
    diagram_frame,
    bg="white"
)

diagram_canvas.pack(
    fill="both",
    expand=True
)

form_frame = ttk.Frame(input_frame)
form_frame.pack(pady=15)

result_frame = ttk.LabelFrame(
    window,
    text="Results"
)

result_frame.pack(
    fill="x",
    padx=20,
    pady=10
)

results_table = ttk.Treeview(
    result_frame,
    columns=("Parameter", "Value"),
    show="headings",
    height=6
)

results_table.heading(
    "Parameter",
    text="Parameter"
)

results_table.heading(
    "Value",
    text="Value"
)

results_table.column(
    "Parameter",
    width=180,
    anchor="center"
)

results_table.column(
    "Value",
    width=150,
    anchor="center"
)

results_table.pack(
    fill="x",
    padx=10,
    pady=10
)

show_welcome()

window.mainloop()