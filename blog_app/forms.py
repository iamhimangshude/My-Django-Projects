from django import forms

from blog_app.models import Post

class AddBlogPost(forms.ModelForm):
    class Meta:
        model = Post
        # fields = "__all__"
        exclude = ['created_at', 'updated_at', 'creator']
        labels = {
            'title': "Title",
            'excerpt':'Excerpt',
            'content':'Content',
            'image':'Image',
        }
        widgets = {
            'title':forms.TextInput({'placeholder':"Enter title"}),
            'excerpt':forms.TextInput({'placeholder':"Some short words here (max 200)"}),
            'content':forms.Textarea({'placeholder':"Describe about the post..."}),
        }