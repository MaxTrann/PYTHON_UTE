import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd

from crud_operations import add_data, update_data, delete_data, save_data, getData

class LargeDatasetViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("Large Dataset Viewer")
        self.root.geometry("2000x600")
        
        self.df = None
        self.page_size = 100
        self.current_page = 0
        self.data_processor = None
        
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
                        self.tree.heading(col, text=col)
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
        self.page_label["text"] = f"Trang {self.current_page + 1}/{total_pages}"

    def get_input_data(self):
        # Implement logic to get input data from user
        # This is a placeholder implementation
        return []

    def get_selected_index(self):
        # Implement logic to get selected index from Treeview
        # This is a placeholder implementation
        selected_item = self.tree.selection()
        if selected_item:
            return int(self.tree.index(selected_item))
        return None

if __name__ == "__main__":
    root = tk.Tk()
    app = LargeDatasetViewer(root)
    root.mainloop()
