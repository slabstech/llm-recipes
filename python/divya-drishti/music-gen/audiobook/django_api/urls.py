from django.urls import path
from your_app.views import ImportDataView

urlpatterns = [
    path('import-data/', ImportDataView.as_view(), name='import-data'),
]