import asyncio

from DataCrawler.DataCrawler import DataCrawler

data_crawler = DataCrawler()

async def add_apex_players_to_db():
    await data_crawler.add_apex_players()


if __name__ == '__main__':
    asyncio.run(add_apex_players_to_db())