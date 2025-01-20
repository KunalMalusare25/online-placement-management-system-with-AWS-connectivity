from django.urls import path
from .import views


urlpatterns = [
    path('',views.index,name='index'),
    path('login/',views.user_login,name='login'),
    path('reg/',views.signup,name='reg'),
    path('sdash/',views.sdash,name='sdash'),
    # path('res/',views.resume,name='resume'),
    path('pro/',views.profile,name='profile'),
    path('jobapp/',views.jobapplied,name='jobapplied'),
    path('tpost/',views.tpopost,name='tpopost'),
    path('forgot/',views.changePassword, name='changePassword'),



    path('tlogin/',views.tpologin,name='tpologin'),
    path('tafterlogin/',views.tpoafterlogin,name='tpoafterlogin'),
    path('dash/',views.dash, name='tpoDash'),
    path('regi/',views.reg, name='register'),
    path('delete/<int:pk>/', views.delete_drive, name='delete_drive'),
    path('jlist/',views.jlist, name='joblist'),
    
    path('studapp/',views.studapp, name='tpoappstud'),
    path('studpro/',views.stuprofile, name='studentprofiles'),
    



]