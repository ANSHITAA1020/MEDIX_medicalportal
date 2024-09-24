from django.contrib import admin
from .models import *
from ckeditor.widgets import CKEditorWidget
from django import forms

# Create a custom form for the BlogPost admin
class BlogPostAdminForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = '__all__'
        widgets = {
            'content': CKEditorWidget(),  # using CKEDitor for formatting
        }

#custom admin class for BlogPost
class BlogPostAdmin(admin.ModelAdmin):
    form = BlogPostAdminForm


admin.site.register(Article)
admin.site.register(PatientProfile)
admin.site.register(BlogPost, BlogPostAdmin) 
admin.site.register(Department)
admin.site.register(ClinicHours)
admin.site.register(Appointment)
admin.site.register(Doctor)
admin.site.register(Document)
admin.site.register(ContactUs)
 