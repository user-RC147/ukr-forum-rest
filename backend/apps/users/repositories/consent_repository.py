from apps.users.models import ConsentText


class ConsentRepository:

    def get_latest(self) -> ConsentText | None:
        return ConsentText.objects.order_by("-created_at").first()


consent_repository = ConsentRepository()
