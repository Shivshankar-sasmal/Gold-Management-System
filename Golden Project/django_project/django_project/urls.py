"""django_project URL Configuration

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
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views

# Urls
from jewellery.views import (
    JewelleryListView,
    JewelleryDetailView,
    JewelleryCreateView,
    JewlleryUpdateView,
    JewlleryConfirmSubmitView,
    JewelleryAllListView,
    JewelleryUrgentListView,
)
from repairing.views import (
    RepairingListView,
    RepairingDetailView,
    RepairingCreateView,
    RepairingUpdateView,
    RepairingConfirmSubmitView,
    RepairingAllListView,
)
from workers.views import (
    WorkerCreateView,
    WorkerUpdateView,
    WorkerListView,
    WorkerListAllView,
    WorkerPassBookListView,
    WorkerLeaveRedirect,
)
from user_profile.views import (
    register,
    profile_owner,
    logout,
    OwnerPassBookListView,
)


urlpatterns = [
    #Admin
    path('admin/', admin.site.urls),

    #home
    path('', JewelleryListView.as_view(), name='jewellery-home'),

    #jewellery detail
    path('jewellery/<int:pk>', JewelleryDetailView.as_view(), name='jewellery-detail'),

    #jewellery create
    path('jewellery/new', JewelleryCreateView.as_view(), name='jewellery-create'),

    #jewellery update
    path('jewellery/<int:pk>/update', JewlleryUpdateView.as_view(), name='jewellery-update'),

    #jewellery submit
    path('jewellery_submit/<int:pk>/', JewlleryConfirmSubmitView.as_view(), name='jewellery-submit'),

    #jewellery all work
    path('jewelleries_all/', JewelleryAllListView.as_view(), name='jewellery-all'),

    #jewellery order
    path('jewellery_order/', JewelleryUrgentListView.as_view(), name='jewellery-order'),

    #repairing
    path('repairing/', RepairingListView.as_view(), name='repairing'),

    #repairing detail
    path('repairing/<int:pk>', RepairingDetailView.as_view(), name='repairing-detail'),

    #repairing create
    path('repairing/new', RepairingCreateView.as_view(), name='repairing-create'),

    #repairing update
    path('repairing/<int:pk>/update', RepairingUpdateView.as_view(), name='repairing-update'),

    #repairing submit
    path('repairing_submit/<int:pk>/', RepairingConfirmSubmitView.as_view(), name='repairing-submit'),

    #repairing all work
    path('repairing_all/', RepairingAllListView.as_view(), name='repairing-all'),

    #nothing
    path('register/', register, name='register'),

    #worker register
    path('worker/new', WorkerCreateView.as_view(), name='worker-create'),

    # worker update
    path('worker/<int:pk>/update', WorkerUpdateView.as_view(), name='worker-update'),

    #worker list
    path('worker_list', WorkerListView.as_view(), name='worker-list'),

    #worker list_all
    path('worker_list_all', WorkerListAllView.as_view(), name='worker-list-all'),

    #worker leave
    path('worker_leave/<int:pk>/', WorkerLeaveRedirect.as_view(), name='worker-leave'),

    #Passbook Owner
    path('owner_passbook/', OwnerPassBookListView.as_view(), name='owner-passbook'),

    # Passbook Worker
    path('passbook/<int:pk>/', WorkerPassBookListView.as_view(), name='worker-passbook'),

    #profile owner
    path('owner_profile/', profile_owner, name='owner_profile'),

    #login and logout
    path('login/', auth_views.LoginView.as_view(template_name='user_profile/login.html'), name='login'),
    path('logout/', logout, name='logout'),

    # Password Reset Tokens
    path('password-reset-done/', auth_views.PasswordResetDoneView.as_view(template_name='user_profile/password_reset.html'), name='password_reset_done'),

    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='user_profile/password_reset.html'), name='password_reset'),

    path('password-reset-confirm/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name='user_profile/password_reset_confirm.html'), name='password_reset_confirm'),

    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='user_profile/password_reset_complete.html'), name='password_reset_complete'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
