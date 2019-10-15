from django.urls import path
from django.contrib.auth.decorators import login_required

from kadent import views

app_name = 'kadent'

urlpatterns = [
    # Patient
    path('patient_create', views.PatientCreate.as_view(), name='patient_create'),
    path('<int:pk>/patient_edit/',
         views.PatientUpdate.as_view(), name='patient_edit'),
    path('<int:pk>/patient_delete/',
         views.PatientDelete.as_view(), name='patient_delete'),
    path('', views.PatientList.as_view(), name='patient_list'),

    # Visit
    path('<int:pk>/visit_create/', views.VisitCreate.as_view(), name='visit_create'),
    path('<int:pk>/visit_edit/',
         views.VisitUpdate.as_view(), name='visit_edit'),
    path('<int:pk>/visit_delete/',
         views.VisitDelete.as_view(), name='visit_delete'),

     # Image
    path('<int:pk>/image_create/', views.ImageCreate.as_view(), name='image_create'),
    path('<int:pk>/image_edit/',
         views.ImageUpdate.as_view(), name='image_edit'),
]
