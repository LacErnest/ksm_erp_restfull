from .models import *
from .serializers import *
from .permissions import *
from rest_framework import generics, filters, permissions, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework_bulk import ListBulkCreateAPIView, BulkCreateAPIView
from rest_framework.views import APIView
from django.db.models import Q, ProtectedError
from rest_framework.exceptions import APIException

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def api_root(request, format=None):
    """
    Page d'acceuil de WiCoNet's APIs COMPANY
    """
    return Response({
        'users': reverse('company_user-list', request=request, format=format),
        'companies': reverse('companies-list', request=request, format=format),
        'structures': reverse('structures-list', request=request, format=format),
        'services': reverse('services-list', request=request, format=format),
        'equipment_types': reverse('equipment_types-list', request=request, format=format),
        'equipements': reverse('equipements-list', request=request, format=format),
        'company_partnership_types': reverse('company_partnership_types-list', request=request, format=format),
        'company_partners': reverse('company_partners-list', request=request, format=format),
        'functions': reverse('functions-list', request=request, format=format),
        'employees': reverse('employees-list', request=request, format=format),
        'contracts': reverse('contracts-list', request=request, format=format),
        'responsabilities': reverse('responsabilities-list', request=request, format=format),
        'employee_responsabilities': reverse('employee_responsabilities-list', request=request, format=format),
        'restraints': reverse('restraints-list', request=request, format=format),
        'employee_restraints': reverse('employee_restraints-list', request=request, format=format),
        'grades': reverse('grades-list', request=request, format=format),
        'indexes': reverse('indexes-list', request=request, format=format),
        'basic_salaries': reverse('basic_salaries-list', request=request, format=format),
        'staff_salaries': reverse('staff_salaries-list', request=request, format=format),
        'promotions': reverse('promotions-list', request=request, format=format),
    })

class CompanyList(generics.ListCreateAPIView):
    """
    Ce generics fournit  les actions `list`, `create` pour les compagnies
    """
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['user__username', 'economic_sphere', 'sizing_and_economic_impact', 'business_sector', 'business_line', 
        'legal_form', 'company_s_object']
    search_fields = ['user__username', 'name', 'head_office_address', 'founding_date', 'business_line', 
        'sizing_and_economic_impact', 'economic_sphere', 'business_sector', 'legal_form', 'company_s_object']
    ordering_fields = ['founding_date', 'created_at']
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        try:
            serializer.save(user=self.request.user)
        except IntegrityError as err:
            raise APIException(
                code=502,
                detail="Integrity error: {0}".format(err), 
            )

class CompanyDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Ce viewset fournit  les actions  `retrieve`,`update` et `destroy` pour les compagnies
    """
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsUserOrReadOnly]

    def perform_destroy(self, instance):
        try:
            instance.delete()
        except ProtectedError as err:
            raise APIException(
                code=502,
                detail="Protected error: {0}".format(err)
            )

class StructureList(generics.ListCreateAPIView):
    """
    Ce generics fournit  les actions `list`, `create` pour les structures
    """
    queryset = Structure.objects.all()
    serializer_class = StructureSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['user__username', 'type_structure', 'town_name', 'country_name', 'mainland_name', 'encompassing_structure__name']
    search_fields = ['user__username', 'name', 'type_structure', 'town_name', 'country_name', 'mainland_name', 'encompassing_structure__name']
    ordering_fields = ['created_at']
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class StructureDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Ce viewset fournit  les actions  `retrieve`,`update` et `destroy` pour les structures
    """
    queryset = Structure.objects.all()
    serializer_class = StructureSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsUserOrReadOnly]

    def perform_destroy(self, instance):
        try:
            instance.delete()
        except ProtectedError as err:
            raise APIException(
                code=502,
                detail="Protected error: {0}".format(err)
            )

class ServiceList(generics.ListCreateAPIView):
    """
    Ce generics fournit  les actions `list`, `create` pour les services
    """
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['user__username', 'structure__name']
    search_fields = ['user__username', 'label', 'code', 'structure__name']
    ordering_fields = ['created_at']
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ServiceDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Ce viewset fournit  les actions  `retrieve`,`update` et `destroy` pour les services 
    """
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsUserOrReadOnly]

    def perform_destroy(self, instance):
        try:
            instance.delete()
        except ProtectedError as err:
            raise APIException(
                code=502,
                detail="Protected error: {0}".format(err)
            )

class EquipmentTypeList(generics.ListCreateAPIView):
    """
    Ce generics fournit  les actions `list`, `create` pour les types d'équipements 
    """
    queryset = EquipmentType.objects.all()
    serializer_class = EquipmentTypeSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['user__username']
    search_fields = ['user__username', 'label', 'code']
    ordering_fields = ['created_at', 'order']
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class EquipmentTypeDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Ce viewset fournit  les actions  `retrieve`,`update` et `destroy` pour les les types d'équipements 
    """
    queryset = EquipmentType.objects.all()
    serializer_class = EquipmentTypeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsUserOrReadOnly]

    def perform_destroy(self, instance):
        try:
            instance.delete()
        except ProtectedError as err:
            raise APIException(
                code=502,
                detail="Protected error: {0}".format(err)
            )
        
