from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class User(models.Model):
    id = models.UUIDField(primary_key=True)
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
        if not self.pk:  # Chỉ hash mật khẩu khi tạo mới
            self.password = make_password(self.password)
        super(User, self).save(*args, **kwargs)

    # Xác minh mật khẩu
    def verify_password(self, raw_password):
        return check_password(raw_password, self.password)
