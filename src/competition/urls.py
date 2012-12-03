# TODO import views and add to urls

urlpatterns = pattern(
    ""
    url(r'^competition/$', 
        name='competition_list'),
    url(r'^competition/(?P<slug>[\w-]+)/$', 
        name='competition_detail'),
    )

urlpatterns += pattern(
    url(r'^competition/(?P<comp_slug>[\w-]+)/team/$', 
        name='team_list'),
    url(r'^competition/(?P<comp_slug>[\w-]+)/team/(?P<slug>[\w-]+)/$', 
        name='team_detail'),
    url(r'^competition/(?P<comp_slug>[\w-]+)/team-create/$', 
        name='team_create')
)
