from pprint import pprint
from pprint import pprint

aa = {"un": 1,
      "deux": 2,
      "ingredients":
          [
            {
                'id': 'en:cocoa-paste',
                'percent_estimate': '4.66666666666667',
                'percent_max': 7,
                'percent_min': '2.33333333333333',
                'text': 'pâte de cacao',
                'vegan': 'yes',
                'vegetarian': 'yes'},
            {
                'id': 'en:unrefined-cane-sugar',
                'percent_estimate': '1.16666666666667',
                'percent_max': '3.5',
                'percent_min': 0,
                'text': 'sucre de canne non raffiné',
                'vegan': 'yes',
                'vegetarian': 'yes'},
            {
                'id': 'en:cocoa-butter',
                'percent_estimate': '1.16666666666667',
                'percent_max': '2.33333333333333',
                'percent_min': 0,
                'text': 'beurre de cacao',
                'vegan': 'yes',
                'vegetarian': 'yes'}]}

if "ingredients" in aa:
    print("Banco !")

