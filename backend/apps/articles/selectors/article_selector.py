from apps.articles.dto.article_dto import ArticleOutDTO, ArticleIdOutDTO
from apps.articles.models.article_model import Article


class AtricleSelector:

    def get_all_article(self, user_id: int | None) -> list[ArticleOutDTO]:

        articles = Article.objects.all()

        dto = [_to_dto_article(article) for article in articles]

        return dto


def _to_dto_article(data) -> list[ArticleIdOutDTO]:

    return ArticleIdOutDTO(
        id=data.id,
        title=data.title,
        description=data.description,
        date_create=data.date_create,
        date_edit=data.date_edit,
        created_by_id=data.created_by_id,
    )
