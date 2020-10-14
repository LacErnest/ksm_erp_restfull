from django.urls import path, include
from rest_framework.routers import DefaultRouter
from product import views
from django.conf import settings
from django.conf.urls.static import static

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'languages', views.LanguageViewSet)
router.register(r'categories', views.CategoryViewSet)
router.register(r'category_descriptions', views.CategoryDescriptionViewSet)
router.register(r'conditionings', views.ConditioningViewSet)
router.register(r'product_descriptions', views.ProductDescriptionViewSet)
router.register(r'products', views.ProductViewSet)
router.register(r'taxes', views.TaxViewSet)
router.register(r'product_taxations', views.ProductTaxationViewSet)
router.register(r'product_packagings', views.ProductPackagingViewSet)
router.register(r'pricing', views.PricingViewSet)
router.register(r'product_details', views.ProductDetailViewSet)
router.register(r'product_illustrations', views.ProductIllustrationViewSet)


urlpatterns = [
    # Les URL des API sont déterminées automatiquement par le routeur.
    path('', include(router.urls)),
    # URL personnalisées.
    path('languages/<uuid:id>/products', views.ListOfProductsDescribedInALanguage.as_view(), name="list_of_products_described_in_a_language"),
    path('languages/<uuid:id>/categories', views.ListOfCategoriesDescribedInALanguage.as_view(), name="list_of_categories_described_in_a_language"),
    path('categories/<uuid:id>/products', views.ListOfProductsInACategory.as_view(), name="list_of_products_in_a_category"),
    path('categories/<uuid:id>/subcategories', views.ListOfSubcategories.as_view(), name="list_of_subcategories"),
    path('categories/<uuid:id>/category_descriptions', views.ListOfCategoryDescriptions.as_view(), name="list_of_category_descriptions"),
    path('categories/<uuid:id>/category_descriptions/<str:code>', views.DescriptionOfACategoryInALanguage.as_view(), name="description_of_a_category_in_a_language"),
    path('products/<uuid:id>/taxes', views.ProductTaxList.as_view(), name="product_taxes_list"),
    path('products/<uuid:id>/category', views.ProductCategory.as_view(), name="product_category"),
    path('products/<uuid:id>/detail', views.ProductDetail.as_view(), name="product_detail"),
    path('products/<uuid:id>/pricing/', views.ProductPricing.as_view(), name="product_pricing"),
    path('products/<uuid:id>/product_illustrations', views.ProductIllustrationList.as_view(), name="product_illustration_list"),
    path('products/<uuid:id>/product_descriptions', views.ProductDescriptionList.as_view(), name="product_description_list"),
    path('products/<uuid:id>/conditionnings', views.ProductPackagingList.as_view(), name="product_packagings_list"),
    path('products/<uuid:id>/product_descriptions/<str:code>', views.ProductDescriptionInOneLanguage.as_view(), name="Product_description_in_one_language"),
    path('taxes/<uuid:id>/products', views.TaxedProducts.as_view(), name="taxed_products"),
    path('conditionings/<uuid:id>/products', views.PackagedProducts.as_view(), name="packaged_products"),
    path('search/products/', views.SearchProduct.as_view(), name="search_product"),
    path('search/categories/', views.SearchCategory.as_view(), name="search_category"),
    path('search/taxes/', views.SearchTax.as_view(), name="search_tax"),
    path('search/users/', views.SearchUser.as_view(), name="search_user_product"),
    path('users/<int:id>/products', views.UserProducts.as_view(), name="user_products"),
    path('users/', views.UserList.as_view(), name='product_user-list'),
    path('users/<int:pk>/', views.UserDetail.as_view(), name='product_user-detail'),
    path('registered/languages', views.RegisteredLanguage.as_view(), name="registered_languages"),
    path('registered/categories', views.RegisteredCategory.as_view(), name="registered_categories"),
    path('registered/category_descriptions', views.RegisteredCategoryDescription.as_view(), name="registered_category_descriptions"),
    path('registered/conditionings', views.RegisteredConditioning.as_view(), name="registered_conditionings"),
    path('registered/product_descriptions', views.RegisteredProductDescription.as_view(), name="registered_product_descriptions"),
    path('registered/products', views.RegisteredProduct.as_view(), name="registered_products"),
    path('registered/taxes', views.RegisteredTax.as_view(), name="registered_taxes"),
    path('registered/product_taxations', views.RegisteredProductTaxation.as_view(), name="registered_product_taxations"),
    path('registered/product_packagings', views.RegisteredProductPackaging.as_view(), name="registered_product_packagings"),
    path('registered/pricing', views.RegisteredPricing.as_view(), name="registered_pricing"),
    path('registered/product_details', views.RegisteredProductDetail.as_view(), name="registered_product_details"),
    path('registered/product_illustrations', views.RegisteredProductIllustration.as_view(), name="registered_product_illustrations"),
]
