import requests
import json

def check_artist(artist):
    print(artist['post_name'])
    audios = set((audio['ID'], audio['post_title'], audio['guid']) for audio in artist['audio'])
    url = "https://api.lipservice.co.uk/api/wp/v2/artists/{}/audio".format(artist['ID'])
    correct_audios = json.loads(requests.get(url).text)
    correct_audios = set((audio['ID'], audio['post_title'], audio['guid']) for audio in correct_audios)
    return artist['post_name'], audios.difference(correct_audios)


def retrieve_data():
    url = "https://api.lipservice.co.uk/api/wp/v2/artists?foreign=false&filter[posts_per_page]=24&page={}"
    errors = set()
    for i in range(20):
        artists = json.loads(requests.get(url.format(i)).text)
        for artist in artists:
            name, audios = check_artist(artist)
            errors = errors.union(audios)
            print(len(errors), errors)
    return errors

if __name__ == "__main__":
    errors = retrieve_data()
    print(errors)
