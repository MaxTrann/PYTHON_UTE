import pandas as pd
import numpy as np
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
def fill_missing_data_prompt(viewer):
    """Hiển thị lời nhắc điền dữ liệu còn thiếu."""
    col_name = simpledialog.askstring("Nhập cột", "Tên cột:")
    if col_name not in viewer.df.columns:
        messagebox.showerror("Lỗi", f"Cột {col_name} không tồn tại.")
        return

    # Kiểm tra ngay lập tức nếu cột không có giá trị thiếu
    missing_cnt = viewer.df[col_name].isna().sum()
    if missing_cnt == 0:
        messagebox.showinfo("Thông báo", f"Cột {col_name} không có giá trị bị thiếu.")
        return

    data_type = simpledialog.askstring("Chọn kiểu dữ liệu", "Nhập 's' để chọn chuỗi hoặc 'n' để chọn số:")
    if data_type not in ['s', 'n']:
        messagebox.showerror("Lỗi", "Vui lòng chọn 's' cho chuỗi hoặc 'n' cho số.")
        return
    
    while True:
        try:
            value = simpledialog.askstring("Nhập giá trị thay thế", "Nhập giá trị thay thế:")
            if value is None:
                return  # Người dùng nhấn hủy
            if data_type == 'n':
                value = int(value)  # Chuyển thành số nếu cần
                if value <= 0:
                    raise ValueError("Giá trị phải lớn hơn 0.")
            elif data_type == 's':
                if len(value.strip()) == 0:
                    raise ValueError("Giá trị không thể trống.")
            break
        except ValueError as e:
            messagebox.showerror("Lỗi", f"Lỗi: {str(e)}")

    # Gọi hàm điền dữ liệu
    viewer.fill_missing_data(col_name, value, data_type)
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