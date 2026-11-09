from pathlib import Path

from django.core.files import File
from django.core.files.storage import default_storage
from django.core.management.base import BaseCommand
from django.db import transaction

from apps.about.models import AboutPage, Step
from apps.custom_users.models import LoginPage, RegisterPage
from apps.home.models import HomePage
from apps.posts.models import RecordPage

# Texts of every page, taken from the original Figma design (BeSound Figma 2).
# Fields that are not in the design have a text written to match it.
# They can be edited later in the admin.
TEXTS = {
    HomePage: {
        'motto': 'Sound experiences to share',
        'instruction': 'tap to hear',
        'error_not_found': 'this sound does not exist or has been deleted',
    },
    LoginPage: {
        'intro': 'you have to be logged in to record sounds',
        'instruction': 'enter your login data',
        'button': 'Log in',
        'signup_intro': 'not registered yet?',
        'signup_link': 'sign up here',
    },
    RegisterPage: {
        'login_text': 'already registered?',
        'login_link': 'Log in',
        'text_part1': 'to sign up, enter contact details',
        'text_part2': 'set your login data',
        'button_end': 'Sign up',
        'confirmation_pre': 'your email',
        'confirmation_post': 'has been<br>successfully created',
    },
    RecordPage: {
        'step1_instruction': '<p>press circle to <strong>start</strong> recording</p>',
        'step2_instruction': '<p>press circle to <strong>stop</strong> recording</p>',
        'step3_instruction': '<p>choose an <strong>effect</strong></p>',
        'step3_back': 'Start again',
        'step3_forward': 'OK',
        'step4_instruction': '<p>give your sound a <strong>name</strong></p>',
        'step4_back': 'Go back',
        'step4_forward': 'Share!',
        'confirmation_generating': 'sharing your sound...',
        'confirmation_pre_title': 'your sound',
        'confirmation_post_title': 'has been<br>successfully posted',
        'confirmation_regret': 'I regret all this!<br>Please delete this post',
        'confirmation_remember': 'Remember, all the posts are<br>completely anonymous &lt;3',
        'error_text_1': 'Delete this post?',
        'error_text_2': 'Your sound will disappear from besound and cannot be recovered.',
        'error_back': 'Cancel',
        'error_forward': 'Delete',
        'delete_success': 'your sound has been<br>successfully deleted',
        'delete_ko': 'this sound could not be deleted,<br>it may have been deleted already',
    },
    AboutPage: {
        'intro_text': 'Besound is a non-profit app aiming to bring you the richness of experimenting with sound and sharing it with the world',
        'ending_text_1': 'For safety reasons, only registered users can post sounds. That helps us track any abusive content. Your personal data will be stored safely.',
        'ending_text_2': 'Becoming a member is and will always remain free for everybody',
    },
}

# Images of the About steps live in the repo, next to the app that uses them,
# and are copied to the storage (local media/ or R2) under about/.
DEFAULT_IMAGES = Path(__file__).resolve().parents[3] / 'about' / 'default_images'

# Steps of the About page: (text, image in DEFAULT_IMAGES or '')
ABOUT_STEPS = [
    ('To record a sound,<br>press the red circle', 'circle.svg'),
    ("While it's filled,<br>recording is taking place,<br>press again to stop recording", 'circle-active.svg'),
    ('Add an effect<br>or leave it as it is', 'effects.svg'),
    ('Name your sound,<br>and share it with the world!', ''),
    ('Remember, all the posts are<br>completely anonymous &lt;3', ''),
]


class Command(BaseCommand):
    help = ('Fill the texts of every page with the ones from the original design. '
            'Texts already written in the admin are kept, unless --overwrite is given.')

    def add_arguments(self, parser):
        parser.add_argument('--overwrite', action='store_true',
                            help='Replace every text and the About steps, even if already written.')

    @transaction.atomic
    def handle(self, *args, overwrite=False, **options):
        for model, fields in TEXTS.items():
            page = model.get_solo()
            filled = [name for name, value in fields.items() if overwrite or not getattr(page, name)]
            for name in filled:
                setattr(page, name, fields[name])
            page.save()
            self.stdout.write(f'{model._meta.verbose_name}: {len(filled)} of {len(fields)} texts filled')

        about = AboutPage.get_solo()
        if overwrite:
            about.steps.all().delete()
        if not about.steps.exists():
            for text, image in ABOUT_STEPS:
                Step.objects.create(page=about, text=text, image=self.store_image(image))
            self.stdout.write(f'About Page: {len(ABOUT_STEPS)} steps created')
        self.stdout.write(self.style.SUCCESS('Done. Review and edit them in the admin.'))

    def store_image(self, filename):
        """Copy a default image to the storage if it is not there yet and return its name."""
        if not filename:
            return ''
        name = f'about/{filename}'
        if not default_storage.exists(name):
            with (DEFAULT_IMAGES / filename).open('rb') as f:
                default_storage.save(name, File(f))
        return name
