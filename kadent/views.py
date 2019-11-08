from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from kadent.models import Patient, Visit, Image
from .forms import ImageForm, PatientForm

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
    form_class = ImageForm

    def post(self, request, *args, **kwargs):
        no_errors = True
        instances = []
        patient = Patient.objects.get(id=self.kwargs['pk'])
        for img in request.FILES.getlist('images'):
            request.FILES['file'] = img
            form = ImageForm(request.POST, request.FILES)
            if form.is_valid():
                instance = form.save(commit=False)
                instances.append(instance)
            else:
                # when first error occures add info message and set no_errors to False
                if no_errors == True:
                    no_errors = False
                    messages.info(
                        request,
                        '''<div class="alert alert-danger" role="alert">
                            <h2 class="text-center">Obrazy nie zostały zapisane!</h2>
                            <h3>Wystąpiły następujące błędy:</h3>
                        </div>'''
                        )
                messages.error(
                    request, 
                    '<div class="alert alert-danger" role="alert">{0}</div>'.format(
                        str(form.errors))
                    )
        
        # save to db only if there were no errors in any of the files 
        if no_errors:
            for instance in instances:
                instance.created_by = request.user
                instance.patient = patient
                instance.save()
            return redirect('kadent:patient_edit', patient.id)
        else:
            return redirect('kadent:image_create_from_visit', patient.id)


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
