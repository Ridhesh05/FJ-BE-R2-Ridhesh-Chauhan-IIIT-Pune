from django.contrib import admin
from django.urls import path,include
from base import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name='home'),
    path('login/', views.log_in, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('expense_add/', views.expense_add, name='expense_add'),  
    path('income_add/',views.income_add,name = 'income_add'),
    path('dashboard/ExpenseTracking.html/',views.expense_trac,name='expense_trac'),
    path('expense/<int:pk>/edit/', views.expense_edit, name='expense_edit'),
    path('expense/<int:pk>/delete/', views.expense_delete, name='expense_delete'),
    path('goal/',views.goal_list,name = 'goal_list'),
    path('goal/add/',views.goal_add,name = 'goal_add'),
    path('goal/<int:pk>/edit/',views.goal_edit,name = 'goal_edit'),
    path('blog/',views.blog_list,name = 'blog'),
    path('predict/',views.predict,name = 'predict'),
    path('profile/', views.profile, name='profile'),
    path('download-income-report/', views.download_income_report, name='download_income_report'),
    path('download-expense-report/', views.download_expense_report, name='download_expense_report'),
    path('download-comparative-report/', views.download_comparative_report, name='download_comparative_report'),
    
    path('__debug__/', include('debug_toolbar.urls')),

]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)