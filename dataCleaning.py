import pandas as pd

def loadData(Data_File):
    return pd.read_csv(Data_File)

def sortData(data, col, greater=True):
    if col not in data.columns:
        raise KeyError(f"Cột '{col}' không tồn tại trong dữ liệu!")
    return data.sort_values(by=col, ascending=greater)

def searchData(data,col,keyword):
    if col in data.columns:
        ans = data[data[col].astype(str).str.contains(keyword, case=True, na=False)]
        print("Kết quả tìm kiếm: ")
        print(ans)
    else:
        print(f"{col} không có trong dữ liệu!")

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