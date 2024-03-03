from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils import timezone
from django.template.loader import render_to_string
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
)

#Threading
import threading

#email
from django.core.mail import EmailMessage

#email host
from django_project.settings import EMAIL_HOST_USER


# models
from .models import Jewellery
from workers.models import Worker
from user_profile.models import Profile
from repairing.models import Repairing

# Query
from django.db.models import Q


# Threading Class
class EmailThread(threading.Thread) :
    def __init__(self,email_message):
        self.email_message = email_message
        super().__init__(args=email_message,kwargs=email_message)

    def run(self):
        self.email_message.send()


# Create your views here.
# Class Based Views
class JewelleryListView(LoginRequiredMixin, ListView):
    model = Jewellery
    template_name = 'jewellery/home.html'
    context_object_name = 'jewelleries'
    paginate_by = 9

    def get_context_data(self, **kwargs):
        context = super(JewelleryListView,self).get_context_data(**kwargs)
        search = self.request.GET.get('search')
        if search :
            search = search.strip()
            context['jewelleries_repairing'] = Repairing.objects.filter(
                (Q(jewellery_name__icontains=search) |
                Q(jewellery_owner_name__icontains=search) |
                Q(worker_name__full_name__icontains=search)) &
                Q(finish_date__isnull=True)
            ).distinct().order_by('start_date')
            return context
        else:
            context['jewelleries_repairing'] = Repairing.objects.filter(finish_date__isnull=True).order_by('start_date')
            return context

    def get_queryset(self):
        search = self.request.GET.get('search')
        if search :
            search = search.strip()
            return Jewellery.objects.filter(
                (Q(jewellery_name__icontains=search) |
                Q(jewellery_owner_name__icontains=search) |
                Q(worker_name__full_name__icontains=search)) &
                Q(finish_date__isnull=True)
            ).distinct().order_by('start_date')
        else:
            return Jewellery.objects.filter(finish_date__isnull=True).order_by('start_date')


class JewelleryDetailView(LoginRequiredMixin, DetailView):
    queryset = Jewellery.objects.all()
    template_name = 'jewellery/detail view work.html'


class JewelleryCreateView(LoginRequiredMixin, CreateView):
    model = Jewellery
    fields = ['jewellery_name', 'jewellery_owner_name', 'total_gold', 'gold_purity', 'KDM', 'worker_name', 'urgent_work_date']

    def form_valid(self, form):
        worker = (Worker.objects.get(pk=form['worker_name'].value()))
        worker_gold_toot = float(worker.gold_toot) / 100
        form.instance.gold = float(form['total_gold'].value()) * float(form['gold_purity'].value()) / 100
        extra = float(form['total_gold'].value()) - form.instance.gold
        form.instance.silver = extra * 0.666667
        form.instance.bronze = extra * 0.333333
        form.instance.jewellery_net_weight = (float(form['total_gold'].value()) + float(form['KDM'].value()))
        form.instance.gold_to_be_given = (float(form['total_gold'].value()) + float(form['KDM'].value())) - float(
            (float(form['total_gold'].value()) + float(form['KDM'].value())) * worker_gold_toot)

        # Email Message
        # email_subject = f'Your Have Given A Jewellery Work !'
        # email_messages = render_to_string('worker/email/jewellery_create.html',
        #                                                 {
        #                                                     'worker' : form['worker_name'].value(),
        #                                                     'owner' : self.request.user.first_name,
        #                                                     'date' : timezone.now(),
        #                                                     'jewellery_name' : form['jewellery_name'].value(),
        #                                                     'gold_purity' : form['gold_purity'].value(),
        #                                                     'total_gold' : form['total_gold'].value(),
        #                                                     'KDM' : form['KDM'].value(),
        #                                                     'net_weight' : form.instance.jewellery_net_weight,
        #                                                 }
        #                                             )
        # Email = EmailMessage(
        #                     email_subject,
        #                     email_messages,
        #                     EMAIL_HOST_USER,
        #                     to=[worker.email]
        # )
        # Email.content_subtype = 'html'
        # EmailThread(email_message=Email).start()

        return super().form_valid(form)


class JewlleryUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Jewellery
    fields = ['jewellery_name', 'jewellery_owner_name', 'extra_KDM', 'extra_gold', 'worker_name', 'urgent_work_date']

    def form_valid(self, form):
        jewellery = self.get_object()
        form.instance.KDM = float(float(jewellery.KDM) + float(form['extra_KDM'].value()))
        worker_gold_toot = float((Worker.objects.get(pk=form['worker_name'].value())).gold_toot) / 100
        form.instance.jewellery_net_weight = float(float(jewellery.total_gold) + float(form['extra_gold'].value()) + float(form.instance.KDM))
        form.instance.gold_to_be_given = (float(jewellery.total_gold) + float(form.instance.KDM) + float(form['extra_gold'].value())) - float((float(jewellery.total_gold) + float(form.instance.KDM) + float(form['extra_gold'].value())) * worker_gold_toot)
        form.instance.extra_KDM = 0
        return super().form_valid(form)

    def test_func(self):
        jewellery = self.get_object()
        if self.request.user == jewellery.worker_name.owner:
            return True
        return False


class JewlleryConfirmSubmitView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Jewellery
    fields = ['gold_given', 'paid','comment']
    template_name = 'jewellery/confirm_submit.html'
    success_url = '/'

    def form_valid(self, form):
        worker = Worker.objects.get(pk=form.instance.worker_name.pk)
        profile = Profile.objects.get(pk=self.request.user.pk)
        form.instance.loss = float(form.instance.gold_to_be_given) - float(form['gold_given'].value())
        worker.loss = float(worker.loss) + float(form.instance.loss)
        worker.paid = float(worker.paid) + float(float(form['paid'].value()))
        profile.loss = float(profile.loss) + float(form.instance.loss)
        profile.paid = float(profile.paid) + float(float(form['paid'].value()))
        profile.total_work = float(profile.total_work) + float(form.instance.jewellery_net_weight)
        form.instance.finish_date = timezone.now()
        worker.save()
        profile.save()
        return super().form_valid(form)

    def test_func(self):
        jewellery = self.get_object()
        if self.request.user == jewellery.worker_name.owner:
            return True
        return False


class JewelleryAllListView(LoginRequiredMixin, ListView):
    model = Jewellery
    template_name = 'jewellery/all_jewellery_work.html'
    context_object_name = 'jewelleries'
    paginate_by = 9

    def get_queryset(self):
        search = self.request.GET.get('search')
        if search :
            search = search.strip()
            return Jewellery.objects.filter(
                Q(jewellery_name__icontains=search) |
                Q(jewellery_owner_name__icontains=search) |
                Q(worker_name__full_name__icontains=search)
            ).distinct().order_by('-start_date')
        else:
            return Jewellery.objects.all().order_by('-start_date')


class JewelleryUrgentListView(LoginRequiredMixin, ListView):
    model = Jewellery
    template_name = 'jewellery/urgent_work.html'
    context_object_name = 'jewelleries'
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super(JewelleryUrgentListView,self).get_context_data(**kwargs)
        search = self.request.GET.get('search')
        if search :
            search = search.strip()
            context['jewelleries_repairing'] = Repairing.objects.filter(
                (Q(jewellery_name__icontains=search) |
                Q(jewellery_owner_name__icontains=search) |
                Q(worker_name__full_name__icontains=search)) &
                (Q(finish_date__isnull=True) &
                Q(urgent_work_date__isnull=False))
            ).distinct().order_by('start_date')
            return context
        else:
            context['jewelleries_repairing'] = Repairing.objects.filter((Q(finish_date__isnull=True) & Q(urgent_work_date__isnull=False))).order_by('start_date')
            return context


    def get_queryset(self):
        search = self.request.GET.get('search')
        if search :
            search = search.strip()
            return Jewellery.objects.filter(
                (Q(jewellery_name__icontains=search) |
                Q(jewellery_owner_name__icontains=search) |
                Q(worker_name__full_name__icontains=search)) &
                (Q(finish_date__isnull=True) &
                Q(urgent_work_date__isnull=False))
            ).distinct().order_by('start_date')
        else:
            return Jewellery.objects.filter((Q(finish_date__isnull=True) & Q(urgent_work_date__isnull=False))).order_by('start_date')
