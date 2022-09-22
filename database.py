class Video:
    def __init__(self, link, name, length, size, resolution, type):
        self.link = link
        self.name = name
        self.length = length
        self.size = size
        self.resolution = resolution
        self.type = type

    def __str__(self):
        return f'{self.name} with {self.length}'


class Videos:
    lis = []

    @staticmethod
    def adding(link, name, length, size, resolution, type):
        video = Video(link, name, length, size, resolution, type)
        Videos.lis.append(video)
        return video

    @staticmethod
    def removing(link):
        for index, video in enumerate(Videos.lis):
            if video.link == link:
                video = Videos.lis.pop(index)
                return video

    @staticmethod
    def change_data_res(link, size, resolution):
        for i, video in enumerate(Videos.lis):
            if video.link == link:
                Videos.lis[i].size = size
                Videos.lis[i].resolution = resolution
                return Videos.lis[i]
