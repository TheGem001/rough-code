import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

# ---------------- CONFIGURATION ----------------
DATA_FILE = "patients_data.json"

class PatientManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Gem Organization - Patient Management System")
        self.root.geometry("850x600")
        
        # Data initialization
        self.patients = []
        self.next_id = 1
        self.load_data()

        # UI Setup
        self.setup_ui()
        self.refresh_table()

    # ---------------- PERSISTENCE ----------------
    def load_data(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r") as f:
                    data = json.load(f)
                    self.patients = data.get("patients", [])
                    self.next_id = data.get("next_id", 1)
            except:
                messagebox.showerror("Error", "Could not load data file.")

    def save_data(self):
        data = {"next_id": self.next_id, "patients": self.patients}
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=4)

    # ---------------- UI COMPONENTS ----------------
    def setup_ui(self):
        # Header
        header = tk.Label(self.root, text="Patient Management System", font=("Arial", 18, "bold"), pady=20)
        header.pack()

        # Input Frame (Left Side)
        input_frame = tk.LabelFrame(self.root, text="Manage Patient", padx=10, pady=10)
        input_frame.pack(side="left", fill="y", padx=20, pady=10)

        # Form Fields
        tk.Label(input_frame, text="Name:").grid(row=0, column=0, sticky="w")
        self.name_entry = tk.Entry(input_frame)
        self.name_entry.grid(row=0, column=1, pady=5)

        tk.Label(input_frame, text="Age:").grid(row=1, column=0, sticky="w")
        self.age_entry = tk.Entry(input_frame)
        self.age_entry.grid(row=1, column=1, pady=5)

        tk.Label(input_frame, text="Gender:").grid(row=2, column=0, sticky="w")
        self.gender_combo = ttk.Combobox(input_frame, values=["Male", "Female", "Other"], state="readonly")
        self.gender_combo.grid(row=2, column=1, pady=5)

        tk.Label(input_frame, text="Disease:").grid(row=3, column=0, sticky="w")
        self.disease_entry = tk.Entry(input_frame)
        self.disease_entry.grid(row=3, column=1, pady=5)

        # Buttons
        btn_add = tk.Button(input_frame, text="Add Patient", command=self.add_patient, bg="#4CAF50", fg="white", width=15)
        btn_add.grid(row=4, column=0, columnspan=2, pady=10)

        btn_discharge = tk.Button(input_frame, text="Discharge Selected", command=self.discharge_patient, bg="#f44336", fg="white", width=15)
        btn_discharge.grid(row=5, column=0, columnspan=2, pady=5)

        btn_delete = tk.Button(input_frame, text="Delete Patient", command=self.delete_patient, bg="#333", fg="white", width=15)
        btn_delete.grid(row=6, column=0, columnspan=2, pady=5)

        # Table Frame (Right Side)
        table_frame = tk.Frame(self.root)
        table_frame.pack(side="right", expand=True, fill="both", padx=10, pady=10)

        # Treeview (Table)
        columns = ("id", "name", "age", "gender", "status", "disease")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        
        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="Name")
        self.tree.heading("age", text="Age")
        self.tree.heading("gender", text="Gender")
        self.tree.heading("status", text="Status")
        self.tree.heading("disease", text="Disease")

        self.tree.column("id", width=30)
        self.tree.column("age", width=40)
        self.tree.pack(expand=True, fill="both")

    # ---------------- LOGIC ----------------
    def refresh_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for p in self.patients:
            self.tree.insert("", "end", values=(p["id"], p["name"], p["age"], p["gender"], p["status"], p["disease"]))

    def add_patient(self):
        try:
            name = self.name_entry.get().strip()
            age = int(self.age_entry.get())
            gender = self.gender_combo.get()
            disease = self.disease_entry.get().strip()

            if not name or not disease or not gender:
                raise ValueError("All fields are required.")

            patient = {
                "id": self.next_id,
                "name": name,
                "age": age,
                "gender": gender,
                "disease": disease,
                "status": "Admitted"
            }

            self.patients.append(patient)
            self.next_id += 1
            self.save_data()
            self.refresh_table()
            self.clear_inputs()
            messagebox.showinfo("Success", "Patient added successfully!")
        except ValueError as e:
            messagebox.showerror("Input Error", str(e) if "required" in str(e) else "Please enter a valid age.")

    def discharge_patient(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection", "Please select a patient from the list.")
            return

        item_values = self.tree.item(selected_item)["values"]
        pid = item_values[0]

        for p in self.patients:
            if p["id"] == pid:
                p["status"] = "Discharged"
                break
        
        self.save_data()
        self.refresh_table()
        messagebox.showinfo("Success", f"Patient {pid} discharged.")

    def delete_patient(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection", "Select a patient to delete.")
            return

        item_values = self.tree.item(selected_item)["values"]
        pid = item_values[0]

        if messagebox.askyesno("Confirm", f"Are you sure you want to delete Patient ID {pid}?"):
            self.patients = [p for p in self.patients if p["id"] != pid]
            self.save_data()
            self.refresh_table()

    def clear_inputs(self):
        self.name_entry.delete(0, tk.END)
        self.age_entry.delete(0, tk.END)
        self.disease_entry.delete(0, tk.END)
        self.gender_combo.set("")

# ---------------- START APP ----------------
if __name__ == "__main__":
    root = tk.Tk()
    app = PatientManager(root)
    root.mainloop()