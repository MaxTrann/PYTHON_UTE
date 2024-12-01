import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
import pandas as pd

from crud_operations import add_data, update_data, delete_data, save_data, getData

class LargeDatasetViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("Phần mềm xử lý dữ liệu")
        self.root.geometry("2000x600")
        
        self.df = None
        self.page_size = 100
        self.current_page = 0
        
        self.create_welcome_screen()
        
    def create_welcome_screen(self):
        self.welcome_frame = tk.Frame(self.root)
        self.welcome_frame.pack(fill=tk.BOTH, expand=True)
        
        welcome_label = tk.Label(self.welcome_frame, text="Chào mừng bạn đến với phần mềm xử lý dữ liệu", font=("Arial", 24))
        welcome_label.pack(pady=20)
        
        continue_button = tk.Button(self.welcome_frame, text="Tiếp tục", command=self.show_file_selection)
        continue_button.pack(pady=10)
        
    def show_file_selection(self):
        self.welcome_frame.destroy()
        self.create_file_selection_screen()
        
    def create_file_selection_screen(self):
        self.file_selection_frame = tk.Frame(self.root)
        self.file_selection_frame.pack(fill=tk.BOTH, expand=True)
        
        open_button = tk.Button(self.file_selection_frame, text="Chọn file CSV", command=self.open_file)
        open_button.pack(pady=10)
        
    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            try:
                self.df = getData(file_path)
                if self.df is not None:
                    self.file_selection_frame.destroy()
                    self.create_widgets()
                    self.tree["columns"] = list(self.df.columns)
                    for col in self.tree["columns"]:
                        self.tree.heading(col, text=col)
                        self.tree.column(col, width=100, stretch=True)
                    self.load_data(0)
                else:
                    messagebox.showerror("Error", "File csv không tồn tại dữ liệu!")
            except Exception as e:
                messagebox.showerror("Error", f"Could not read file: {e}")
        
    def create_widgets(self):
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)
        
        crud_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="CRUD", menu=crud_menu)
        crud_menu.add_command(label="Thêm dữ liệu", command=lambda: add_data(self))
        crud_menu.add_command(label="Cập nhật dữ liệu", command=lambda: update_data(self))
        crud_menu.add_command(label="Xóa dữ liệu", command=lambda: delete_data(self))
        crud_menu.add_command(label="Lưu dữ liệu", command=lambda: save_data(self))
        
        cleaning_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Cleaning", menu=cleaning_menu)
        cleaning_menu.add_command(label="Xóa hàng trống", command=self.remove_empty_rows)
        cleaning_menu.add_command(label="Xóa cột trống", command=self.remove_empty_columns)
        cleaning_menu.add_command(label="Điền dữ liệu còn thiếu", command=self.fill_missing_data_prompt)

        visual_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Visualize", menu=visual_menu)
        visual_menu.add_command(label="Histogram", command=self.show_histogram)
        visual_menu.add_command(label="Scatter Plot", command=self.show_scatter_plot)
        
        frame = tk.Frame(self.root)
        frame.pack(fill=tk.BOTH, expand=True)

        self.tree = ttk.Treeview(frame, show="headings")
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar_y = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscroll=scrollbar_y.set)

        scrollbar_x = ttk.Scrollbar(self.root, orient=tk.HORIZONTAL, command=self.tree.xview)
        scrollbar_x.pack(fill=tk.X)
        self.tree.configure(xscroll=scrollbar_x.set)

        nav_frame = tk.Frame(self.root)
        nav_frame.pack(fill=tk.X)

        self.prev_button = tk.Button(nav_frame, text="Trang trước", command=lambda: self.load_data(self.current_page - 1))
        self.prev_button.pack(side=tk.LEFT, padx=5)

        self.page_label = tk.Label(nav_frame, text="")
        self.page_label.pack(side=tk.LEFT, padx=5)

        self.next_button = tk.Button(nav_frame, text="Trang sau", command=lambda: self.load_data(self.current_page + 1))
        self.next_button.pack(side=tk.LEFT, padx=5)
        
    def load_data(self, page):
        self.current_page = page
        for row in self.tree.get_children():
            self.tree.delete(row)

        start = page * self.page_size
        end = start + self.page_size
        for index, row in self.df.iloc[start:end].iterrows():
            self.tree.insert("", tk.END, values=list(row))

        self.update_page_buttons()

    def update_page_buttons(self):
        total_pages = (len(self.df) + self.page_size - 1) // self.page_size
        self.prev_button["state"] = tk.NORMAL if self.current_page > 0 else tk.DISABLED
        self.next_button["state"] = tk.NORMAL if self.current_page < total_pages - 1 else tk.DISABLED
        self.page_label["text"] = f"Trang {self.current_page + 1}/{total_pages}"

    def remove_empty_rows(self):
        self.df.dropna(how='all', inplace=True)
        self.load_data(self.current_page)

    def remove_empty_columns(self):
        self.df.dropna(axis=1, how='all', inplace=True)
        self.tree["columns"] = list(self.df.columns)
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
        self.load_data(self.current_page)

    def fill_missing_data_prompt(self):
        col_name = simpledialog.askstring("Nhập cột", "Tên cột:")
        if col_name not in self.df.columns:
            messagebox.showerror("Lỗi", f"Cột {col_name} không tồn tại.")
            return

        # Prompt the user to choose the type of data to input
        data_type = simpledialog.askstring("Chọn kiểu dữ liệu", "Nhập 's' để chọn chuỗi hoặc 'n' để chọn số:")
        if data_type not in ['s', 'n']:
            messagebox.showerror("Lỗi", "Vui lòng chọn 's' cho chuỗi hoặc 'n' cho số.")
            return
        
        while True:
            try:
                if data_type == 'n':
                    # If the user chooses a number, ask for a numeric value
                    value = simpledialog.askstring("Nhập giá trị thay thế", "Nhập giá trị thay thế (số):")
                    if value is None:
                        return  # User clicked cancel
                    value = int(value)  # Convert input to integer
                    if value <= 0:
                        raise ValueError("Giá trị phải lớn hơn 0.")
                elif data_type == 's':
                    # If the user chooses a string, ask for a string value
                    value = simpledialog.askstring("Nhập giá trị thay thế", "Nhập giá trị thay thế (chuỗi):")
                    if value is None:
                        return  # User clicked cancel
                    if len(value.strip()) == 0:
                        raise ValueError("Giá trị không thể trống.")
                break
            except ValueError as e:
                messagebox.showerror("Lỗi", f"Lỗi:giá trị không hợp lệ")

        self.fill_missing_data(col_name, value, data_type)

    def fill_missing_data(self, col_name, value, data_type):
        if col_name in self.df.columns:
            missing_cnt = self.df[col_name].isna().sum()
            if missing_cnt > 0:
                if data_type == 'n':  # Handle number case
                    self.df[col_name].fillna(value, inplace=True)
                elif data_type == 's':  # Handle string case
                    self.df[col_name].fillna(value, inplace=True)
                messagebox.showinfo("Thông báo", f"Đã điền {missing_cnt} giá trị vào cột {col_name} với giá trị {value}.")
                self.load_data(self.current_page)
            else:
                messagebox.showinfo("Thông báo", f"Cột {col_name} không có giá trị bị thiếu.")
        else:
            messagebox.showerror("Lỗi", f"Cột {col_name} không tồn tại.")

    def show_histogram(self):
        pass

    def show_scatter_plot(self):
        pass

if __name__ == "__main__":
    root = tk.Tk()
    app = LargeDatasetViewer(root)
    root.mainloop()
