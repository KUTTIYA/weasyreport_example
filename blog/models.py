from django.db import models

class Blog(models.Model):
    name = models.CharField(max_length=100)
    tagline = models.TextField()

    def __str__(self):
        return self.name

class Author(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()

    def __str__(self):
        return self.name

class Entry(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    headline = models.CharField(max_length=255)
    body_text = models.TextField()
    pub_date = models.DateField()
    mod_date = models.DateField()
    authors = models.ManyToManyField(Author)
    number_of_comments = models.IntegerField()
    number_of_pingbacks = models.IntegerField()
    rating = models.IntegerField()

    def __str__(self):
        return self.headline

class MasterPart(models.Model):
    part_id = models.AutoField(primary_key=True, auto_created=True, serialize=False, editable=False)
    customer_code = models.TextField(verbose_name='Customer Code')
    project_code = models.TextField(verbose_name='Project Code')
    supplier_code = models.TextField(verbose_name='Supplier Code')
    part_no = models.TextField(verbose_name='Part No')
    part_name = models.TextField(verbose_name='Part Name', blank=True)
    snp = models.IntegerField(verbose_name='Snp', blank=True)
    image = models.TextField(verbose_name='Image', blank=True)
    status = models.TextField(verbose_name='Status')
    model = models.TextField(verbose_name='Model')
    remark = models.TextField(verbose_name='Remark', blank=True)
    updated_by = models.TextField(verbose_name='Updated By')
    updated_timestamp = models.DateTimeField(verbose_name='Updated Timestamp', auto_now_add=True, blank=True)