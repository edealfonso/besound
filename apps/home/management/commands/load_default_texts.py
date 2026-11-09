from django.core.management.base import BaseCommand
from django.db import transaction

from apps.about.models import AboutPage, Step
from apps.custom_users.models import LoginPage, RegisterPage
from apps.home.models import HomePage
from apps.posts.models import RecordPage

# Default texts for every page of the app. They can be edited later in the admin.
TEXTS = {
    HomePage: {
        'motto': 'Sound experiences to share',
        'instruction': 'Click on a word to listen',
        'error_not_found': "This sound doesn't exist or has been deleted.",
    },
    LoginPage: {
        'intro': 'Share what you hear.',
        'instruction': 'Log in to record and publish your own sound.',
        'button': 'Log in',
        'signup_intro': "Don't have an account yet?",
        'signup_link': 'Sign up here',
    },
    RegisterPage: {
        'login_text': 'Already have an account?',
        'login_link': 'Log in here',
        'text_part1': 'Tell us a little about yourself:',
        'text_part2': 'And choose how you will log in:',
        'button_end': 'Sign up',
        'confirmation_pre': 'Welcome! Your user:',
        'confirmation_post': 'Your account is ready. Log in to record your first sound.',
    },
    RecordPage: {
        'step1_instruction': '<p>Find a sound around you that you would like to share.</p><p>When you are ready, press the button to start recording.</p>',
        'step2_instruction': '<p>Recording… You have up to <strong>15 seconds</strong>.</p><p>Press the button again to stop.</p>',
        'step3_instruction': '<p>Choose an effect for your sound, or keep it as it is.</p>',
        'step3_back': 'Record again',
        'step3_forward': 'Next',
        'step4_instruction': '<p>Give your sound a title: <strong>a single word</strong>.</p>',
        'step4_back': 'Back',
        'step4_forward': 'Publish',
        'confirmation_generating': 'Publishing your sound…',
        'confirmation_pre_title': 'Your sound is now online as',
        'confirmation_post_title': 'Thank you for sharing what you hear.',
        'confirmation_regret': 'Changed your mind? Delete this sound.',
        'confirmation_remember': 'Remember: every sound on besound is anonymous.',
        'error_text_1': 'Delete this sound?',
        'error_text_2': 'It will disappear from besound and cannot be recovered.',
        'error_back': 'Cancel',
        'error_forward': 'Delete',
        'delete_success': 'Your sound has been deleted.',
        'delete_ko': 'This sound could not be deleted. It may have been deleted already.',
    },
    AboutPage: {
        'intro_text': '<p>besound is a place to share short sound experiences.</p>',
        'ending_text_1': '<p>Every sound is anonymous: only its word is shown.</p>',
        'ending_text_2': '<p>A project by Elsa de Alfonso.</p>',
    },
}

ABOUT_STEPS = [
    'Record up to 15 seconds of the sound around you.',
    'Add an effect and give it a one-word title.',
    'Publish it and let everyone listen.',
]


class Command(BaseCommand):
    help = 'Fill the empty texts of every page with default texts. Texts already written in the admin are kept.'

    @transaction.atomic
    def handle(self, *args, **options):
        for model, fields in TEXTS.items():
            page = model.get_solo()
            filled = [name for name, value in fields.items() if not getattr(page, name)]
            for name in filled:
                setattr(page, name, fields[name])
            page.save()
            self.stdout.write(f'{model._meta.verbose_name}: {len(filled)} of {len(fields)} texts filled')

        about = AboutPage.get_solo()
        if not about.steps.exists():
            for text in ABOUT_STEPS:
                Step.objects.create(page=about, text=text)
            self.stdout.write(f'About Page: {len(ABOUT_STEPS)} steps created')
        self.stdout.write(self.style.SUCCESS('Done. Review and edit them in the admin.'))
