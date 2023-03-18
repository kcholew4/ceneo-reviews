class ProductInfoHelper:
    ELEMENT_SELECTORS = {
        "name": ".product-top__product-info__name"
    }

    def __init__(self, page):
        self.page = page

    def name(self):
        name = self.page.select_one(self.ELEMENT_SELECTORS["name"])

        return name.string.strip() if name else None
