import asyncio
from bs4 import BeautifulSoup
from os import wait
from time import sleep


import aiofiles
from playwright.async_api import async_playwright

from config import load_config


async def form_table(input_table):
    soup = BeautifulSoup(input_table, "lxml")
    rows = []
    for tr in soup.select("tr"):
        cells = tr.select("th, td")
        row = [cell.get_text(" ", strip=True) for cell in cells]

        if row:
            rows.append(row)

    return rows[1:]


async def parse_page():
    async with async_playwright() as p:
        config = load_config()
        browser = await p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--disable-gpu",
            ],
        )

        context = await browser.new_context(
            viewport={"width": 1440, "height": 1000},
            locale="ru-RU",
            user_agent=(
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/125.0 Safari/537.36"
            ),
        )

        page = await context.new_page()

        await page.goto(config.url, wait_until="domcontentloaded")

        await page.locator("input[name='ctl00$LastName']").fill(config.rc_surname)
        await page.locator("input[name='ctl00$FirstName']").fill(config.rc_name)
        await page.locator("input[name='ctl00$MidName']").fill(config.rc_patronymic)
        await page.locator("input[name='ctl00$Number']").fill(str(config.rc_id))

        await page.locator("input[name='ctl00$AcceptDataProcessing']").check()

        async with page.expect_navigation(wait_until="domcontentloaded"):
            await page.locator("input[name='ctl00$LoginButton']").click()

        await page.locator("input[name='ctl00$ContentPlaceHolder1$AcceptCheckBox']").check()

        async with page.expect_navigation(wait_until="domcontentloaded"):
            await page.locator("input[name='ctl00$ContentPlaceHolder1$AcceptButton']").click()

        async with page.expect_navigation(wait_until="domcontentloaded"):
            await page.get_by_role("link", name="Результаты экзаменов").first.click()

        await page.screenshot(path="test-results/screenshot.png")


        await page.locator("[id='ctl00_ContentPlaceHolder1_ResExams'] tr").first.wait_for(state="attached")

        table = await page.locator("[id='ctl00_ContentPlaceHolder1_ResExams']").evaluate(
            "element => element.outerHTML"
        )

        await context.close()
        await browser.close()

    return await form_table(table)




async def main() -> None:
    result = await parse_page()
    print(result)



if __name__ == "__main__":
    asyncio.run(main())