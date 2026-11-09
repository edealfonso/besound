from io import StringIO

from django.core.management import call_command
from django.test import TestCase

from apps.about.models import AboutPage
from apps.home.management.commands.load_default_texts import TEXTS
from apps.home.models import HomePage


class LoadDefaultTextsTests(TestCase):
    def run_command(self):
        call_command('load_default_texts', stdout=StringIO())

    def test_fills_every_text_and_fits_the_field_lengths(self):
        self.run_command()
        for model, fields in TEXTS.items():
            page = model.get_solo()
            page.full_clean()  # fails if a text is longer than its field allows
            for name, value in fields.items():
                self.assertEqual(getattr(page, name), value)

    def test_keeps_texts_already_written_in_the_admin(self):
        home = HomePage.get_solo()
        home.motto = 'Mi lema'
        home.save()

        self.run_command()
        self.run_command()  # running it twice changes nothing

        home.refresh_from_db()
        self.assertEqual(home.motto, 'Mi lema')
        self.assertEqual(AboutPage.get_solo().steps.count(), 3)
