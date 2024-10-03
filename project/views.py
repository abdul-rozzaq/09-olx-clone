from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout

from django.core.handlers.wsgi import WSGIRequest
from django.db.models import Q

from .forms import AuthenticationForm, UserCreationForm
from .models import Announcement, AnnouncementImage, Category
from .forms import AnnouncementForm


def home_page(request: WSGIRequest):
    all_announcements = Announcement.objects.all()
    announcements = Announcement.objects.all()

    query = request.GET.get("q", "")
    category = request.GET.get("c", "")

    if category:
        announcements = announcements.filter(category_id=category)
    
    if query:
        announcements = announcements.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )
    
    

    categories = Category.objects.all()
    context = {
        "announcements": announcements,
        "categories": categories,
        "q": query,
        "all_announcements": all_announcements,
    }

    return render(request, "index.html", context)


@login_required(login_url="login")
def detail_page(request: WSGIRequest, pk: int):
    ann = Announcement.objects.get(pk=pk)
    context = {"announcement": ann}
    return render(request, "detail_page.html", context)


@login_required(login_url="login")
def add_announcement(request: WSGIRequest):

    if request.method == "POST":
        data = {**request.POST.dict(), "owner": request.user.pk}
        form = AnnouncementForm(data)
        images = request.FILES.getlist("images")

        if form.is_valid() and len(images) > 0:
            obj = form.save()

            for img in images:
                AnnouncementImage.objects.create(ann=obj, image=img)

            return redirect("home_page")

    else:
        form = AnnouncementForm()

    categories = Category.objects.all()
    context = {"form": form, "categories": categories}
    return render(request, "add_announcement.html", context)


@login_required(login_url="login")
def edit_announcement(request: WSGIRequest, pk):
    announcement = get_object_or_404(Announcement, pk=pk, owner=request.user)
    images = AnnouncementImage.objects.filter(ann=announcement)

    if request.method == "POST":
        form = AnnouncementForm(
            {**request.POST.dict(), "owner": request.user}, instance=announcement
        )
        new_images = request.FILES.getlist("images")

        if form.is_valid():
            form.save()

            if new_images:
                AnnouncementImage.objects.filter(ann=announcement).delete()
                for img in new_images:
                    AnnouncementImage.objects.create(ann=announcement, image=img)

            return redirect("home_page")

        print(form.errors)
    else:
        form = AnnouncementForm(instance=announcement)

    categories = Category.objects.all()
    context = {
        "form": form,
        "categories": categories,
        "announcement": announcement,
        "images": images,
    }
    return render(request, "edit_announcement.html", context)


@login_required(login_url="login")
def delete_announcement(request: WSGIRequest, pk: int):
    ann_item = get_object_or_404(Announcement, pk=pk)

    if request.user == ann_item.owner:
        ann_item.delete()

    return redirect("home_page")


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():

            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")

            user = authenticate(username=username, password=password)

            if user is not None:

                login(request, user)

                return redirect("home_page")
    else:
        form = AuthenticationForm()

    return render(request, "login.html", {"form": form})


def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home_page")
    else:
        form = UserCreationForm()

    return render(request, "register.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("home_page")
