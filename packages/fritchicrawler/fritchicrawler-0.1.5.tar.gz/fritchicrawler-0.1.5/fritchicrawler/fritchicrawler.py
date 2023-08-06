import dataclasses
import logging
from collections import defaultdict
from typing import Optional

import pendulum
import playwright.sync_api as psync
import playwright.async_api as pasync
import re
import pickle
from path import Path


@dataclasses.dataclass
class NutritionInfo:
    cals: int
    fat: str
    carbs: int
    fibers: int
    proteins: int
    salt: int

    @classmethod
    def from_locator(cls, main_locator: psync.Locator):
        """

        :param main_locator:
        :return:
        """
        cals, fat, carbs, fibers, proteins, salt = [
            int(
                re.search(r"(\d+)", i.inner_text())[0]
                if re.search(r"(\d+)", i.inner_text())
                else "0"
            )
            for i in main_locator.locator("var").all()
        ]
        return NutritionInfo(cals, fat, carbs, fibers, proteins, salt)

    @classmethod
    async def from_locator_async(cls, main_locator: pasync.Locator):
        """

        :param main_locator:
        :return:
        """
        cals, fat, carbs, fibers, proteins, salt = [
            int(
                re.search(r"(\d+)", await i.inner_text())[0]
                if re.search(r"(\d+)", await i.inner_text())
                else "0"
            )
            for i in await main_locator.locator("var").all()
        ]
        return NutritionInfo(cals, fat, carbs, fibers, proteins, salt)


@dataclasses.dataclass
class Product:
    name: str
    coming_from: str
    ingredients: list[str]
    allergens: list[str]
    portion: int
    url: str
    pic: str
    nutritions: Optional[NutritionInfo] = None

    @classmethod
    def from_page(cls, page: psync.Page, url: str) -> "Product":
        """

        :param page:
        :param url:
        :return:
        """
        main_locator = page.locator("main").first
        sections = [i for i in main_locator.locator("section").all()]
        product_data = {
            i.locator("h2").first.inner_text(): "".join(
                [j.inner_text() for j in i.locator("p").all()]
            )
            for i in sections
        }
        return Product(
            name=main_locator.first.locator("h3").inner_text(),
            ingredients=[
                i.strip() for i in "".join(product_data["Ingrédients"]).split(",")
            ]
            if "Ingrédients" in product_data.keys()
            else "",
            allergens=[
                i.strip() for i in "".join(product_data["Allergènes"]).split(",")
            ]
            if "Allergènes" in product_data.keys()
            else "",
            portion=int(
                re.search(r"(\d+)g", product_data["Poids"])[0][:-1]
                if "Poids" in product_data.keys()
                else 0
            ),
            coming_from=main_locator.locator("header").locator("p").first.inner_text(),
            nutritions=NutritionInfo.from_locator(main_locator)
            if main_locator.get_by_text("nutritionnelles").all()
            else None,
            pic=main_locator.locator("img").first.get_attribute("src"),
            url=url,
        )

    @classmethod
    async def from_page_async(cls, page: pasync.Page, url: str) -> "Product":
        """

        :param page:
        :param url:
        :return:
        """
        main_locator = page.locator("main").first
        sections = [i for i in await main_locator.locator("section").all()]
        product_data = {
            await i.locator("h2").first.inner_text(): "".join(
                [await j.inner_text() for j in await i.locator("p").all()]
            )
            for i in sections
        }
        return Product(
            name=await main_locator.first.locator("h3").inner_text(),
            ingredients=[
                i.strip() for i in "".join(product_data["Ingrédients"]).split(",")
            ]
            if "Ingrédients" in product_data.keys()
            else "",
            allergens=[
                i.strip() for i in "".join(product_data["Allergènes"]).split(",")
            ]
            if "Allergènes" in product_data.keys()
            else "",
            portion=int(
                re.search(r"(\d+)g", product_data["Poids"])[0][:-1]
                if "Poids" in product_data.keys()
                else 0
            ),
            coming_from=await main_locator.locator("header").locator("p").first.inner_text(),
            nutritions=await NutritionInfo.from_locator_async(main_locator)
            if await main_locator.get_by_text("nutritionnelles").all()
            else None,
            pic=await main_locator.locator("img").first.get_attribute("src"),
            url=url,
        )


@dataclasses.dataclass
class Tempdata:
    stamp: pendulum.DateTime
    data: dict[str, list[Product]]


