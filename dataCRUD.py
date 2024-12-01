import csv
import math as m
import pandas as pd

class dataProcessing:
    def __init__(self, filePath):
        self.filePath = filePath
        self.data = self.getData()
        
    def getData(self):
        # <Tải dữ liệu từ file csv>
        try:
            data = pd.read_csv(self.filePath)
            if data.empty:
                print("File csv không tồn tại dữ liệu!")
                return None
            return data
        except Exception as e:
            print(f"File {self.filePath} gặp lỗi {e}")
            return None
    
    def outputData(self, record_per_page = 1000):
        # <In dữ liệu có hỗ trợ phân trang>
        if not self.data.empty:
            total_records = len(self.data)
            total_pages = m.ceil(total_records / record_per_page)
            curr_page = 1            
            
            while True:
                # Tính chỉ số dòng bắt đầu và kết thúc
                start_idx = (curr_page - 1) * record_per_page
                end_idx = min(start_idx + record_per_page, total_records)
                
                # Lấy dữ liệu cho trang
                data_page = self.data.iloc[start_idx:end_idx]
                
                print(f"Trang {curr_page}/{total_pages}")
                print(data_page)
                
                if curr_page == total_pages:
                    print("END!")
                    break
                
                # Yêu cầu thao tác của người dùng:
                option = int(input("Nhập '1' để sang trang, '-1' để quay lại, '0' để thoát: "))
                if option == 1 and curr_page < total_pages:
                    curr_page += 1
                elif option == -1 and curr_page > 1:
                    curr_page -= 1
                elif option == 0:
                    print("Thoát!")
                    break
                else:
                    print("Lựa chọn không hợp lệ!")
        else:
            print("Dữ liệu rỗng!")
            

    def getSampleData(self):
        # <Trả về bản ghi đầu tiên của dữ liệu để làm định dạng mẫu>
        if not self.data.empty:
            return self.data.iloc[0] # Dạng series
        else:
            print("Dữ liệu rỗng!")
            return None
        
    def addData(self, newData):
        # <Thêm bản ghi cho file dữ liệu>

        if isinstance(newData, list) and len(newData) == len(self.data.columns):
            new_record = pd.DataFrame([newData], columns=self.data.columns)
            self.data = pd.concat([self.data, new_record], ignore_index=True)
            print("Dữ liệu đã được thêm!")
        else:
            print("Dữ liệu chưa chính xác hoặc có lỗi")
            
    def updateData(self, index, newData):
        # <Cập nhật dữ liệu mới cho record thông qua chỉ số dòng>
        if index >= 0 and index < len(self.data):
            if isinstance(newData, list) and len(newData) == len(self.data.columns):
                self.data.iloc[index] = newData
                print("Cập nhật dữ liệu thành công!")
            else:
                print("Dữ liệu chưa chính xác hoặc có lỗi")
        else:
            print("Chỉ số dòng không hợp lệ!")

    def deleteData(self, index):
        # < Xoá bản ghi thông qua chỉ số dòng>
        if index >= 0 and index < len(self.data):
            self.data = self.data.drop(index).reset_index(drop=True)
            print("Xóa dữ liệu thành công!")
        else:
            print("Chỉ số dòng không hợp lệ!")
            
    
    def saveData(self):
        # <Lưu dữ liệu hiện tại vào lại file csv>
        try:
            self.data.to_csv(self.filePath)
            print("Dữ liệu đã được lưu thành công!")
        except Exception as e:
            print(f"File {self.filePath} gặp lỗi {e}")
                
    