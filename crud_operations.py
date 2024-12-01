import pandas as pd
from tkinter import simpledialog, messagebox, filedialog

def add_data(viewer):
    # Implement logic to add data
    new_data = viewer.get_input_data()
    if new_data:
        viewer.df = viewer.df.append(new_data, ignore_index=True)
        viewer.load_data(viewer.current_page)

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
    # Implement logic to delete data
    index = viewer.get_selected_index()
    if index is not None:
        viewer.df = viewer.df.drop(index).reset_index(drop=True)
        viewer.load_data(viewer.current_page)

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
            print("File csv không tồn tại dữ liệu!")
            return None
        return data
    except Exception as e:
        print(f"File {filePath} gặp lỗi {e}")
        return None