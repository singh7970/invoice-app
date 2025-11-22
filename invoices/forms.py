from django import forms
from django.forms import inlineformset_factory
from .models import Invoice, LineItem, Sender, Client, Product

class SenderForm(forms.ModelForm):
    class Meta:
        model = Sender
        fields = '__all__'
        widgets = {'address': forms.Textarea(attrs={'rows': 3})}

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'
        widgets = {'address': forms.Textarea(attrs={'rows': 3})}

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = [
            'sender_name', 'sender_address', 'sender_state', 'sender_gstin',
            'client_name', 'client_address', 'client_state', 'client_gstin',
            'invoice_number', 'invoice_date', 'is_gst_applicable'
        ]
        widgets = {
            'invoice_date': forms.DateInput(attrs={'type': 'date'}),
            'sender_address': forms.Textarea(attrs={'rows': 3}),
            'client_address': forms.Textarea(attrs={'rows': 3}),
        }

LineItemFormSet = inlineformset_factory(
    Invoice, LineItem,
    fields=['description', 'quantity', 'rate', 'tax_rate'],
    extra=1,
    can_delete=True
)
