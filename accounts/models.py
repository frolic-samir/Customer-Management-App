from django.db import models

# Create your models here.
class Customer(models.Model):
  name = models.CharField(max_length=200,null=True)
  email = models.EmailField()
  contact = models.CharField(max_length=15)
  created_date = models.DateTimeField()
  
  def __str__(self):
    return self.name

class Tag(models.Model):
  name=models.CharField(max_length=200)
  
  def __str__(self):
    return self.name
    
class Product(models.Model):
  CHOICE=(
    ('Indoor','Indoor'),
    ('Outdoor','Outdoor')
    )
  name=models.CharField(max_length=200)
  price=models.FloatField()
  catogary = models.CharField(max_length=200, choices=CHOICE)
  added_date=models.DateTimeField(auto_now=True)
  tag = models.ManyToManyField(Tag)
  
  def __str__(self):
    return self.name
    
class Order(models.Model):
  STATUS=(
    ('Pending','Pending'),
    ('Sent','Sent'),
    ('Delivered','Delivered')
    )
  customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
  product = models.ForeignKey(Product,on_delete=models.CASCADE)
  status= models.CharField(max_length=200,choices=STATUS)
  created_date=models.DateTimeField(auto_now_add=True)