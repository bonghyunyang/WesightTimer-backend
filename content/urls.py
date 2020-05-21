from django.urls     import path

from .views          import (
    PlayLisInfoView,
    PlayListMain,
)

urlpatterns = [
    path('/playlistinfo/<int:playlist_id>',  PlayLisInfoView.as_view()),
    path('/playlistmain', PlayListMain.as_view()),
]
