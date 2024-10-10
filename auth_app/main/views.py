from django.views.generic import TemplateView, CreateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .forms import RegistrationForm, PostForm
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login
from .models import Post, User
from django.contrib.auth.models import Group
from django.contrib import messages

class HomeView(LoginRequiredMixin, TemplateView):
    login_url = 'login/'
    template_name = 'main/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        post_id = request.POST.get('post-id')
        user_id = request.POST.get('user-id')

        if post_id:
            try:
                post = Post.objects.get(id=post_id)

                if post.author == request.user or request.user.has_perm('main.delete_post'):
                    post.delete()
            except Post.DoesNotExist:
                pass
        elif user_id:
            try:
                user = User.objects.get(id=user_id)

                if user.is_staff:
                    default_group = Group.objects.get(name='default')
                    mod_group = Group.objects.get(name='mod')

                    default_group.user_set.remove(user)
                    mod_group.user_set.remove(user)

                    messages.success(self.request, "User Banned!")
            except User.DoesNotExist:
                pass
            except Group.DoesNotExist:
                pass
            except Exception as e:
                print(f"Unexpected error: {e}")

        return HttpResponseRedirect(reverse_lazy('home'))


class SignUpView(CreateView):
    form_class = RegistrationForm
    template_name = 'registration/sign-up.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        response = super().form_valid(form)

        username = form.cleaned_data.get('username', None)
        password = form.cleaned_data.get('password1', None)
        user = authenticate(self.request, username=username, password=password)

        if user is not None:
            login(self.request, user)

        return response


class UserLoginView(LoginView):
    template_name = 'registration/login.html'
    success_url = reverse_lazy('home')

    def get_success_url(self):
        return self.success_url


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('login')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class CreatePostView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    login_url = 'login/'
    permission_required = ('main.add_post',)
    raise_exception = True
    form_class = PostForm
    template_name = 'main/create-post.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)