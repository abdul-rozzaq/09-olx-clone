from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=256)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self) -> str:
        return self.name


class Announcement(models.Model):
    owner = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    title = models.CharField(max_length=256)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.PositiveIntegerField()

    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ("pk",)

    def __str__(self):
        return f"{self.owner} - {self.title}"


class AnnouncementImage(models.Model):
    ann = models.ForeignKey(Announcement, on_delete=models.CASCADE, related_name='images')

    image = models.ImageField(upload_to="images/")
