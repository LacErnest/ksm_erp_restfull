from django.core.exceptions import ValidationError

def validate_name(value): 
    """Cette méthode nous permet de vérifier que la longueur d'une chaine de caractere est supérieure à 6"""
    if len(value) < 6:
        raise ValidationError("This value must be greater than 6 characters")
