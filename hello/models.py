from django.db import models


class Image(models.Model):
    id = models.AutoField(primary_key=True)
    file = models.FileField(upload_to='images/')
    width = models.IntegerField()
    height = models.IntegerField()
    channels = models.CharField(max_length=10)

    def __str__(self):
        return f'{self.id} - {self.file} ({self.width}, {self.height}, {self.channels})'


class Pdf(models.Model):
    id = models.AutoField(primary_key=True)
    file = models.FileField(upload_to='pdfs/')
    title = models.CharField(max_length=255, blank=True)
    author = models.CharField(max_length=255, blank=True)
    num_pages = models.IntegerField()
    page_width = models.IntegerField()
    page_height = models.IntegerField()


    def __str__(self):
        return f'{self.id} - {self.file} - {self.title} - {self.author} - {self.num_pages} - ({self.page_width}, {self.page_height})'