class EquipmentList(generics.ListCreateAPIView):
    """
    Ce generics fournit  les actions `list`, `create` pour les équipements
    """
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['user__username', 'vesting_date', 'expiry_date', 
        'equipment_type__label', 'service__label']
    search_fields = ['user__username', 'label', 'code', 'vesting_date', 
        'equipment_type__label', 'service__label']
    ordering_fields = ['expiry_date', 'vesting_date', 'created_at']
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        try:
            serializer.save(user=self.request.user)
        except IntegrityError as err:
            raise APIException(
                code=502,
                detail="Integrity error: {0}".format(err), 
            )

class EquipmentDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Ce viewset fournit  les actions  `retrieve`,`update` et `destroy` pour les équipements
    """
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsUserOrReadOnly]

    def perform_destroy(self, instance):
        try:
            instance.delete()
        except ProtectedError as err:
            raise APIException(
                code=502,
                detail="Protected error: {0}".format(err)
            )

class CompanyPartnerTypeList(generics.ListCreateAPIView):
    """
    Ce generics fournit  les actions `list`, `create` pour les types de partenariat
    """
    queryset = CompanyPartnerType.objects.all()
    serializer_class = CompanyPartnerTypeSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['user__username']
    search_fields = ['user__username', 'label', 'code']
    ordering_fields = ['created_at']
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CompanyPartnerTypeDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Ce viewset fournit  les actions  `retrieve`,`update` et `destroy` pour les types de partenariat
    """
    queryset = CompanyPartnerType.objects.all()
    serializer_class = CompanyPartnerTypeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsUserOrReadOnly]

    def perform_destroy(self, instance):
        try:
            instance.delete()
        except ProtectedError as err:
            raise APIException(
                code=502,
                detail="Protected error: {0}".format(err)
            )         

class CompanyPartnerList(generics.ListCreateAPIView):
    """
    Ce generics fournit  les actions `list`, `create` pour les partenaires
    """
    queryset = CompanyPartner.objects.all()
    serializer_class = CompanyPartnerSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['user__username', 'city', 'country', 'partner_type__label']
    search_fields = ['user__username', 'name', 'matricule', 'social_reason', 'juridical_form', 
        'society', 'partner_type__label', 'creation_date']
    ordering_fields = ['creation_date']
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CompanyPartnerDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Ce viewset fournit  les actions  `retrieve`,`update` et `destroy` pour les partenaires 
    """
    queryset = CompanyPartner.objects.all()
    serializer_class = CompanyPartnerSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsUserOrReadOnly]

    def perform_destroy(self, instance):
        try:
            instance.delete()
        except ProtectedError as err:
            raise APIException(
                code=502,
                detail="Protected error: {0}".format(err)
            )

class FunctionList(generics.ListCreateAPIView):
    """
    Ce generics fournit  les actions `list`, `create` pour les fonctions
    """
    queryset = Function.objects.all()
    serializer_class = FunctionSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['user__username']
    search_fields = ['user__username', 'label']
    ordering_fields = ['created_at']
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class FunctionDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Ce viewset fournit  les actions  `retrieve`,`update` et `destroy` pour les fonctions
    """
    queryset = Function.objects.all()
    serializer_class = FunctionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsUserOrReadOnly]

    def perform_destroy(self, instance):
        try:
            instance.delete()
        except ProtectedError as err:
            raise APIException(
                code=502,
                detail="Protected error: {0}".format(err)
            )
 
