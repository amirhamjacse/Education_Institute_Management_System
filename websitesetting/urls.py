
from django.urls import path
from websitesetting import views

app_name = 'websitesetting'

urlpatterns = [

    # web heading add
    path(
        'web/heading',
        views.WebHeadinView.as_view(),
        name='web_heading_add'
    ),
]
