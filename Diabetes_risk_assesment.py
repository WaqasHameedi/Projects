from tkinter import *
from tkinter import messagebox
from fpdf import FPDF
import csv
import os

# BACKEND
def calculate_risk():
    required_string_vars = [gen_value, act_value, veg_value, med_value, BP_value, family_value]
    required_numeric_vars = [age_value, weight_value, height_value, waist_value]
    for var in required_string_vars:
        if var.get() == "":
            messagebox.showerror("Input Error",
                                 "Please select an option for all multiple-choice fields (Gender, Activity, etc.).")
            return
    for var in required_numeric_vars:
        if var.get().strip() == "":
            messagebox.showerror("Input Error", "Please enter values for all numeric fields (Age, BMI, Waist Size).")
            return
    try:
        name=name_value.get()
        age = int(age_value.get())
        gender = gen_value.get()
        height = float(height_value.get())
        weight = float(weight_value.get())
        waist = float(waist_value.get())
        activeness = act_value.get()
        veg = veg_value.get()
        med = med_value.get()
        bp = BP_value.get()
        family = family_value.get()
        bmi = weight / (height) ** 2
        score = 0
        suggestion = []

        # same logic
        if age < 45:
            score += 0
        elif 45 <= age <= 54:
            score += 2
        elif 55 <= age <= 64:
            score += 3
        else:
            score += 4

        if bmi < 25:
            score += 0
        elif 25 <= bmi < 30:
            score += 1
            suggestion.append("Work on weight or height (if possible) ")
        else:
            score += 3
            suggestion.append("Work on weight or height (if possible)")

        if gender == "Male":
            if waist < 94:
                score += 0
            elif 94 <= waist <= 102:
                score += 3
                suggestion.append("Reduce waist size ")
            else:
                score += 4
                suggestion.append("Reduce waist size ")
        else:
            if waist < 80:
                score += 0
            elif 80 <= waist <= 88:
                score += 3
                suggestion.append("Reduce waist size ")
            else:
                score += 4
                suggestion.append("Reduce waist size ")

        if activeness == "Yes":
            score += 0
        else:
            score += 2
            suggestion.append("Increase your activity")

        if veg == "Every day":
            score += 0
        else:
            score += 1
            suggestion.append("Increase your vegetable intake")

        if med == "Yes":
            score += 2
            suggestion.append("Avoid taking tension")

        if bp == "Yes":
            score += 5
            suggestion.append("Keep BP and glucose maintained")

        if family == "No":
            score += 0
        elif family == "Yes (grandparent, aunt, uncle, cousin)":
            score += 3
        elif family == "Yes (parent, sibling, or child)":
            score += 5

        if score < 7:
            risk = "Low risk (1 in 100 chance within 10 years)"
        elif 7 <= score <= 11:
            risk = "Slightly elevated (1 in 25 chance)"
        elif 12 <= score <= 14:
            risk = "Moderate risk (1 in 6 chance)"
        elif 15 <= score <= 20:
            risk = "High risk (1 in 3 chance)"
        else:
            risk = "Very high risk (1 in 2 chance)"

        messagebox.showinfo("Diabetes Risk Result",
                            f"Your total score: {score}\n{risk}\n\nSuggestions:\n- " + "\n- ".join(suggestion))

    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numeric values for age, BMI, and waist size.")
    #for report generation

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 12, "Diabetes Risk Assessment Report", ln=True, align="C")
    pdf.ln(10)

    pdf.cell(0, 10, "Personal Information", ln=True, align="l")

    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 8, f"Name: {name_value.get()}", ln=True)
    pdf.cell(0, 8, f"Age: {age_value.get()}", ln=True)
    pdf.cell(0, 8, f"Gender: {gen_value.get()}", ln=True)
    pdf.ln(5)
    pdf.set_font("Helvetica", "B", 13)

    # Health data
    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(0, 10, " Health Information", ln=True)
    pdf.set_font("Helvetica", "", 12)
    pdf.cell(0, 8, f"Height: {height_value.get()} m", ln=True)
    pdf.cell(0, 8, f"Weight: {weight_value.get()} kg", ln=True)
    pdf.cell(0, 8, f"Waist: {waist_value.get()} cm", ln=True)
    pdf.cell(0, 8, f"Activity Level: {act_value.get()}", ln=True)
    pdf.cell(0, 8, f"Vegetable Intake: {veg_value.get()}", ln=True)
    pdf.cell(0, 8, f"Hypertension Medication: {med_value.get()}", ln=True)
    pdf.cell(0, 8, f"BP/Glucose History: {BP_value.get()}", ln=True)
    pdf.cell(0, 8, f"Family History: {family_value.get()}", ln=True)
    pdf.ln(5)
    pdf.set_font("Helvetica", "B", 13)

    pdf.cell(0, 10, "Score and Risk level", ln=True, align="l")
    pdf.set_font("Arial", "", 12)

    pdf.cell(0, 8, f"Total Score: {score}", ln=True)
    pdf.cell(8, 10, f"Risk Level: {risk}",ln=True)
    pdf.ln(5)

    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(0, 10, "Suggestions", ln=True, align="L")

    # Temporarily switch to a Unicode-friendly font for the bullet points
    # You must install the ttf file and import it if you use a font other than the standard core 14 fonts.
    # The standard FPDF does NOT ship with DejaVuSans by default, but you can try using a simple dash or a different font if you prefer not to add a custom one.

    # Option 1: Use a simple dash (which is ASCII) - RECOMMENDED SIMPLE FIX
    pdf.set_font("Arial", "", 12)  # Revert to a standard font for text content
    if suggestion:
        for item in suggestion:
            pdf.cell(0, 7, f"- {item}", ln=True)  # Changed • to - (a simple dash)
    else:
        pdf.cell(0, 7, "Your current inputs indicate a low-risk lifestyle")
    pdf.ln(5)

    pdf.output(f"{name} Diabetes_Report.pdf")

    messagebox.showinfo("PDF Saved", f"Report generated successfully as '{name} Diabetes_Report.pdf'")

    #save data
    # Save data to CSV
    filename = "diabetes_data.csv"
    file_exists = os.path.isfile(filename)

    with open(filename, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        if not file_exists:
            # Write header only once #at the time of creation
            writer.writerow([
                "Name", "Age", "Gender", "Height (m)", "Weight (kg)", "Waist (cm)",
                "Activity", "Vegetable Intake", "Medication", "BP/Glucose History",
                "Family History", "BMI", "Score", "Risk Level", "Suggestions"
            ])
        #when create file then it will append
        writer.writerow([
            name, age, gender, height, weight, waist, activeness, veg, med, bp, family,
            round(bmi, 2), score, risk, " | ".join(suggestion) if suggestion else "None"
        ])


# FRONTEND
root = Tk()
root.title("Diabetes Risk Assessment Tool")
root.geometry("500x500")  # smaller height on purpose
root.configure(bg="#f4f6f7")
root.wm_iconbitmap("diabetes_measure_blood_icon_208792.ico")


# Scrollable canvas
main_frame = Frame(root, bg="#f4f6f7")
main_frame.pack(fill=BOTH, expand=1)

canvas = Canvas(main_frame, bg="#f4f6f7", highlightthickness=0)
canvas.pack(side=LEFT, fill=BOTH, expand=1)

scrollbar = Scrollbar(main_frame, orient=VERTICAL, command=canvas.yview)
scrollbar.pack(side=RIGHT, fill=Y)

canvas.configure(yscrollcommand=scrollbar.set)
canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

scrollable_frame = Frame(canvas, bg="#f4f6f7")
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

#TITLE

title_frame = Frame(scrollable_frame, bg="#2e86c1", pady=15)
title_frame.pack(fill="x")
Label(title_frame, text="💙 Diabetes Risk Calculator", font=("Helvetica", 18, "bold"),
      bg="#2e86c1", fg="white").pack()
#DEF labels for

def create_label_entry(parent, text, variable=None, options=None):
    frame = Frame(parent, bg="#f4f6f7")
    frame.pack(fill="x", pady=6)
    Label(frame, text=text, font=("Arial", 11, "bold"), bg="#f4f6f7").pack(anchor="w")
    if options:
        OptionMenu(frame, variable, *options).pack(fill="x", pady=2)
    else:
        Entry(frame, textvariable=variable, font=("Arial", 11)).pack(fill="x", pady=2)

name_value = StringVar()
age_value = StringVar()
gen_value = StringVar()
act_value = StringVar()
veg_value = StringVar()
med_value = StringVar()
BP_value = StringVar()
weight_value = StringVar()
height_value = StringVar()
waist_value = StringVar()
family_value = StringVar()

create_label_entry(scrollable_frame, "👤 Name:", name_value)
create_label_entry(scrollable_frame, "🎂 Age:", age_value)
create_label_entry(scrollable_frame, "⚥ Gender:", gen_value, ["Male", "Female"])
create_label_entry(scrollable_frame, "🚶 Do you walk daily (≥30 min)?", act_value, ["Yes", "No"])
create_label_entry(scrollable_frame, "🥦 How often do you eat vegetables?", veg_value, ["Every day", "Not every day", "Never"])
create_label_entry(scrollable_frame, "💊 Regular medication for hypertension?", med_value, ["Yes", "No"])
create_label_entry(scrollable_frame, "🩸 Have you had high BP or glucose before?", BP_value, ["Yes", "No"])
create_label_entry(scrollable_frame, "⚖️ Weight (kg):", weight_value)
create_label_entry(scrollable_frame, "📏 Height (m):", height_value)
create_label_entry(scrollable_frame, "📉 Waist circumference (cm):", waist_value)
create_label_entry(scrollable_frame, "👪 Family history of diabetes:", family_value,
                   ["No", "Yes (grandparent, aunt, uncle, cousin)", "Yes (parent, sibling, or child)"])

Button(scrollable_frame, text="Calculate My Risk", command=calculate_risk,
       bg="#2e86c1", fg="white", font=("Arial", 13, "bold"),
       relief="raised", padx=10, pady=8).pack(pady=25)

Label(scrollable_frame, text=" Created by WAQAS HAMEEDI | Stay Active. Eat Healthy. Stay Safe.",
      bg="#f4f6f7", fg="gray", font=("Arial", 9, "italic")).pack(pady=10)
#for message after 400 milliseconds
root.after(400, lambda: messagebox.showinfo("NOTICE", "This is just a risk calculator"))


root.mainloop()