def get_products(
        force=False, no_cache=False, pickle_dir="./"
) -> dict[str, list[Product]]:
    """
    fetch all front page products from frichti and cache the data in a pickle file
    :param force: force the crawling and file generation.
    :param no_cache: don't cache data in a picke file.
    :param pickle_dir: specify a directory to store the serialized data. default: './'
    :return:
    """
    pickle_dir = Path(pickle_dir)
    if not force:
        try:
            with open(pickle_dir / "data.pickle", "rb") as f:
                data: Tempdata = pickle.load(f)
                if pendulum.Date.today() == data.stamp or pendulum.today().hour < 8:
                    return data.data
        except FileNotFoundError:
            pass

    with psync.sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto("https://frichti.co/")
        page.get_by_role("textbox").fill("Conserto Rennes")
        page.get_by_role("listbox").first.locator("li").locator("div").first.wait_for()
        page.get_by_role("listbox").click()
        main_tag = page.get_by_role("main").first
        main_tag.locator("section").first.wait_for()
        raw_products = {
            i.locator("h2").first.inner_text(): [
                j.locator("a").first.get_attribute("href")
                for j in i.locator("article").all()
                if j.locator("header").all()
            ]
            for i in main_tag.locator("section").all()
            if i.get_attribute("id") not in ["nouveautes-epd-market"]
        }
        baked_products: defaultdict[str, [Product]] = defaultdict(list)
        for title, items in raw_products.items():
            logging.info("processings products for:", title)
            for i, product_url in enumerate(items):
                page.goto(f"https://frichti.co/{product_url}")
                if page.get_by_text("Houston").all():
                    logging.info("\t", "404, skipping.")
                    continue
                logging.info("\t", f"processing product {i + 1}/{len(items)}")
                try:
                    baked_products[title].append(Product.from_page(page, product_url))
                except KeyError as e:
                    logging.info("\t", "unformated data, skipping.")
                except Exception as e:
                    page.screenshot(
                        path=f"product-{product_url}-error.png".replace("/", "\\")
                    )
                    raise e

    baked_products: dict[str, [Product]] = dict(baked_products)

    if not no_cache:
        with open(pickle_dir / "data.pickle", "wb") as f:
            pickle.dump(
                Tempdata(stamp=pendulum.Date.today(), data=baked_products),
                f,
                pickle.HIGHEST_PROTOCOL,
            )
        return baked_products


async def get_products_async(
        force=False, no_cache=False, pickle_dir="./"
) -> dict[str, list[Product]]:
    """
    fetch all front page products from frichti and cache the data in a pickle file
    :param force: force the crawling and file generation.
    :param no_cache: don't cache data in a picke file.
    :param pickle_dir: specify a directory to store the serialized data. default: './'
    :return:
    """
    pickle_dir = Path(pickle_dir)
    if not force:
        try:
            with open(pickle_dir / "data.pickle", "rb") as f:
                data: Tempdata = pickle.load(f)
                if pendulum.Date.today() == data.stamp or pendulum.today().hour < 8:
                    return data.data
        except FileNotFoundError:
            pass

    async with pasync.async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto("https://frichti.co/")
        await page.get_by_role("textbox").fill("Conserto Rennes")
        await page.get_by_role("listbox").first.locator("li").locator("div").first.wait_for()
        await page.get_by_role("listbox").click()
        main_tag = page.get_by_role("main").first
        await main_tag.locator("section").first.wait_for()
        raw_products = {
            await i.locator("h2").first.inner_text(): [
                await j.locator("a").first.get_attribute("href")
                for j in await i.locator("article").all()
                if await j.locator("header").all()
            ]
            for i in await main_tag.locator("section").all()
            if await i.get_attribute("id") not in ["nouveautes-epd-market"]
        }
        baked_products: defaultdict[str, [Product]] = defaultdict(list)
        for title, items in raw_products.items():
            logging.info("processings products for:", title)
            for i, product_url in enumerate(items):
                await page.goto(f"https://frichti.co/{product_url}")
                if await page.get_by_text("Houston").all():
                    logging.info("\t", "404, skipping.")
                    continue
                logging.info("\t", f"processing product {i + 1}/{len(items)}")
                try:
                    baked_products[title].append(await Product.from_page_async(page, product_url))
                except KeyError as e:
                    logging.info("\t", "unformated data, skipping.")
                except Exception as e:
                    await page.screenshot(
                        path=f"product-{product_url}-error.png".replace("/", "\\")
                    )
                    raise e

    baked_products: dict[str, [Product]] = dict(baked_products)

    if not no_cache:
        with open(pickle_dir / "data.pickle", "wb") as f:
            pickle.dump(
                Tempdata(stamp=pendulum.Date.today(), data=baked_products),
                f,
                pickle.HIGHEST_PROTOCOL,
            )
        return baked_products


if __name__ == "__main__":
    print(get_products())
