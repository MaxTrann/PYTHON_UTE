import tkinter as tk
from tkinter import ttk
import pandas as pd
from vdcrud import add_row, delete_row  # Import các hàm từ module

# Khởi tạo DataFrame
df = pd.DataFrame(columns=["ID", "Name", "Age"])

# Hàm tải dữ liệu
def load_data():
    for row in tree.get_children():
        tree.delete(row)
    for _, row in df.iterrows():
        tree.insert("", tk.END, values=list(row))

# Giao diện chính
root = tk.Tk()
root.title("Data Management App")

# Entry nhập dữ liệu
entry_frame = tk.Frame(root)
entry_frame.pack()

entry_id = tk.Entry(entry_frame, width=10)
entry_name = tk.Entry(entry_frame, width=20)
entry_age = tk.Entry(entry_frame, width=5)

entry_id.pack(side=tk.LEFT, padx=5)
entry_name.pack(side=tk.LEFT, padx=5)
entry_age.pack(side=tk.LEFT, padx=5)

# Bảng dữ liệu (Treeview)
tree = ttk.Treeview(root, columns=["ID", "Name", "Age"], show="headings")
tree.heading("ID", text="ID")
tree.heading("Name", text="Name")
tree.heading("Age", text="Age")
tree.pack(fill=tk.BOTH, expand=True)

# Nút thêm và xóa
button_frame = tk.Frame(root)
button_frame.pack()

btn_add = tk.Button(
    button_frame,
    text="Add Row",
    command=lambda: update_df(add_row(entry_id, entry_name, entry_age, df, load_data))  # Update DataFrame
)
btn_delete = tk.Button(
    button_frame,
    text="Delete Row",
    command=lambda: update_df(delete_row(tree, df, load_data))  # Update DataFrame
)

btn_add.pack(side=tk.LEFT, padx=5)
btn_delete.pack(side=tk.LEFT, padx=5)

def update_df(new_df):
    global df
    df = new_df
    load_data()

root.mainloop()
