from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('-n', '--name', action='append',
                            type=str, required=False)

    def handle(self, *args, **options):
        from apps.core.background import Worker
        w = Worker(options.get('name'))
        w.start()
