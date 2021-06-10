from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django import forms
from django.urls.base import reverse
import random
import secrets
import markdown2
from . import util

def random(request):
    entries = util.list_entries()
    print(entries)
    entry = secrets.choice(entries)
    print(entry)
    str = "/wiki/"
    str = str + entry
    return HttpResponseRedirect(str)


def edit(request, name):
    if request.method == "POST":
        value = request.POST
        content = value["content"]
        title = name
        util.save_entry(title, content)
        str = "/wiki/"
        str = str + title
        return HttpResponseRedirect(str)
    else:
        if util.get_entry(name):
            return render(request, "encyclopedia/edit.html", {
                "content": util.get_entry(name),
                "title": name
            })
        else:
            return render(request, "encyclopedia/error.html",{
                "title": name
            })


def create(request):
    if request.method == "POST":
        values = request.POST
        title = values["title"]
        content = values["content"]
        print(values)
        print(title, content)
        if util.get_entry(title):
            return render(request, "encyclopedia/error.html",{
            "title": title
        })
        else:
            util.save_entry(title, content)
            str = "/wiki/"
            str = str + title
            return HttpResponseRedirect(str)
    return render(request, "encyclopedia/create.html")
def index(request):
    if request.method == "POST":
        res = {}
        print(util.list_entries())
        for entry in util.list_entries():
            res[entry] = [entry[i: j].lower() for i in range(len(entry))
          for j in range(i + 1, len(entry) + 1)]
        print(res)
        values = request.POST
        value = values['q']
        print(value)
        for key, v in res.items():
            print(key, v)
            if value.lower() in v:
                print("came here")
                str = "/wiki/"
                str = str + key
                return HttpResponseRedirect(str)
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def wiki(request, name):
    
    # markdown2.markdown(util.get_entry(name))  # or use `html = markdown_path(PATH)`
    # u'<p><em>boo!</em></p>\n'

    # from markdown2 import Markdown
    # markdowner = Markdown()
    # markdowner.convert("*boo!*")
    # u'<p><em>boo!</em></p>\n'
    # markdowner.convert("**boom!**")
    # u'<p><strong>boom!</strong></p>\n'

    if util.get_entry(name):
        return render(request, "encyclopedia/wiki.html", {
            "wiki": markdown2.markdown(util.get_entry(name)),
            "title": name
        })
    else:
        return render(request, "encyclopedia/error.html",{
            "title": name
        })

