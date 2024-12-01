import pandas as pd

def add_row(entry_id, entry_name, entry_age, df, load_data_callback):
    """
    Hàm thêm dữ liệu vào DataFrame và cập nhật Treeview.
    """
    new_id = entry_id.get()
    new_name = entry_name.get()
    new_age = entry_age.get()
    if new_id and new_name and new_age:
        df = pd.concat([df, pd.DataFrame([[new_id, new_name, new_age]], columns=df.columns)], ignore_index=True)
        load_data_callback()
    return df

def delete_row(tree, df, load_data_callback):
    """
    Hàm xóa dòng được chọn trong Treeview và cập nhật DataFrame.
    """
    selected_item = tree.selection()
    if selected_item:
        for item in selected_item:
            values = tree.item(item, "values")
            df = df[~((df["ID"] == values[0]) & (df["Name"] == values[1]) & (df["Age"] == values[2]))]
        load_data_callback()
    return df
