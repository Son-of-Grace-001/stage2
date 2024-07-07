from rest_framework import serializers
from .models import User, Organisation

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('userId', 'firstName', 'lastName', 'email', 'password', 'phone')

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            firstName=validated_data['firstName'],
            lastName=validated_data['lastName'],
            phone=validated_data.get('phone', '')
        )
        user.set_password(validated_data['password'])
        user.save()

        organisation = Organisation.objects.create(
            name=f"{user.firstName}'s Organisation",
            description=f"{user.firstName}'s default organisation"
        )
        organisation.users.add(user)
        organisation.save()

        return user

class OrganisationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organisation
        fields = ('orgId', 'name', 'description')

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('password', 'email')