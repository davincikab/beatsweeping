from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('user.urls'))
]

admin.site.site_header = "BeatSweeping"
admin.site.site_title = "BeatSweeping Administration"
admin.site.index_title = "BeatSweeping Administration"