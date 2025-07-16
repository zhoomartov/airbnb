from django.template.defaulttags import comment

from .models import *
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
import joblib
from django.conf import settings
import os

model_path = os.path.join(settings.BASE_DIR, 'model.pkl')
model = joblib.load(model_path)

vec_path = os.path.join(settings.BASE_DIR, 'vec.pkl')
vec = joblib.load(vec_path)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('username', 'password', 'first_name', 'last_name', 'email',
                'phone_number', 'role', 'date_registered')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = UserProfile.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Неверные учетные данные")

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class UserProfileSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('id', 'username', 'email', 'role', 'avatar')

class UserProfileForPropertySerializers(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('id', 'username', 'avatar')

class PropertyImageSerializers(serializers.ModelSerializer):
    class Meta:
        model = PropertyImage
        fields = ['image']


class PropertyCreateSerializers(serializers.ModelSerializer):
    image = PropertyImageSerializers(read_only=True,many=True)

    class Meta:
        model = Property
        fields = ['image','description','title', 'price_per_night',
                  'city', 'address','property_type','rules',
                  'owner','max_guests','bedrooms','bathrooms','is_active']

class PropertyListSerializers(serializers.ModelSerializer):
    image = PropertyImageSerializers(read_only=True,many=True)
    count_reviews = serializers.SerializerMethodField()
    avg_rating = serializers.SerializerMethodField()

    class Meta:
        model = Property
        fields = ['id','image', 'city' , 'avg_rating', 'count_reviews']

    def get_avg_rating(self, obj):
        return obj.get_avg_rating()

    def get_count_reviews(self, obj):
        return obj.get_count_reviews()


class ReviewForPropertySerializers(serializers.ModelSerializer):
    guest = UserProfileForPropertySerializers()

    class Meta:
        model = Review
        fields = ['guest','rating', 'comment', 'created_at']

class PropertyDetailSerializers(serializers.ModelSerializer):
    image = PropertyImageSerializers(read_only=True,many=True)
    owner = UserProfileForPropertySerializers()
    avg_rating = serializers.SerializerMethodField()
    reviews_property = ReviewForPropertySerializers(many=True, read_only=True)

    class Meta:
        model = Property
        fields = ['id', 'title', 'description', 'price_per_night',
                  'city', 'address', 'property_type','rules', 'max_guests',
                  'owner','bedrooms','bathrooms','image','is_active', 'avg_rating', 'reviews_property']

    def get_avg_rating(self, obj):
        return obj.get_avg_rating()

class BookingSerializers(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'

class BookingListSerializers(serializers.ModelSerializer):
    check_in = serializers.DateField(format='%d-%m-%y')
    check_out = serializers.DateField(format='%d-%m-%y')
    created_at = serializers.DateTimeField(format='%d-%m-%y , %H:%M', read_only=True)

    class Meta :
        model = Booking
        fields = ['property','guest','check_in',
                  'check_out','created_at']



class BookingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['property', 'check_in', 'check_out']

class ReviewSerializers(serializers.ModelSerializer):
    check_comments = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = ['property','rating','comment', 'check_comments']

    def get_check_comments(self, obj):
        return model.predict(vec.transform([obj.comment]))

class ReviewAllSerializers(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

