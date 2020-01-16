class Product:
    """
    Defining the product based on principles found in the POG.
    """
    def __init__(self, upc, name, width, size, manufacturer, brand, shelf_no,
                 shelf_length, shelf_position, start_position, end_position, shelf_height, description):
        self.upc = upc
        self.name = name
        self.width = width
        self.size = size
        self.manufacturer = manufacturer
        self.brand = brand
        self.shelf_no = shelf_no
        self.shelf_length = shelf_length
        self.shelf_position = shelf_position
        self.start_position = start_position
        self.end_position = end_position
        self.description = description
        self.shelf_height = shelf_height

    def __repr__(self):
        return str(self.brand)