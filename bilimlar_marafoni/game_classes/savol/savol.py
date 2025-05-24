class Savol:
    def __init__(self, id: int, matn: str, variant: dict, togri_javob: int, kategorya: str, subcategory: str):
        self.id = id
        self.matn = matn
        self.variant = variant
        self.togri_javob = togri_javob
        self.kategorya = kategorya
        self.subcategory = subcategory
        self.variant_savol = list(variant.values())

    def check_answer(self, javob):
        if self.variant[self.togri_javob] == javob:
            return True
        return False

    def get_variants(self):
        return tuple(self.variant.values())

    def get_option_id(self, javob):
        for k, v in self.variant.items():
            if v == javob:
                return k

    def __str__(self):
        return self.matn

if __name__ == "__main__":
    pass