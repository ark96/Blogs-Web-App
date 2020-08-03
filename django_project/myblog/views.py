from django.shortcuts import render,get_object_or_404,render_to_response
from django.http import HttpResponse,HttpResponseRedirect,HttpResponseNotFound
from .models import Post
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView,View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib import messages
from django.core.paginator import Paginator

def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'myblog/home.html', context)

class PostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'myblog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 2

class UserPostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'myblog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 2

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

class SearchView(LoginRequiredMixin,ListView):
        model = Post
        template_name = 'myblog/home.html'
        context_object_name = 'posts'
        ordering = ['-date_posted']
        paginate_by = 2
        def get(self,request):
            posts = Post.objects.all().order_by('-date_posted')
            paginator = Paginator(posts,2)
            page = request.GET.get('page')
            if 'search' in request.GET and request.GET['search']:
                search = request.GET['search']
                #path = str(request.get_full_path)
                #indextemp = path.find('search=')
                #search = path[indextemp+7 : -3]
                for post in posts:
                    if search.lower() == post.author.username.lower():
                        userid = post.author_id
                        break
                    else:
                        userid = None
                if userid == None:
                    #post : Post.objects.all().order_by('-date_posted')
                    context = {
                    'posts': paginator.get_page(page),
                            #'posts' : paginator.get_page(page),
                    'message' : 'No search found'
                    }
                    return render(request,'myblog/search.html', context)
                    #return render_to_response('myblog/search.html',  context)
                else:
                    post = Post.objects.filter(author=userid).order_by('-date_posted')
                    paginator = Paginator(post,2)
                    page = request.GET.get('page')
                    context = {
                            'posts' : paginator.get_page(page),
                            'query' : search
                            }
                    return render(request, 'myblog/search.html', context)
            else:
                #page = request.GET.get('page')
                print(page)

                if page == None:
                    messages.warning(request, 'Search Box cannot be empty!')
                    context={
                    'posts' : paginator.get_page(page)
                    }
                else:
                    context={
                    'posts' : paginator.get_page(page)
                    }
                return render(request,'myblog/search.html',context)
                #return HttpResponseRedirect(reverse('blog-home' ))


class PostDetailView(DetailView):
    model = Post

def ErrorView(request):
        context = {
            'posts' : []
        }
        return render(request, 'myblog/error.html', context)

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title','content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title','content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/blog/'
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, 'myblog/about.html', {'title' : 'About'})
