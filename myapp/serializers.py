from rest_framework import serializers
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = [
            'username', 'email', 'password', 'confirm_password',
            'first_name', 'last_name', 'city', 'state', 'address', 'phone'
        ]

    def validate(self, data):
        password = data.get('password')
        confirm_password = data.get('confirm_password')

        # Ensure passwords match
        if password and confirm_password and password != confirm_password:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        
        return data

    def create(self, validated_data):
        # Remove confirm_password and hash password
        validated_data.pop('confirm_password')
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        # Handle password separately
        password = validated_data.pop('password', None)
        validated_data.pop('confirm_password', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)
        instance.save()
        return instance
    

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = [
            'id', 'username', 'first_name', 'last_name',
            'email', 'city', 'state', 'address', 'phone'
        ]
        read_only_fields = ['id', 'email']  # Make email and ID read-only
