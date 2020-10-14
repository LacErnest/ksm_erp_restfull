from rest_framework import serializers
from rest_framework.serializers import ListSerializer
from rest_framework.reverse import reverse
from company.models import *
from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework_bulk import BulkListSerializer, BulkSerializerMixin
from phone_field import PhoneField

class CompanySerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='companies-detail')
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Company
        fields = ['url', 'id', 'user', 'name', 'founding_date', 'web_site', 'head_office_address', 'mail_address_one', 
                    'mail_address_two', 'telephone_one', 'telephone_two', 'economic_sphere', 'sales_turnover', 'number_of_employees', 
                    'sizing_and_economic_impact', 'business_sector', 'business_line', 'legal_form', 'company_s_object', 'mission', 'history', 
                    'description', 'created_at', 'update_at']
        read_only_fields = ['created_at', 'update_at', 'id', 'user', 'number_of_employees']
                    
class StructureSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='structures-detail')
    user = serializers.ReadOnlyField(source='user.username')
    encompassing_structure = serializers.SlugRelatedField(many=False, queryset=Company.objects.all(), slug_field='name', label="Compagnie  associée")
    direct_top_structure = serializers.SlugRelatedField(many=False, allow_null=True, required=False, queryset=Structure.objects.all(), slug_field='name', label="Structure directement supérieure")

    class Meta:
        model = Structure
        fields = ['url', 'id', 'user', 'name', 'web_site', 'adresse', 'legal_position', 'type_structure', 'latitude', 'longitude', 'town_name', 
                    'country_name', 'mainland_name', 'description', 'encompassing_structure', 'direct_top_structure', 
                    'created_at', 'update_at']
        read_only_fields = ['created_at', 'update_at', 'id', 'user']
        extra_kwargs = {'direct_top_structure':{'view_name':'structures-detail'},
            'encompassing_structure':{'view_name':'companies-detail'}}

class ServiceSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='services-detail')
    user = serializers.ReadOnlyField(source='user.username')
    structure = serializers.SlugRelatedField(many=False, queryset=Structure.objects.all(), slug_field='name', label="Structure  associée")

    class Meta:
        model = Service
        fields = ['url', 'id', 'user', 'code', 'label', 'mission', 'description', 'count_equipment', 'number_employee', 'structure', 'created_at', 'update_at']
        read_only_fields = ['created_at', 'update_at', 'id', 'user', 'count_equipment', 'number_employee']

class EquipmentTypeSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='equipment_types-detail')
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = EquipmentType
        fields = ['url', 'id', 'user', 'code', 'label', 'count_type', 'description', 'created_at', 'update_at']
        read_only_fields = ['created_at', 'update_at', 'id', 'user', 'count_type']

class EquipmentSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='equipements-detail')
    user = serializers.ReadOnlyField(source='user.username')
    equipment_type = serializers.SlugRelatedField(many=False, queryset=EquipmentType.objects.all(), slug_field='code', label="Type d'équipement associé")
    service = serializers.SlugRelatedField(many=False, queryset=Service.objects.all(), slug_field='label', label="Service associé")

    class Meta:
        model = Equipment 
        fields = ['url', 'id', 'user', 'code', 'label', 'vesting_date', 'expiry_date', 
            'description', 'equipment_type', 'service', 'created_at', 'update_at']
        read_only_fields = ["created_at", "update_at", "id", "user"]

    def validate(self, data):
        """
        Vérification que la date d'expiration n'est pas inferieur ou egale a la date d'acquisition
        """
        if data['expiry_date'] <= data['vesting_date']:
                raise serializers.ValidationError("The vesting date cannot be later than the expiry date.")
        return data

class CompanyPartnerTypeSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='company_partnership_types-detail')
    user = serializers.ReadOnlyField(source='user.username')
    
    class Meta:
        model = CompanyPartnerType
        fields = ['url', 'id', 'user', 'code', 'label', 'description', 'created_at', 'update_at']

class CompanyPartnerSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='company_partners-detail')
    user = serializers.ReadOnlyField(source='user.username')
    partner_type = serializers.SlugRelatedField(many=False, queryset=CompanyPartnerType.objects.all(), slug_field='label', label="Type de partenariat associé")
    
    class Meta:
        model = CompanyPartner
        fields = ['url', 'id', 'user', 'name', 'matricule', 'state', 'photo', 'social_reason', 'juridical_form', 'society', 'description', 'family', 
                    'city', 'country', 'creation_date', 'partner_type', 'created_at', 'update_at']
        read_only_fields = ["created_at", "update_at", "id", "user"]
        extra_kwargs = {'partner_type':{'view_name':'company_partnership_types-detail'}}

class FunctionSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='functions-detail')
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Function
        fields = ['url', 'id', 'user','label', 'description', 'number_employee', 'created_at', 'update_at']
        read_only_fields = ['created_at', 'update_at', 'id', 'user', 'number_employee']

class EmployeeSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='employees-detail')
    user = serializers.ReadOnlyField(source='user.username')
    grade = serializers.SlugRelatedField(many=False, queryset=Grade.objects.all(), slug_field='label', label="Grade associé")
    index = serializers.SlugRelatedField(many=False, queryset=Index.objects.all(), slug_field='value', label="Index associé")
    service = serializers.SlugRelatedField(many=False, queryset=Service.objects.all(), slug_field='label', label="Service associé")
    function = serializers.SlugRelatedField(many=False, queryset=Function.objects.all(), slug_field='label', label="Fonction associée")

    class Meta:
        model = Employee
        fields = ['url', 'id', 'user', 'matricule', 'name', 'surname', 'birth_date', 'birth_place', 'nationality', 'sex', 'no_cni', 
                    'mail_address', 'phone', 'curriculum_vitae', 'grade', 'index', 'service', 'function', 'created_at', 'update_at']
        read_only_fields = ['created_at', 'update_at', 'id', 'user']

class ContractSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='contracts-detail')
    user = serializers.ReadOnlyField(source='user.username')
    structure = serializers.SlugRelatedField(many=False, queryset=Structure.objects.all(), slug_field='name', label="Structure associée")
    employee = serializers.SlugRelatedField(many=False, queryset=Employee.objects.all(), slug_field='matricule', label="Employé associé")
    partner = serializers.SlugRelatedField(many=False, queryset=CompanyPartner.objects.all(), slug_field='name', label="Partenaire associé")

    class Meta:
        model = Contract
        fields = ['url', 'id', 'user','entry_date', 'signing_date', 'start_date', 'end_date', 'type_contract', 'renewable', 'state', 
                    'created_at', 'update_at', 'structure', 'employee', 'partner']
        read_only_fields = ["created_at", "update_at", "id", "user"]

class ResponsabilitySerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='responsabilities-detail')
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Responsability
        fields = ['url', 'id', 'user', 'code', 'label', 'percentage_bonus', 'value_amount_or_percentage', 'description', 
                    'created_at', 'update_at']
        read_only_fields = ["created_at", "update_at", "id", "user"]

    def validate(self, data):
        """
        Cette méthode nous permet de vérifier que le type de prime correspond à sa valeur
        """
        if data['percentage_bonus'] == 'YES':
            if data['value_amount_or_percentage'] > 100:
                raise ValidationError("This value must be less than 100 because you have chosen the deduction expressed as a %.")
        return data

class EmployeeResponsabilitySerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='employee_responsabilities-detail')
    user = serializers.ReadOnlyField(source='user.username')
    employee = serializers.SlugRelatedField(many=False, queryset=Employee.objects.all(), slug_field='matricule', label="Employé associé")
    responsability = serializers.SlugRelatedField(many=False, queryset=Responsability.objects.all(), slug_field='label', label="Responsabilité concerné")

    class Meta:
        model = EmployeeResponsability
        fields = ['url', 'id', 'user', 'state', 'grant_date', 'suspension_date', 'created_at', 'update_at', 'employee', 'responsability']
        read_only_fields = ["created_at", "update_at", "id", "user"]

class RestraintSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='restraints-detail')
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Restraint
        fields = ['url', 'id', 'user', 'code', 'label', 'percentage_deduction', 'value_amount_or_percentage', 'description', 
                    'created_at', 'update_at']
        read_only_fields = ['created_at', 'update_at', 'id', 'user']

        def validate(self, data):
            """
            Cette méthode nous permet de vérifier que le type de retenue correspond à sa valeur
            """
            if data['percentage_deduction'] == 'YES':
                if data['value_amount_or_percentage'] > 100:
                    raise ValidationError("This value must be less than 100 because you have chosen the deduction expressed as a %.")
            return data

class EmployeeRestraintSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='employee_restraints-detail')
    user = serializers.ReadOnlyField(source='user.username')
    employee = serializers.SlugRelatedField(many=False, queryset=Employee.objects.all(), slug_field='matricule', label="Employé associé")
    restraint = serializers.SlugRelatedField(many=False, queryset=Restraint.objects.all(), slug_field='label', label="Element de retenu concerné")

    class Meta:
        model = EmployeeRestraint
        fields = ['url', 'id', 'user', 'state', 'submission_date', 'suspension_date', 'description', 'created_at', 'update_at',
                    'employee', 'restraint']
        read_only_fields = ["created_at", "update_at", "id", "user"]
        extra_kwargs = {'employee':{'view_name':'employees-detail'}, 'restraint':{'view_name':'restraints-detail'}}

class GradeSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='grades-detail')
    user = serializers.ReadOnlyField(source='user.username')
    next_higher_grade = serializers.SlugRelatedField(many=False, allow_null=True, required=False, queryset=Grade.objects.all(), slug_field='label', label="Grade directement supérieur")

    class Meta:
        model = Grade
        fields = ['url', 'id', 'user', 'label', 'description', 'number_employee', 'created_at', 'update_at', 'next_higher_grade']
        read_only_fields = ['created_at', 'update_at', 'id', 'user', 'number_employee']
        extra_kwargs = {'next_higher_grade':{'view_name':'grades-detail'}}

class IndexSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='indexes-detail')
    user = serializers.ReadOnlyField(source='user.username')
    grade = serializers.SlugRelatedField(many=False, queryset=Grade.objects.all(), slug_field='label', label="Grade concerné")

    class Meta:
        model = Index
        fields = ['url', 'id', 'user', 'value', 'number_employee', 'created_at', 'update_at', 'grade']
        read_only_fields = ['created_at', 'update_at', 'id', 'user', 'number_employee']

class BasicSalarySerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='basic_salaries-detail')
    user = serializers.ReadOnlyField(source='user.username')
    grade = serializers.SlugRelatedField(many=False, queryset=Grade.objects.all(), slug_field='label', label="Grade concerné")
    index = serializers.SlugRelatedField(many=False, queryset=Index.objects.all(), slug_field='value', label="Index concerné")

    class Meta:
        model = BasicSalary
        fields = ['url', 'id', 'user', 'amount', 'created_at', 'update_at', 'grade', 'index']
        read_only_fields = ['created_at', 'update_at', 'id', 'user']

class StaffSalarySerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='staff_salaries-detail')
    user = serializers.ReadOnlyField(source='user.username')
    premium_accrual = serializers.DecimalField(max_digits=22, decimal_places=2, required=False, allow_null=True, label="Montant cumulé des primes")
    accumulated_deductions = serializers.DecimalField(max_digits=22, decimal_places=2, required=False, allow_null=True, label="Montant cumulé des déductions")
    employee = serializers.SlugRelatedField(many=False, queryset=Employee.objects.all(), slug_field='matricule', label="Employé associé")
    
    class Meta:
        model = StaffSalary
        fields = ['url', 'id', 'user', 'premium_accrual', 'accumulated_deductions', 'amount_due', 'created_at', 'update_at', 'employee', 'basic_salary']
        read_only_fields = ['created_at', 'update_at', 'id', 'user', 'amount_due']
        extra_kwargs = {'basic_salary':{'view_name':'basic_salaries-detail'}}

class PromotionSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='promotions-detail')
    user = serializers.ReadOnlyField(source='user.username')
    employee = serializers.SlugRelatedField(many=False, queryset=Employee.objects.all(), slug_field='matricule', label="Employé concerné")
    grade = serializers.SlugRelatedField(many=False, queryset=Grade.objects.all(), slug_field='label', label="Grade concerné")
    index = serializers.SlugRelatedField(many=False, queryset=Index.objects.all(), slug_field='value', label="Index concerné")
    service = serializers.SlugRelatedField(many=False, queryset=Service.objects.all(), slug_field='label', label="Service concerné")
    function = serializers.SlugRelatedField(many=False, queryset=Function.objects.all(), slug_field='label', label="Fonction concernée")

    class Meta:
        model = Promotion
        fields = ['url', 'id', 'user', 'promotion_date', 'created_at', 'update_at', 'employee', 'grade', 'index', 'service', 'function']
        read_only_fields = ['created_at', 'update_at', 'id', 'user']

class UserSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='company_user-detail')
    user_companies = serializers.HyperlinkedIdentityField(view_name='user_companies', lookup_field='id')

    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active', 'is_superuser', 'user_companies']
