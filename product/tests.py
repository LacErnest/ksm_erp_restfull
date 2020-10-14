from django.test import TestCase

from .models import *
from django.contrib.auth.models import User
#test du model Language
class TestModelLanguage(TestCase):
    # -initialisation du test ddu model Language
    def setUp(self):
        user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        self.language_default = Language.objects.create(
            user = user,
            code="Fr-fr",
            name="Francais",
            is_default="OUI"
        )
        self.language = Language.objects.create(
            user = user,
            code="En-en",
            name="Anglais",
            is_default="NON"
        )

    # -creer une langue simple
    def test_language(self):
        self.assertEqual(self.language.__class__.__name__, 'Language')
    
    # -creer la langue par défaut
    def test_language_default(self):
        self.assertEqual(self.language_default.__class__.__name__,'Language')

#test du model Category
class TestModelCategory(TestCase):
    # -initialisation du test du model Category
    def setUp(self):
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        self.category = Category.objects.create(
            user = self.user,
            name="Electronique",
            image="https://bit.ly/3dvUuzu"
        )

    # -verifier la creation de la categorie
    def test_category(self):
        self.assertEqual(self.category.__class__.__name__, 'Category')

    # -mise à jour du champ category_parent avec sa propre clée primaire
    def test_category_parent_with_its_primary_key(self):
        self.category.category_parent = self.category
        self.category.save()
        self.assertEqual(self.category.category_parent, self.category)
    
    # -creer une sous categorie
    def test_category_child(self):
        category_child = Category.objects.create(
            user = self.user,
            name="Telephone",
            image="https://bit.ly/3fxaOBN",
            category_parent = self.category
        )
        self.assertEqual(category_child.__class__.__name__, 'Category')

#test du model CategoryDescription
class TestModelCategoryDescription(TestCase):
    # -initialisation du test du model CategoryDescription
    def setUp(self):
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        language = Language.objects.create(
            user=self.user,
            code="En-en",
            name="Anglais",
            is_default="NON"
        )
        category = Category.objects.create(
            user=self.user,
            name="Electronique",
            image="https://bit.ly/3dvUuzu"
        )
        self.category_description = CategoryDescription.objects.create(
            user=self.user,
            specification="Description en anglais de la categorie Electronique",
            description="Toutes les informations",
            language = language,
            category  = category
        )

    # -verifier la creation de la description d'une categorie
    def test_category_description(self):
        self.assertEqual(self.category_description.__class__.__name__, 'CategoryDescription')

# test du model Conditioning
class TestModelConditioning(TestCase):
    # -initialisation du test du model Conditioning
    def setUp(self):
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        self.conditioning = Conditioning.objects.create(
            user = self.user,
            name = "Palette de jus 1.5 litre",
            description ="Toutes autres informations",
            quantity = 6
        )

    # -verifier la creation de la description d'une categorie
    def test_conditioning(self):
        self.assertEqual(self.conditioning.__class__.__name__, 'Conditioning')

# test du model Product
class TestModelProduct(TestCase):
    # -initialisation du test du model Product
    def setUp(self):
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        conditioning = Conditioning.objects.create(
            user = self.user,
            name = "Emballage smartphone",
            description ="Toutes autres informations",
            quantity = 1
        )
        category = Category.objects.create(
            user = self.user,
            name="Electronique",
            image="https://bit.ly/3dvUuzu"
        )

        self.product = Product.objects.create(
            user = self.user, 
            code = "0001TA",
            name = "Top Ananas",
            conditioning_purchase = conditioning,
            conditioning_sale = conditioning,
            category = category
        )
    
    # -verifier la creation d'un produit
    def test_product(self):
        self.assertEqual(self.product.__class__.__name__, 'Product')

# test du model ProductDescription
class TestModelProductDescription(TestCase):
    # -initialisation du test du model ProductDescription
    def setUp(self):
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        conditioning = Conditioning.objects.create(
            user = self.user,
            name = "Emballage smartphone",
            description ="Toutes autres informations",
            quantity = 1
        )
        category = Category.objects.create(
            user = self.user,
            name = "Electronique",
            image = "https://bit.ly/3dvUuzu"
        )
        product = Product.objects.create(
            user = self.user,
            code = "0001TA",
            name = "Itel Hive2",
            conditioning_purchase = conditioning,
            conditioning_sale = conditioning,
            category = category
        )
        language = Language.objects.create(
            user = self.user,
            code="En-en",
            name="Anglais",
            is_default="NON"
        )

        self.product_description = ProductDescription.objects.create(
            user = self.user,
            specification="Description en anglais du produit Itel Hive2",
            description="Toutes les informations",
            language = language,
            product  = product
        )

    # -verifier la creation de la description d'un produit
    def test_product_description(self):
        self.assertEqual(self.product_description.__class__.__name__, 'ProductDescription')


