from django.urls import path
from .views import MarkdownDocumentViewSet, RegisterAPIView
from rest_framework_simplejwt.views import TokenObtainPairView

doc_view = MarkdownDocumentViewSet.as_view

urlpatterns = [
    # path('', include(router.urls)),
    path('auth/register/', RegisterAPIView.as_view(), name='register'),
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('documents/', doc_view({'get': 'list', 'post': 'create'}), name='document-list-create'),
    path('documents/<int:pk>/', doc_view({'get': 'retrieve', 'patch': 'partial_update', 'delete': 'destroy'}), name='document-detail'),

]
