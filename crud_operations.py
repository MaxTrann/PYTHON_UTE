import pandas as pd
def add_data(viewer):
    # Implement logic to add data
    new_data = viewer.get_input_data()
    if new_data:
        viewer.data_processor.addData(new_data)
        viewer.load_data(viewer.current_page)

def update_data(viewer):
    # Implement logic to update data
    index = viewer.get_selected_index()
    new_data = viewer.get_input_data()
    if index is not None and new_data:
        viewer.data_processor.updateData(index, new_data)
        viewer.load_data(viewer.current_page)

def delete_data(viewer):
    # Implement logic to delete data
    index = viewer.get_selected_index()
    if index is not None:
        viewer.data_processor.deleteData(index)
        viewer.load_data(viewer.current_page)

def save_data(viewer):
    # Implement logic to save data
    viewer.data_processor.saveData()

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