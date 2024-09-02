from django.core.management.base import BaseCommand
from llmapp.fine_tune import fine_tune_bert

class Command(BaseCommand):
    help = 'Fine-tune BERT model'

    def handle(self, *args, **kwargs):
        fine_tune_bert()