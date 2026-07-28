from apps.articles.dto.article_dto import ArticleInDTO, ArticleOutDTO
from apps.articles.models.article_model import Article


class ArticleRepo:

    def create(self, dto: ArticleInDTO, user_id: int) -> ArticleOutDTO:
        ...
