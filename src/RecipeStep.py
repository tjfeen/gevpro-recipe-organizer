class RecipeStep:
    def __init__(self, text):
        self.text = text
        
    @staticmethod
    def from_str(str):
        return RecipeStep(str.strip())
    
    @staticmethod
    def from_linked_data(ld_step):
        return RecipeStep(ld_step['text'].strip())
        
    def get_text(self):
        return self.text