""" Views of list app. Visitors can view and create lists and listitems. """
from django.shortcuts import render, redirect
from lists.models import Item, List
from django.core.exceptions import ValidationError
from .forms import EMPTY_LIST_ERROR



def home_page(request):
    return render(request, 'home.html')


def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    error = None
    if request.method == 'POST':
        try:
            item = Item(text=request.POST['item_text'], list=list_)
            item.full_clean()
            item.save()
            return redirect(list_)
        except ValidationError:
            error = EMPTY_LIST_ERROR

    return render(request, 'list.html', {'list': list_, 'error': error})


def new_list(request):
    list_ = List.objects.create()
    item = Item(text=request.POST['item_text'], list=list_)
    try:
        item.full_clean()
        item.save()
    except ValidationError:
        if list_.item_set.count() == 0:
            list_.delete()
        error = EMPTY_LIST_ERROR
        return render(request, 'home.html', {'error': error})

    return redirect(list_)