class EmployeeList(generics.ListCreateAPIView):
    """
    Ce generics fournit  les actions `list`, `create` pour les employés
    """
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['user__username', 'sex', 'birth_place', 'nationality', 'grade__label', 
        'service__label', 'function__label']
    search_fields = ['user__username', 'name', 'surname', 'no_cni', 'birth_date', 'birth_place', 
        'nationality', 'grade__label', 'service__label', 'function__label']
    ordering_fields = ['created_at']
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class EmployeeDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Ce viewset fournit  les actions  `retrieve`,`update` et `destroy` pour les employés
    """
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsUserOrReadOnly]

    def perform_update(self, serializer):
        try:
            serializer.save()
        except IntegrityError as err:
            raise APIException(
                code=502,
                detail="Integrity error: {0}".format(err), 
            )

    def perform_destroy(self, instance):
        try:
            instance.delete()
        except ProtectedError as err:
            raise APIException(
                code=502,
                detail="Protected error: {0}".format(err)
            )
            
class ContractList(generics.ListCreateAPIView):
    """
    Ce generics fournit  les actions `list`, `create` pour les contrats
    """
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['user__username', 'structure__name', 'type_contract', 'renewable', 'state']
    search_fields = ['user__username', 'structure__name', 'employee__name', 'partner__name', 'type_contract']
    ordering_fields = ['created_at', 'signing_date']
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ContractDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Ce viewset fournit  les actions  `retrieve`,`update` et `destroy` pour les contrats
    """
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsUserOrReadOnly]

    def perform_destroy(self, instance):
        try:
            instance.delete()
        except ProtectedError as err:
            raise APIException(
                code=502,
                detail="Protected error: {0}".format(err)
            )
 
class ResponsabilityList(generics.ListCreateAPIView):
    """
    Ce generics fournit  les actions `list`, `create` pour les responsabilités
    """
    queryset = Responsability.objects.all()
    serializer_class = ResponsabilitySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['user__username', 'percentage_bonus']
    search_fields = ['user__username', 'label', 'code']
    ordering_fields = ['created_at']
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ResponsabilityDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Ce viewset fournit  les actions  `retrieve`,`update` et `destroy` pour les responsabilités
    """
    queryset = Responsability.objects.all()
    serializer_class = ResponsabilitySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsUserOrReadOnly]

    def perform_destroy(self, instance):
        try:
            instance.delete()
        except ProtectedError as err:
            raise APIException(
                code=502,
                detail="Protected error: {0}".format(err)
            )

class EmployeeResponsabilityList(generics.ListCreateAPIView):
    """
    Ce generics fournit  les actions `list`, `create` pour les reponsabilités des employés
    """
    queryset = EmployeeResponsability.objects.all()
    serializer_class = EmployeeResponsabilitySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['user__username', 'state', 'responsability__label', 'employee__name']
    search_fields = ['user__username', 'grant_date', 'suspension_date', 'responsability__label', 'employee__name']
    ordering_fields = ['grant_date', 'created_at']
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class EmployeeResponsabilityDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Ce viewset fournit  les actions  `retrieve`,`update` et `destroy` pour les reponsabilités des employés
    """
    queryset = EmployeeResponsability.objects.all()
    serializer_class = EmployeeResponsabilitySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsUserOrReadOnly]

    def perform_destroy(self, instance):
        try:
            instance.delete()
        except ProtectedError as err:
            raise APIException(
                code=502,
                detail="Protected error: {0}".format(err)
            )
 
class RestraintList(generics.ListCreateAPIView):
    """
    Ce generics fournit  les actions `list`, `create` pour les retenues
    """
    queryset = Restraint.objects.all()
    serializer_class = RestraintSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['user__username', 'percentage_deduction']
    search_fields = ['user__username', 'code', 'label']
    ordering_fields = ['created_at']
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class RestraintDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Ce viewset fournit  les actions  `retrieve`,`update` et `destroy` pour les retenues
    """
    queryset = Restraint.objects.all()
    serializer_class = RestraintSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsUserOrReadOnly]

    def perform_destroy(self, instance):
        try:
            instance.delete()
        except ProtectedError as err:
            raise APIException(
                code=502,
                detail="Protected error: {0}".format(err)
            ) 
 
class EmployeeRestraintList(generics.ListCreateAPIView):
    """
    Ce generics fournit  les actions `list`, `create` pour les retenues des employés
    """
    queryset = EmployeeRestraint.objects.all()
    serializer_class = EmployeeRestraintSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['user__username', 'state', 'employee__name', 'restraint__label']
    search_fields = ['user__username', 'submission_date', 'suspension_date', 'restraint__label', 'employee__name']
    ordering_fields = ['submission_date', 'suspension_date']
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class EmployeeRestraintDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Ce viewset fournit  les actions  `retrieve`,`update` et `destroy` pour les retenues des employés
    """
    queryset = EmployeeRestraint.objects.all()
    serializer_class = EmployeeRestraintSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsUserOrReadOnly]

    def perform_destroy(self, instance):
        try:
            instance.delete()
        except ProtectedError as err:
            raise APIException(
                code=502,
                detail="Protected error: {0}".format(err)
            )

