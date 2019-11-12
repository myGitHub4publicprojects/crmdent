from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from kadent.models import Patient, Visit, Image
from .forms import ImageFormSet, PatientForm

class PatientCreate(LoginRequiredMixin, CreateView):
    model = Patient
    fields = ['first_name', 'last_name', 'notes']

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.created_by = self.request.user
        return super(PatientCreate, self).form_valid(form)


class PatientUpdate(LoginRequiredMixin, UpdateView):
    model = Patient
    form_class = PatientForm
    template_name_suffix = '_update_form'
    def get_initial(self):
        return {'first_name': self.object.first_name,
                'last_name': self.object.last_name,
                'notes': self.object.notes}

    def get_context_data(self, **kwargs):
        context = super(PatientUpdate, self).get_context_data(**kwargs)
        context['images'] = Image.objects.filter(patient=self.object)
        context['visits'] = Visit.objects.filter(patient=self.object)
        return context


class PatientDelete(LoginRequiredMixin, DeleteView):
    model = Patient
    success_url = reverse_lazy('kadent:patient_list')


class PatientList(LoginRequiredMixin, ListView):
    model = Patient
    paginate_by = 50


class VisitCreate(LoginRequiredMixin, CreateView):
    model = Visit
    fields = ['note']

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.doctor = self.request.user
        obj.patient = Patient.objects.get(id=self.kwargs['pk'])
        return super(VisitCreate, self).form_valid(form)

class VisitUpdate(LoginRequiredMixin, UpdateView):
    model = Visit
    fields = ['note']
    template_name_suffix = '_update_form'
    def get_initial(self):
        return {'note': self.object.note}


class VisitDelete(LoginRequiredMixin, DeleteView):
    model = Visit
    def get_success_url(self):
        return reverse('kadent:patient_edit', args=(self.object.patient.id,))


class ImageCreateFromPatient(LoginRequiredMixin, CreateView):
    '''Create Image object when request send from PatientUpdate view'''
    model = Image
    fields = ['note', 'file']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formset'] = ImageFormSet(queryset=Image.objects.none())
        return context

    def post(self, request, *args, **kwargs):
        counter = 0
        request.POST = request.POST.copy()
        for img in request.FILES.getlist('images'):
            request.FILES['form-{0}-file'.format(counter)] = img
            note = request.POST[img.name]
            request.POST['form-{0}-note'.format(counter)] = note
            counter += 1
        formset = ImageFormSet(self.request.POST, self.request.FILES)
        no_errors = True
        alert_div = '<div class="alert alert-danger" role="alert">{0}</div>'
        if formset.is_valid():
            return self.form_valid(formset)
        else:
            if no_errors:
                messages.info(
                    request, alert_div.format(
                        '<h2 class="text-center">Uwaga!</h2><h3>Wystąpiły następujące błędy:</h3>'
                    )
                )
                no_errors = False
            for errors_dicts in formset.errors:
                for val in errors_dicts.values():
                    messages.error(request, alert_div.format(val[0]))
            return redirect('kadent:image_create_from_patient', self.kwargs['pk'])

    def form_valid(self, form, **kwargs):
        patient = Patient.objects.get(id=self.kwargs['pk'])
        instances = form.save(commit=False)
        for instance in instances:
            instance.uploaded_by = self.request.user
            instance.patient = patient
        form.save()
        return redirect('kadent:patient_edit', patient.id)



class ImageCreateFromVisit(LoginRequiredMixin, CreateView):
    '''Create Image object when request send from VisitUpdate view'''

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.uploaded_by = self.request.user
        visit = Visit.objects.get(id=self.kwargs['pk'])
        obj.visit = visit
        obj.patient = visit.patient
        return super(ImageCreateFromVisit, self).form_valid(form)

    def get_success_url(self):
        visit = Visit.objects.get(id=self.kwargs['pk'])
        return reverse('kadent:visit_edit', args=(visit.id,))

class ImageUpdate(LoginRequiredMixin, UpdateView):
    model = Image
    fields = ['note']
    template_name_suffix = '_update_form'

    def get_initial(self):
        return {'note': self.object.note}
