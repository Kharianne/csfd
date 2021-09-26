import django.db.utils
from django.core.management.base import BaseCommand
from csfd_search.models import Movie, Actor
import requests
from lxml import html
from urllib.parse import urljoin
import asyncio
from asgiref.sync import sync_to_async
import functools


class Command(BaseCommand):
    HEADERS = {
            'User-Agent': 'Mozilla/5.0',
        }
    MOVIES_XPATH = "//a[@class='film-title-name']"
    ACTORS_XPATH = "//h4[contains(text(), 'Hrají:')]/parent::div//a"

    BASE_URL = 'https://www.csfd.cz'
    START_URL = 'https://www.csfd.cz/zebricky/filmy/nejlepsi/?showMore=1'

    def handle(self, *args, **options):
        """
        In this case, I delete rows from DB via Django ORM because on_delete
        does not create constraint - using DELETE FROM <table> would be however
        faster.

        Possible improvements: allow to use "truncate" or "append/update" data
        """
        Movie.objects.all().delete()
        Actor.objects.all().delete()

        loop = asyncio.get_event_loop()
        loop.run_until_complete(
            self._parse_movies(self.START_URL))

    async def _parse_movies(self, url):
        loop = asyncio.get_event_loop()
        future_trees = []
        r = requests.get(url, headers=self.HEADERS)
        tree = html.fromstring(r.text)
        movies = tree.xpath(self.MOVIES_XPATH)

        for movie in movies:
            movie = Movie(csfd_id=movie.xpath("@href")[0],
                          name=movie.xpath("@title")[0])
            await sync_to_async(movie.save)()
            url = urljoin(self.BASE_URL, movie.csfd_id)
            future = loop.run_in_executor(None,
                                          functools.partial(requests.get,
                                                            url,
                                                            headers=self.HEADERS
                                                            )
                                          )
            future_trees.append((movie.pk, future))
            self.stdout.write(movie.name)

        for future_tree in future_trees:
            pk = future_tree[0]
            r = await future_tree[1]
            await self._parse_actors(pk, r)

    async def _parse_actors(self, movie_id, response):
        movie = await sync_to_async(Movie.objects.get)(pk=movie_id)
        movie_tree = html.fromstring(response.text)
        actors = movie_tree.xpath(self.ACTORS_XPATH)
        for actor in actors:
            try:
                csfd_id = actor.xpath('@href')[0]
                name = actor.xpath('text()')[0]
            except IndexError:
                # In case we do not get some of the data for Actor
                # skip it
                continue
            if csfd_id == '#':
                # The last result is "více"
                break
            actor = Actor(csfd_id=csfd_id, name=name)
            try:
                # Check for
                await sync_to_async(actor.save)()
            except django.db.utils.IntegrityError:
                actor = await sync_to_async(Actor.objects.get)(csfd_id=csfd_id)

            await sync_to_async(movie.actors.add)(actor)
            self.stdout.write(actor.name)
