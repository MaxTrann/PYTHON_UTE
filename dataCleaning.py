import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog, END
from datetime import datetime

def loadData(Data_File):
    return pd.read_csv(Data_File)

def sortData(data, col, greater=True):
    if col not in data.columns:
        raise KeyError(f"Cột '{col}' không tồn tại trong dữ liệu!")
    return data.sort_values(by=col, ascending=greater)

def search_data(viewer):
        # Duyệt qua tất cả các điều kiện và áp dụng chúng lên DataFrame
        filtered_df = viewer.df
        conditions_dict = {}

        # Nhóm các điều kiện theo cột
        for column, key in viewer.search_conditions:
            if column not in conditions_dict:
                conditions_dict[column] = []
            conditions_dict[column].append(key)

        # Lọc dữ liệu theo từng cột và điều kiện
        for column, keys in conditions_dict.items():
            # Tạo điều kiện cho mỗi giá trị trong cột
            condition = filtered_df[column].astype(str).str.lower().isin([key.lower() for key in keys])

            # Áp dụng điều kiện lọc lên DataFrame
            filtered_df = filtered_df[condition]

        # Hiển thị dữ liệu tìm kiếm trong cửa sổ mới
        viewer.show_search_results(filtered_df)

        # Xóa điều kiện sau khi tìm kiếm
        viewer.search_conditions = []
        viewer.condition_listbox.delete(0, END)

def deleteOutliers(data, col, default_values):
    if col not in data.columns:
        raise KeyError(f"Cột '{col}' không tồn tại trong dữ liệu!")
    
    filtered_data = data[data[col].isin(default_values)]
    return filtered_data
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

def fill_missing_data_prompt(viewer):
    """Hiển thị giao diện điền dữ liệu còn thiếu với ràng buộc nhập liệu."""
    
    def validate_date_format(date_string):
        """Kiểm tra chuỗi có đúng định dạng ngày tháng năm."""
        formats = ["%d/%m/%Y", "%Y-%m-%d"]  # Các định dạng ngày tháng hợp lệ
        for fmt in formats:
            try:
                datetime.strptime(date_string, fmt)
                return True
            except ValueError:
                continue
        return False

    # Tạo cửa sổ con
    top = tk.Toplevel()
    top.title("Điền dữ liệu còn thiếu")
    top.geometry("400x300")
    top.configure(bg="#f5f5f5")
    top.transient(viewer.root)

    tk.Label(top, text="Chọn cột cần điền dữ liệu", font=("Arial", 14, "bold"), bg="#f5f5f5").pack(pady=10)
    
    col_var = tk.StringVar()
    column_combobox = ttk.Combobox(top, textvariable=col_var, state="readonly", font=("Arial", 11))
    column_combobox['values'] = viewer.df.columns.tolist()
    column_combobox.pack(pady=5, padx=20, ipadx=5, ipady=5)

    tk.Label(top, text="Chọn kiểu dữ liệu:", font=("Arial", 12), bg="#f5f5f5").pack(pady=10)
    data_type_var = tk.StringVar(value='s')
    frame_radio = tk.Frame(top, bg="#f5f5f5")
    frame_radio.pack(pady=5)
    ttk.Radiobutton(frame_radio, text="Chuỗi", variable=data_type_var, value='s').pack(side=tk.LEFT, padx=10)
    ttk.Radiobutton(frame_radio, text="Số", variable=data_type_var, value='n').pack(side=tk.LEFT, padx=10)

    def on_confirm():
        col_name = col_var.get()
        if not col_name:
            messagebox.showerror("Lỗi", "Vui lòng chọn một cột.")
            return

        missing_cnt = viewer.df[col_name].isna().sum()
        if missing_cnt == 0:
            messagebox.showinfo("Thông báo", f"Cột '{col_name}' không có giá trị bị thiếu.")
            top.destroy()
            return

        data_type = data_type_var.get()

        while True:
            try:
                value = simpledialog.askstring("Nhập giá trị thay thế", "Nhập giá trị thay thế:")
                if value is None:
                    return  # Người dùng nhấn hủy

                # Kiểm tra dữ liệu theo kiểu đã chọn
                if data_type == 'n':
                    if not value.isdigit():
                        raise ValueError("Giá trị phải là số nguyên dương.")
                    value = int(value)
                elif data_type == 's':
                    if validate_date_format(value):
                        # Là ngày tháng hợp lệ
                        pass
                    else:
                        if any(char.isdigit() for char in value):
                            raise ValueError("Giá trị chuỗi không được chứa số (trừ khi là ngày tháng).")
                        if len(value.strip()) == 0:
                            raise ValueError("Giá trị không thể trống.")
                break
            except ValueError as e:
                messagebox.showerror("Lỗi", f"{str(e)} Vui lòng nhập lại.")

        viewer.fill_missing_data(col_name, value, data_type)
        top.destroy()

    btn_frame = tk.Frame(top, bg="#f5f5f5")
    btn_frame.pack(pady=20)
    ttk.Button(btn_frame, text="Xác nhận", command=on_confirm).pack(side=tk.LEFT, padx=10)
    ttk.Button(btn_frame, text="Hủy", command=top.destroy).pack(side=tk.LEFT, padx=10)
