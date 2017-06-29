from django.core.management.base import BaseCommand, CommandError
import argparse
from subs.models import *
import pysrt
import re

class Command(BaseCommand):
    help = "Import srt files into database"

    def add_arguments(self, parser):
        parser.add_argument('files', nargs='*', type=argparse.FileType('r'))

    def format_time(self, t):
        return "{:02d}:{:02d}:{:02d}.{:03d}".format(t.hours,
                                                    t.minutes,
                                                    t.seconds,
                                                    t.milliseconds)

    def handle(self, *args, **options):
        for f in options['files']:
            try:
                subs = pysrt.open(f.name)
                regex = re.compile(r"Futurama - (\d)x(\d\d) - (.+)\.en")
                matches = regex.search(f.name)
                season, num, name = (matches.group(1), matches.group(2), matches.group(3))
                episode = Episode(name=name, season=season, number=num)
                episode.save()
                for sub in subs:
                    sub = Sub(episode=episode,
                              line=sub.text_without_tags,
                              line_formatted=sub.text,
                              start=self.format_time(sub.start),
                              duration=self.format_time(sub.duration),
                              end=self.format_time(sub.end),
                              index=sub.index)
                    sub.save()
            except Exception as e:
                print(e)
