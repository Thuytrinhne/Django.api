from django.db import models
from django.contrib.auth.hashers import make_password, check_password
import uuid  # Thêm import uuid

class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # Thêm default và editable=False
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)  # Email nên là duy nhất
    password = models.TextField()
    role = models.CharField(max_length=255, default='user')  # Mặc định là "user"
    created_at = models.DateTimeField(auto_now_add=True)
    last_login_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'User'

    # Hash mật khẩu trước khi lưu
    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)

    # Xác minh mật khẩu
    def verify_password(self, raw_password):
        print("Login - Raw password:", raw_password)
        print("Login - Stored hash:", self.password)
        result = check_password(raw_password, self.password)
        print("Login - Password match:", result)
        return result
