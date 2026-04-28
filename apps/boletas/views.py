from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from weasyprint import HTML
from .models import Boleta, ItemBoleta
from .forms import BoletaForm, ItemBoletaFormSet


class BoletaListView(LoginRequiredMixin, ListView):
    model = Boleta
    template_name = 'boletas/lista.html'
    context_object_name = 'boletas'
    paginate_by = 20

    def get_queryset(self):
        qs = super().get_queryset().select_related('cliente')
        q = self.request.GET.get('q', '')
        if q:
            qs = qs.filter(cliente__nombre__icontains=q) | qs.filter(numero__icontains=q)
        return qs


class BoletaCreateView(LoginRequiredMixin, CreateView):
    model = Boleta
    form_class = BoletaForm
    template_name = 'boletas/form.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if self.request.POST:
            ctx['formset'] = ItemBoletaFormSet(self.request.POST)
        else:
            ctx['formset'] = ItemBoletaFormSet()
        return ctx

    def form_valid(self, form):
        ctx = self.get_context_data()
        formset = ctx['formset']
        if formset.is_valid():
            # auto-número correlativo
            ultimo = Boleta.objects.order_by('-numero').first()
            form.instance.numero = (ultimo.numero + 1) if ultimo else 1
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return super().form_valid(form)
        return self.form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('boletas:detalle', kwargs={'pk': self.object.pk})


class BoletaDetailView(LoginRequiredMixin, DetailView):
    model = Boleta
    template_name = 'boletas/detalle.html'
    context_object_name = 'boleta'

    def get_queryset(self):
        return super().get_queryset().prefetch_related('items').select_related('cliente')


class BoletaUpdateView(LoginRequiredMixin, UpdateView):
    model = Boleta
    form_class = BoletaForm
    template_name = 'boletas/form.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if self.request.POST:
            ctx['formset'] = ItemBoletaFormSet(self.request.POST, instance=self.object)
        else:
            ctx['formset'] = ItemBoletaFormSet(instance=self.object)
        return ctx

    def form_valid(self, form):
        ctx = self.get_context_data()
        formset = ctx['formset']
        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return super().form_valid(form)
        return self.form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('boletas:detalle', kwargs={'pk': self.object.pk})


@login_required
def boleta_pdf(request, pk):
    boleta = get_object_or_404(
        Boleta.objects.prefetch_related('items').select_related('cliente'), pk=pk
    )
    html_string = render_to_string('boletas/pdf.html', {'boleta': boleta})
    pdf = HTML(string=html_string, base_url=request.build_absolute_uri('/')).write_pdf()
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="boleta_{boleta.numero}.pdf"'
    return response
