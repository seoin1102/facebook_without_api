# Facebook Scraper

Scrape Facebook public pages without an API key. 


## Install

```sh
pip install facebook-scraper
```


## Usage

Send the unique **page name** as the first parameter and you're good to go:

```python
>>> from facebook_scraper import get_posts

>>> for post in get_posts('nintendo', pages=1):
...     print(post['text'][:50])
...
The final step on the road to the Super Smash Bros
We’re headed to PAX East 3/28-3/31 with new games
```


### Optional parameters

*(For the `get_posts` function)*.

- **group**: group id, to scrape groups instead of pages. Default is `None`.
- **pages**: how many pages of posts to request, the first 2 pages may have no results, so try with a number greater than 2. Default is 10.
- **timeout**: how many seconds to wait before timing out. Default is 5.
- **credentials**: tuple of user and password to login before requesting the posts. Default is `None`.
- **extra_info**: bool, if true the function will try to do an extra request to get the post reactions. Default is False.
- **youtube_dl**: bool, use Youtube-DL for (high-quality) video extraction. You need to have youtube-dl installed on your environment. Default is False.


## CLI usage
### 1. Run 'facebook_scraper.py'
```sh
$ python -m facebook_scraper -f dosiciety.csv -p 100 --group dosiciety --encoding utf-8
```

Run `facebook-scraper --help` for more details on CLI usage.

### 2. Run 'send_data.py'



## Post example

```python
{'post_id': '2257188721032235',
 'text': 'Don’t let this diminutive version of the Hero of Time fool you, '
         'Young Link is just as heroic as his fully grown version! Young Link '
         'joins the Super Smash Bros. series of amiibo figures!',
 'time': datetime.datetime(2019, 4, 29, 12, 0, 1),
 'image': 'https://scontent.flim16-1.fna.fbcdn.net'
          '/v/t1.0-0/cp0/e15/q65/p320x320'
          '/58680860_2257182054366235_1985558733786185728_n.jpg'
          '?_nc_cat=1&_nc_ht=scontent.flim16-1.fna'
          '&oh=31b0ba32ec7886e95a5478c479ba1d38&oe=5D6CDEE4',
 'images': ['https://scontent.flim16-1.fna.fbcdn.net'
          '/v/t1.0-0/cp0/e15/q65/p320x320'
          '/58680860_2257182054366235_1985558733786185728_n.jpg'
          '?_nc_cat=1&_nc_ht=scontent.flim16-1.fna'
          '&oh=31b0ba32ec7886e95a5478c479ba1d38&oe=5D6CDEE4'],
 'likes': 2036,
 'comments': 214,
 'shares': 0,
 'reactions': {'like': 135, 'love': 64, 'haha': 10, 'wow': 4, 'anger': 1},  # if `extra_info` was set
 'post_url': 'https://m.facebook.com/story.php'
             '?story_fbid=2257188721032235&id=119240841493711',
 'link': 'https://bit.ly/something', 
 'is_live': False}
```


### Notes

- There is no guarantee that every field will be extracted (they might be `None`).
- Shares doesn't seem to work at the moment.
- Group posts may be missing some fields like `time` and `post_url`.
- Group scraping may return only one page and not work on private groups.
- You can get 20 posts per page. (There are 18 posts on the first page. 1page - 18 post, 2page - 38post ...)
- It takes 15 minutes to get 100 pages.(There will be 1998 posts.) 


## To-Do

- ~~Extract to json file.~~
- ~~Import only the latest pages, not the number of pages to recall.~~
- ~~Filter posts to get.~~
- Get Comments.
- Link Instagram to Facebook.
- Import profile picture.
