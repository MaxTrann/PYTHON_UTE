import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib.ticker import MaxNLocator

def bar_chart(data, labels, title='Bar Chart', xlabel='X-axis', ylabel='Y-axis'):
    plt.figure(figsize=(10, 6))
    plt.bar(labels, data, color='blue')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()

def plot_patient_count_by_month_and_condition(data, year=2023):
    # Chuẩn bị dữ liệu
    data = data.copy()  # Make a copy of the DataFrame
    data['Date of Admission'] = pd.to_datetime(data['Date of Admission'], errors='coerce')  # Chuyển đổi sang kiểu ngày
    data = data[data['Date of Admission'].dt.year == 2023]  # Chỉ lấy dữ liệu của năm 2023
    data['Month'] = data['Date of Admission'].dt.to_period('M')  # Gộp nhóm theo tháng
    medical_conditions = data['Medical Condition'].unique()  # Lấy danh sách các bệnh duy nhất

    # Gộp nhóm dữ liệu theo tháng
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

def plot_admission_type_pie_chart(data):
    # Kiểm tra cột 'Admission Type' và tính toán tỷ lệ
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

def plot_blood_type_pie_chart(data):
    if 'Blood Type' not in data.columns:
        raise KeyError("Dữ liệu không chứa thông tin 'Blood Type'")
    
    # Đếm số lượng từng nhóm máu
    blood_type_counts = data['Blood Type'].value_counts()
    labels = blood_type_counts.index
    sizes = blood_type_counts.values

    # Vẽ biểu đồ tròn
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis('equal')  # Đảm bảo biểu đồ tròn không bị méo
    ax.pie(
        sizes, 
        labels=labels, 
        autopct='%1.2f%%', 
        startangle=90, 
        colors=plt.cm.Set3.colors
    )
    ax.set_title("Tỷ lệ nhóm máu của bệnh nhân", fontsize=16)
    plt.show()


def plot_stacked_bar_age_insurance(data):
    # Chuẩn hóa tên cột
    data.columns = [col.strip().title() for col in data.columns]

    # Kiểm tra lại cột 'Age' và 'Insurance Provider'
    if 'Age' not in data.columns or 'Insurance Provider' not in data.columns:
        raise KeyError("Dữ liệu không chứa thông tin 'Age' hoặc 'Insurance Provider'")
    
    # Chuyển cột Age sang dạng số
    data['Age'] = pd.to_numeric(data['Age'], errors='coerce')

    if data['Age'].isna().all():
        raise ValueError("Không có giá trị hợp lệ trong cột 'Age'")

    # Phân loại nhóm tuổi
    bins = [0, 18, 35, 50, 65, 120]
    labels = ['0-18', '19-35', '36-50', '51-65', '65+']
    data['Age Group'] = pd.cut(data['Age'], bins=bins, labels=labels, right=False)

    # Gộp nhóm dữ liệu theo Insurance Provider và Age Group
    grouped_data = data.groupby(['Insurance Provider', 'Age Group'], observed=False).size().unstack(fill_value=0)

    # Vẽ biểu đồ cột chồng
    grouped_data.plot(kind='bar', stacked=True, figsize=(12, 8), colormap='viridis')
    plt.title("Phân phối nhóm tuổi theo Insurance Provider", fontsize=16)
    plt.xlabel("Insurance Provider", fontsize=12)
    plt.ylabel("Số lượng bệnh nhân", fontsize=12)
    plt.legend(title="Age Group", fontsize=10, bbox_to_anchor=(1.05, 1))
    plt.xticks(rotation=45, fontsize=10)
    plt.tight_layout()
    plt.show()
