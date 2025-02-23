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
    path('profile/', views.profile, name='profile'),
    path('download-income-report/', views.download_income_report, name='download_income_report'),
    path('download-expense-report/', views.download_expense_report, name='download_expense_report'),
    path('download-comparative-report/', views.download_comparative_report, name='download_comparative_report'),
    path("send_test_email/", views.send_test_email, name="send_test_email"),
    path('investments/', views.investment_dashboard, name='investment'),
    path('investments/fd/add/', views.add_fixed_deposit, name='add_fd'),
    path('investments/fd/edit/<int:pk>/', views.edit_fixed_deposit, name='edit_fd'),
    path('investments/fd/delete/<int:pk>/', views.delete_fixed_deposit, name='delete_fd'),
    path('investments/fd/<int:pk>/', views.fixed_deposit_detail, name='fd_detail'),
    path('investments/stock/add/', views.add_stock, name='add_stock'),
    path('investments/stock/edit/<int:pk>/', views.edit_stock, name='edit_stock'),
    path('investments/stock/delete/<int:pk>/', views.delete_stock, name='delete_stock'),
    path('investments/stock/<int:pk>/', views.stock_detail, name='stock_detail'),
    path('calculator/', views.calculate_emi, name='calculate_emi'),
    path('__debug__/', include('debug_toolbar.urls')),

]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)