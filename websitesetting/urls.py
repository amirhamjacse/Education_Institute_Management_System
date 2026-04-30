
from django.urls import path
from websitesetting.views.web_site_customize import WebHeadinView

app_name = 'websitesetting'

urlpatterns = [
    path(
        '',
        WebHeadinView.as_view(),
        name='web_heading_default'
    ),

    # web heading add
    path(
        'web/heading/',
        WebHeadinView.as_view(),
        name='web_heading_add'
    ),
]
