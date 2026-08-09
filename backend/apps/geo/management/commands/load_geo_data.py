import csv
from decimal import Decimal, InvalidOperation
import gzip
import os

from django.core.management.base import BaseCommand, CommandError

from apps.geo.models.city import CityModel
from apps.geo.models.country import CountryModel
from apps.geo.models.region import RegionModel

# Файли за замовчуванням лежать поруч зі скриптом
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_COUNTRIES = os.path.join(BASE_DIR, "countries.csv.gz")
DEFAULT_REGIONS = os.path.join(BASE_DIR, "regions.csv.gz")
DEFAULT_CITIES = os.path.join(BASE_DIR, "cities.csv.gz")


def open_csv(path):
    """Прозрачно відкриває .csv або .csv.gz"""  # noqa: RUF002
    if path.endswith(".gz"):
        return gzip.open(path, "rt", encoding="utf-8", newline="")
    return open(path, encoding="utf-8", newline="")


class Command(BaseCommand):
    help = (
        "Імпорт країн/регіонів/міст. За замовчуванням бере countries.csv.gz, "  # noqa: RUF001
        "regions.csv.gz, cities.csv.gz поруч зі скриптом. Ідемпотентно: нові "
        "записи створюються, для вже існуючих оновлюється name_ua, якщо в csv "
        "з'явилось непорожнє значення."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "countries_csv",
            type=str,
            nargs="?",
            default=DEFAULT_COUNTRIES,
            help=f"Шлях до countries.csv(.gz) (за замовчуванням: {DEFAULT_COUNTRIES})",
        )
        parser.add_argument(
            "regions_csv",
            type=str,
            nargs="?",
            default=DEFAULT_REGIONS,
            help=f"Шлях до regions.csv(.gz) (за замовчуванням: {DEFAULT_REGIONS})",
        )
        parser.add_argument(
            "cities_csv",
            type=str,
            nargs="?",
            default=DEFAULT_CITIES,
            help=f"Шлях до cities.csv(.gz) (за замовчуванням: {DEFAULT_CITIES})",
        )
        parser.add_argument(
            "--batch-size",
            type=int,
            default=5000,
            help="Розмір пачки для bulk_create/bulk_update (за замовчуванням 5000)",
        )

    def handle(self, *args, **options):
        batch_size = options["batch_size"]

        country_by_code, id_country_to_code = self._load_countries(
            options["countries_csv"], batch_size
        )
        region_by_api_id = self._load_regions(
            options["regions_csv"], country_by_code, id_country_to_code, batch_size
        )
        self._load_cities(
            options["cities_csv"],
            country_by_code,
            id_country_to_code,
            region_by_api_id,
            batch_size,
        )

        self.stdout.write(self.style.SUCCESS("Готово!"))

    def _read_rows(self, path):
        try:
            f = open_csv(path)
        except FileNotFoundError:
            raise CommandError(f"Файл не знайдено: {path}")
        with f:
            yield from csv.DictReader(f)

    @staticmethod
    def _clean_ua(row):
        return (row.get("name_ua") or "").strip()

    def _load_countries(self, path, batch_size):
        existing_by_code = {c.code: c for c in CountryModel.objects.all()}
        to_create = []
        to_update = []
        id_country_to_code = {}

        for row in self._read_rows(path):
            code = row["iso2"]
            id_country_to_code[row["id_country"]] = code
            if not code:
                continue

            name_ua = self._clean_ua(row)

            existing = existing_by_code.get(code)
            if existing is not None:
                if name_ua and existing.name_ua != name_ua:
                    existing.name_ua = name_ua
                    to_update.append(existing)
                continue

            obj = CountryModel(
                name=row["country"],
                code=code,
                flag_emoji=row.get("emoji") or "",
                currency=row.get("currency") or "",
                name_ua=name_ua,
            )
            to_create.append(obj)
            existing_by_code[code] = obj  # щоб не задублювати в межах файлу

        CountryModel.objects.bulk_create(to_create, batch_size=batch_size)
        if to_update:
            CountryModel.objects.bulk_update(
                to_update, ["name_ua"], batch_size=batch_size
            )

        self.stdout.write(
            f"  Країн створено: {len(to_create)}, оновлено name_ua: {len(to_update)}"
        )

        country_by_code = {c.code: c for c in CountryModel.objects.all()}
        return country_by_code, id_country_to_code

    def _load_regions(self, path, country_by_code, id_country_to_code, batch_size):
        # Справжня унікальність регіону — пара (name, country), саме на ній
        # unique_together у моделі. У вихідних даних буває, що кілька різних  # noqa: RUF003
        # region_id відповідають одній і тій самій назві регіону в тій самій  # noqa: RUF003
        # країні (наприклад дублі на кшталт "Almaty" в Казахстані) — тому
        # дедуплікація лише по region_id недостатня і падає на constraint.
        existing_by_key = {(r.name, r.country_id): r for r in RegionModel.objects.all()}
        to_create = {}  # (name, country_id) -> RegionModel (ще не збережений)
        to_update = {}  # (name, country_id) -> RegionModel (вже в базі)
        region_id_to_key = {}  # region_id з csv -> (name, country_id)
        skipped = 0

        for row in self._read_rows(path):
            rid = int(row["region_id"])

            code = id_country_to_code.get(row["id_country"])
            country = country_by_code.get(code) if code else None
            if country is None:
                skipped += 1
                continue

            key = (row["region"], country.id)
            region_id_to_key[rid] = key
            name_ua = self._clean_ua(row)

            existing = existing_by_key.get(key)
            if existing is not None:
                if name_ua and existing.name_ua != name_ua and key not in to_update:
                    existing.name_ua = name_ua
                    to_update[key] = existing
                continue

            if key in to_create:
                if name_ua and not to_create[key].name_ua:
                    to_create[key].name_ua = name_ua
                continue

            to_create[key] = RegionModel(
                name=row["region"],
                country=country,
                api_id=rid,
                name_ua=name_ua,
            )

        RegionModel.objects.bulk_create(list(to_create.values()), batch_size=batch_size)
        if to_update:
            RegionModel.objects.bulk_update(
                list(to_update.values()), ["name_ua"], batch_size=batch_size
            )

        self.stdout.write(
            f"  Регіонів створено: {len(to_create)}, оновлено name_ua: {len(to_update)}"
            + (f" (пропущено без країни: {skipped})" if skipped else "")
        )

        all_regions = {(r.name, r.country_id): r for r in RegionModel.objects.all()}
        # region_id (з csv) -> реальний об'єкт RegionModel (можливо, спільний
        # для кількох region_id, якщо вони збігались за назвою+країною)
        return {
            rid: all_regions[key]
            for rid, key in region_id_to_key.items()
            if key in all_regions
        }

    def _load_cities(
        self, path, country_by_code, id_country_to_code, region_by_api_id, batch_size
    ):
        existing_by_api_id = {
            c.api_id: c for c in CityModel.objects.only("id", "api_id", "name_ua")
        }
        create_buffer = []
        update_buffer = []
        created = 0
        updated = 0
        skipped = 0

        def flush_create():
            nonlocal created, create_buffer
            if create_buffer:
                CityModel.objects.bulk_create(create_buffer, batch_size=batch_size)
                created += len(create_buffer)
                create_buffer = []

        def flush_update():
            nonlocal updated, update_buffer
            if update_buffer:
                CityModel.objects.bulk_update(
                    update_buffer, ["name_ua"], batch_size=batch_size
                )
                updated += len(update_buffer)
                update_buffer = []

        for row in self._read_rows(path):
            api_id = int(row["id_city"])
            name_ua = self._clean_ua(row)

            existing = existing_by_api_id.get(api_id)
            if existing is not None:
                if name_ua and existing.name_ua != name_ua:
                    existing.name_ua = name_ua
                    update_buffer.append(existing)
                    if len(update_buffer) >= batch_size:
                        flush_update()
                continue

            code = id_country_to_code.get(row["id_country"])
            country = country_by_code.get(code) if code else None
            region = region_by_api_id.get(int(row["region_id"]))
            if country is None or region is None:
                skipped += 1
                continue

            create_buffer.append(
                CityModel(
                    name=row["name"],
                    country=country,
                    region=region,
                    api_id=api_id,
                    latitude=self._to_decimal(row.get("latitude")),
                    longitude=self._to_decimal(row.get("longitude")),
                    name_ua=name_ua,
                )
            )
            existing_by_api_id[api_id] = (
                None  # заглушка, щоб не задублювати в межах файлу
            )

            if len(create_buffer) >= batch_size:
                flush_create()
                self.stdout.write(f"  ...створено міст: {created}")

        flush_create()
        flush_update()

        self.stdout.write(
            f"  Міст створено: {created}, оновлено name_ua: {updated}"
            + (f" (пропущено без країни/регіону: {skipped})" if skipped else "")
        )

    @staticmethod
    def _to_decimal(value):
        if value in (None, ""):
            return None
        try:
            return Decimal(str(value))
        except InvalidOperation:
            return None
