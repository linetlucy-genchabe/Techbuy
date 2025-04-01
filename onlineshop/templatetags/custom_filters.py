from django import template

register = template.Library()

@register.filter
def currency_kes(value):
    """Format number as Kenyan Shillings (KES)"""
    try:
        return f"KES {float(value):,.2f}"
    except (ValueError, TypeError):
        return "KES 0.00"