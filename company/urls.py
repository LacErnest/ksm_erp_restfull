from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from company import views
from django.conf.urls import url

# Les URL des API sont déterminées automatiquement par le routeur.
urlpatterns = [
    path('', views.api_root),
    path('users/', views.UserList.as_view(), name='company_user-list'),
    path('users/<int:pk>/', views.UserDetail.as_view(), name='company_user-detail'),
    path('users/<int:id>/companies', views.UserCompanies.as_view(), name="user_companies"),
    path('companies/', views.CompanyList.as_view(), name='companies-list'),
    path('companies/<uuid:pk>/', views.CompanyDetail.as_view(), name='companies-detail'),
    path('structures/', views.StructureList.as_view(), name='structures-list'),
    path('structures/<uuid:pk>/', views.StructureDetail.as_view(), name='structures-detail'),
    path('services/', views.ServiceList.as_view(), name='services-list'),
    path('services/<uuid:pk>/', views.ServiceDetail.as_view(), name='services-detail'),
    path('equipment_types/', views.EquipmentTypeList.as_view(), name='equipment_types-list'),
    path('equipment_types/<uuid:pk>/', views.EquipmentTypeDetail.as_view(), name='equipment_types-detail'),
    path('equipements/', views.EquipmentList.as_view(), name='equipements-list'),
    path('equipements/<uuid:pk>/', views.EquipmentDetail.as_view(), name='equipements-detail'),
    path('company_partnership_types/', views.CompanyPartnerTypeList.as_view(), name='company_partnership_types-list'),
    path('company_partnership_types/<uuid:pk>/', views.CompanyPartnerTypeDetail.as_view(), name='company_partnership_types-detail'),
    path('company_partners/', views.CompanyPartnerList.as_view(), name='company_partners-list'),
    path('company_partners/<uuid:pk>/', views.CompanyPartnerDetail.as_view(), name='company_partners-detail'),
    path('functions/', views.FunctionList.as_view(), name='functions-list'),
    path('functions/<uuid:pk>/', views.FunctionDetail.as_view(), name='functions-detail'),
    path('employees/', views.EmployeeList.as_view(), name='employees-list'),
    path('employees/<uuid:pk>/', views.EmployeeDetail.as_view(), name='employees-detail'),
    path('contracts/', views.ContractList.as_view(), name='contracts-list'),
    path('contracts/<uuid:pk>/', views.ContractDetail.as_view(), name='contracts-detail'),
    path('responsabilities/', views.ResponsabilityList.as_view(), name='responsabilities-list'),
    path('responsabilities/<uuid:pk>/', views.ResponsabilityDetail.as_view(), name='responsabilities-detail'),
    path('employee_responsabilities/', views.EmployeeResponsabilityList.as_view(), name='employee_responsabilities-list'),
    path('employee_responsabilities/<uuid:pk>/', views.EmployeeResponsabilityDetail.as_view(), name='employee_responsabilities-detail'),
    path('restraints/', views.RestraintList.as_view(), name='restraints-list'),
    path('restraints/<uuid:pk>/', views.RestraintDetail.as_view(), name='restraints-detail'),
    path('employee_restraints/', views.EmployeeRestraintList.as_view(), name='employee_restraints-list'),
    path('employee_restraints/<uuid:pk>/', views.EmployeeRestraintDetail.as_view(), name='employee_restraints-detail'),
    path('grades/', views.GradeList.as_view(), name='grades-list'),
    path('grades/<uuid:pk>/', views.GradeDetail.as_view(), name='grades-detail'),
    path('indexes/', views.IndexList.as_view(), name='indexes-list'),
    path('indexes/<uuid:pk>/', views.IndexDetail.as_view(), name='indexes-detail'),
    path('basic_salaries/', views.BasicSalaryList.as_view(), name='basic_salaries-list'),
    path('basic_salaries/<uuid:pk>/', views.BasicSalaryDetail.as_view(), name='basic_salaries-detail'),
    path('staff_salaries/', views.StaffSalaryList.as_view(), name='staff_salaries-list'),
    path('staff_salaries/<uuid:pk>/', views.StaffSalaryDetail.as_view(), name='staff_salaries-detail'),
    path('promotions/', views.PromotionList.as_view(), name='promotions-list'),
    path('promotions/<uuid:pk>/', views.PromotionDetail.as_view(), name='promotions-detail'),
] 

urlpatterns = format_suffix_patterns(urlpatterns)