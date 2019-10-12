from django.urls import path
from django.contrib.auth.decorators import login_required

from kadent import views

app_name = 'kadent'

urlpatterns = [
    path('patient_create', views.PatientCreate.as_view(), name='patient_create'),
    path('<int:pk>/patient_edit/',
         views.PatientUpdate.as_view(), name='patient_edit'),
    path('<int:pk>/patient_delete/',
         views.PatientDelete.as_view(), name='patient_delete'),
    path('', views.PatientList.as_view(), name='patient_list'),
]
