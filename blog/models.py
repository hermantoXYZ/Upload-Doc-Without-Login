from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor.fields import RichTextField
from taggit.managers import TaggableManager
from django.urls import reverse

STATUS = (
    (0, "Draft"),
    (1, "Publish")
)


class Kategori(models.Model):
    kategori = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.kategori

    def get_absolute_url(self):
        return reverse('kategori_show', args=[str(self.kategori)])


class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    updated_on = models.DateTimeField(auto_now=True)
    content = RichTextUploadingField(blank=True, null=True)
    kategori = models.ForeignKey(Kategori, on_delete=models.CASCADE, related_name='blog_kategori')
    tags = TaggableManager()
    banner = models.ImageField(upload_to='banner_pics', blank=True)
    meta_deskripsi = models.TextField(null=True, verbose_name='Caption')
    meta_keyword = models.CharField(max_length=200, unique=False, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    is_headline = models.BooleanField(default=False)  # New field to indicate if it's a headline

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.urls import reverse

        return reverse("post_detail", kwargs={"slug": str(self.slug)})


class Dokumen(models.Model):
    STATUS_CHOICES = [
        ('belum', 'Belum Terverifikasi'),
        ('terverifikasi', 'Terverifikasi'),
    ]

    PROGRAM_PENDIDIKAN_CHOICES = [
        ('SMP', 'SMP'),
        ('SMA', 'SMA'),
    ]

    nama = models.CharField(max_length=200)
    document = models.FileField(upload_to='user_documents/')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_documents', null=True, blank=True)
    program_pendidikan = models.CharField(max_length=3, choices=PROGRAM_PENDIDIKAN_CHOICES, default='SMP')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='belum')

    def __str__(self):
        return self.nama

    def status_display(self):
        return dict(self.STATUS_CHOICES)[self.status]
