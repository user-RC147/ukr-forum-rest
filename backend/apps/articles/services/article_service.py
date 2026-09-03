from apps.articles.dto.article_dto import ArticleInDTO, ArticleOutDTO,UserShortOutDTO
from apps.articles.selectors.article_selector import AtricleSelector
from apps.articles.repositories.article_repo import ArticleRepo

from apps.users.contracts.user_contract import get_user_short_contract

from core.func_print import prt


class ArticleService:


    def __init__(self,**kwargs):
        super().__init__(**kwargs)

        self._selector= AtricleSelector()
        self._repositopy = ArticleRepo()


    def get_all_article(self,user_id:int|None)->list[ArticleOutDTO]:

        articles = self._selector.get_all_article(user_id=None)

        user_ids = {user.created_by_id for user in articles}
        users = get_user_short_contract().get_many(user_ids)

        prt(users)


        dto = _to_dto_article_out(articles,users)
        prt(dto)

        return dto
    

    def create(self,dto:ArticleInDTO,user_id:int)->ArticleOutDTO:
        ...



def _to_dto_article_out(data,users) -> list[ArticleOutDTO]:

    return [ArticleOutDTO(
        id=article.id,
        title=article.title,
        description=article.description,
        date_create=article.date_create,
        date_edit=article.date_edit,
        created_by=UserShortOutDTO(
            id=users[article.created_by_id].id,
            display_name=users[article.created_by_id].display_name,
        )
    )for article in data]