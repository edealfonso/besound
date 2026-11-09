from pathlib import Path

from django.conf import settings
from django.core.files import File
from django.core.files.storage import default_storage
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Upload the files in MEDIA_ROOT (or a given folder) to the configured storage (e.g. Cloudflare R2), skipping the ones already there."

    def add_arguments(self, parser):
        parser.add_argument('folder', nargs='?', default=str(settings.MEDIA_ROOT))

    def handle(self, folder, **options):
        root = Path(folder)
        uploaded = skipped = 0
        for path in sorted(p for p in root.rglob('*') if p.is_file() and not p.name.startswith('.')):
            name = path.relative_to(root).as_posix()
            if default_storage.exists(name):
                skipped += 1
                continue
            with path.open('rb') as f:
                default_storage.save(name, File(f))
            uploaded += 1
            self.stdout.write(f'  ↑ {name}')
        self.stdout.write(self.style.SUCCESS(f'{uploaded} uploaded, {skipped} already there'))
