from django.contrib import admin
from .models import *

"""" Admin panel 

Keyword arguments:
model -- take the model 'table' from model.py
modelAdmin -- take the model that will display in the admin panel
Return: the admin panel that display when enter localhost:admin
"""

#Noura
class CategoryAdmin(admin.ModelAdmin):
    """custom display

    Args:
        fieldsets : the display of create category form
        list_display : the display of the category list
        search_fields : search fields to custom the list display
    """
    fieldsets = (
        ['Category Details',{'fields':['Name']}],
    )
    list_display = ('Name',)
    search_fields = ['Name']

#Yostos
class TagAdmin(admin.ModelAdmin):
    fieldsets = (
        ['Category Details',{'fields':['Name']}],
    )
    list_display = ('Name',)
    search_fields = ['Name']

#mounir
class PostAdmin(admin.ModelAdmin):
    fieldsets = ( # picture is string [url]
        ['User Details',{'fields':['Title','Picture','Content','Post_category','Date','User_id','Tags']}], #'Likes','Dislikes','Date',
    )
    list_display = ('Title','Picture','Content','Dislikes','Post_category','Date','User_id') #'Date',

#mostafa
class PostlikeAdmin(admin.ModelAdmin):
    fieldsets = (
        ['User Details',{'fields':['Islike','Isdislike','Post_id','User_id']}],
    )
    list_display = ('Islike','Isdislike','Post_id','User_id')

#muhab
class WordAdmin(admin.ModelAdmin):
    fieldsets = (
        ['Category Details',{'fields':['Name']}],
    )
    list_display = ('Name',)
    search_fields = ['Name']

#muhab
class CommentAdmin(admin.ModelAdmin):
    fieldsets = (
        ['User Details',{'fields':['Text','Post_id','User_id']}], #'Time',
    )
    list_display = ('Text','Post_id','User_id') #'Time',

    """admin page
    that take (the table,custom display)
    """
#noura
admin.site.register(Category,CategoryAdmin)
#yostos
admin.site.register(Tag,TagAdmin)
#mounir
admin.site.register(Post,PostAdmin)
#mostafa
admin.site.register(Postlike,PostlikeAdmin)
#muhab
admin.site.register(Word,WordAdmin)
#muhab
admin.site.register(Comment,CommentAdmin)

admin.site.register(CategoryMembership)