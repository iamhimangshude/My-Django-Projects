from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from file_app.forms import FileFieldForm
from file_app.models import File, Folder

# Create your views here.


def index(request):
    files = File.objects.filter(folder=None)
    folders = Folder.objects.filter(is_subfolder=False)

    return render(
        request,
        "file_app/index.html",
        context={
            "files": files,
            "folders": folders,
        },
    )


def file_upload_view(request):
    form = FileFieldForm()
    if request.method == "POST":
        form = FileFieldForm(request.POST, request.FILES)
        if form.is_valid():
            files = request.FILES.getlist("file_field")
            for file in files:
                File.objects.create(file=file)
    return render(request, "file_app/file-upload.html", context={"form": form})


def folder_view(request, folder_id):
    folder = Folder.objects.get(folder_id=folder_id)
    return render(request, "file_app/folder.html", context={"folder": folder})


def file_view(request, file_id):
    file_obj = get_object_or_404(File, pk=file_id)
    file_obj_type = file_obj.file_type()

    response = HttpResponse()

    if file_obj_type == "image":
        if file_obj.get_extension() == "webp":
            with open(file_obj.file.path, "rb") as f:
                response = HttpResponse(f.read(), content_type="image/webp")

        else:
            with open(file_obj.file.path, "rb") as f:
                response = HttpResponse(f.read(), content_type="image/jpeg")

    elif file_obj_type == "audio":
        with open(file_obj.file.path, "rb") as f:
            response = HttpResponse(f.read(), content_type="audio/mp3")

    elif file_obj_type == "document":
        file_ext = file_obj.get_extension()
        if file_ext == "pdf":
            response = HttpResponse(file_obj.file, content_type="application/pdf")

        elif file_ext == "txt":
            response = HttpResponse(file_obj.file, content_type="text/plain")

        else:
            response = HttpResponse(
                file_obj.file, content_type="application/octet-stream"
            )
            response["Content-Disposition"] = 'attachment; filename="{}"'.format(
                file_obj.file.name
            )

    elif file_obj_type == "video":
        with open(file_obj.file.path, "rb") as f:
            response = HttpResponse(f.read(), content_type="video/mp4")

    else:

        response = HttpResponse(file_obj.file, content_type="application/octet-stream")
        response["Content-Disposition"] = 'attachment; filename="{}"'.format(
            file_obj.file.name
        )

    return response
