"""ksm_project_restfull URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))"""
# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.

from django.conf.urls import url, include
from django.urls import include, path
from django.contrib import admin
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from stock.views import *
from user.views import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.static import serve

<<<<<<< HEAD

api_urlpatterns = [
    path('ksm-api/product/', include('product.urls')),
    path('ksm-api/company/', include('company.urls')),
    path('ksm-api/partner/', include('partner.urls')),
    path('ksm-api/stock/', include('stock.urls')),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(api_urlpatterns)),
    path('api/auth/',include('rest_framework.urls')),
    path('api/token/', obtain_auth_token, name='obtain-token'),
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls'))
    ]

=======
>>>>>>> e50fe4af2c5e706961ba3369d6c568cc3c7ce4ea
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import permissions
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

import os

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def api_root(request, format=None):
    """
    Retrouvez la lien vers la vue par defaut des APIs
    """
    if os.environ.get('ENV') == 'PRODUCTION':
        return Response({
            'PRODUCT APIs': "https://wiconet.herokuapp.com/product-api/",
            'PARTNER APIs': "https://wiconet.herokuapp.com/partner-api/",
            'COMPANY APIs': "https://wiconet.herokuapp.com/company-api/",
            'GOCOM APIs': "https://wiconet.herokuapp.com/gocom-api/",
            'STOCK APIs': "https://wiconet.herokuapp.com/stock-api/",
        })
    elif os.environ.get('ENV_PA') == 'PRODUCTION':
        return Response({
            'PRODUCT APIs': "https://anselme.pythonanywhere.com/product-api/",
            'PARTNER APIs': "https://anselme.pythonanywhere.com/partner-api/",
            'COMPANY APIs': "https://anselme.pythonanywhere.com/company-api/",
            'GOCOM APIs': "https://anselme.pythonanywhere.com/gocom-api/",
            'STOCK APIs': "https://anselme.pythonanywhere.com/stock-api/",
        })
    else:
        return Response({
            'PRODUCT APIs': "http://localhost:8000/product-api/",
            'PARTNER APIs': "http://localhost:8000/partner-api/",
            'COMPANY APIs': "http://localhost:8000/company-api/",
            'GOCOM APIs': "http://localhost:8000/gocom-api/",
            'STOCK APIs': "http://localhost:8000/stock-api/",
        })
        

urlpatterns = [
    path('admin-ksm/', admin.site.urls),
    path('product-api/', include('product.urls')),
    path('company-api/', include('company.urls')),
    path('partner-api/', include('partner.urls')),
    path('gocom-api/', include('gocom.urls')),
    path('stock-api/', include('stock.urls')),
    path('api/auth/',include('rest_framework.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api-token-auth/', CustomAuthToken.as_view()),
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),
<<<<<<< HEAD
    path('', api_root),
=======
    path('', api_root)
>>>>>>> e50fe4af2c5e706961ba3369d6c568cc3c7ce4ea
] 

# This is only needed when using runserver.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
