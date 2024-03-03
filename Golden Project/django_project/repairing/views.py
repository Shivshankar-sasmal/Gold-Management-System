from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
)
from django.utils import timezone

# models
from .models import Repairing
from workers.models import Worker
from user_profile.models import Profile

# Query
from django.db.models import Q

# Create Views Here
class RepairingListView(LoginRequiredMixin, ListView):
    model = Repairing
    template_name = 'repairing/repairing.html'
    context_object_name = 'jewelleries_repairing'
    paginate_by = 9

    def get_queryset(self):
        search = self.request.GET.get('search')
        if search :
            search = search.strip()
            return Repairing.objects.filter(
                (Q(jewellery_name__icontains=search) |
                Q(jewellery_owner_name__icontains=search) |
                Q(worker_name__full_name__icontains=search)) &
                Q(finish_date__isnull=True)
            ).distinct().order_by('start_date')
        else:
            return Repairing.objects.filter(finish_date__isnull=True).order_by('start_date')


class RepairingDetailView(LoginRequiredMixin, DetailView):
    queryset = Repairing.objects.all()
    template_name = 'repairing/detail_repairing_work.html'


class RepairingCreateView(LoginRequiredMixin, CreateView):
    model = Repairing
    fields = ['jewellery_name', 'jewellery_owner_name', 'total_gold', 'KDM', 'worker_name', 'urgent_work_date']

    def form_valid(self, form):
        worker = (Worker.objects.get(pk=form['worker_name'].value()))
        worker_gold_toot = float(worker.gold_toot) / 100
        form.instance.jewellery_net_weight = (float(form['total_gold'].value()) + float(form['KDM'].value()))
        form.instance.gold_to_be_given = form.instance.jewellery_net_weight
        return super().form_valid(form)


class RepairingUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Repairing
    fields = ['jewellery_name', 'jewellery_owner_name', 'extra_KDM', 'extra_gold', 'worker_name', 'urgent_work_date']

    def form_valid(self, form):
        jewellery = self.get_object()
        form.instance.KDM = float(float(jewellery.KDM) + float(form['extra_KDM'].value()))
        form.instance.jewellery_net_weight = float(float(jewellery.total_gold) + float(form['extra_gold'].value()) + float(form.instance.KDM))
        form.instance.gold_to_be_given = float(form.instance.jewellery_net_weight)
        form.instance.extra_KDM = 0
        return super().form_valid(form)

    def test_func(self):
        jewellery_repairing = self.get_object()
        if self.request.user == jewellery_repairing.worker_name.owner:
            return True
        return False


class RepairingConfirmSubmitView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Repairing
    fields = ['gold_given', 'paid','comment']
    template_name = 'repairing/submit_repairing_work.html'
    success_url = '/'

    def form_valid(self, form):
        worker = Worker.objects.get(pk=form.instance.worker_name.pk)
        profile = Profile.objects.get(pk=self.request.user.pk)
        form.instance.loss = float(form.instance.gold_to_be_given) - float(form['gold_given'].value())
        worker.loss = float(worker.loss) + float(form.instance.loss)
        worker.paid = float(worker.paid) + float(float(form['paid'].value()))
        profile.loss = float(profile.loss) + float(form.instance.loss)
        profile.paid = float(profile.paid) + float(float(form['paid'].value()))
        form.instance.finish_date = timezone.now()
        worker.save()
        profile.save()
        return super().form_valid(form)

    def test_func(self):
        jewellery_repairing = self.get_object()
        if self.request.user == jewellery_repairing.worker_name.owner:
            return True
        return False


class RepairingAllListView(LoginRequiredMixin, ListView):
    model = Repairing
    template_name = 'repairing/all_repairing_work.html'
    context_object_name = 'jewelleries_repairing'
    paginate_by = 9

    def get_queryset(self):
        search = self.request.GET.get('search')
        if search :
            search = search.strip()
            return Repairing.objects.filter(
                Q(jewellery_name__icontains=search) |
                Q(jewellery_owner_name__icontains=search) |
                Q(worker_name__full_name__icontains=search)
            ).distinct().order_by('-start_date')
        else:
            return Repairing.objects.all().order_by('-start_date')


