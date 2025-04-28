from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # Authentication endpoints
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),

    # Cruise endpoints
    path('cruises/', views.CruiseDetailFinalList.as_view(), name='cruise-list'),
    path('rooms/<int:cruise_id>/<str:room_type>/<str:location>/', 
         views.get_rooms, name='get_rooms'),

    # Booking endpoints
    path('bookings/create/', views.CreateBooking.as_view(), name='create_booking'),
    path('bookings/cancel/', views.cancel_booking, name='cancel-booking'),
    path('bookings/confirm/', views.ConfirmBooking.as_view(), name='confirm-booking'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)