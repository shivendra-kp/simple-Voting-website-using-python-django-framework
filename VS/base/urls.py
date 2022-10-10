from django.urls import path
from . import views

urlpatterns = [
    path('', views.home , name= "home"),
    path('voter_login/', views.voterlogin , name= "voter-login"),
    path('voter_logout/', views.voterlogout , name= "logout"),
    path('voter_signup/', views.votersignup , name= "voter-signup"),
    path('voter_home/',views.voterhome,name="voter-home"),
    path('voter_edit/',views.voteredit,name="voter-edit"),
    path('voter_news/',views.voternews,name="voter-news"),
    path('verificationform/',views.verificationform,name="verification-form"),
    path('castvote/<str:eid>',views.castvote,name="cast-vote"),
    path('oncastvote/<str:eid>/<str:cid>',views.oncastvote,name="on-cast-vote"),
    path('viewresults/<str:eid>',views.viewresults,name="view-results"),
    path('temp',views.temp,name="temp"),

]