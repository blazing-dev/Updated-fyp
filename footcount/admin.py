from django.contrib import admin
from .models import login
from .models import Employees
from .models import Visitors
from .models import VisitLog
from .models import EmployeeVisit
from .models import footcount

# Register your models here.
admin.site.register(login)
admin.site.register(Employees)
admin.site.register(Visitors)
admin.site.register(VisitLog)
admin.site.register(EmployeeVisit)
admin.site.register(footcount)
