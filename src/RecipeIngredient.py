import re

INGREDIENT_PATTERN = re.compile(r"^ *([0-9\.,/]+)\s*([A-z']+) *([A-z' ()+0-9-]*)", re.M)
INGREDIENT_COUNT_PATTERN = re.compile(r'([0-9\/,.]+)')

class RecipeIngredient:
    def __init__(self, text = ''):       
        if text:
            self.text = re.sub(r' +', ' ', text.strip())
        
    @staticmethod
    def from_str(str):       
        return RecipeIngredient(str)
    
    def sub_callback(self, modifier):
        def sub(match):
            count_str = match.groups()[0]
            count_num = None
            
            if('/' in count_str):
                # Convert fractions to decimals, e.g. 1/2 to 0.5
                match = re.search(r'([0-9])\s*/\s*([0-9])', count_str)
                if(match): 
                    val_a, val_b = match.groups()
                    count_num = float(val_a) / float(val_b)
            elif(',' in count_str):
                # Replace comma with period
                count_num = float(count_str.replace(',', '.'))
            elif count_str.isnumeric():
                count_num = float(count_str)
            else:
                return count_str
                
            return f'{round(count_num * modifier, 1):g}'
        return sub
    
    def get_multiplied_text(self, modifier = 1):       
        return INGREDIENT_COUNT_PATTERN.sub(self.sub_callback(modifier), self.text)
        
    def get_text(self):
        return f'{self.get_multiplied_text(1)}'
    
    def is_valid(self):
        if(not len(self.text)): return False
        if('[object Object]' in self.text): return False
        return True