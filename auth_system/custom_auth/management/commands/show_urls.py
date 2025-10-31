from django.core.management.base import BaseCommand
from django.urls import get_resolver

class Command(BaseCommand):
    help = 'Show all URLs'

    def handle(self, *args, **options):
        resolver = get_resolver()
        patterns = resolver.url_patterns
        
        def print_patterns(patterns, prefix='', depth=0):
            for pattern in patterns:
                if hasattr(pattern, 'url_patterns'):
                    # Это include - рекурсивно обрабатываем вложенные patterns
                    new_prefix = prefix + pattern.pattern.regex.pattern
                    self.stdout.write('  ' * depth + f"📁 {new_prefix}")
                    print_patterns(pattern.url_patterns, new_prefix, depth + 1)
                else:
                    full_path = prefix + pattern.pattern.regex.pattern
                    self.stdout.write('  ' * depth + f"🔗 {full_path} -> {pattern.name or 'No name'}")

        print_patterns(patterns)