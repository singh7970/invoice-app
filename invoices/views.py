from django.shortcuts import render, redirect, get_object_or_404
import datetime
from .models import Invoice, Sender, Client, Product
from .forms import InvoiceForm, LineItemFormSet, SenderForm, ClientForm, ProductForm

def master_dashboard(request):
    return render(request, 'invoices/master_dashboard.html')

def sender_list(request):
    senders = Sender.objects.all()
    if request.method == 'POST':
        form = SenderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('sender_list')
    else:
        form = SenderForm()
    return render(request, 'invoices/sender_list.html', {'senders': senders, 'form': form})

def client_list(request):
    clients = Client.objects.all()
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('client_list')
    else:
        form = ClientForm()
    return render(request, 'invoices/client_list.html', {'clients': clients, 'form': form})

def product_list(request):
    products = Product.objects.all()
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'invoices/product_list.html', {'products': products, 'form': form})

def create_invoice(request):
    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        formset = LineItemFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            invoice = form.save()
            items = formset.save(commit=False)
            for item in items:
                item.invoice = invoice
                item.save()
            return redirect('invoice_detail', pk=invoice.pk)
    else:
        # Auto-generate Invoice Number
        last_invoice = Invoice.objects.order_by('-id').first()
        if last_invoice:
            try:
                # Try to parse "INV-001" format or just integers
                last_num = int(last_invoice.invoice_number.replace('INV-', ''))
                next_num = f"INV-{last_num + 1:03d}"
            except ValueError:
                # Fallback if format is different
                next_num = f"INV-{Invoice.objects.count() + 1:03d}"
        else:
            next_num = "INV-001"
            
        initial_data = {
            'invoice_number': next_num,
            'invoice_date': datetime.date.today()
        }
        form = InvoiceForm(initial=initial_data)
        formset = LineItemFormSet()
    
    return render(request, 'invoices/invoice_form.html', {
        'form': form,
        'formset': formset,
        'senders': Sender.objects.all(),
        'clients': Client.objects.all(),
        'products': Product.objects.all(),
    })

def invoice_detail(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    items = invoice.items.all()
    
    subtotal = 0
    total_tax = 0
    grand_total = 0
    
    processed_items = []
    
    # Determine Tax Type
    is_inter_state = invoice.sender_state != invoice.client_state
    tax_type = 'IGST' if is_inter_state else 'CGST/SGST'
    
    for item in items:
        amount = item.quantity * item.rate
        tax_amount = 0
        
        if invoice.is_gst_applicable:
            tax_amount = (amount * item.tax_rate) / 100
            
        subtotal += amount
        total_tax += tax_amount
        
        processed_items.append({
            'description': item.description,
            'quantity': item.quantity,
            'rate': item.rate,
            'amount': amount,
            'tax_rate': item.tax_rate,
            'tax_amount': tax_amount
        })
        
    grand_total = subtotal + total_tax
    
    context = {
        'invoice': invoice,
        'items': processed_items,
        'subtotal': subtotal,
        'total_tax': total_tax,
        'grand_total': grand_total,
        'tax_type': tax_type,
        'is_inter_state': is_inter_state,
    }
    
    return render(request, 'invoices/invoice_detail.html', context)
