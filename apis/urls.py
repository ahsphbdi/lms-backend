from django.urls import path, include
from apis.views import CheckConnection

urlpatterns = [
    path('is_up/', CheckConnection.as_view()),
    path('accounts/', include('accounts.apis.urls')),
    path('students/', include('students.apis.urls'))
]
