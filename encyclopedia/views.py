from django.shortcuts import render
import markdown
from markdown2 import Markdown
from django.http import HttpResponseRedirect
from django import forms
from django.urls import reverse
from django.shortcuts import redirect
import random


from . import util

# django form with fields to add newPage or edit
class NewPageForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput, label="Title")
    content = forms.CharField(widget=forms.Textarea, label="Content") 
   
# index page to list entries
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

# entry page convert markdown files to html 
def entry(request, title):
    title = util.get_entry(title)
    
    if title is not None:
        title = Markdown().convert(title)
        return render(request, "encyclopedia/entry.html",{ "title": title})
    else: 
        return render(request,"encyclopedia/error.html",{"title": title,"error": "Entry was not found"})
 
# search entries from nav bar   
def search(request): 
    entries = util.list_entries()
    x = request.GET.get("q","")
    if x is None:
       return HttpResponseRedirect(x)
    else:
       results = [entry for entry in entries if x.lower() in entry.lower()]
       return render(request, "encyclopedia/search.html", {"entries": results})

# newPage form, save and add to entries list in index
def newPage(request):
    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']  
            content = form.cleaned_data['content']
            util.save_entry(title,content)
            return HttpResponseRedirect(reverse('index'))
    else:
        return render(request, "encyclopedia/newPage.html", {"form": NewPageForm()})

# edit entries with newpage form and save   
def edit(request,title):
    getEntry = util.get_entry(title)
    
    if getEntry is  None:
        return render(request,"encyclopedia/error.html",{
            "title":title,
            "title": "Edit Error"
        })
    else:
         form = NewPageForm()
         form.fields['title'].initial = title
         form.fields['content'].initial = getEntry
         return render(request, "encyclopedia/edit.html",{
            "form":form,
            "titles":form.fields['title'].initial
        })
# save entry after edit         
def save(request):
    form = NewPageForm(request.POST)
       
    if form.is_valid():
            title = form.cleaned_data['title']  
            content = form.cleaned_data['content']
            util.save_entry(title=title,content=content)
            return HttpResponseRedirect(reverse('index'))
    else:
        return render(request, "encyclopedia/newPage.html", {"form": NewPageForm()})

# random entry link 
def randomEntry(request):
    return render(request,"encyclopedia/randomEntry.html",{
        "entry": random.choice(util.list_entries())
        })