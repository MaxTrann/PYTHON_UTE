import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
from dataCRUD import dataProcessing

class LargeDatasetViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("Large Dataset Viewer")
        self.root.geometry("2000x600")
        
        self.df = None
        self.page_size = 100
        self.current_page = 0
        self.data_processor = None
        
        self.create_widgets()
        
    def create_widgets(self):
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

        # Nút mở file
        open_button = tk.Button(self.root, text="Chọn file CSV", command=self.open_file)
        open_button.pack(pady=10)

        # Nút CRUD
        crud_frame = tk.Frame(self.root)
        crud_frame.pack(fill=tk.X)

        add_button = tk.Button(crud_frame, text="Thêm dữ liệu", command=self.add_data)
        add_button.pack(side=tk.LEFT, padx=5)

        update_button = tk.Button(crud_frame, text="Cập nhật dữ liệu", command=self.update_data)
        update_button.pack(side=tk.LEFT, padx=5)

        delete_button = tk.Button(crud_frame, text="Xóa dữ liệu", command=self.delete_data)
        delete_button.pack(side=tk.LEFT, padx=5)

        save_button = tk.Button(crud_frame, text="Lưu dữ liệu", command=self.save_data)
        save_button.pack(side=tk.LEFT, padx=5)
        
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

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            try:
                self.data_processor = dataProcessing(file_path)
                self.df = self.data_processor.data
                # Xóa các cột cũ trong Treeview
                self.tree["columns"] = list(self.df.columns)
                for col in self.tree["columns"]:
                    self.tree.heading(col, text=col)
                    self.tree.column(col, width=100, stretch=True)  # Tự co giãn theo nội dung
                self.load_data(0)  # Tải dữ liệu trang đầu tiên
            except Exception as e:
                messagebox.showerror("Error", f"Could not read file: {e}")

    def add_data(self):
        # Implement logic to add data
        new_data = self.get_input_data()
        if new_data:
            self.data_processor.addData(new_data)
            self.load_data(self.current_page)

    def update_data(self):
        # Implement logic to update data
        index = self.get_selected_index()
        new_data = self.get_input_data()
        if index is not None and new_data:
            self.data_processor.updateData(index, new_data)
            self.load_data(self.current_page)

    def delete_data(self):
        # Implement logic to delete data
        index = self.get_selected_index()
        if index is not None:
            self.data_processor.deleteData(index)
            self.load_data(self.current_page)

    def save_data(self):
        # Implement logic to save data
        self.data_processor.saveData()

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
