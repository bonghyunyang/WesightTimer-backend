from django.urls     import path

from .views          import (
    PlayLisInfoView,
    PlayListMain,
    ContentPlay
)

urlpatterns = [
    path('/playlistinfo/<int:playlist_id>',  PlayLisInfoView.as_view()),
    path('/playlistmain', PlayListMain.as_view()),
    path('/playcontent/<int:content_id>', ContentPlay.as_view()),
]
