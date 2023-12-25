from django.db import models

class Clients(models.Model):
    name = models.CharField(max_length=200)
    balance = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Alcohol(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Taste(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Group(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Ingridient(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    availability = models.BooleanField(default=False)
    cost = models.IntegerField(default=100)

    def __str__(self):
        return self.name

class Cocktail(models.Model):
    name = models.CharField(max_length=200)
    ingridients = models.ManyToManyField(Ingridient)
    alcohol = models.ForeignKey(Alcohol, blank=True, on_delete=models.CASCADE)
    taste = models.ForeignKey(Taste, blank=True, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, blank=True, on_delete=models.CASCADE)
    cost = models.IntegerField(default=1)
    comment = models.CharField(max_length=400, default='Это коктейль')
    img = models.ImageField(upload_to='media/', default='media/default.jpg')

    def __str__(self):
        return self.name

class Ingridient_Cost(models.Model):
    ingridient_id = models.ForeignKey(Ingridient, on_delete=models.CASCADE)
    cocktail_id = models.ForeignKey(Cocktail, on_delete=models.CASCADE)
    value = models.IntegerField(default=1)