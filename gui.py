import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
from dataCleaning import sortData, search_data#, deleteOutliers, deleteMissingDataRow  # Import hàm sortData từ dataSorting.py

from crud_operations import add_data, update_data, delete_data, save_data, getData

class LargeDatasetViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("Phần mềm xử lý dữ liệu")
        self.root.geometry("2000x600")
        
        self.df = None
        self.page_size = 50
        self.current_page = 0
        self.data_processor = None
        self.sort_reverse = {col: False for col in []}  # Dictionnary to store sort order for each column
        self.search_conditions = []  # Danh sách lưu các điều kiện lọc
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
                    # Xóa các cột cũ trong Treeview
                    self.tree["columns"] = list(self.df.columns)
                    for col in self.tree["columns"]:
                        self.tree.heading(col, text=col, command=lambda _col=col: self.show_sort_menu(_col))
                        self.tree.column(col, width=100, stretch=True)  # Tự co giãn theo nội dung
                    self.load_data(0)  # Tải dữ liệu trang đầu tiên
                else:
                    messagebox.showerror("Error", "File csv không tồn tại dữ liệu!")
            except Exception as e:
                messagebox.showerror("Error", f"Could not read file: {e}")
        
    def create_widgets(self):
        # Tạo menu
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)
        
        crud_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="CRUD", menu=crud_menu)
        crud_menu.add_command(label="Thêm dữ liệu", command=lambda: add_data(self))
        crud_menu.add_command(label="Cập nhật dữ liệu", command=lambda: update_data(self))
        crud_menu.add_command(label="Xóa dữ liệu", command=lambda: delete_data(self))
        crud_menu.add_command(label="Lưu dữ liệu", command=lambda: save_data(self))
        
        # Thêm menu Cleaning
        cleaning_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Cleaning", menu=cleaning_menu)
        cleaning_menu.add_command(label="Xóa hàng trống", command=self.remove_empty_data_rows)
        cleaning_menu.add_command(label="Xóa cột trống", command=self.remove_empty_columns)
        # cleaning_menu.add_command(label="Xoá giá trị ngoại lai", command=lambda: delete_outliers_menu(self))
        cleaning_menu.add_command(label="Tìm kiếm", command=self.create_search_widget)  # Thêm mục tìm kiếm vào menu Cleaning


        visual_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Visualize", menu=visual_menu)
        visual_menu.add_command(label="Histogram", command=self.show_histogram)
        visual_menu.add_command(label="Scatter Plot", command=self.show_scatter_plot)

        # Bảng dữ liệu (Treeview) với thanh cuộn
        frame = tk.Frame(self.root)
        frame.pack(fill=tk.BOTH, expand=True)

        self.tree = ttk.Treeview(frame, show="headings")
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Thanh cuộn dọc
        scrollbar_y = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscroll=scrollbar_y.set)

        # Thanh cuộn ngang
        scrollbar_x = ttk.Scrollbar(self.root, orient=tk.HORIZONTAL, command=self.tree.xview)
        scrollbar_x.pack(fill=tk.X)
        self.tree.configure(xscroll=scrollbar_x.set)

        # Thanh điều hướng phân trang
        nav_frame = tk.Frame(self.root)
        nav_frame.pack(fill=tk.X)

        self.head_button = tk.Button(nav_frame, text="Trang đầu", command=lambda: self.load_data(0))
        self.head_button.pack(side=tk.LEFT, padx=5)

        self.prev_button = tk.Button(nav_frame, text="Trang trước", command=lambda: self.load_data(self.current_page - 1))
        self.prev_button.pack(side=tk.LEFT, padx=5)

        self.page_label = tk.Label(nav_frame, text="")
        self.page_label.pack(side=tk.LEFT, padx=5)

        self.next_button = tk.Button(nav_frame, text="Trang sau", command=lambda: self.load_data(self.current_page + 1))
        self.next_button.pack(side=tk.LEFT, padx=5)

        self.tail_button = tk.Button(nav_frame, text="Trang cuối", command=lambda: self.load_data(-1))
        self.tail_button.pack(side=tk.LEFT, padx=5)
        
    def show_sort_menu(self, col):
        def sort_ascending():
            self.df = sortData(self.df, col, greater=True)  # Gọi hàm sortData
            self.load_data(self.current_page)  # Tải lại dữ liệu sau khi sắp xếp

        def sort_descending():
            self.df = sortData(self.df, col, greater=False)  # Gọi hàm sortData
            self.load_data(self.current_page)  # Tải lại dữ liệu sau khi sắp xếp
    
        # Tạo menu thả xuống
        sort_menu = tk.Menu(self.tree, tearoff=0)
        sort_menu.add_command(label="Sắp xếp tăng dần", command=sort_ascending)
        sort_menu.add_command(label="Sắp xếp giảm dần", command=sort_descending)

        # Vị trí nhấp chuột
        sort_menu.post(self.root.winfo_pointerx(), self.root.winfo_pointery())

    def create_search_widget(self):
        # Tạo phần tìm kiếm
        search_frame = tk.Frame(self.root)
        search_frame.pack(fill=tk.X, padx=10, pady=10)

        search_label = tk.Label(search_frame, text="Nhập từ khóa tìm kiếm:")
        search_label.pack(side=tk.LEFT, padx=5)

        self.search_entry = tk.Entry(search_frame, width=40)
        self.search_entry.pack(side=tk.LEFT, padx=5)

        column_label = tk.Label(search_frame, text="Chọn cột:")
        column_label.pack(side=tk.LEFT, padx=5)

        self.column_combobox = ttk.Combobox(search_frame, values=list(self.df.columns), state="readonly")
        self.column_combobox.pack(side=tk.LEFT, padx=5)
        self.column_combobox.set("Chọn")  # Giá trị mặc định

        add_condition_button = tk.Button(search_frame, text="Thêm điều kiện", command=self.add_search_condition)
        add_condition_button.pack(side=tk.LEFT, padx=5)

        search_button = tk.Button(search_frame, text="Tìm kiếm", command=lambda: search_data(self))
        search_button.pack(side=tk.LEFT, padx=5)
        # Bảng hiển thị các điều kiện đã thêm
        self.condition_label = tk.Label(self.root, text="Các điều kiện tìm kiếm đã thêm:")
        self.condition_label.pack(pady=10)
        self.condition_listbox = tk.Listbox(self.root, height=5, width=50)
        self.condition_listbox.pack(pady=5)
        # Thêm nút Exit để thoát khỏi chế độ tìm kiếm
        exit_button = tk.Button(search_frame, text="Thoát", command=self.exit_search)
        exit_button.pack(side=tk.LEFT, padx=5)
    # def exit_search(self):
    #     """Tắt giao diện tìm kiếm và quay lại giao diện chính."""
    #     # Xóa tất cả các widget liên quan đến tìm kiếm
    #     if hasattr(self, 'search_widgets'):  # Kiểm tra nếu danh sách widget tồn tại
    #         for widget in self.search_widgets:
    #             widget.destroy()  # Xóa từng widget
    #         del self.search_widgets  # Xóa danh sách để tránh lỗi
        
    #     # Hiển thị lại các widget chính (giao diện chính sau khi chọn file)
    #     self.create_widgets()

    def add_search_condition(self):
        # Lấy key và cột từ người dùng
        key = self.search_entry.get()
        column = self.column_combobox.get()

        if column == "Chọn":
            messagebox.showerror("Error", f"Bạn chưa chọn cột để tìm kiếm")
            return

        if key == "":
            messagebox.showerror("Error", "Bạn phải nhập giá trị tìm kiếm!")
            return

        # Thêm điều kiện vào danh sách điều kiện
        condition = f"{column}: {key}"
        self.search_conditions.append((column, key))
        self.condition_listbox.insert(tk.END, condition)
        self.search_entry.delete(0, tk.END)  # Xóa ô nhập sau khi thêm

    def show_search_results(self, filtered_df):
        # Kiểm tra nếu DataFrame không có dữ liệu
        if filtered_df.empty:
            messagebox.showinfo("Không có kết quả", "Không tìm thấy kết quả nào.")
            return
        
        # Tạo cửa sổ mới để hiển thị kết quả tìm kiếm
        search_window = tk.Toplevel(self.root)
        search_window.title("Kết quả tìm kiếm")
        search_window.geometry("1000x400")

        # Tạo Treeview để hiển thị dữ liệu tìm kiếm dưới dạng bảng
        tree = ttk.Treeview(search_window, show="headings")
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Thiết lập các cột của Treeview
        tree["columns"] = list(filtered_df.columns)
        for col in tree["columns"]:
            tree.heading(col, text=col)
            tree.column(col, width=100, stretch=True)

        # Thanh cuộn dọc
        scrollbar_y = ttk.Scrollbar(search_window, orient=tk.VERTICAL, command=tree.yview)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        tree.configure(yscroll=scrollbar_y.set)

        # Thanh cuộn ngang
        scrollbar_x = ttk.Scrollbar(search_window, orient=tk.HORIZONTAL, command=tree.xview)
        scrollbar_x.pack(fill=tk.X)
        tree.configure(xscroll=scrollbar_x.set)

        # Hiển thị số lượng cột tìm được
        count_label = tk.Label(search_window, text=f"Số lượng cột tìm được: {len(filtered_df.columns)}")
        count_label.pack(pady=5)

        # Thêm dữ liệu vào Treeview
        for row in filtered_df.values:
            tree.insert("", tk.END, values=list(row))

    def load_data(self, page):
        if page < 0:
            page = (len(self.df) + self.page_size - 1) // self.page_size - 1
        elif page >= (len(self.df) + self.page_size - 1) // self.page_size:
            page = 0

        self.current_page = page
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Lấy dữ liệu theo trang
        start = page * self.page_size
        end = start + self.page_size
        for index, row in self.df.iloc[start:end].iterrows():
            self.tree.insert("", tk.END, values=list(row))

        # Cập nhật trạng thái trang
        self.update_page_buttons()

    def update_page_buttons(self):
        total_pages = (len(self.df) + self.page_size - 1) // self.page_size
        self.prev_button["state"] = tk.NORMAL if self.current_page > 0 else tk.DISABLED
        self.next_button["state"] = tk.NORMAL if self.current_page < total_pages - 1 else tk.DISABLED
        self.head_button["state"] = tk.NORMAL if self.current_page > 0 else tk.DISABLED
        self.tail_button["state"] = tk.NORMAL if self.current_page < total_pages - 1 else tk.DISABLED
        self.page_label["text"] = f"Trang {self.current_page + 1}/{total_pages}"

    def get_selected_index(self):
        # Implement logic to get selected index from Treeview
        # This is a placeholder implementation
        selected_item = self.tree.selection()
        lines = []
        if selected_item:
            for it in selected_item:
                tree_index = int(self.tree.index(it))
                df_index = self.current_page * self.page_size + tree_index
                lines.append(df_index)
            return lines
        else:
            return None

    def remove_empty_data_rows(self):
        if self.df is not None:
            self.df = self.df.dropna(axis=0)  # Xóa dòng có bất kỳ giá trị NaN nào
            self.load_data(self.current_page)  # Cập nhật lại dữ liệu
            messagebox.showinfo("Thông báo", "Đã xóa các dòng chứa dữ liệu trống.")
        else:
            messagebox.showerror("Lỗi", "Không có dữ liệu để xử lý.")

    def remove_empty_columns(self):
        if self.df is not None:
            self.df = self.df.dropna(axis=1, how="all")  # Xóa các cột chứa toàn bộ là NaN
            self.load_data(self.current_page)  # Tải lại dữ liệu sau khi làm sạch
            messagebox.showinfo("Thông báo", "Đã xóa các cột trống.")
        else:
            messagebox.showerror("Lỗi", "Không có dữ liệu để xử lý.")

    def show_histogram(self):
        # Placeholder implementation for showing histogram
        pass
    def show_scatter_plot(self):
        # Placeholder implementation for showing scatter plot
        pass
if __name__ == "__main__":
    root = tk.Tk()
    app = LargeDatasetViewer(root)
    root.mainloop()
