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
        # Ràng buộc tên phải là các kí tự
        if data["Name"].isdigit():
            messagebox.showerror("Lỗi", "Name phải là chuỗi kí tự!")
            return
        # Kiểm tra định dạng số cho Age
        if not data["Age"].isdigit():
            messagebox.showerror("Lỗi", "Age phải là một số nguyên dương!")
            return
        if int(data["Age"]) > 120:
            messagebox.showerror("Lỗi", "Tuổi chỉ từ 0 - 120!")
            return
            
        room_num = data["Room Number"].strip()
        try:
            room_num_int = int(room_num)
            if room_num_int < 0: 
                messagebox.showerror("Lỗi", "Room Number không được là số âm!")
                return
        except:
            messagebox.showerror("Lỗi", "Room Number phải là một số!")
            return
            
        # Thêm dữ liệu vào DataFrame
        try:
            for key in ["Age", "Room Number"]:
                data[key] = int(data[key])
            data["Billing Amount"] = float(data["Billing Amount"])
            viewer.df = pd.concat(
                [viewer.df, pd.DataFrame([data])],
                ignore_index=True
            )
            # Ensure data types are maintained
            viewer.df = viewer.df.convert_dtypes()
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
    if index is None or len(index) != 1:
        messagebox.showwarning("Cảnh báo", "Chỉ được chọn 1 dòng để cập nhật!")
        return
    index = index[0]

    
    # Tạo cửa sổ
    update_window = tk.Toplevel(viewer.root)
    update_window.title("Cập nhật dữ liệu")
    
    # Danh sách các cột dữ liệu
    labels = viewer.df.columns
    entries = {}
    
    # Hiện thị các ô và dữ liệu đã được nhập trước đó
    for i, label in enumerate(labels):
        tk.Label(update_window, text=f"{label}:").grid(row=i, column=0, padx=10, pady=5)
        entry = tk.Entry(update_window)
        entry.insert(0, str(viewer.df.at[index, label]))
        entry.grid(row=i, column=1,padx=10,pady=5)
        entries[label] = entry
        
    # Xử lí
    def submit_update():
        new_data = {label: entry.get().strip() for label, entry in entries.items()}
        # Ensure data types are maintained
        for key, value in new_data.items():
            if key in ["Age", "Room Number"]:
                viewer.df.at[index, key] = int(value)
            elif key == "Billing Amount":
                viewer.df.at[index, key] = float(value)
            else:
                viewer.df.at[index, key] = value
        viewer.df = viewer.df.convert_dtypes()
    

        # Kiểm tra định dạng số cho Age
        if not new_data["Age"].isdigit():
            messagebox.showerror("Lỗi", "Age phải là một số nguyên dương!")
            return
        
        if new_data["Name"].isdigit():
            messagebox.showerror("Lỗi", "Name phải là chuỗi kí tự!")
            return

        if int(new_data["Age"]) > 120:
            messagebox.showerror("Lỗi", "Tuổi chỉ từ 0 - 120!")
            return
            
        room_num = new_data["Room Number"].strip()
        try:
            room_num_int = int(room_num)
            if room_num_int < 0: 
                messagebox.showerror("Lỗi", "Room Number không được là số âm!")
                return
        except:
            messagebox.showerror("Lỗi", "Room Number phải là một số!")
            return
        
        viewer.load_data(viewer.current_page)
        update_window.destroy()
        
    # Nút Cập nhật
    tk.Button(update_window, text="Cập nhật", command=submit_update).grid(row=len(labels), column=0, columnspan=2, pady=10)

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
