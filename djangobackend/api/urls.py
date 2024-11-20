from django.urls import path
from api import views
from django.conf import settings
from django.conf.urls.static import static
from .views import get_rooms
# from .views import AvailableRoomsView
# from .views import  CreateBooking
from .views import SignupView, LoginView,LogoutView


urlpatterns=[
    # path('student/',views.StudentList.as_view()),
    path('cruise/',views.CruiseDetailFinalList.as_view()),
      path('available-rooms/<int:cruise_id>/<str:room_type>/', views.available_rooms, name='available_rooms'),
    # path('rooms/<int:cruise_id>/', get_rooms, name='get_rooms'),
    path('rooms/<int:cruise_id>/<str:room_type>/<str:location>/', get_rooms, name='get_rooms'),
     path('book/', views.CreateBooking.as_view(), name='create_booking'),
    path('rooms/cancel-booking/', views.cancel_booking, name='cancel-booking'),
    # path('api/available-rooms/', AvailableRoomsView.as_view(), name='available-rooms'),

    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('book/confirm-booking/', views.ConfirmBooking.as_view(), name='confirm-booking'),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)