from django.conf.urls import url

from .views import PropietarioView, LoginView, UploadImageMarcaView, UploadImageMarcaCompareView, SaveImageCompare, \
    GetImagesCompare, PropietarioViewUpdate, GetImagesIntermediate, getDepartamentos, UsuarioPropietarioView, verifyssl, ReportePersonasPDF

urlpatterns = [
    url(r'^api/login/$', LoginView.as_view()),
    url(r'^api/propietario/$', PropietarioView.as_view()),
    url(r'^api/propietario/(?P<doc>\d+)/$', PropietarioView.as_view()),
    url(r'^api/propietario/delete/(?P<pk>\d+)/$', PropietarioView.as_view()),
    url(r'^api/propietario/update/$', PropietarioViewUpdate.as_view()),
    url(r'^api/propietario/marca/$', UploadImageMarcaView.as_view()),
    url(r'^api/propietario/usuario/$', UsuarioPropietarioView.as_view()),
    url(r'^api/marca/(?P<documento>\d+)/$', UploadImageMarcaView.as_view()),
    url(r'^api/compare/$', UploadImageMarcaCompareView.as_view()),
    url(r'^api/compare/save/$', SaveImageCompare.as_view()),
    url(r'^api/compare/list/$', GetImagesCompare.as_view()),
    url(r'^api/compare/list-intermediate/(?P<id>\d+)/$', GetImagesIntermediate.as_view()),
    url(r'^departamentos/', getDepartamentos),
    # url(r'^generar-pdf/(?P<pk>\d+)/$', generaPdf),
    url(r'^generar-pdf/$', ReportePersonasPDF.as_view()),
    url(r'^.well-known/acme-challenge/mUYH46lnjWEzIIMsV5NwBURpJ_3ifY2SPHS3x0AnzC4', verifyssl)
]