import autocomplete_light
from models import Products


class ProductAutocomplete(autocomplete_light.AutocompleteModelBase):
    search_fields = ['^product_name', 'product_disc']
    model = Products
    def choices_for_request(self):
        if not self.request.user.is_staff:
            self.choices = self.choices.filter(private=False)
        return super(ProductAutocomplete, self).choices_for_request()
# we have specified PersonAutocomplete.model, so we don't have to repeat
# the model class as argument for register()
autocomplete_light.register(ProductAutocomplete)