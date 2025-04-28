from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'households', views.HouseholdViewSet, basename='household')
router.register(r'guest-profiles', views.GuestProfileViewSet, basename='guest-profile')
router.register(r'products', views.ProductViewSet, basename='product')
router.register(r'packages', views.PackageViewSet, basename='package')
router.register(r'group-bookings', views.GroupBookingViewSet, basename='group-booking')
router.register(r'booking-itineraries', views.BookingItineraryViewSet, basename='booking-itinerary')
router.register(r'onboard-spending', views.OnboardSpendingViewSet, basename='onboard-spending')

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

    # New endpoints
    path('', include(router.urls)),
    path('guest-spending/<int:guest_id>/', views.guest_spending_history, name='guest-spending-history'),
    path('refer-guest/', views.refer_guest, name='refer-guest'),
    path('suggest-products/', views.suggest_products, name='suggest-products'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)