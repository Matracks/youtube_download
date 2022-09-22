from pytube import YouTube
from pytube.exceptions import RegexMatchError, VideoUnavailable
import database as db
import os


def video_validation(url):
    try:
        title = YouTube(url).title
        if bool(db.Videos.lis):
            for item in db.Videos.lis:
                if title != item.name:
                    return [True, 'Correct']
                else:
                    return [False, 'Duplicated Link']
        else:
            return [True, 'Correct']
    except RegexMatchError:
        return [False, 'Incorrect Link']
    except VideoUnavailable:
        return [False, 'Incorrect Link2']


def data_video(url, x):
    yt = YouTube(url)
    name = yt.title
    len = round(yt.length / 60, 2)
    link = url
    if x == 'Song':
        size = yt.streams.get_audio_only()
        size = round(size.filesize/1048576, 2)
        resolution = '-'
    else:
        size = yt.streams.filter(progressive=True).last()
        size = round(size.filesize/1048576, 2)
        resolution = '720'
    return [link, name, len, size, resolution, x]


def data_resolution(vid):
    yt = YouTube(vid)
    filter_list = yt.streams.filter(type='video', progressive=True)
    res = []
    for i in filter_list:
        if '720p' in str(i):
            res.append(720)
        if '480p' in str(i):
            res.append(480)
        if '360p' in str(i):
            res.append(360)
        if '240p' in str(i):
            res.append(240)
        if '144p' in str(i):
            res.append(144)
    return sorted(list(set(res)), reverse=True)


def new_resolution_size(url, resolution):
    yt = YouTube(url)
    new_size = yt.streams.filter(res=f'{resolution}p', progressive=True).last()
    return round(new_size.filesize / 1048576, 2)


def type_validation(type):
    return type == 'Video'


def download(directory):
    for i in db.Videos.lis:
        yt = YouTube(i.link)
        if i.type == 'Song':
            print(f'Descargando {i.name} - {i.type}')
            out_file = yt.streams.get_audio_only().download(directory)
            base, ext = os.path.splitext(out_file)
            new_file = base + '.mp3'
            os.rename(out_file, new_file)
        else:
            res = int(i.resolution)
            down = yt.streams.filter(res=f'{res}p', progressive='True')
            down.last().download(directory)
