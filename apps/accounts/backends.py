from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

UserModel = get_user_model()

class EmailAuthBackend(ModelBackend):
    """
    Xác thực người dùng dựa trên cột 'email' thay vì 'username'.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        # Biến 'username' mà form gửi lên thực chất là giá trị Email người dùng gõ
        try:
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            return None
            
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
