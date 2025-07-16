from django.urls import path , include
from rest_framework import routers
from .views import (
    UserProfileViewSet, LogoutView, CustomLoginView, RegisterView,BookingCreateViewSet,
    BookingListViewSet,ReviewsListApiViewSet,ReviewEditApiViewSet,PropertyListAPIViewSet,
    ReviewsCreateApiViewSet,PropertyCreateViewSet,PropertyUpdateAPIViewSet,PropertyDetailViewSet,
    BookingDetailViewSet,ReviewDetailViewSet
)


router = routers.SimpleRouter()
router.register(r'users', UserProfileViewSet, basename='users')


urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('property/', PropertyListAPIViewSet.as_view(), name='property'),
    path('property/<int:pk>/', PropertyDetailViewSet.as_view(), name='property_detail'),
    path('property/create', PropertyCreateViewSet.as_view(), name='property_create'),
    path('property/<int:pk>/edit', PropertyUpdateAPIViewSet.as_view(), name='property_edit'),
    path('booking/', BookingListViewSet.as_view(), name='booking'),
    path('booking/<int:pk>/', BookingDetailViewSet.as_view(), name='booking_detail'),
    path('booking/create', BookingCreateViewSet.as_view(), name='booking_create'),
    path('review/', ReviewsListApiViewSet.as_view(), name='review'),
    path('review/create', ReviewsCreateApiViewSet.as_view(), name='review_create'),
    path('review/<int:pk>/', ReviewDetailViewSet.as_view(), name='review_detail'),
    path('review/<int:pk>/edit', ReviewEditApiViewSet.as_view(), name='review_edit'),
]