from django.db import models

INDIAN_STATES = [
    ('AN', 'Andaman and Nicobar Islands'),
    ('AP', 'Andhra Pradesh'),
    ('AR', 'Arunachal Pradesh'),
    ('AS', 'Assam'),
    ('BR', 'Bihar'),
    ('CH', 'Chandigarh'),
    ('CT', 'Chhattisgarh'),
    ('DN', 'Dadra and Nagar Haveli and Daman and Diu'),
    ('DL', 'Delhi'),
    ('GA', 'Goa'),
    ('GJ', 'Gujarat'),
    ('HR', 'Haryana'),
    ('HP', 'Himachal Pradesh'),
    ('JK', 'Jammu and Kashmir'),
    ('JH', 'Jharkhand'),
    ('KA', 'Karnataka'),
    ('KL', 'Kerala'),
    ('LA', 'Ladakh'),
    ('LD', 'Lakshadweep'),
    ('MP', 'Madhya Pradesh'),
    ('MH', 'Maharashtra'),
    ('MN', 'Manipur'),
    ('ML', 'Meghalaya'),
    ('MZ', 'Mizoram'),
    ('NL', 'Nagaland'),
    ('OR', 'Odisha'),
    ('PY', 'Puducherry'),
    ('PB', 'Punjab'),
    ('RJ', 'Rajasthan'),
    ('SK', 'Sikkim'),
    ('TN', 'Tamil Nadu'),
    ('TG', 'Telangana'),
    ('TR', 'Tripura'),
    ('UP', 'Uttar Pradesh'),
    ('UT', 'Uttarakhand'),
    ('WB', 'West Bengal'),
]

class Sender(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    state = models.CharField(max_length=2, choices=INDIAN_STATES)
    gstin = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.name

class Client(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    state = models.CharField(max_length=2, choices=INDIAN_STATES)
    gstin = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    description = models.CharField(max_length=255)
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

    def __str__(self):
        return self.description

class Invoice(models.Model):
    # Sender Details
    sender_name = models.CharField(max_length=255)
    sender_address = models.TextField()
    sender_state = models.CharField(max_length=2, choices=INDIAN_STATES)
    sender_gstin = models.CharField(max_length=15, blank=True, null=True)

    # Client Details
    client_name = models.CharField(max_length=255)
    client_address = models.TextField()
    client_state = models.CharField(max_length=2, choices=INDIAN_STATES)
    client_gstin = models.CharField(max_length=15, blank=True, null=True)

    # Invoice Details
    invoice_number = models.CharField(max_length=50)
    invoice_date = models.DateField()
    is_gst_applicable = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Invoice {self.invoice_number} - {self.client_name}"

class LineItem(models.Model):
    invoice = models.ForeignKey(Invoice, related_name='items', on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, help_text="Tax rate in %")

    @property
    def amount(self):
        return self.quantity * self.rate

    def __str__(self):
        return f"{self.description} ({self.quantity} x {self.rate})"
