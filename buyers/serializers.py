# from dataclasses import field
from rest_framework import serializers
# from .models import Employee, EmployeeBasicDetails, EmployeeKYCDetails, EmployeeFamilyDetails, EmployeeEducationDetails, EmployeePastWorkExperienceDetails, EmployeeBankDetails
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, StaffProfile, ClientBusiness, ClientAddress, ClientCataloge


class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'full_name', 'nick_name', 'phone', 'is_staff')


class ResetPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password')


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('old_password', 'new_password')

    def validate(self, attrs):
        user = self.context['request'].user
        if not user.check_password(attrs['old_password']):
            raise serializers.ValidationError({"error": "invalid password"})
        attrs.pop('old_password')
        return attrs

    def save(self, **kwargs):
        user = self.context['request'].user
        new_password = self.validated_data['new_password']
        user.set_password(new_password)
        user.save()
        return user


class StaffProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffProfile
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'full_name', 'nick_name', 'phone', 'email')
        read_only_fields = ('email',)


# ClientBusinessSerializer,ClientCatalogeSerializer,ClientAddressSerializer


class ClientBusinessSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientBusiness
        fields = '__all__'
        read_only_fields = ('user',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        request = self.context.get('request')
        if request and not request.user.is_superuser:
            self.fields.pop('user')
            self.fields.pop('sales_rep')


class ClientCatalogeSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = ClientCataloge
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        request = self.context.get('request')
        if request and not request.user.is_superuser:
            self.fields.pop('user')

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None


class ClientAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientAddress
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        request = self.context.get('request')
        if request and not request.user.is_superuser:
            self.fields.pop('user')