# test du model Tax
class TestModelTax(TestCase):
    # -initialisation du test du model Tax
    def setUp(self):
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        self.tax = Tax.objects.create(
            user = self.user,
            name = "Taxe sur valeur ajouté",
            value=19.5
        )
    
    # -verifier la creation d'une taxe
    def test_tax(self):
        self.assertEqual(self.tax.__class__.__name__, 'Tax')
        
# test du model ProductTaxation
class TestModelProductTaxation(TestCase):
    # -initialisation du test du model ProductTaxation
    def setUp(self):
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        conditioning = Conditioning.objects.create(
            user = self.user,
            name = "Emballage smartphone",
            description ="Toutes autres informations",
            quantity = 1
        )
        category = Category.objects.create(
            user = self.user,
            name="Electronique",
            image="https://bit.ly/3dvUuzu"
        )
        product = Product.objects.create(
            user = self.user,
            code = "0001TA",
            name = "Itel Hive2",
            conditioning_purchase = conditioning,
            conditioning_sale = conditioning,
            category = category
        )
        tax = Tax.objects.create(
            user = self.user,
            name = "Taxe sur valeur ajouté",
            value=19.5
        )

        self.product_taxation = ProductTaxation.objects.create(
            user = self.user,
            product = product,
            tax = tax
        )

    # -verifier la creation de l'association d'une taxe et d'un produit
    def test_product_taxation(self):
        self.assertEqual(self.product_taxation.__class__.__name__, 'ProductTaxation')

# test du model Pricing
class TestModelPricing(TestCase):
    # -initialisation du test du model Pricing
    def setUp(self):
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        conditioning = Conditioning.objects.create(
            user = self.user,
            name = "Emballage smartphone",
            description ="Toutes autres informations",
            quantity = 1
        )
        category = Category.objects.create(
            user = self.user,
            name="Electronique",
            image="https://bit.ly/3dvUuzu"
        )
        product = Product.objects.create(
            user = self.user,
            code = "0001TA",
            name = "Itel Hive2",
            conditioning_purchase = conditioning,
            conditioning_sale = conditioning,
            category = category
        )

        self.pricing = Pricing.objects.create(
            user = self.user,
            average_price = 10,
            cost_price = 10,
            unit_pricing = 10, 
            percentage_expence = 10,
            percentage_margin_rate = 10,
            percentage_brand_taxes = 10,
            half_wholesale_price = 10,
            wholesale_price = 10,
            percentage_half_big_price = 10,
            percentage_wholesale_price = 10,
            total_accumulated_price = 10,
            type_pricing = "SALE",
            product = product
        )

    # -verifier la creation de la tarification d'un produit 
    def test_pricing(self):
        self.assertEqual(self.pricing.__class__.__name__, 'Pricing')

# test du model ProductDetail
class TestModelProductDetail(TestCase):
    # -initialisation du test du model ProductDetail
    def setUp(self):
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        conditioning = Conditioning.objects.create(
            user = self.user,
            name = "Emballage smartphone",
            description ="Toutes autres informations",
            quantity = 1
        )
        category = Category.objects.create(
            user = self.user,
            name="Electronique",
            image="https://bit.ly/3dvUuzu"
        )
        product = Product.objects.create(
            user = self.user,
            code = "0001TA",
            name = "Itel Hive2",
            conditioning_purchase = conditioning,
            conditioning_sale = conditioning,
            category = category
        )

        self.product_detail = ProductDetail.objects.create(
            user = self.user,
            model = "Notebook",
            mark = "Itel",
            weight = 500,
            conservation = "Kg",
            origin = "Japon, Taiwan",
            composition = "Processeur *64, Ecran CLD",
            product = product
        )

    # -verifier la creation du detail d'un produit 
    def test_product_detail(self):
        self.assertEqual(self.product_detail.__class__.__name__, 'ProductDetail')
    
# test du model ProductIllustration
class TestModelProductIllustration(TestCase):
    # -initialisation du test du model ProductIllustration
    def setUp(self):
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        conditioning = Conditioning.objects.create(
            user = self.user,
            name = "Emballage smartphone",
            description ="Toutes autres informations",
            quantity = 1
        )
        category = Category.objects.create(
            user = self.user,
            name="Electronique",
            image="https://bit.ly/3dvUuzu"
        )
        product = Product.objects.create(
            user = self.user,
            code = "0001TA",
            name = "Itel Hive2",
            conditioning_purchase = conditioning,
            conditioning_sale = conditioning,
            category = category
        )

        self.product_illustration = ProductIllustration.objects.create(
            user = self.user,
            image = "https://bit.ly/3dvUuzu",
            video = "https://bit.ly/3dvUuzu",
            product = product
        )

    # -verifier la creation de l'illustration d'un produit 
    def test_product_illustration(self):
        self.assertEqual(self.product_illustration.__class__.__name__, 'ProductIllustration')

