from typing import Any, Dict, Optional, Type
from django.db.models.query import QuerySet
from django.forms.forms import BaseForm
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy, reverse
from django.views.generic.list import ListView
from django.views.generic.edit import FormView, UpdateView, DeleteView
from django.views.generic.dates import ArchiveIndexView

from .models import Bb, Rubric
from .forms import BbForm



    


def index(request):
    bbs = Bb.objects.all()
    rubrics = Rubric.objects.all()
    context = {'bbs' : bbs, 'rubrics' : rubrics}
    return render(request, 'bboard/index.html', context)


def by_rubric(request, rubric_id):
    bbs=Bb.objects.filter(rubric=rubric_id)
    rubrics = Rubric.objects.all()
    current_rubric = Rubric.objects.get(pk=rubric_id)
    context = {'bbs' : bbs, 'rubrics' : rubrics, 'current_rubric' : current_rubric}
    return render(request, 'bboard/by_rubric.html', context)


class BbCreateView(CreateView):
    template_name = 'bboard/create.html'
    form_class = BbForm
    success_url = reverse_lazy('index')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context


#Стандартный контроллер-класс, который компактно позволяет писать
class BbDetailView(DetailView):
    model = Bb 
    
    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context
    
    
# выводит страницу с объявлениями из выбранной посетителем рубрики
class BbByRubricView(ListView):
    template_name = 'bboard/by_rubric.html'
    context_object_name = 'bbs'
   
    
    
        
    def get_queryset(self):
        return Bb.objects.filter(rubric=self.kwargs['rubric_id'])
    def get_ordering(self):
            ordering =  Bb.objects.filter(rubric=self.kwargs['rubric_id'])('ordering', '-published')
            # validate ordering here
            print("сортировка")
            return ordering
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.all()
        context['current_rubric'] = Rubric.objects.get(
                                    pk=self.kwargs['rubric_id'])
        return context
    
#Добавляет на виртуальную доску новое объявление и сохраняет его 
class BbAddView(FormView):
    template_name = 'bboard/create.html'
    form_class = BbForm
    initial = {'price': 0.0}
    
    def get_context_data(self, *args ,**kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context
    
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)  
    
    def get_form(self, form_class=None):
        self.object = super().get_form(form_class)
        return self.object
    
    def get_success_url(self):
        return reverse('bboard:by_rubric',
                       kwargs={'rubric_id': self.object.cleaned_data['rubric'].pk})


# выполняет исправление объявления
class BbEditView(UpdateView):
    model = Bb
    form_class = BbForm
    success_url = '/bboard/{rubric_id}'
    
    def get_context_data(self,  *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context


#выполняет удаление объявления
class BbDeleteView(DeleteView):
    model = Bb
    success_url = '/bboard/{rubric_id}'
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context
    
# выводит хронологический список записей, отсортированных по убыванию значения заданного поля
class BbIndexView(ArchiveIndexView):
    model = Bb
    date_field = 'published'
    date_list_period = 'year'
    template_name = 'bboard/index.html'
    context_object_name = 'bbs'
    allow_empty = True
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context 
       