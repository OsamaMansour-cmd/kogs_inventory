from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    def __str__(self):
        return self.name

class Location(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField(blank=True)
    def __str__(self):
        return self.name

class Tool(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('checked_out', 'Checked Out'),
        ('maintenance', 'Under Maintenance'),
        ('lost', 'Lost'),
    ]
    name = models.CharField(max_length=200)
    serial_number = models.CharField(max_length=100, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='tools')
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, related_name='tools')
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    purchase_date = models.DateField(null=True, blank=True)
    value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    image = models.ImageField(upload_to='tool_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.name} ({self.serial_number})"

class Attachment(models.Model):
    tool = models.ForeignKey(Tool, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='attachments/')
    description = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Attachment for {self.tool.name}"

class Employee(models.Model):
    """Represents tool users (linked to Django user for auth)"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=150)
    role = models.CharField(max_length=50, choices=[('admin','Admin'), ('technician','Technician'), ('viewer','Viewer')], default='technician')
    phone = models.CharField(max_length=30, blank=True)
    department = models.CharField(max_length=100, blank=True)
    def __str__(self):
        return self.full_name

class CheckOut(models.Model):
    tool = models.ForeignKey(Tool, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)
    checked_out_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField(null=True, blank=True)
    remarks = models.TextField(blank=True)
    def __str__(self):
        return f"{self.tool.name} checked out by {self.employee.full_name}"

class CheckIn(models.Model):
    tool = models.ForeignKey(Tool, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)
    checked_in_at = models.DateTimeField(auto_now_add=True)
    remarks = models.TextField(blank=True)
    def __str__(self):
        return f"{self.tool.name} checked in by {self.employee.full_name}"

class Maintenance(models.Model):
    tool = models.ForeignKey(Tool, on_delete=models.CASCADE, related_name='maintenance_logs')
    description = models.TextField()
    scheduled_date = models.DateField(null=True, blank=True)
    completed_date = models.DateField(null=True, blank=True)
    performed_by = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    remarks = models.TextField(blank=True)
    def __str__(self):
        return f"Maintenance for {self.tool.name}"

class AuditLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=100)
    tool = models.ForeignKey(Tool, on_delete=models.SET_NULL, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.TextField(blank=True)
    def __str__(self):
        return f"{self.timestamp}: {self.action} by {self.user}"
