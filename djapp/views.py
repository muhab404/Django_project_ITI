from .forms import *
from .models import *
from pickle import TRUE
from django import forms
from .forms import UserForm
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.admin import User
from django.shortcuts import render , redirect
from django.contrib.auth.models import auth,User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import get_object_or_404, render , redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

# Register page
def register(request):
    # create register form
    signup_form = UserForm()
    # if the method post
    if(request.method =='POST'):
        signup_form = UserForm(request.POST)  #input from user
        if(signup_form.is_valid()):
            # the user is active (not block)
            signup_form.instance.is_staff = True
            signup_form.save()
            msg = 'User account created for username: ' + signup_form.cleaned_data.get('username')
            messages.info(request, msg)
            return redirect('login')
        # else:
        #     context = {'signup_form': signup_form}
        #     return render(request, 'djapp/register.html', context)
    # if the method not post
    context = {'signup_form': signup_form}
    return render(request, 'djapp/register.html', context)

# Log in page
def loginPg(request):
    # if the user already logedin
    if request.user.is_authenticated:
        # return to home
        return redirect('home')
    else:
        # if the method is post (contain data)
        if request.method == 'POST':
            name = request.POST.get('username')
            passwd = request.POST.get('password')
            user = authenticate(username= name, password =passwd)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                # show error massage if user name or password was incorrect
                messages.info(request, 'User name or password is incorrect')
        # go to login if :
        # user not authenticated or the name or password not correct
        return render(request, 'djapp/login.html')

# Sign out function
def signoutPg(request):
    logout(request)
    return redirect('home')

# Home page
def home(request):
    # select all categories in db
    all_categories = Category.objects.all()
    # select all posts in db
    post = Post.objects.all()
    # check if the user logedin or not
    if request.user.id != None:
        # if login
        x = []
        # get all category for specific user
        cat = CategoryMembership.objects.filter(userr=request.user.id)
        # list of user's categories
        for i in cat :
            x.append(i.categoryy.Name)
        context= {'categories': all_categories,'my_category':x,'posts':post, 'u_id': request.user.id }
        return render(request,'djapp/home.html',context)
    # if not login
    else:
        context = {'categories': all_categories,'posts':post}
        return render(request,'djapp/home.html',context)

# post page
def showPost(request, p_id):
    # search in post table for that specific post with id
    post = Post.objects.get(id = p_id)
    # search in Comment table for all comments that is relative to that post
    comments = Comment.objects.filter(Post_id = post)
    # count post likes
    post.Likes = Postlike.objects.filter(Post_id=p_id,Islike=True).count()
    # count post dislikes
    post.Dislikes = Postlike.objects.filter(Post_id=p_id,Isdislike=True).count()
    # save counters in post db
    post.save()
    user = request.user.id
    # check if the user logedin or not
    if request.user.id !=None:
        # if login
        # check if the method is post
        if request.method=='POST':
            # take the comment form data
            form = CommentForm(request.POST)
            # check the comment data validation
            if form.is_valid():
                # if valid set the comment data in comment table
                comment = Comment(User_id= request.user,Text=form.cleaned_data['Text'],Post_id=post)
                comments = str(comment)
                comments = comments.split(" ")
                censor = Word.objects.all()
                censors = str(censor)
                for i,word in enumerate(comments):
                    if word in censors:
                        comments[i] = '*****'     
                comment.Text = " ".join(comments)
                # and save the data in db
                comment.save()
                # back to post page
                return redirect(f'/djapp/post/{p_id}')
        # if the method is not post
        else:
            # create empty comment form
            form = CommentForm()
            # find if the user already like that post or not
            pos = Postlike.objects.filter(User_id=user,Post_id=post.id,Islike=True,Isdislike=False)
            pos1 = Postlike.objects.filter(User_id=user,Post_id=post.id,Islike=False,Isdislike=True)
            return render(request,'djapp/post.html',{'Post':post,'my_post':pos,'my_post1':pos1,'Likes_no': post.Likes,'Dislikes_no': post.Dislikes,'data':post,'form':form,'comments':comments})
    else:    
        context = { 'Post' : post }
        return render(request,'djapp/post.html',context)

# Category functions
@login_required(login_url='login')
def subscribe(request,id):
    userr = request.user
    categoryy = Category.objects.get(id=id)
    adding_to_model = CategoryMembership(userr=userr,categoryy=categoryy)
    adding_to_model.save()
    return redirect('home')

@login_required(login_url='login')       
def unsubscribe(request,id):
    userr = request.user
    categoryy = Category.objects.get(id=id)
    CategoryMembership.objects.filter(userr=userr,categoryy=categoryy).delete()
    return redirect('home')

# like functions
def like(request,id):
    user = request.user
    post = Post.objects.get(id=id)
    adding_to_model = Postlike(User_id=user,Post_id=post,Islike=True,Isdislike=False)
    adding_to_model.save()
    Postlike.objects.filter(User_id=user,Post_id=post,Isdislike=True,Islike=False).delete()
    return redirect(f'/djapp/post/{id}')  

