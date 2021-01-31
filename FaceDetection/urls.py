from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout, name='logout' ),
    path('memolistview/', views.memolist_view, name='memolist_view'),
    path('update_memo/', views.update_memo, name='update_memo'),
    path('finishedlistview/', views.finishedlist_view, name='finishedlist_view'),
    path('add_memo/', views.add_memo, name='add_memo'),
    path('basketlist/', views.basketlist, name='basketlist'),
    path('ocr/', views.ocr, name='ocr'),
    path('delete_item/', views.delete_item, name='delete_item'),
    path('view_item/', views.view_item, name='view_item'),
    path('add_item/', views.add_item, name='add_item'),
    path('edit_item/', views.edit_item, name='edit_item'),
    path('update_item/', views.update_item, name='update_item'),
    path('finish-list-item/<id>/', views.finish_list_item, name='finish-list-item'),
    path('delete-list-item/<id>/', views.delete_list_item, name='delete-list-item'),
    path('recover-list-item/<id>/', views.recover_list_item, name='recover-list-item'),
    path('userpage/', views.userpage, name='userpage' ),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)