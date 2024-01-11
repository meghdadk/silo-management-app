from django.urls import path
from django.conf import settings

from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.index, name='index'),
    path('report_page/', views.report_page, name='report_page'),
    path('report_search/', views.report_search, name='report_search'),
    path('group_report_search/', views.group_report_search, name='group_report_search'),
    path('upload_idphoto/', views.upload_idphoto_page, name='upload_idphoto'),
    path('register_factories/', views.register_factories_page, name='register_factories'),
    path('register_factory/', views.register_factory, name='register_factory'),
    path('edit_factory/', views.edit_factory, name='edit_factory'),
    path('searchfactoryid/<int:id>', views.searchfactoryid, name='searchfactoryid'),
    path('get_idphoto/', views.get_idphoto, name='get_idphoto'),
    path('search_idphoto/<str:nationalid>/', views.search_idphoto, name='search_idphoto'),
    path('print/<str:carid>/<str:nationalid>/<str:reciept>', views.print_page, name='print'),
	path('editloads/<str:carid>/<str:nationalid>/<str:reciept>', views.edit_page, name='editloads'),
	path('fastresults/', views.fastresults_page, name='fastresults'),
	path('getfastresults/<str:id>/<str:carid>/<str:name>', views.getfastresults, name='getfastresults'),
    path('stuff/', views.stuff, name='stuff'),
    path('lastedited/', views.lastedited, name='lastedited'),
    path('dailystatistics/', views.dailystatistics, name='dailystatistics'),
    path('initialization/', views.initialization, name='initialization'),
    path('read_temp_loadings/', views.read_temp_loadings, name='read_temp_loadings'),
    path('delete_from_temps/', views.delete_from_temps, name='delete_from_temps'),
    path('delete_full_invoice/', views.delete_full_invoice, name='delete_full_invoice'),
	path('register_temp_edits/', views.register_temp_edits, name='register_temp_edits'),
	path('register_full_edits/', views.register_full_edits, name='register_full_edits'),
	path('oregister/', views.oregister, name='oregister'),
    path('temp_as_full/', views.temp_as_full, name='temp_as_full'),
    path('temp_as_empty/', views.temp_as_empty, name='temp_as_empty'),
    path('autocarnumber/', views.autocarnumber, name='autocarnumber'),
	path('oautocarnumber/', views.oautocarnumber, name='oautocarnumber'),
    path('searchid/<int:id>', views.searchid, name='searchid'),
    path('osearchid/<int:id>', views.osearchid, name='osearchid'),
    path('getweightfromclient/<str:token>/<int:weight>', views.getweightfromclient, name='getweightfromclient'),
    path('print_temp_invoice/<str:carid>', views.print_temp_invoice, name='print_temp_invoice'),
	path('print_other_invoice/<str:carid>', views.print_other_invoice, name='print_other_invoice'),
    path('print_full_invoice/<str:reciept>', views.print_full_invoice, name='print_full_invoice'),
	path('edit_temp_invoice/<str:carid>', views.edit_temp_invoice, name='edit_temp_invoice'),
    path('edit_full_invoice/<str:reciept>', views.edit_full_invoice, name='edit_full_invoice'),
    path('register/', views.register, name='register'),
    path('read_recent_invoices/', views.read_recent_invoices, name='read_recent_invoices'),
	path('initlocations/', views.initlocations, name='initlocations'),
	path('initnames/', views.initnames, name='initnames')
	
    
]