def unlike(request,id):
    user = request.user
    post = Post.objects.get(id=id)
    Postlike.objects.filter(User_id=user,Post_id=post,Islike=True,Isdislike=False).delete()
    return redirect(f'/djapp/post/{id}')

def dislike(request,id):
    user = request.user
    post = Post.objects.get(id=id)
    adding_to_model = Postlike(User_id=user,Post_id=post,Islike=False,Isdislike=True)
    adding_to_model.save()
    Postlike.objects.filter(User_id=user,Post_id=post,Isdislike=False,Islike=True).delete()
    return redirect(f'/djapp/post/{id}')  

def undislike(request,id):
    user = request.user
    post = Post.objects.get(id=id)
    Postlike.objects.filter(User_id=user,Post_id=post,Islike=False,Isdislike=True).delete()
    return redirect(f'/djapp/post/{id}')


@login_required(login_url='login') 
def addUser(request):
    user_form = UForm()
    if request.method == "POST":
        user_form = UForm(request.POST)
        if user_form.is_valid():
            user_form.save()
            return redirect('blog')
    context = { 'form' : user_form }
    return render(request,'djapp/u_add.html',context)

@login_required(login_url='login')  
def delUser(request,u_id):
    user = User.objects.get(id = u_id)
    user.delete()
    return redirect('blog')

@login_required(login_url='login')  
def editUser(request,u_id):
    user = User.objects.get(id = u_id)
    if request.method == "POST":
        form = UForm(request.POST,instance=user)
        if form.is_valid():
            form.save()
            return redirect('blog')
    form = UForm(instance=user)
    context = { 'form' : form }
    return render(request,'djapp/u_add.html',context)

# Post functions
@login_required(login_url='login')  
def addPost(request):
    form = PForm()
    if request.method == 'POST':
        form = PForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('blog')
    context = {'form' : form }
    return render(request, 'djapp/p_add.html', context)

@login_required(login_url='login')  
def editPost(request, p_id):
    post = Post.objects.get(id = p_id)
    if request.method == "POST":
        form = PForm(request.POST,request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('blog')

    form = PForm(instance = post)
    context = {'form': form}
    return render(request, 'djapp/p_add.html', context)

@login_required(login_url='login')  
def delPost(request, p_id):
    post = Post.objects.get(id = p_id)
    post.delete()
    return redirect('blog') 

# manage blog page 
def manageBlog(request):
    if request.user.is_superuser:
        users = User.objects.all()
        posts = Post.objects.all()
        categories = Category.objects.all()
        words = Word.objects.all()
        context = { 'users' : users , 'posts' : posts , 'categories' : categories , 'words' : words}
        return render(request,'djapp/blog.html',context)
    else:
        return redirect('home') 

# search posts with tags or category
def search(request):
    if request.method == "POST":
        searched = request.POST['searched']
        posts = Post.objects.filter(Tags__Name__icontains=searched) | Post.objects.filter(Title__icontains=searched)
        return render(request,'djapp/search.html',{'searched':searched,'Posts':posts})
    else:
        return render(request,'djapp/home.html')

def categoryposts(request,c_id):
    posts = Post.objects.filter(Post_category=c_id)
    return render(request,'djapp/categoryposts.html',{'Posts':posts})

#category's functions
@login_required(login_url='login')  
def addCatagory(request):
    form = CategoryForm()
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('blog')
    context = {'form' : form }
    return render(request, 'djapp/Cat_add.html', context)

@login_required(login_url='login')  
def editCatagory(request, cat_id):
    category = Category.objects.get(id = cat_id)
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('blog')
    form = CategoryForm(instance = category)
    context = {'form': form}
    return render(request,'djapp/CategoriesForm.html', context)

@login_required(login_url='login')  
def delCatagory(requset, cat_id):
    category = Category.objects.get(id = cat_id)
    category.delete()
    return redirect('blog') 

#undesired words function
@login_required(login_url='login')  
def addWord(request):
    form = BadWordsForm()
    if request.method == 'POST':
        form = BadWordsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('blog')
    context = {'form' : form }
    return render(request, 'djapp/w_add.html', context)

@login_required(login_url='login')  
def editWord(request, w_id):
    word = Word.objects.get(id = w_id)
    if request.method == "POST":
        # send the new word to db
        form = BadWordsForm(request.POST, instance=word)
        if form.is_valid(): 
            form.save()
            return redirect('blog')
    # displaying the old word when accessing the page for the first time
    form = BadWordsForm(instance = word)
    context = {'form': form}
    return render(request,'djapp/Bad_Words_Form.html', context)

@login_required(login_url='login')  
def delWord(request, w_id):
    word = Word.objects.get(id = w_id)
    word.delete()
    return redirect('blog')
