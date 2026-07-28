from apps.articles.dto.article_dto import ArticleInDTO, ArticleOutDTO
from apps.articles.selectors.article_selector import AtricleSelector
from apps.articles.repositories.article_repo import ArticleRepo




class ArticleService:


    def __init__(self,**kwargs):
        super().__init__(**kwargs)

        self._selector= AtricleSelector()
        self._repositopy = ArticleRepo()


    def get_all_article(self,user_id:int)->ArticleOutDTO:
        return self._selector.get_all_article(user_id)
    

    def create(self,dto:ArticleInDTO,user_id:int)->ArticleOutDTO:
        ...


