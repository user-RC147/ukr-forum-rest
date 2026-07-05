from apps.household.selectors.category_selector import CategorySelector



class CategoryService:

    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self._selector = CategorySelector()


    def get_all_category(self):
        categories = self._selector.get_all_category()

        return categories