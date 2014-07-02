from django.core.management.base import BaseCommand

from basic.modelgenerator import ModelGenerator

class Command(BaseCommand):
	def handle(self, *args, **options):
		if len(args) == 0:
			return "Enter filename"
		ModelGenerator(open(args[0])).run()