""":
        FunFacts _urls.py
"""


from django.conf.urls import url,include
from . import views

urlpatterns = [
    #url(r'^admin/', admin.site.urls),
    url(r'^$', views.index),
    url(r'^funfacts_process$', views.funfacts_process),
    url(r'^funfacts$', views.funfacts),
]
