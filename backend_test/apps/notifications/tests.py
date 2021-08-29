from django.test import TestCase

# Create your tests here.
def fuct(x):
    return x+5

def test_method():
    assert fuct(3) == 8