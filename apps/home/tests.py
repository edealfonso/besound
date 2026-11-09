import shutil
import tempfile
from io import StringIO

from django.core.files.storage import default_storage
from django.core.management import call_command
from django.test import TestCase, override_settings

from apps.about.models import AboutPage
from apps.home.management.commands.load_default_texts import TEXTS
from apps.home.models import HomePage


TEST_MEDIA = tempfile.mkdtemp()


@override_settings(MEDIA_ROOT=TEST_MEDIA)
class LoadDefaultTextsTests(TestCase):
    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(TEST_MEDIA, ignore_errors=True)
        super().tearDownClass()

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
        self.assertEqual(AboutPage.get_solo().steps.count(), 5)

    def test_overwrite_replaces_existing_texts_and_steps(self):
        home = HomePage.get_solo()
        home.motto = 'Mi lema'
        home.save()
        self.run_command()

        call_command('load_default_texts', '--overwrite', stdout=StringIO())

        home.refresh_from_db()
        self.assertEqual(home.motto, TEXTS[HomePage]['motto'])
        steps = AboutPage.get_solo().steps.all()
        self.assertEqual(steps.count(), 5)
        self.assertEqual(steps[0].image.name, 'about/circle.svg')

    def test_copies_the_about_images_to_the_storage(self):
        self.run_command()
        for name in ['about/circle.svg', 'about/circle-active.svg', 'about/effects.svg']:
            self.assertTrue(default_storage.exists(name))
        self.run_command()  # running it again does not duplicate them
        self.assertEqual(sorted(default_storage.listdir('about')[1]),
                         ['circle-active.svg', 'circle.svg', 'effects.svg'])
