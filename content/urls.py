from django.urls     import path

from .views          import PlayLisInfoView, PlayListMain, ContentPlay, StressReviewView, StressPlaylistView, MainView

urlpatterns = [
    path('/playlistinfo/<int:playlist_id>',  PlayLisInfoView.as_view()),
    path('/playlistmain', PlayListMain.as_view()),
    path('/playcontent/<int:content_id>', ContentPlay.as_view()),
    path('/detail', StressPlaylistView.as_view()),
    path('/stressreview', StressReviewView.as_view()),
    path('/main', MainView.as_view())
]
