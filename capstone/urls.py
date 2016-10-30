from django.conf.urls import include, url
from django.contrib import admin

# urlpatterns = patterns('',
#     # Examples:
#     # url(r'^$', 'capstone.views.home', name='home'),
#     # url(r'^blog/', include('blog.urls')),

#     url(r'^admin/', include(admin.site.urls)),
# )

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^plots/', include('plots.urls')), 
]