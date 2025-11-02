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

class Method(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name

class Ingridient(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    availability = models.BooleanField(default=False)
    cost = models.IntegerField(default=100)
    alcohol_perc = models.IntegerField(default=1)
    count = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class Cocktail(models.Model):
    name = models.CharField(max_length=200)
    alcohol = models.ForeignKey(Alcohol, blank=True, on_delete=models.CASCADE)
    taste = models.ForeignKey(Taste, blank=True, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, blank=True, on_delete=models.CASCADE)
    method = models.ForeignKey(Method, blank=True, on_delete=models.CASCADE, default=1)
    cost = models.IntegerField(default=1)
    comment = models.CharField(max_length=400, default='Это коктейль')
    img = models.ImageField(upload_to='media/', default='media/default.jpg')
    alcohol_perc = models.IntegerField(default=1)

    def __str__(self):
        return self.name

class Ingridient_Cost(models.Model):
    ingridient_id = models.ForeignKey(Ingridient, on_delete=models.CASCADE)
    cocktail_id = models.ForeignKey(Cocktail, on_delete=models.CASCADE)
    value = models.IntegerField(default=1)

class Bill(models.Model):
    timestamp = models.DateTimeField()
    cock_name = models.CharField(max_length=30)
    cost = models.IntegerField()
    client = models.CharField(max_length=20, default='anon')