def clean_string(val):
    """Chuẩn hóa chuỗi: loại bỏ khoảng trắng thừa và viết hoa chữ cái đầu mỗi từ."""
    if pd.isna(val):
        return val
    # Tách các từ, loại bỏ khoảng trắng thừa, ghép lại với một dấu cách
    return ' '.join(str(val).strip().split()).title()

def normalize_gender(val):
    """Chuẩn hóa giới tính: đồng nhất thành 'Male' hoặc 'Female'."""
    if pd.isna(val):
        return val
    val = str(val).strip().lower()
    return 'Male' if val in ['m', 'male'] else 'Female' if val in ['f', 'female'] else np.nan

def normalize_blood_type(val):
    """Chuẩn hóa nhóm máu: chấp nhận A, B, AB, O kèm dấu + hoặc -."""
    valid_types = {'A', 'B', 'AB', 'O'}
    if pd.isna(val):
        return val
    val = str(val).strip().upper()  # Xóa khoảng trắng thừa và chuyển thành chữ hoa
    
    # Kiểm tra giá trị hợp lệ
    if val in valid_types:
        return val  # Nhóm máu hợp lệ không có dấu
    elif len(val) > 1 and val[:-1] in valid_types and val[-1] in ['+', '-']:
        return val  # Nhóm máu hợp lệ có dấu + hoặc -
    else:
        return np.nan  # Không hợp lệ

def is_valid_date(day, month, year):
    """Kiểm tra xem ngày, tháng, năm có hợp lệ không."""
    try:
        # Tạo đối tượng datetime để kiểm tra tính hợp lệ
        datetime(year, month, day)
        return True
    except ValueError:
        return False

def normalize_date(val):
    """Chuẩn hóa ngày tháng năm, đảm bảo ngày hợp lệ và định dạng đúng (YYYY-MM-DD)."""
    if pd.isna(val):
        return np.nan

    # Danh sách các định dạng ngày đầu vào có thể chấp nhận
    possible_formats = ["%d/%m/%Y", "%d-%m-%Y", "%Y-%m-%d", "%m/%d/%Y", "%Y/%m/%d"]

    for fmt in possible_formats:
        try:
            # Chuyển đổi chuỗi thành đối tượng datetime
            parsed_date = datetime.strptime(val.strip(), fmt)
            
            # Kiểm tra tính hợp lệ của ngày, tháng, năm
            if is_valid_date(parsed_date.day, parsed_date.month, parsed_date.year):
                # Trả về định dạng chuẩn YYYY-MM-DD
                return parsed_date.strftime('%Y-%m-%d')
        except (ValueError, TypeError):
            continue
    
    # Nếu tất cả các kiểm tra thất bại, trả về NaN
    return np.nan

def normalize_billing_amount(val):
    """Chuẩn hóa số tiền thanh toán: chuyển thành số thực."""
    try:
        return float(val)
    except (ValueError, TypeError):
        return np.nan

def normalize_column(df, col):
    """Chuẩn hóa dữ liệu trong cột cụ thể."""
    if col not in df.columns:
        raise ValueError(f"Cột {col} không tồn tại trong DataFrame.")
    
    # Dictionary mapping column names to normalization functions
    normalization_map = {
        "Name": clean_string,
        "Gender": normalize_gender,
        "Blood Type": normalize_blood_type,
        "Medical Condition": clean_string,
        "Date of Admission": normalize_date,
        "Doctor": clean_string,
        "Hospital": clean_string,
        "Insurance Provider": clean_string,
        "Billing Amount": normalize_billing_amount,
        "Room Number": clean_string,
        "Admission Type": clean_string,
        "Discharge Date": normalize_date,
        "Medication": clean_string,
        "Test Results": clean_string,
    }

    if col in normalization_map:
        df[col] = df[col].apply(normalization_map[col])
        return df
    else:
        raise ValueError(f"Cột {col} không được hỗ trợ chuẩn hóa.")

# def delete_outliers_menu (data, col, valid_values):
#     # Xóa giá trị ngoại lai
#     def delete_outliers():
#         if self.df is not None:
#             if col in self.df.columns:
#                 self.df = deleteOutliers(self.df, col, valid_values)
#                 self.load_data(self.current_page)  # Tải lại dữ liệu sau khi làm sạch
#                 messagebox.showinfo("Thông báo", f"Đã xóa các dòng có giá trị ngoại lệ ở cột {col}.")
#             else:
#                 messagebox.showerror("Lỗi", f"Cột '{col}' không tồn tại trong dữ liệu.")
#         else:
#             messagebox.showerror("Lỗi", "Không có dữ liệu để xử lý.")
    
#     delete_menu = tk.Menu(self.tree, tearoff=0)
#     delete_menu.add_command(label=f"Xóa dữ liệu ngoại lai trong {col}", command=delete_outliers)
#     delete_menu.post(self.root.winfo_pointerx(), self.root.winfo_pointery())