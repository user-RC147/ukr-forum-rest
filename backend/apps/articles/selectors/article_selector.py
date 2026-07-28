from apps.articles.dto.article_dto import ArticleOutDTO



class AtricleSelector:

    def get_all_article(self,user_id:int)->ArticleOutDTO:
        ...