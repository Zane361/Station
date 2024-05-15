from django.db import models
from random import sample
import string
import os

class CodeGenerate(models.Model):
    code = models.CharField(max_length=255, blank=True,unique=True)
    
    @staticmethod
    def generate_code():
        return ''.join(sample(string.ascii_letters + string.digits, 15)) 
    

    def save(self, *args, **kwargs):
        if not self.id:
            while True:
                code = self.generate_code()
                if not self.__class__.objects.filter(code=code).count():
                    self.code = code
                    break
        super(CodeGenerate,self).save(*args, **kwargs)

    class Meta:
        abstract = True

class Type(CodeGenerate):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    

class Station(CodeGenerate):
    name = models.CharField(max_length=255)
    description = models.TextField()
    lat = models.FloatField()
    lng = models.FloatField()
    banner = models.ImageField(upload_to='banner/')
    start_time = models.TimeField()
    end_time = models.TimeField()
    
    def __str__(self):
        return self.name
    
    def delete(self, *args, **kwargs):
        if self.banner:
            file_path = self.banner.path
            if os.path.exists(file_path):
                os.remove(file_path)
        super(Station, self).delete(*args, **kwargs)


class StationImage(CodeGenerate):
    station = models.ForeignKey(Station, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='station-images/')

    def __str__(self):
        return self.station.name
    
    def delete(self, *args, **kwargs):
        if self.image:
            file_path = self.image.path
            if os.path.exists(file_path):
                os.remove(file_path)
        super(StationImage, self).delete(*args, **kwargs)

    
class TypeOfStation(CodeGenerate):
    type = models.ForeignKey(Type, on_delete=models.CASCADE)
    station = models.ForeignKey(Station, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        something = TypeOfStation.objects.filter(type=self.type, station=self.station)
        if something.count() == 0:
            super(TypeOfStation, self).save(*args, **kwargs)
        else:
            raise ValueError('Bu turdagi shahobcha allaqachon mavjud')
    

