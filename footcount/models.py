from django.db import models


# Create your models here.


class login(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=150)

    class Meta:
        db_table = "login"
    def __str__(self):
        return self.username


class Employees(models.Model):
    emp_id = models.CharField(max_length=50, primary_key=True)
    emp_name = models.CharField(max_length=50)
    emp_mobile = models.CharField(max_length=15)
    emp_address = models.CharField(max_length=100)
    emp_designation = models.CharField(max_length=50)
    emp_photo_path = models.ImageField(upload_to='employees/', null=True, blank=True)

    class Meta:
        db_table = "employee"
    
    def __str__(self):
        return self.emp_name


class Visitors(models.Model):
    vis_id = models.CharField(max_length=50, primary_key=True)
    vis_name = models.CharField(max_length=50, default=None, null=True)
    vis_email = models.EmailField(max_length=100, null=True, default=None)
    vis_type = models.CharField(max_length=50)
    vis_feature_vector = models.CharField(max_length=200)
    vis_photo_path = models.ImageField(upload_to='visitors/', null=True, blank=True)
    vis_photo_file = models.FileField(upload_to='Visitors/', default=None, null=True)

    class Meta:
        db_table = "visitors"

    def __str__(self):
        return self.vis_id


class VisitLog(models.Model):
    log_visit_id = models.AutoField(primary_key = True)
    log_visitor_id = models.ForeignKey(Visitors, on_delete = models.CASCADE)
    log_time_in = models.DateTimeField(null=True)
    log_time_out = models.DateTimeField(null=True)

    class Meta:
        db_table = "visitlog"
    
    def __str__(self):
        return str(self.log_visitor_id)


class EmployeeVisit(models.Model):
    emp_visit_id = models.AutoField(primary_key= True)
    emp_visit_emp_id = models.ForeignKey(Employees, on_delete = models.CASCADE)

    class Meta:
        db_table = "employee_visit"
    
    def __str__(self):
        return self.emp_visit_emp_id


class footcount(models.Model):
    count = models.CharField(null=True, max_length=20)
    month = models.CharField(null=True, max_length=50)

    class Meta:
        db_table = "footcount"

    def __str__(self):
        return self.month