class GradeList(generics.ListCreateAPIView):
    """
    Ce generics fournit  les actions `list`, `create` pour les grades
    """
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['user__username']
    search_fields = ['user__username', 'label']
    ordering_fields = ['created_at']
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class GradeDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Ce viewset fournit  les actions  `retrieve`,`update` et `destroy` pour les grades
    """
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsUserOrReadOnly]

    def perform_destroy(self, instance):
        try:
            instance.delete()
        except ProtectedError as err:
            raise APIException(
                code=502,
                detail="Protected error: {0}".format(err)
            )

class IndexList(generics.ListCreateAPIView):
    """
    Ce generics fournit  les actions `list`, `create` pour les indices
    """
    queryset = Index.objects.all()
    serializer_class = IndexSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['user__username', 'grade__label']
    search_fields = ['user__username', 'grade__label']
    ordering_fields = ['created_at']
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class IndexDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Ce viewset fournit  les actions  `retrieve`,`update` et `destroy` pour les indices
    """
    queryset = Index.objects.all()
    serializer_class = IndexSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsUserOrReadOnly]

    def perform_destroy(self, instance):
        try:
            instance.delete()
        except ProtectedError as err:
            raise APIException(
                code=502,
                detail="Protected error: {0}".format(err)
            )

class BasicSalaryList(generics.ListCreateAPIView):
    """
    Ce generics fournit  les actions `list`, `create` pour les salaires de base
    """
    queryset = BasicSalary.objects.all()
    serializer_class = BasicSalarySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['user__username', 'grade__label']
    search_fields = ['user__username', 'grade__label']
    ordering_fields = ['created_at']
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class BasicSalaryDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Ce viewset fournit  les actions  `retrieve`,`update` et `destroy` pour les salaires de base
    """
    queryset = BasicSalary.objects.all()
    serializer_class = BasicSalarySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsUserOrReadOnly]

    def perform_destroy(self, instance):
        try:
            instance.delete()
        except ProtectedError as err:
            raise APIException(
                code=502,
                detail="Protected error: {0}".format(err)
            )

class StaffSalaryList(generics.ListCreateAPIView):
    """
    Ce generics fournit  les actions `list`, `create` pour les salaires des employés.
    """
    queryset = StaffSalary.objects.all()
    serializer_class = StaffSalarySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['user__username', 'employee__name']
    search_fields = ['user__username', 'employee__name']
    ordering_fields = ['created_at']
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class StaffSalaryDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Ce viewset fournit  les actions  `retrieve`,`update` et `destroy` pour les salaires des employés.
    """
    queryset = StaffSalary.objects.all()
    serializer_class = StaffSalarySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsUserOrReadOnly]

    def perform_destroy(self, instance):
        try:
            instance.delete()
        except ProtectedError as err:
            raise APIException(
                code=502,
                detail="Protected error: {0}".format(err)
            )
 
class PromotionList(generics.ListCreateAPIView):
    """
    Ce generics fournit  les actions `list`, `create` pour les promotions des employés
    """
    queryset = Promotion.objects.all()
    serializer_class = PromotionSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['user__username', 'grade__label', 'employee__name']
    search_fields = ['user__username', 'grade__label', 'employee__name']
    ordering_fields = ['promotion_date', 'created_at']
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class PromotionDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Ce viewset fournit  les actions  `retrieve`,`update` et `destroy` pour les promotions des employés
    """
    queryset = Promotion.objects.all()
    serializer_class = PromotionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsUserOrReadOnly, UpdatePromotionPermission]

    def perform_destroy(self, instance):
        try:
            instance.delete()
        except ProtectedError as err:
            raise APIException(
                code=502,
                detail="Protected error: {0}".format(err)
            )
 
class UserList(generics.ListAPIView):
    """
    Ce generics fournit  les actions `list` pour les utilisateurs
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['username', 'is_staff', 'is_superuser']
    search_fields = ['username', 'is_staff', 'is_superuser']
    permission_classes = [IsSuperUserAndIsAuthenticated, DeleteUserPermission]

class UserDetail(generics.RetrieveAPIView):
    """
    Ce viewset fournit  l'action  `retrieve` pour les utilisateurs
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsSuperUserAndIsAuthenticated, DeleteUserPermission]
 
class UserCompanies(APIView):
    """
    Retrouver la liste des compagnies enregistrées par un utilisateur.
    """
    permission_classes = [IsSuperUserAndIsAuthenticated]

    def get_object(self, id):
        try:
            return User.objects.get(id=id)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        companies = (self.get_object(id)).companies.all()
        serializer = CompanySerializer(companies, many=True, context={'request': request})
        return Response(serializer.data)