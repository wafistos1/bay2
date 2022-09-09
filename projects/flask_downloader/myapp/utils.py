from pytube import YouTube


def return_yt(link):
    return YouTube(link).streams.filter(file_extension='mp4').first().download()


if __name__=='__main__':
    return_yt('https://www.youtube.com/watch?v=sa4Fr2LWo9A')