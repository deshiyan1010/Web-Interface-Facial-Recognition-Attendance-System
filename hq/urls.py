from django.urls import path
from . import views
from django.conf.urls.static import static
from face_att import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

app_name = "hq"

urlpatterns = [
    path('new_entry/<id>-<name>/',views.capImg,name='capImg'),
    path('new_entry/',views.new_entry,name='new_entry'),
    path('profile/<id>/',views.profile,name='profile'),
    path('delete/<pid>/<imgid>/',views.deleteimg,name='deleteimg'),
    path('search/',views.search,name='search'),
    path('startstream/',views.startstream,name='startstream'),
    path('sync/',views.sync,name='sync'),
    path('streamer/',views.streamer,name='streamer'),
    path('delete-<id>/',views.delete_entry,name='delete_entry'),
    path('edit-<id>/',views.edit_entry,name='edit_entry'),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()
