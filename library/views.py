from django.shortcuts import render,redirect
from .models import Student,Books, IssuedItem
from django.contrib import messages
from django.contrib.auth.models import auth, User
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from datetime import date
from django.core.paginator import Paginator

# Create your views here.
def home(request):
    return render(request,"home.html")

def loginstu(request):
     # If request is post then get username and password from request
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        # Authenticate user
        user = auth.authenticate(username=username, password=password)
        # If user is authenticated then login user
        if user is not None:
            auth.login(request, user)
            # Redirect to home page
            return redirect("/")
        else:
            # If user is not authenticated then show error message
            # and redirect to login page
            messages.info(request, "Invalid Credential")
            return redirect("loginstu")
    else:
        # If request is not post then render login page
        return render(request, "loginstu.html")
# Register view to register user
def registerstu(request):
    # If request is post then get user details from request
    if request.method == "POST":
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        username = request.POST["username"]
        email = request.POST["email"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]
        # Check if password and confirm password matches
        if password1 == password2:
            # Check if username or email already exists
            if User.objects.filter(username=username).exists():
                messages.info(request, "Username already exist")
                return redirect("registerstu")
            # Check if email already exists
            elif User.objects.filter(email=email).exists():
                messages.info(request, "Email already registered")
                return redirect("registerstu")
            # If username and email does not exists then create user
            else:
                # Create user
                user = User.objects.create_user(
                    first_name=first_name,
                    last_name=last_name,
                    username=username,
                    email=email,
                    password=password1,
                )
                # Save user
                user.save()
                # Redirect to login page
                return redirect("loginstu")
        else:
            # If password and confirm password does not matches then show error message
            messages.info(request, "Password not matches")
            return redirect("registerstu")
    else:
        # If request is not post then render register page
        return render(request, "registerstu.html")
# Logout view to logout user
def logout(request):
    # Logout user and redirect to home page
    auth.logout(request)
    return redirect("/")

def index(request):
    return render(request,"index.html")

def student(request):
    data=Student.objects.all()
    context={"data":data}
    return render(request,"student.html",context)

def books(request):
    data=Books.objects.all()
    context={"data":data}
    return render(request,"books.html",context)

def insertdata(request):
    if request.method=="POST":
        name=request.POST.get('name')
        email=request.POST.get('email')
        age=request.POST.get('age')
        gender=request.POST.get('gender')
        print(name,email,age,gender)
        query=Student(name=name,email=email,age=age,gender=gender)
        query.save()
        messages.info(request,"Data Inserted Successfully")
        return redirect("student")
    
    return render(request,"student.html")

def insertbook(request):
    if request.method=="POST":
        book_id=request.POST.get('bid')
        book_name=request.POST.get('btitle')
        author_name=request.POST.get('bauthor')
        print(book_id,book_name,author_name)
        ins=Books(book_id=book_id, book_name=book_name, author_name=author_name)
        ins.save()
        messages.info(request,"Book added Successfully")
        return redirect("books")
    
    return render(request,"books.html")


def updateData(request,id):
    if request.method=="POST":
        name=request.POST['name']
        email=request.POST['email']
        age=request.POST['age']
        gender=request.POST['gender']

        edit=Student.objects.get(id=id)
        edit.name=name
        edit.email=email
        edit.gender=gender
        edit.age=age
        edit.save()
        messages.warning(request,"Data Updated Successfully")
        return redirect("student")

    d=Student.objects.get(id=id) 
    context={"d":d}
    return render(request,"edit.html",context)

def deleteData(request,id):
    d=Student.objects.get(id=id) 
    d.delete()
    messages.error(request,"Data deleted Successfully")
    return redirect("student")


def deletebooks(request,id):
    d=Books.objects.get(id=id) 
    d.delete()
    messages.error(request,"Data deleted Successfully")
    return redirect("books")

# Issue view to issue book to user
@login_required(login_url='login')
def issue(request):
    
    if request.method == "POST":
            book_id = request.POST["bid"]
            current_book = Books.objects.get(id=book_id)
            data = Books.objects.filter(bid=book_id)
            issue_item = IssuedItem.objects.create(
                user_id=request.user, book_id=current_book
            )
            issue_item.save()
            books.update(quantity=books[0].quantity - 1)
            # Show success message and redirect to issue page
            messages.success(request, "Book issued successfully.")
        # Get all books which are not issued to user
    my_items = IssuedItem.objects.filter(
       user_id=request.user, return_date__isnull=True
        ).values_list("book_id")
    books = Books.objects.exclude(id__in=my_items).filter(quantity__gt=0)
        # Return issue page with books that are not issued to user
    return render(request, "issue_item.html", {"books": books})
    

# Return view to return book to library
@login_required(login_url='login')
def return_item(request):

    # If request is post then get book id from request
    if(request.method == 'POST'):

        # Get book id from request
        book_id = request.POST['book_id']

        # Get book object
        current_book = Books.objects.get(id=book_id)

        # Update book quantity
        book = Books.objects.filter(id=book_id)
        book.update(quantity = book[0].quantity+1)

        # Update return date of book and show success message
        issue_item = IssuedItem.objects.filter(user_id=request.user,book_id=current_book,return_date__isnull=True)
        issue_item.update(return_date=date.today())
        messages.success(request, 'Book returned successfully.')

    # Get all books which are issued to user
    my_items = IssuedItem.objects.filter(user_id = request.user,return_date__isnull=True).values_list('book_id')
    
    # Get all books which are not issued to user
    books = Books.objects.exclude(~Q(id__in=my_items))

    # Return return page with books that are issued to user
    params = {'books':books}
    return render(request,'return_item.html',params)
