from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from kadent.models import Patient, Visit, Image


class PatientCreate(LoginRequiredMixin, CreateView):
    model = Patient
    fields = ['first_name', 'last_name', 'notes']

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.created_by = self.request.user
        return super(PatientCreate, self).form_valid(form)


class PatientUpdate(LoginRequiredMixin, UpdateView):
    model = Patient
    fields = ['first_name', 'last_name', 'notes']
    template_name_suffix = '_update_form'
    def get_initial(self):
        return {'first_name': self.object.first_name,
                'last_name': self.object.last_name,
                'notes': self.object.notes}


class PatientDelete(LoginRequiredMixin, DeleteView):
    model = Patient
    success_url = reverse_lazy('kadent:patient_list')


class PatientList(LoginRequiredMixin, ListView):
    model = Patient
    paginate_by = 50
