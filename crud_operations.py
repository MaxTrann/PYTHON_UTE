import pandas as pd
from tkinter import simpledialog, messagebox, filedialog
import tkinter as tk

def add_data(viewer):
    # Tạo cửa sổ nhập liệu
    input_window = tk.Toplevel(viewer.root)
    input_window.title("Thêm dữ liệu")

    # Danh sách các trường nhập liệu
    labels = [
        "Name", "Age", "Gender", "Blood Type", "Medical Condition",
        "Date of Admission", "Doctor", "Hospital", "Insurance Provider",
        "Billing Amount", "Room Number", "Admission Type",
        "Discharge Date", "Medication", "Test Results"
    ]
    entries = {}

    # Tạo các nhãn và ô nhập liệu
    for i, label in enumerate(labels):
        tk.Label(input_window, text=f"{label}:").grid(row=i, column=0, padx=10, pady=5)
        entry = tk.Entry(input_window)
        entry.grid(row=i, column=1, padx=10, pady=5)
        entries[label] = entry

    # Hàm xử lý khi nhấn nút Thêm
    def submit_data():
        # Lấy dữ liệu từ các trường nhập liệu
        data = {label: entry.get().strip() for label, entry in entries.items()}

        # Kiểm tra đầu vào bắt buộc
        if not data["Name"] or not data["Age"]:
            messagebox.showerror("Lỗi", "Các trường Name và Age không được để trống!")
            return

        # Kiểm tra định dạng số cho Age và Billing Amount
        if not data["Age"].isdigit():
            messagebox.showerror("Lỗi", "Age phải là một số nguyên dương!")
            return
        

        if int(data["Age"]) > 120:
            messagebox.showerror("Lỗi", "Tuổi chỉ từ 0 - 100!")
            return
            
        if not data["Room Number"].isdigit():
            messagebox.showerror("Lỗi", "Room Number phải là một số nguyên dương!")
            return

        # Thêm dữ liệu vào DataFrame
        try:
            viewer.df = pd.concat(
                [viewer.df, pd.DataFrame([data])],
                ignore_index=True
            )
            viewer.load_data(viewer.current_page)  # Move this line inside the try block
            input_window.destroy()
            messagebox.showinfo("Thành công", "Thêm dữ liệu thành công!")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể thêm dữ liệu: {str(e)}")

    # Nút Thêm
    tk.Button(input_window, text="Thêm", command=submit_data).grid(row=len(labels), column=0, columnspan=2, pady=10)
    

def update_data(viewer):
    # Implement logic to update data
    index = viewer.get_selected_index()
    if index is not None:
        new_data = viewer.get_input_data()
        if new_data:
            for key, value in new_data.items():
                viewer.df.at[index, key] = value
            viewer.load_data(viewer.current_page)

def delete_data(viewer):
    index = viewer.get_selected_index()
    if index is None:
        messagebox.showwarning("Cảnh báo", "Hãy chọn một dòng để xóa!")
        return

    try:
        viewer.df = viewer.df.drop(index).reset_index(drop=True)
        viewer.load_data(viewer.current_page)
        messagebox.showinfo("Thành công", f"Xóa {len(index)} dòng thành công!")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể xóa dữ liệu: {str(e)}")


def save_data(viewer):
    # Implement logic to save data
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if file_path:
        viewer.df.to_csv(file_path, index=False)
        messagebox.showinfo("Success", "Data saved successfully")

def getData(filePath):
    # Tải dữ liệu từ file csv
    try:
        data = pd.read_csv(filePath)
        if data.empty:
            return None
        return data
    except Exception as e:
        return None
