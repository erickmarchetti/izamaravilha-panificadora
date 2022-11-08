# Generated by Django 4.1.2 on 2022-11-08 16:33

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("categorias", "0002_alter_categoria_id"),
    ]

    operations = [
        migrations.CreateModel(
            name="Produto",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("preco", models.DecimalField(decimal_places=2, max_digits=5)),
                ("nome", models.CharField(max_length=100)),
                ("imagem", models.TextField()),
                ("descricao", models.TextField(null=True)),
                (
                    "categoria",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="produtos",
                        to="categorias.categoria",
                    ),
                ),
            ],
        ),
    ]
