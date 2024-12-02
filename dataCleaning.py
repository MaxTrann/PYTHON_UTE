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

def deleteMissingDataRow(data):
    return data.dropna()

def deleteOutliers(data, col, default_values):
    if col not in data.columns:
        raise KeyError(f"Cột '{col}' không tồn tại trong dữ liệu!")
    
    filtered_data = data[data[col].isin(default_values)]
    return filtered_data