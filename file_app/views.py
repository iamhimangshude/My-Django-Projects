from django.shortcuts import render

from file_app.forms import FileFieldForm
from file_app.models import File, Folder

# Create your views here.


def index(request):
    form = FileFieldForm()
    if request.method == "POST":
        form = FileFieldForm(request.POST, request.FILES)
        if form.is_valid():
            files = request.FILES.getlist("file_field")
            for file in files:
                File.objects.create(file=file)
    return render(request, "file_app/index.html", context={"form": form})
