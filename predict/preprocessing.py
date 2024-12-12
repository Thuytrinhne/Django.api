import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder


def convert_to_dataframe(data):
    """
    Chuyển dict thành DataFrame với thứ tự cột cố định
    """
    columns = [
        'Gender', 'Height', 'Weight', 'Cholesterol', 'BMI', 
        'Blood_Glucose', 'Bone_Density', 'Vision', 'Hearing',
        'Physical_Activity', 'Smoking', 'Alcohol', 'Diet',
        'Chronic_Diseases', 'Medication', 'Family_History',
        'Cognitive_Function', 'Mental_Health', 'Sleep', 'Stress',
        'Pollution', 'Sun_Exposure', 'Education', 'Income', 'Age',
        'Systolic_BP', 'Diastolic_BP'
    ]
    return pd.DataFrame([data])[columns]

def normalize_numeric_features(df: pd.DataFrame, numeric_columns: list) -> pd.DataFrame:
    """
    Chuẩn hóa các biến số bằng StandardScaler
    """
    scaler = StandardScaler()
    df[numeric_columns] = scaler.fit_transform(df[numeric_columns])
    return df

def encode_categorical_features(df, categorical_columns):
    """
    Mã hóa one-hot cho các biến phân loại trong DataFrame.
    """
    encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
    encoded_features = encoder.fit_transform(df[categorical_columns])
    feature_names = encoder.get_feature_names_out(categorical_columns)
    
    # Thêm các cột encoded vào DataFrame gốc
    for i, col_name in enumerate(feature_names):
        df[col_name] = encoded_features[:, i]
    
    # Xóa các cột categorical gốc
    df = df.drop(columns=categorical_columns)
    return df

def preprocess_data(data):
    """
    Tiền xử lý dữ liệu: chuyển đổi, chuẩn hóa và mã hóa
    """
    # 1. Chuyển thành DataFrame theo thứ tự
    df = convert_to_dataframe(data)
    
    numeric_columns = df.select_dtypes(include=['number']).columns.tolist()
    categorical_columns = df.select_dtypes(include=['category', 'object']).columns.tolist()

    if numeric_columns:
        df = normalize_numeric_features(df, numeric_columns)

    if categorical_columns:
        df = encode_categorical_features(df, categorical_columns)
    return df