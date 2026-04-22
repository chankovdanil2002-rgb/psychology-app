"""
Корневая конфигурация URL для приложения записи к психологу.
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from apps.psychologists.urls import admin_urlpatterns as psychologist_admin_urls

urlpatterns = [
    path('admin/', admin.site.urls),

    # API endpoints
    path('api/auth/', include('apps.users.urls')),
    path('api/profile/', include('apps.clients.urls')),
    path('api/specializations/', include('apps.specializations.urls')),
    path('api/psychologists/', include('apps.psychologists.urls')),
    path('api/schedule/', include('apps.schedule.urls')),
    path('api/appointments/', include('apps.appointments.urls')),
    path('api/reviews/', include('apps.reviews.urls')),

    # Административные API endpoints
    path('api/admin/', include(psychologist_admin_urls)),
]

# Отдача медиа-файлов в режиме разработки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
