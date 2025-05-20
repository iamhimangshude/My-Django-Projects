from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import Notes

# Create your views here.
def home(request):
    all_notes = Notes.objects.all().order_by("-created_at")
    return render(request, 'notes/home.html', {"all_notes": all_notes})

def add_note(request):
    if request.method == "POST":
        title = request.POST["title"]
        content = request.POST["content"]
        note = Notes(title=title, content=content)
        note.save()
        return HttpResponseRedirect(reverse("home"))
    return render(request, 'notes/add_note.html')

def edit_note(request, id):
    print(id)
    print(request.GET)
    if request.method == "POST":
        note = Notes.objects.get(id=id)
        note.title = request.POST.get("title")
        note.content = request.POST.get("content")
        note.save()
        return HttpResponseRedirect(reverse("home"))
    note = Notes.objects.get(id=id)
    return render(request, "notes/edit_note.html", {
        "note": note
    })

def delete_note(request, id):
    note = Notes.objects.get(id=id)
    note.delete()
    return HttpResponseRedirect(reverse("home"))