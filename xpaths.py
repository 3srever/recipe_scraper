#file to manage the xpaths & classes for each

def x_path(class_name):
    return f'//*[@class="{class_name}"]'

def x_path_selector(url):
    if url == "https://marleyspoon.com/menu":
        recipes_field = [
            x_path('menu-page__recipe-list-container'),                         # recipe container (class holding all recipes)
            x_path('menu-page__recipe')                                         # individual recipe class
        ]

        page_elements = [
            x_path('recipe-name'),                                              # recipe name
            x_path('recipe-specs'),                                             # specs (serving time, level, nutrition, allergens)
            x_path('dish-details__attribute-detail'),                           # individual spec
            x_path('recipe-labels'),                                            # tags
            x_path('recipe-attributes__labels'),                                 # individual tag
            x_path('dish-detail__we-send nui__row nui__col-8 nui__nopadding'),  # ingredients
            x_path('dish-detail__ingredient nui__col-2')                        # individual ingredient
        ]

        dates_field = [                                                         # subclasses within data selector
            x_path('delivery-weeks__container'),                                # container holding all dates
            x_path('delivery-week__btn ')                                       # buttons with dates

        ]
        return recipes_field, page_elements, dates_field

    else:
        raise NameError('URL is not supported yet.')