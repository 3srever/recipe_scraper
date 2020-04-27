import pandas as pd
import scraper_class
import xpaths
import numpy as np

#display full length columns in pandas for legibility
pd.set_option('display.expand_frame_repr', False)

#instantiate the spider for interaction & scraper for grabbing content
marley_spoon = scraper_class.Scraper(
    r"C:\Users\stefa\PycharmProjects\RecipeScraper\chromedriver\chromedriver.exe"
)

domains = ['de', 'at', 'com.au', 'be', 'dk', 'nl', 'se', 'com']
#domains = ['de']
url = "https://marleyspoon.com/menu"
marley_spoon.get_url(url)

#collecting website xpaths
ms_recipes, ms_recipe_elements, ms_dates = xpaths.x_path_selector(url)

#creating a frame of dataframes for concatenation
frames = []

#false = automatically gathers furthest week, true = pick a week from list
def week_picker(default=False):

    weeks = marley_spoon.show_text(
        marley_spoon.grab_web_element(
            ms_dates[0]
        )
    )[0]
    weeks = weeks.splitlines()

    if default:
        print("Weeks available for scraping:")
        for i in range(len(weeks)):
            print(f"{i}. week: {weeks[i]}")
        choice = int(input(f"Pick a week to scrape (0-{len(weeks) - 1}): "))
        return choice, weeks[choice]

    else:
        return 3, weeks[-1]

choice, chosen_week = week_picker()

for domain in domains:
    url = f'https://marleyspoon.{domain}/menu'
    print(url)
    marley_spoon = scraper_class.Scraper(
        r"C:\Users\stefa\PycharmProjects\RecipeScraper\chromedriver\chromedriver.exe"
    )
    marley_spoon.get_url(url)

    #click selection & scroll to page to load all content
    marley_spoon.click(
        marley_spoon.grab_index(
            ms_dates[1],
            choice
        )
    )

    #count number of recipes and create a list of num * the week of choice string
    num_elements = marley_spoon.__len__(
        marley_spoon.grab_web_element(
            ms_recipes[1]
        )
    )

    recipe_links = []
    for num in range(1, num_elements+1):
        recipe_link = marley_spoon.show_href(
            marley_spoon.grab_web_element(
                ms_recipes[0] + f'/div[{num}]' + '/a'
            )
        )
        recipe_links.append(recipe_link[0])

    marley_spoon.quit()

    for link in recipe_links:
        # instantiate the spider for interaction & scraper for grabbing content
        marley_spoon = scraper_class.Scraper(
            r"C:\Users\stefa\PycharmProjects\RecipeScraper\chromedriver\chromedriver.exe"
        )
        marley_spoon.get_url(link)
        marley_spoon.scroll_down()

        num_ingredients = marley_spoon.__len__(
            marley_spoon.grab_web_element(
                ms_recipe_elements[6]
            )
        )

        recipe_name = recipe_ingredient = marley_spoon.show_text(
            marley_spoon.grab_web_element(
                ms_recipe_elements[0]
            )
        )

        recipe_specs = marley_spoon.show_text(
            marley_spoon.grab_web_element_list(
                ms_recipe_elements[1],
                '/li',
                ms_recipe_elements[2]
            )
        )

        recipe_tags = marley_spoon.show_text(
            marley_spoon.grab_web_element_list(
                ms_recipe_elements[4],
                '/li',
                ''
            )
        )

        recipe_ingredients = []
        for num in range(1, num_ingredients+1):
            recipe_ingredient = marley_spoon.show_text(
                marley_spoon.grab_web_element(
                    ms_recipe_elements[5] + f'/div[{num}]'
                )
            )
            recipe_ingredients.append(recipe_ingredient[0])

        num_ingredients = len(recipe_ingredients)

        domain_list = [domain] * num_ingredients
        date_list = [chosen_week] * num_ingredients
        name_list = [recipe_name[0]] * num_ingredients
        serving_time_list = [recipe_specs[0]] * num_ingredients
        level_list = [recipe_specs[1]] * num_ingredients
        nutrition_list = [recipe_specs[2]] * num_ingredients
        allergens_list = [recipe_specs[3]] * num_ingredients
        tags_list = [recipe_tags] * num_ingredients
        ingredients_list = []

        for i in range(num_ingredients):
            ingredients_list.append(recipe_ingredients[i])

        df_dict = {
            'domain': domain_list,
            'date': date_list,
            'name': name_list,
            'serving_time': serving_time_list,
            'level': level_list,
            'nutrition': nutrition_list,
            'allergens': allergens_list,
            'tags': tags_list,
            'ingredient': ingredients_list
        }
        df = pd.DataFrame(df_dict)
        frames.append(df)

        marley_spoon.quit()

df = pd.concat(frames)
print(df.info())

df.to_csv('marleyspoon.csv', sep=';')