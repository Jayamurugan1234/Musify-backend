from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # 🔥 FIX HERE
        if user.is_superuser:
            token["role"] = "admin"
        else:
            token["role"] = user.role

        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        # 🔥 FIX HERE TOO
        if self.user.is_superuser:
            role = "admin"
        else:
            role = self.user.role

        data["role"] = role
        data["username"] = self.user.username
        data["email"] = self.user.email

        return data