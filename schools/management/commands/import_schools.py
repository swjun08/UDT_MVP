import csv
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from schools.models import School


CSV_COLUMNS = [
    "name", "school_type", "establishment", "education_office", "homepage",
    "zipcode", "address", "address_detail", "sido", "sigungu", "sublocal",
    "departments", "track_auto", "school_code",
    "phone_principal", "phone_academic", "phone_admin", "phone_career", "fax",
]


class Command(BaseCommand):
    help = "Import schools from a cleaned CSV file."

    def add_arguments(self, parser):
        parser.add_argument(
            "csv_path",
            type=str,
            help="Path to hifive_schools_mvp_clean.csv",
        )
        parser.add_argument(
            "--truncate",
            action="store_true",
            help="Delete all existing schools before importing.",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        csv_path = Path(options["csv_path"])
        if not csv_path.exists():
            raise CommandError(f"CSV not found: {csv_path}")

        if options["truncate"]:
            deleted, _ = School.objects.all().delete()
            self.stdout.write(self.style.WARNING(f"Deleted {deleted} rows."))

        with csv_path.open("r", encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            missing = [c for c in CSV_COLUMNS if c not in reader.fieldnames]
            if missing:
                raise CommandError(f"Missing columns in CSV: {missing}")

            upserts = 0
            for row in reader:
                # 필수값 체크
                if not row.get("school_code") or not row.get("name"):
                    continue

                defaults = {k: (row.get(k) or "").strip() for k in CSV_COLUMNS}
                school_code = defaults.pop("school_code")

                obj, _created = School.objects.update_or_create(
                    school_code=school_code,
                    defaults=defaults,
                )
                upserts += 1

        self.stdout.write(self.style.SUCCESS(f"Imported/updated {upserts} schools."))