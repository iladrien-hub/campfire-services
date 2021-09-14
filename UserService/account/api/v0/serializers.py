from rest_framework import serializers

from account.models import Account


class UserRegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = Account
        fields = ['email', 'username', 'password', 'confirm_password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_confirm_password(self, dob):
        if dob != self.initial_data['password']:
            raise serializers.ValidationError("Password must match")
        return dob

    def save(self):
        account = Account(
            email=self.validated_data['email'],
            username=self.validated_data['username'],
        )
        pwd1 = self.validated_data['password']

        account.set_password(pwd1)
        account.save()
        return account


class PersonalInfoSerializer(serializers.Serializer):

    name = serializers.CharField()
    surname = serializers.CharField(allow_blank=True)
    phone = serializers.CharField(allow_blank=True)


class ChangePasswordSerializer(serializers.Serializer):

    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate_confirm_password(self, dob):
        if dob != self.initial_data['password']:
            raise serializers.ValidationError("Password must match")
        return dob


class ChangeUsernameSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = ['username']


