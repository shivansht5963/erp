from django.db import migrations, models
import django.utils.timezone

class Migration(migrations.Migration):

    dependencies = [
        ('fees', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='feereminder',
            name='amount_due',
            field=models.DecimalField(
                decimal_places=2,
                default=0,
                help_text='Amount due for payment',
                max_digits=10
            ),
        ),
        migrations.AddField(
            model_name='feereminder',
            name='due_date',
            field=models.DateField(
                default=django.utils.timezone.now,
                help_text='Due date for the payment'
            ),
        ),
    ]
