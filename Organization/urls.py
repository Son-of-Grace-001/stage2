from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import RegisterUserView, LoginView, UserDetailView, UserOrganisationsView, OrganisationDetailView, CreateOrganisationView, AddUserToOrganisationView

urlpatterns = [
    path('auth/register/', RegisterUserView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/users/<uuid:id>/', UserDetailView.as_view(), name='user-detail'),
    path('api/organisations/', UserOrganisationsView.as_view(), name='user-organisations'),
    path('api/organisations/<uuid:pk>/', OrganisationDetailView.as_view(), name='organisation-detail'),
    path('api/createorganisations/', CreateOrganisationView.as_view(), name='create-organisation'),
    path('api/organisations/<uuid:orgId>/users/', AddUserToOrganisationView.as_view(), name='add-user-to-organisation'),
]
