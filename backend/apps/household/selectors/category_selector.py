from apps.household.models.category import Category



class CategorySelector:

    def get_all_category(self):
        categories = Category.objects.all()
        return categories