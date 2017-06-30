from django.shortcuts import render, redirect
from django.conf import settings
from subs.models import *
import subprocess
import re

# Create your views here.
def episode_index(request):
    episodes = Episode.objects.all()
    return render(request, 'episode_index.html', {'episodes':episodes})

def episode_lines(request, id):
    episode = Episode.objects.get(pk=id)
    lines = Sub.objects.filter(episode=episode)
    return render(request, 'episode_lines.html', {'episode': episode,
                                                  'lines': lines})

def write_linefile(sub):
    file_name = "{}{}".format(settings.MEDIA_ROOT, sub.id)
    with open(file_name, 'w') as f:
        f.write(sub.line)
    return file_name

def create_media(request, id, file_format):
    sub = Sub.objects.get(pk=id)
    name = '{}x{}-{}'.format(sub.episode.season, sub.episode.number, sub.index)
    text_file = write_linefile(sub)
    font_size = int((28 / len(max(sub.line.split('\n'), key=len))) * 50)
    if font_size > 50:
        font_size = 50
    command = ' '.join(['ffmpeg',
                '-y',
                '-ss', sub.start,
                '-i', '"{}"'.format(sub.episode.episode_file),
                '-to', sub.duration,
                '-strict', '-2',
                '-vf', 'drawtext="fontfile=/usr/share/fonts/TTF/impact.ttf:textfile={}:fontcolor=white:fontsize={}:x=(w-text_w)/2:y=((h*1.75)-text_h)/2:borderw=3"'.format(text_file, font_size),
                '"{}{}.{}"'.format(settings.MEDIA_ROOT, name, file_format)])
    p = subprocess.Popen(command, shell=True)
    p.wait()
    return redirect('{}{}.{}'.format(settings.MEDIA_URL, name, file_format))
