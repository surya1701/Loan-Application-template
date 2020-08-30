from django.test import TestCase

# Create your tests here.
from .models import Prediction


class TestModel(TestCase):
    def test_page_is_created_successfully(self):
        pred = Prediction(
            uname="Testf",
            gender="Testl",
            married="Yes",
            depend="2",
            education="Graduate",
            self_employ="Yes",
            aincome=100,
            caincome=100,
            loanamt=10,
            loanterm=10,
            credhist=1,
            area="Rural",
            pred="Y"
        )
        pred.save()
