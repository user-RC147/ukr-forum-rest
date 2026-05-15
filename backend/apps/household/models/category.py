from django.db import models


class Category(models.Model):
    """
    Категорія витрат — загальна для всіх користувачів системи.
    Підтримує ієрархію (дерево категорій) через поле parent.
    Керується тільки через Django admin.
    """
    name=models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Назва категорій",
        )
    icon=models.CharField(
        max_length=10,
        blank=True,
        default="",
        verbose_name="Іконка (emoji)",
    )
    is_active=models.BooleanField(
        default=True,
        verbose_name="Активна",
    )
    parent=models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="children",
        verbose_name="Батьківська категорія"
    )

    class Meta:
        db_table="household_category"
        verbose_name="Категорія"
        verbose_name_plural="Категорії"
        ordering=["name"]

    def __str__(self):
        return f"{self.icon} {self.name}".strip()
    

    def get_full_path(self)->str:
        """
        Повертає повний шлях категорії.
        Продукти → Напої → Алкоголь → Віскі
        """
        parts=[self.name]
        current=self
        while current.parent:
            parts.insert(0,current.parent.name)
            current=current.parent
        return " → ".join(parts)
    
    def is_root(self)->bool:
        """Чи є категорія кореневою (без батька)."""
        return self.parent is None
    
    def is_leaf(self)->bool:
        """Чи є категорія листком (без дітей)."""
        return not self.children.exists()