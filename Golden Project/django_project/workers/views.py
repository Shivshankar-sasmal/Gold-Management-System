from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.utils import timezone
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    RedirectView,
)

# models
from .models import Worker
from jewellery.models import Jewellery
from user_profile.models import Profile
from repairing.models import Repairing

# Query
from django.db.models import Q

# Create your views here.
class WorkerCreateView(LoginRequiredMixin, CreateView):
    model = Worker
    fields = ['username','full_name', 'phone', 'email', 'aadhar_card', 'address', 'state', 'skills', 'gold_toot', 'image']

    def form_valid(self, form):
        form.instance.owner = self.request.user
        owner = User.objects.get(pk=self.request.user.pk)
        owner.profile.no_of_employees = int(owner.profile.no_of_employees) + 1
        owner.save()
        return super().form_valid(form)

class WorkerUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Worker
    fields = ['username','full_name', 'phone', 'address', 'state', 'skills', 'gold_toot','image']

    def form_valid(self, form):
        return super().form_valid(form)

    def test_func(self):
        worker = self.get_object()
        if worker.owner == self.request.user :
            return True
        return False

class WorkerListView(LoginRequiredMixin, ListView):
    model = Worker
    template_name = 'workers/worker_list.html'
    context_object_name = 'workers'
    paginate_by = 6

    def get_queryset(self):
        search = self.request.GET.get('search')
        if search:
            search = search.strip()
            return Worker.objects.filter(
                (Q(full_name__icontains=search) |
                Q(skills__icontains=search) |
                Q(phone__icontains=search) |
                Q(email__icontains=search) |
                Q(state__state__icontains=search)) &
                Q(left_date__isnull=True)
            ).distinct().order_by('full_name')
        else:
            return Worker.objects.filter(left_date__isnull=True).order_by('full_name')


class WorkerListAllView(LoginRequiredMixin, ListView):
    model = Worker
    template_name = 'workers/worker_listall.html'
    context_object_name = 'workers'
    paginate_by = 6

    def get_queryset(self):
        search = self.request.GET.get('search')
        if search:
            search = search.strip()
            return Worker.objects.filter(
                Q(full_name__icontains=search) |
                Q(skills__icontains=search) |
                Q(phone__icontains=search) |
                Q(email__icontains=search) |
                Q(state__state__icontains=search)
            ).distinct().order_by('full_name')
        else:
            return Worker.objects.all()

class WorkerPassBookListView(LoginRequiredMixin,ListView) :
    model = Jewellery
    template_name = 'workers/passbook_worker.html'
    context_object_name = 'passbook_detail'

    def get_context_data(self, **kwargs):
        context = super(WorkerPassBookListView,self).get_context_data(**kwargs)
        worker = get_object_or_404(Worker, pk=self.kwargs.get('pk'))
        passbook_detail_repairing = Repairing.objects.filter(worker_name = worker).order_by('-start_date')
        context['worker'] = worker
        context['passbook_detail_repairing'] = passbook_detail_repairing
        return context

    def get_queryset(self):
        worker = get_object_or_404(Worker, pk=self.kwargs.get('pk'))
        return Jewellery.objects.filter(worker_name=worker).order_by('-start_date')


class WorkerLeaveRedirect(LoginRequiredMixin,RedirectView) :
    def get_redirect_url(self, *args, **kwargs):
        object = get_object_or_404(Worker,pk=self.kwargs.get('pk'))
        user_profile = Profile.objects.get(user=self.request.user)
        object.left_date = timezone.now()
        user_profile.no_of_employees = int(user_profile.no_of_employees) - 1
        object.save()
        user_profile.save()
        return object.get_passbook_url()


