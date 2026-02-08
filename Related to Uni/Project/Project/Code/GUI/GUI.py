import tkinter as tk
from tkinter import ttk, messagebox
import json, os

# Using the same database file as the CLI version for consistency
DB_FILE = "finance_data.json"

class FinanceMaster:
    def __init__(self, root):
        self.root = root
        self.root.title("FinanceMaster Pro | IUB")
        self.root.geometry("1000x650")
        self.root.configure(bg="#2c3e50")

        self.db = self.load_db()
        self.current_user = None
        self.show_login_screen()

    def load_db(self):
        if os.path.exists(DB_FILE):
            with open(DB_FILE, "r") as f: 
                data = json.load(f)
                # Handle both CLI and GUI structure formats
                return data.get("users", data)
        return {"admin": {"password": "123", "expenses": []}}

    def save_db(self):
        # Save in the structured format required by the project
        with open(DB_FILE, "w") as f: 
            json.dump({"users": self.db}, f, indent=4)

    def show_login_screen(self):
        self.clear_window()
        frame = tk.Frame(self.root, bg="#ecf0f1", padx=30, pady=30)
        frame.place(relx=0.5, rely=0.5, anchor="center")
        tk.Label(frame, text="User Login", font=("Arial", 18), bg="#ecf0f1").pack(pady=10)
        
        tk.Label(frame, text="Username:", bg="#ecf0f1").pack()
        self.u_ent = tk.Entry(frame); self.u_ent.pack(pady=5)
        
        tk.Label(frame, text="Password:", bg="#ecf0f1").pack()
        self.p_ent = tk.Entry(frame, show="*"); self.p_ent.pack(pady=5)
        
        tk.Button(frame, text="Login", command=self.handle_login, bg="#27ae60", fg="white").pack(fill="x", pady=5)
        tk.Button(frame, text="Sign Up", command=self.handle_signup).pack(fill="x")

    def handle_login(self):
        u, p = self.u_ent.get(), self.p_ent.get()
        if u in self.db and self.db[u]["password"] == p:
            self.current_user = u
            self.show_main_dashboard()
        else: messagebox.showerror("Error", "Invalid credentials!")

    def handle_signup(self):
        u, p = self.u_ent.get(), self.p_ent.get()
        if not u or not p:
            messagebox.showwarning("Warning", "Fields cannot be empty")
            return
        if u in self.db:
            messagebox.showerror("Error", "User already exists!")
            return
        
        self.db[u] = {"password": p, "expenses": []}
        self.save_db()
        messagebox.showinfo("Success", f"Account for {u} created successfully!")

    def show_main_dashboard(self):
        self.clear_window()
        sidebar = tk.Frame(self.root, width=300, bg="#ecf0f1", padx=15, pady=15)
        sidebar.pack(side="left", fill="y")
        
        content = tk.Frame(self.root, bg="#ffffff", padx=20, pady=20)
        content.pack(side="right", expand=True, fill="both")

        tk.Label(sidebar, text="Item Name:", bg="#ecf0f1").pack(fill="x")
        self.e_name = tk.Entry(sidebar); self.e_name.pack(fill="x", pady=5)
        
        tk.Label(sidebar, text="Amount (Rs.):", bg="#ecf0f1").pack(fill="x")
        self.e_amt = tk.Entry(sidebar); self.e_amt.pack(fill="x", pady=5)
        
        tk.Button(sidebar, text="Add Expense", command=self.add_rec, bg="#2ecc71").pack(fill="x", pady=2)
        tk.Button(sidebar, text="Update Selected", command=self.upd_rec, bg="#3498db").pack(fill="x", pady=2)
        tk.Button(sidebar, text="Delete Selected", command=self.del_rec, bg="#e67e22").pack(fill="x", pady=2)
        tk.Button(sidebar, text="Logout", command=self.show_login_screen).pack(fill="x", pady=20)

        self.bal_lbl = tk.Label(content, text="Total: Rs.0.00", font=("Arial", 20), bg="white")
        self.bal_lbl.pack(pady=10)

        self.tree = ttk.Treeview(content, columns=("ID", "Name", "Cost"), show="headings")
        self.tree.heading("ID", text="ID"); self.tree.heading("Name", text="Item"); self.tree.heading("Cost", text="Rs.")
        self.tree.pack(expand=True, fill="both")
        self.refresh_table()

    def add_rec(self):
        try:
            name = self.e_name.get()
            cost_str = self.e_amt.get()
            if not name or not cost_str:
                messagebox.showwarning("Input Error", "Please fill all fields")
                return
            
            cost = float(cost_str)
            exps = self.db[self.current_user]["expenses"]
            # Correct ID generation to avoid duplicates
            new_id = max([e["id"] for e in exps], default=0) + 1
            
            self.db[self.current_user]["expenses"].append({"id": new_id, "name": name, "cost": cost})
            self.save_db()
            self.e_name.delete(0, tk.END)
            self.e_amt.delete(0, tk.END)
            self.refresh_table()
        except ValueError: 
            messagebox.showerror("Error", "Please enter a valid numeric amount")

    def del_rec(self):
        sel = self.tree.selection()
        if not sel: return
        for s in sel:
            idx = int(self.tree.item(s, "values")[0])
            self.db[self.current_user]["expenses"] = [e for e in self.db[self.current_user]["expenses"] if e["id"] != idx]
        self.save_db()
        self.refresh_table()

    def upd_rec(self):
        sel = self.tree.selection()
        if not sel: 
            messagebox.showinfo("Update", "Please select a row to update")
            return
        try:
            idx = int(self.tree.item(sel[0], "values")[0])
            for e in self.db[self.current_user]["expenses"]:
                if e["id"] == idx:
                    e["name"] = self.e_name.get() or e.get("name") or e.get("item")
                    new_val = self.e_amt.get()
                    if new_val: e["cost"] = float(new_val)
            self.save_db()
            self.refresh_table()
        except ValueError: 
            messagebox.showerror("Error", "Invalid amount format")

    def refresh_table(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        total = 0
        for e in self.db[self.current_user]["expenses"]:
            # Support both 'name' and 'item' keys for CLI compatibility
            name = e.get("name") or e.get("item")
            self.tree.insert("", "end", values=(e["id"], name, f"{e['cost']:.2f}"))
            total += e["cost"]
        self.bal_lbl.config(text=f"Total: Rs.{total:,.2f}")

    def clear_window(self):
        for widget in self.root.winfo_children(): widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = FinanceMaster(root)
    root.mainloop()