import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import MaxNLocator

def bar_chart(data, labels, title='Bar Chart', xlabel='X-axis', ylabel='Y-axis'):
    plt.figure(figsize=(10, 6))
    plt.bar(labels, data, color='blue')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()

# Đường dẫn tới file CSV
file_path = "healthcare_dataset.csv"

# Đọc dữ liệu từ file CSV
data = pd.read_csv(file_path)

def plot_patient_count_by_month_and_condition(data, year=2023):
    # Chuẩn bị dữ liệu
    data['Date of Admission'] = pd.to_datetime(data['Date of Admission'], errors='coerce')  # Chuyển đổi sang kiểu ngày
    data = data[data['Date of Admission'].dt.year == 2023]  # Chỉ lấy dữ liệu của năm 2023
    medical_conditions = data['Medical Condition'].unique()  # Lấy danh sách các bệnh duy nhất

    # Gộp nhóm dữ liệu theo tháng
    data['Month'] = data['Date of Admission'].dt.to_period('M')  # Gộp nhóm theo tháng
    grouped_data = data.groupby(['Month', 'Medical Condition']).size().reset_index(name='Count')

    # Tạo lưới biểu đồ
    fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(18, 12))  # Tăng chiều rộng biểu đồ
    axes = axes.flatten()

    # Đặt tiêu đề chung cho toàn bộ figure
    fig.suptitle("Số lượng bệnh nhân theo Ngày nhập viện (theo tháng) và Tình trạng bệnh", fontsize=18)

    # Vẽ biểu đồ từng loại bệnh
    for idx, condition in enumerate(medical_conditions):
        if idx >= len(axes):  # Nếu số bệnh > số ô biểu đồ
            break

        # Lọc dữ liệu theo loại bệnh
        condition_data = grouped_data[grouped_data['Medical Condition'] == condition]

        # Vẽ dữ liệu
        ax = axes[idx]
        ax.bar(condition_data['Month'].astype(str), condition_data['Count'], color='skyblue', alpha=0.8)
        ax.set_title(f"Tình trạng bệnh: {condition}", fontsize=14)
        
        # Hiển thị nhãn tháng rõ ràng
        ax.set_xticks(range(len(condition_data['Month'])))
        ax.set_xticklabels(condition_data['Month'].astype(str), rotation=75, fontsize=10, ha='right')
        
        ax.set_xlabel("Tháng", fontsize=12)
        ax.set_ylabel("Số lượng", fontsize=12)
        ax.tick_params(axis='y', labelsize=10)
        ax.yaxis.set_major_locator(MaxNLocator(integer=True))  # Chỉ hiển thị số nguyên

    # Xóa các ô trống nếu số ô > số loại bệnh
    for i in range(len(medical_conditions), len(axes)):
        fig.delaxes(axes[i])

    # Tăng khoảng cách giữa các biểu đồ con
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.subplots_adjust(hspace=0.5, wspace=0.3)  # Tăng khoảng cách giữa các biểu đồ

    # Hiển thị biểu đồ
    plt.show()
# Gọi hàm để vẽ biểu đồ
plot_patient_count_by_month_and_condition(data, year=2023)

def plot_admission_type_pie_chart(data):
#Kiểm tra cột 'Admission Type' và tính toán tỷ lệ
    admission_counts = data['Admission Type'].value_counts()  # Đếm số lượng từng loại
    admission_percentages = admission_counts / admission_counts.sum() * 100  # Tính tỷ lệ phần trăm

    # Tạo biểu đồ tròn
    plt.figure(figsize=(8, 8))
    plt.pie(
        admission_percentages, 
        labels=admission_counts.index,  # Nhãn là các loại nhập viện
        autopct='%1.1f%%',             # Hiển thị tỷ lệ phần trăm
        startangle=140,                # Xoay biểu đồ để nhãn rõ hơn
        colors=plt.cm.Paired.colors    # Màu sắc đa dạng
    )

    # Thêm tiêu đề
    plt.title("Tỷ lệ bệnh nhân nhập viện theo từng loại (Admission Type)", fontsize=16)

    # Hiển thị biểu đồ
    plt.show()
# Gọi hàm để vẽ biểu đồ
plot_admission_type_pie_chart(data)