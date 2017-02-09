from django.test import TestCase
from django.db import connections

import requests

from .forms import Index_Form
from .views import reset_database
from .models import Fs_database
from django.conf import settings
from foursquare_request import Foursquare_Req


# Create your tests here.

class ProjectTestCase(TestCase):

    def test_is_valid_form(self):
        'form is not valid'  # print this text if the test fails.
        form_data = {'objct':'pizza', 'location':'Antalya'}  # instance of the form fields
        form = Index_Form(data=form_data)
        self.assertTrue(form.is_valid())  # test if the form is valid

    def test_invalid_form(self):
        'form is valid'
        form_data = {'objct':'', 'location':'Antalya'}  # instance of the form fields
        form = Index_Form(data=form_data)
        self.assertFalse(form.is_valid())  # test if the form is valid

    def test_foursquare_api_query(self):
        'foursquare api does not work fine'
        form_data = {'objct':'pizza', 'location':'Antalya'}
        fs = Foursquare_Req(client_id = getattr(settings, 'FS_CLIENT_ID', None),  # (6)
                            client_secret = getattr(settings, 'FS_CLIENT_SECRET', None),
                            version = getattr(settings, 'FS_VERSION', None))

        result = fs.veneus (form_data['objct'], form_data['location'])
        self.assertEqual(result['response']['venues'][0]['location']['city'], 'Antalya')
        self.assertEqual(result['meta']['code'], 200)

    def test_database_is_empty(self):
        'delete function doesnt work properly'
        reset_database()
        db_objects = Fs_database.objects.all()
        self.assertFalse(db_objects.exists())
