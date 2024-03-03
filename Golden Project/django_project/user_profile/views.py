from django.shortcuts import render,redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import auth
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils import timezone
from django.views.generic import (
    ListView,
)

#Threading
import threading

#email
from django.core.mail import EmailMessage

#email host
from django_project.settings import EMAIL_HOST_USER

#form
from .forms import UserUpdateForm, ProfileUpdateForm

#models
from jewellery.models import Jewellery
from repairing.models import Repairing


# Threading Class
class EmailThread(threading.Thread) :
    def __init__(self,email_message):
        self.email_message = email_message
        super().__init__(args=email_message,kwargs=email_message)

    def run(self):
        self.email_message.send()


# Create your views here.
#Class Views
class OwnerPassBookListView(LoginRequiredMixin,ListView) :
    model = Jewellery
    template_name = 'user_profile/passbook_owner.html'
    context_object_name = 'passbook_detail'

    def get_context_data(self, **kwargs):
        context = super(OwnerPassBookListView,self).get_context_data(**kwargs)
        context['passbook_detail_repairing'] = Repairing.objects.all().order_by('-start_date')
        return context

    def get_queryset(self):
        return Jewellery.objects.filter(worker_name__owner=self.request.user).order_by('-start_date')


#Function Views
@login_required
def register(request) :
    return render(request, 'user_profile/register.html')

@login_required
def profile_owner(request) :
    if request.method == 'POST' :
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid() :
            u_form.save()
            p_form.save()
            messages.info(request, f'Your Account Is Has been Updated !')
            return redirect('owner_profile')

    else :
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form' : u_form,
        'p_form' : p_form
    }
    return render(request, 'user_profile/profile view owner.html', context)

@login_required
def logout(request):
    # Email Message
    email_subject = f'Your Have Been Logged Out !'
    email_messages = render_to_string('user_profile/email/logout.html',
                                                    {
                                                        'name' : request.user.first_name,
                                                        'date' : timezone.now(),
                                                    }
                                                )
    Email = EmailMessage(
                        email_subject,
                        email_messages,
                        EMAIL_HOST_USER,
                        to=[request.user.email]
    )
    Email.content_subtype = 'html'
    EmailThread(email_message=Email).start()
    auth.logout(request)
    messages.info(request, f'You Have been Logged Out !')
    return redirect('login')
