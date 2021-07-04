from bs4 import BeautifulSoup
from pyppeteer import launch
import asyncio

async def main():
    browser = await launch()

    page = await browser.newPage()

    page_path = "https://kiezburn.dreams.wtf/kb21"

    await page.goto(page_path)
    page_content = await page.content()

    mt7 = await page.xpath("//div[contains(@class, 'mt-7')]")
    mt7 = mt7[0]
    print(mt7.toString())
    await mt7.screenshot({"path": "test.png"})


    #soup = BeautifulSoup(page_content)
    #a_all = soup.findAll("a", href=True)
    #buttons = soup.findAll("button")
    #print(len(buttons))
    #print(buttons)
    #dream_refs = [a.get('href') for a in a_all if a.get('href').startswith('/kb21/')]
    #print(dream_refs)


asyncio.get_event_loop().run_until_complete(main())