from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ('name', )
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class Item(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    treatment = models.TextField(blank=True, null=True)
    img_url = models.TextField(blank=True, null=True)
    specialist = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name