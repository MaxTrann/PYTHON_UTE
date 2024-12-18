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

def plot_blood_type(data):
    if 'Blood Type' not in data.columns:
        raise KeyError("Dữ liệu không chứa thông tin 'Blood Type'")
    
    # Đếm số lượng từng nhóm máu
    blood_type_counts = data['Blood Type'].value_counts()
    labels = blood_type_counts.index
    sizes = blood_type_counts.values

    # Vẽ biểu đồ tròn
    plt.figure(figsize=(8, 8))
    plt.pie(sizes, labels=labels, autopct='%1.2f%%')
    plt.title(label="Blood rate by type")
    plt.show()

def plot_stacked_bar_age_insurance(data):
    # Phân loại nhóm tuổi
    bins = [0, 18, 44, 65, 120]
    labels = ['0-18', '19-44', '45-65', '65+']
    data['Age Group'] = pd.cut(data['Age'], bins=bins, labels=labels)

    # Gộp nhóm dữ liệu theo Insurance Provider và Age Group
    grouped_data = data.groupby(['Insurance Provider', 'Age Group']).size().unstack(fill_value=0)

    # Vẽ biểu đồ cột chồng
    grouped_data.plot(kind='bar', stacked=True, figsize=(12, 8), colormap='viridis')
    plt.title("Age group distribution by Insurance Provider", fontsize=16)
    plt.xlabel("Insurance Provider", fontsize=10)
    plt.ylabel("Patient Count", fontsize=10)
    plt.legend(title="Age Group", fontsize=8)
    plt.xticks(rotation=45, fontsize=10)
    plt.tight_layout()
    plt.show()
    
def plot_gender_distribution(data):
    count_data = data.groupby(['Medical Condition', 'Gender']).size().reset_index(name='Số lượng')
    # Vẽ biểu đồ cột
    plt.figure(figsize=(10, 6))
    sns.barplot(x='Medical Condition', y='Số lượng', hue='Gender', data=count_data)
    # Thêm tiêu đề và nhãn
    plt.title('SỐ LƯỢNG BỆNH NHÂN THEO GIỚI TÍNH VÀ LOẠI BỆNH')
    plt.xlabel('Loại bệnh')
    plt.ylabel('Số lượng bệnh nhân')
    # Hiển thị biểu đồ
    plt.show()
def plot_age_medical_condition_distribution(data):
    # Nhóm dữ liệu theo Age và Medical Condition, sau đó đếm số lượng bệnh nhân
    age_medical_counts = data.groupby(['Medical Condition', 'Age']).size().reset_index(name='patient_count')

    # Lấy danh sách các loại bệnh
    medical_conditions = age_medical_counts['Medical Condition'].unique()

    # Tạo lưới 2x3 để hiển thị 6 biểu đồ
    fig, axes = plt.subplots(2, 3, figsize=(18, 10))
    axes = axes.flatten()

    # Lặp qua từng loại bệnh để vẽ biểu đồ riêng
    for i, condition in enumerate(medical_conditions):
        # Lọc dữ liệu cho loại bệnh hiện tại
        subset = age_medical_counts[age_medical_counts['Medical Condition'] == condition]
        
        # Vẽ biểu đồ đường cho loại bệnh
        sns.lineplot(
            data=subset, x='Age', y='patient_count', ax=axes[i], marker='o'
        )
        axes[i].set_title(f'Loại bệnh: {condition}')
        axes[i].set_xlabel('Tuổi')
        axes[i].set_ylabel('Số lượng bệnh nhân')

    # Ẩn các ô không sử dụng (nếu có thừa ô)
    for j in range(i + 1, len(axes)):
        axes[j].axis('off')

    # Tiêu đề chung cho bảng biểu đồ
    plt.suptitle('SỐ LƯỢNG BỆNH NHÂN THEO ĐỘ TUỔI VÀ LOẠI BỆNH', fontsize=16)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.show()