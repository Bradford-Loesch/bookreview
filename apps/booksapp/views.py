from django.shortcuts import render, redirect
from django.contrib import messages
import models
import bcrypt
import re

# Create your views here.
def index(request):
    # Test for login
    if not 'login' in request.session:
        request.session['login'] = False
    # If logged in, redirect to main page
    if request.session['login']:
        return redirect('/main')
    return render(request, 'booksapp/index.html')

def main(request):
    # Check for login, if not redirect
    if not request.session['login']:
        messages.error(request, 'Please log in to access the reviews.')
        return redirect('/')
    # Get current user info and render page
    user = models.User.objects.get(id = request.session['login'])
    books = models.Book.objects.all()
    reviews = models.Review.objects.all().order_by('-created_at')[:3]
    context = {
        'user' : user,
        'books' : books,
        'reviews' : reviews
    }
    return render(request, 'booksapp/main.html', context)

def books(request, bid):
    # Get data
    user  = models.User.objects.get(id = request.session['login'])
    book = models.Book.objects.get(id = bid)
    reviews = models.Review.objects.filter(Book_id = bid)
    context = {
    'user' : user,
    'book' : book,
    'reviews' : reviews
    }
    return render(request, 'booksapp/showbook.html', context)

def users(request, uid):
    # Get data
    user  = models.User.objects.get(id = request.session['login'])
    dispuser  = models.User.objects.get(id = uid)
    count = models.Review.objects.filter(User_id = uid).count()
    reviews = models.Review.objects.filter(User_id = uid)
    context = {
        'user' : user,
        'dispuser' : dispuser,
        'count' : count,
        'reviews' : reviews
    }
    return render(request, 'booksapp/showuser.html', context)

def bookreview(request):
    user  = models.User.objects.get(id = request.session['login'])
    authors = models.Author.objects.all()
    context = {
        'user' : user,
        'authors': authors
    }
    print authors
    return render(request, 'booksapp/addbookreview.html', context)

def addbook(request):
    if request.method == 'POST':
        context = request.POST
        if context['authors'] == 'null':
            newauthor = models.Author(name = context['authortext'])
            newauthor.save()
        else:
            newauthor = models.Author.objects.get(name = context['authors'])
        newbook = models.Book(name = context['title'], Author = newauthor)
        newbook.save()
        newreview = models.Review(rating = context['rating'], comment = context['review'], User_id = request.session['login'], Book = newbook)
        newreview.save()
    return redirect('/main')

def addreview(request):
    if request.method == 'POST':
        context = request.POST
        newreview = models.Review(rating = context['rating'], comment = context['review'], User_id = request.session['login'], Book_id = context['bookid'])
        newreview.save()
    return redirect('/main')

def register(request):
    # Get post data and add to database
    if request.method == 'POST':
        # Get data
        context = request.POST
        #Check if data is valid
        if validate(request, context):
            # Encrypt password and add entry
            hashed = encrypt(context['passworda'])
            new = models.User(first_name = context['first_name'], last_name = context['last_name'], email = context['email'], password = hashed)
            new.save()
            # Set login to user id and redirect to main page
            return redirect('/main')
    return redirect('/')

def login(request):
    # Fetch user information and check password
    if request.method == 'POST':
        try:
            user = models.User.objects.get(email = request.POST['loginemail'])
        except:
            messages.error(request, 'Please enter a valid username and password.')
            return redirect('/')
        if comparePass(request.POST['loginpassword'], user.password):
            request.session['login'] = user.id
        else:
            messages.error(request, 'Password did not match.')
            return redirect('/')
    return redirect('/main')

def logout(request):
    # Show logout message and set request.session variable to false
    messages.error(request, 'You have been logged out.')
    request.session['login'] = False
    return redirect('/')

def encrypt(password):
    # encode and hash password
    password = password.encode()
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())
    return hashed

def comparePass(password, hashed):
    # compare entered and stored passwords
    password = password.encode()
    hashed = hashed.encode()
    if bcrypt.hashpw(password, hashed) == hashed:
        return True
    return False

def validate(request, context):
    # Validation testing
    EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
    failboat = False
    if (len(context['first_name']) < 2):
        messages.error(request, 'First name must be at least 2 characters.')
        failboat = True
    if (len(context['last_name']) < 2):
        messages.error(request, 'First name must be at least 2 characters.')
        failboat = True
    if not EMAIL_REGEX.match(context['email']):
        messages.error(request, 'Email is not valid. Please enter a valid email address.')
        failboat = True
    if (len(context['passworda']) < 8 or len(context['passwordb']) < 8):
        messages.error(request, 'Password must be at least 8 characters')
        failboat = True
    if (context['passworda'] != context['passwordb']):
        messages.error(request, 'Passwords must match')
        failboat = True
    if failboat:
        return False
    return True
