from django import forms
from .models import Property, Broker, City, MicroMarket

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['google_location', 'broker', 'parcel_size_acres', 'price_per_acre', 'city', 'micro_market']

        broker = forms.ModelChoiceField(queryset=Broker.objects.all())
        city = forms.ModelChoiceField(queryset=City.objects.all())
        micro_market = forms.ModelChoiceField(queryset=MicroMarket.objects.all())

class BrokerForm(forms.ModelForm):
    class Meta:
        model = Broker
        fields = ['name', 'contact_info']

class CityForm(forms.ModelForm):
    class Meta:
        model = City
        fields = ['name']

class MicroMarketForm(forms.ModelForm):
    class Meta:
        model = MicroMarket
        fields = ['name', 'city']