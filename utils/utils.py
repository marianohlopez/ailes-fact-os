def get_color(dias):
    if dias < 30:
        return 'verde'
    elif dias <= 60:
        return 'amarillo'
    else:
        return 'rojo'