from django.urls import path
from . import views

urlpatterns = [
    path('home', views.adminhome , name= "admin-home"),
    path('login', views.adminlogin, name= "admin-login"),

    path('create_election', views.createelection, name= "create-election"),
    path('create_party', views.createparty, name= "create-party"),
    path('create_candidate/<str:eid>', views.createcandidate, name= "create-candidate"),

    path('edit_election/<str:pk>', views.editelection, name= "edit-election"),
    path('edit_party/<str:pk>', views.editparty, name= "edit-party"),
    path('edit_candidate/<str:pk>/<str:eid>', views.editcandidate, name= "edit-candidate"),

    path('delete_election/<str:pk>', views.deleteelection, name= "delete-election"),
    path('delete_party/<str:pk>', views.deleteparty, name= "delete-party"),
    path('delete_candidate/<str:pk>/<str:eid>', views.deletecandidate, name= "delete-candidate"),

    path('start_election/<str:pk>', views.startelection, name= "start-election"),
    path('end_election/<str:pk>', views.endelection, name= "end-election"),
    path('publish_results/<str:pk>', views.publishelection, name= "publish-election"),
    path('view_election/<str:pk>', views.viewelection, name= "view-election"),
    path('archive_election/<str:pk>', views.archiveelection, name= "archive-election"),
    path('make_public/<str:pk>', views.makepublic, name= "make-public"),


    path('manage_parties', views.manageparties, name= "manage-parties"),
    path('manage_candidates', views.managecandidates, name= "manage-candidates"),

    path('approve_voter/<str:pk>', views.approvevoter, name= "approve-voter"),
    path('deny_voter/<str:pk>', views.denyvoter, name= "deny-voter"),

    
    path('vvl', views.vvl, name= "voter-verification-list"),
]