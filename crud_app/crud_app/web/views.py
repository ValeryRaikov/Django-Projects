from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from django.urls import reverse_lazy
from .models import Core


class IndexView(ListView):
    model = Core
    template_name = 'core/index.html'
    context_object_name = 'index'


class SingleView(DetailView):
    model = Core
    template_name = 'core/single.html'
    context_object_name = 'post'


class PostsView(ListView):
    model = Core
    template_name = 'core/posts.html'
    context_object_name = 'post_list'


class AddView(CreateView):
    model = Core
    fields = '__all__'
    template_name = 'core/add.html'
    success_url = reverse_lazy('core:posts')


class EditView(UpdateView):
    model = Core
    template_name = 'core/edit.html'
    fields = '__all__'
    success_url = reverse_lazy('core:posts')


class PostDeleteView(DeleteView):
    model = Core
    success_url = reverse_lazy('core:posts')
    template_name = 'core/confirm-delete.html'
