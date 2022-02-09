import asyncio

from DataCrawler.DataCrawler import DataCrawler

data_crawler = DataCrawler()

async def add_apex_players_to_db():
    await data_crawler.add_apex_players()

async def add_non_apex_players_to_db():
    await data_crawler.add_players_from_all_leagues_in_pages(range(11, 51))


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(data_crawler.add_all_matchs())