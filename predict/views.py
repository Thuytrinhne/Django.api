from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, viewsets
from django.shortcuts import render
import joblib
import numpy as np
import os
import pandas as pd
from .preprocessing import preprocess_data
import pickle
# Đường dẫn đến thư mục chứa model
MODEL_PATH = "./models/model.sav"

# Tải model khi khởi động server
try:
    print("ĐANG LOAD MODEL", MODEL_PATH)
    model = joblib.load(MODEL_PATH)
except Exception as e:
    print(f"Không thể load model: {str(e)}")
    model = None

class PredictViewSet(viewsets.ViewSet):
    def create(self, request):
        """Xử lý POST request để thực hiện dự đoán"""
        try:
            data = request.data
            
            if not data:
                return Response(
                    {'error': 'Không có dữ liệu đầu vào'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if model is None:
                return Response(
                    {'error': 'Model chưa được load'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            try:
                # Tiền xử lý dữ liệu
                df_processed = preprocess_data(data)
                input_data = df_processed.values

            except Exception as e:
                return Response(
                    {'error': f'Lỗi khi xử lý dữ liệu: {str(e)}'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Thực hiện dự đoán
            prediction = model.predict(input_data)
            

        

            return Response({
                'prediction': prediction[0].tolist(),
                'message': 'Dự đoán thành công'
            })

        except Exception as e:
            return Response(
                {'error': f'Lỗi khi dự đoán: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
