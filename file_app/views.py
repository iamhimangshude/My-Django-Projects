from django.shortcuts import render

from file_app.forms import FileFieldForm
from file_app.models import File, Folder

# Create your views here.


def index(request):
    files = File.objects.all()
    folders = Folder.objects.filter(is_subfolder=False)
    return render(
        request,
        "file_app/index.html",
        context={
            "files": files,
            "folders": folders,
        },
    )


def file_view(request):
    form = FileFieldForm()
    if request.method == "POST":
        form = FileFieldForm(request.POST, request.FILES)
        if form.is_valid():
            files = request.FILES.getlist("file_field")
            for file in files:
                File.objects.create(file=file)
    return render(request, "file_app/file-upload.html", context={"form": form})
