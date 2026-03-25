from django.core.exceptions import ValidationError

def validate_ico_png(image):
    if not image.name.lower().endswith(('.ico', '.png')):
        raise ValidationError('A imagem deve ser em formato .ico ou .png')