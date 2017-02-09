from __future__ import absolute_import

from django.shortcuts import render
from django.conf import settings

from .forms import Index_Form
from .models import Fs_database
from .foursquare_request import Foursquare_Req


def index(request):

    f_object = ''  # the one where the user enters the part "What I am looking for .."
    f_location = ''
    fs_result = []
    fs_meta = ''
    error = ''
    searched_dict = []

    if request.method == 'GET':  # from input fields - (1) and (2)
        i_form = Index_Form(data=request.GET)

        if request.GET.get('objct') is not None:  # (7)

            if i_form.is_valid():

                f_object = i_form.cleaned_data['objct']
                f_location = i_form.cleaned_data['location']
            else:
                error = 'Invalid form'

    # if I do not get any f_food at all, that means parameters are still in their initial values
    if f_object is not '':

        (fs, fs_meta) = connect_to_api(fs_meta, f_object, f_location)

        if fs_meta['code'] != 200:  # meta = 200 for successful, 400 for failure
            error = "Unsuccessful data"

        else:
            (fs_result, searched_dict ) = save_to_database(fs, fs_result, searched_dict, f_object, f_location)

    # clear the searched history
    if request.GET.get('delete') == '1':
        reset_database()


    return render(request, "index.html", {'error': error, 'results': fs_result, 'searched_dict': searched_dict})


def connect_to_api(fs_meta, f_object, f_location):
    fs = Foursquare_Req(client_id = getattr(settings, 'FS_CLIENT_ID', None),  # (6)
                        client_secret = getattr(settings, 'FS_CLIENT_SECRET', None),
                        version = getattr(settings, 'FS_VERSION', None))

    fs.veneus(f_object, f_location)
    fs_meta = fs.get_meta()
    return fs, fs_meta


def save_to_database(fs, fs_result, searched_dict, f_object, f_location):
    fs_result = fs.get_places()  # this is keeping the veneus dict
    d = Fs_database(objct = f_object, location = f_location) # same as the INSERT INTO
    d.save()
    last_twenty = Fs_database.objects.all().order_by('-id')[:20]  # take the last 20 search
    searched_dict = last_twenty.values()  # turn it to a array of dictionaries
    return fs_result, searched_dict


def reset_database():
    Fs_database.objects.all().delete()
