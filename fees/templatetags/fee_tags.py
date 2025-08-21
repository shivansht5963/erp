from django import template
from fees.models import FeePayment

register = template.Library()

@register.simple_tag(takes_context=True)
def get_fee_summary(context, student):
    """
    Template tag to get the fee summary for a student.
    Usage in template: {% get_fee_summary student as fee_summary %}
    """
    return FeePayment.get_student_fee_summary(student)

@register.filter
def get_fee_status(amount_due, total_fees):
    """
    Determine the fee status based on amount due and total fees.
    Returns: 'paid', 'partial', or 'unpaid'
    """
    if amount_due <= 0:
        return 'paid'
    elif amount_due < total_fees:
        return 'partial'
    return 'unpaid'
