from django.views.generic import TemplateView, FormView, UpdateView
from django.views.generic.edit import ProcessFormView, ModelFormMixin
from django.shortcuts import render, redirect, reverse

from accounts.models import Staff
from airstaffapp.forms import StaffRoleEditForm


class HomeView(TemplateView):
    template_name = "home_staff.html"

    def get_context_data(self):
        context = super(HomeView, self).get_context_data()
        context['role'] = Staff.objects.get(user=self.request.user).role
        return context


class StaffListView(TemplateView):
    template_name = "staff_list.html"

    def get_context_data(self):
        context = super(StaffListView, self).get_context_data()
        staff = Staff.objects.all()
        editable_staff = []
        for person in staff:
            if person.role != 'supervisor':
                editable_staff.append(person)
        context['staff'] = editable_staff
        return context


class EditRoleView(UpdateView):
    template_name = "edit_role.html"
    form_class = StaffRoleEditForm
    model = Staff

    def get_success_url(self):
        return reverse('staff:staff list')

    def get_context_data(self):
        context = super(EditRoleView, self).get_context_data()
        person = Staff.objects.get(id=self.kwargs['pk'])
        context['person'] = person
        return context

    def form_valid(self, form):
        form_data = form.save(commit=False)
        form_data.save()
        return super().form_valid(form)
