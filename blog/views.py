from django.shortcuts import render,get_object_or_404,redirect
from .models import Post, comment
from django.utils import timezone
from .forms import PostForm, commentForm
from django.contrib.auth.decorators import login_required

def post_list(request):
    posts=Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'blog/post_list.html', {'posts':posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post':post})

@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()

    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)

    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_draft_list(request):
    posts=Post.objects.filter(published_date__isnull=True).order_by('-created_date')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})

@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)

@login_required
def post_rm(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')

def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = commentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)

    else:
        form = commentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})

@login_required
def comment_approve(request, pk):
    commentt = get_object_or_404(comment, pk=pk)
    commentt.approve()
    return redirect('post_detail', pk=commentt.post.pk)

@login_required
def comment_remove(request, pk):
    com = get_object_or_404(comment, pk=pk)
    com.delete()
    return redirect('post_detail', pk=com.post.pk)
