import pandas as pd
from tkinter import ttk, filedialog, messagebox

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
        viewer.condition_listbox.delete(0, ttk.END)

def deleteOutliers(data, col, default_values):
    if col not in data.columns:
        raise KeyError(f"Cột '{col}' không tồn tại trong dữ liệu!")
    
    filtered_data = data[data[col].isin(default_values)]
    return filtered_data

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