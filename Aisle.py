import Product

class Aisle:
    """
    Constructs UPC data onto shelves for the specified planogram.
    """
    def __init__(self, df, planogram):
        id = df['POG_NAME'] == planogram
        filter_df = df[id] #filters the planogram df to just the requested planogram
        sorted_df = filter_df.sort_values(by=['Shelf_Num', 'Product_X_Pos_Abs'], ascending=[True, True])
        aisle = []
        y_vals = len(set(sorted_df['Shelf_Y_Pos']))

        #Assigning proper values to each row to correspond with each item in the given planogram
        for i in sorted_df.index:

            upc = sorted_df.at[i, 'UPC']
            name = sorted_df.at[i, 'Product_Description']
            width = sorted_df.at[i, 'Product_Width']
            size = sorted_df.at[i, 'Product_Size']
            manufacturer = sorted_df.at[i, 'Manufacturer']
            brand = sorted_df.at[i, 'Brand']
            shelf_no = sorted_df.at[i, 'Shelf_Num']
            shelf_length = sorted_df.at[i, 'Shelf_Width']
            shelf_position = sorted_df.at[i, 'Product_POS']
            start_position = sorted_df.at[i, 'Product_X_Pos_Abs']
            end_position = sorted_df.at[i, 'Product_End_X_Pos_Abs']
            shelf_height = sorted_df.at[i, 'Shelf_Y_Pos']
            description = sorted_df.at[i, 'Product_Description']
            #form = sorted_df.at[i, 'Form']

            product = Product.Product(upc, name, width, size, manufacturer, brand, shelf_no,
                              shelf_length, shelf_position, start_position, end_position, shelf_height, description)

            if len(aisle) < shelf_no: #Adds a shelf to the aisle if necessary
                aisle.append([])

            aisle[-1].append(product) #Adds the product to the end of the current shelf

        new_aisle = []

        #Adjusts for the actual aisles since planogram aisles can often say there are more aisles than actually are
        for i in range(len(aisle)):
            real_shelf = i % y_vals #using modulo to make sure shelves stay together
            #POG files have shelf numbers that don't intuitively line up i.e. might have 12 shelves when there are
            #actually 6
            if len(new_aisle) <= real_shelf:
                new_aisle.append(aisle[real_shelf])
            else:
                new_aisle[real_shelf].extend(aisle[i])

        self.shelves = new_aisle
        self.shelves.reverse()
        self.length = self.shelves[0][0].shelf_length #Gets the aisle length from the first product on the first shelf

    def __repr__(self):
        return(str(self.shelves))

    # !!! Need Clarification in order to do this !!!
    # def is_next_to(self, brand1, brand2):
    #     """
    #     Returns whether brand1 is next to brand2 somewhere in the aisle.
    #     :param brand1: str
    #     :param brand2: str
    #     :return: bool
    #     """
    #     flag = False
    #     for shelf in self.shelves:
    #         for i in range(1, len(shelf)-1):
    #             if shelf[i].brand == brand1:
    #                 if brand2 not in [shelf[i-1].brand, shelf[i+1].brand]:
    #                     return False

        # return True

    def helper(self, list1, string):
        """
        Returns true if any of list1 are a sub string of string.
        :param list1: list or str
        :param string: str
        :return: bool
        """
        for i in list1:
            if i in string:
                return True
        return False

    def helper2(self, list1, list2):
        """
        Returns true if any of the elements in list1 are a substring of any elements in list2.
        :param list1: list of str
        :param list2: list of str
        :return: bool
        """
        for i in list1:
            for j in list2:
                if i in j:
                    return True
        return False

    def is_not_next_to(self, brand1, brand2):
        """
        Returns whether brand1 is next to brand2 somewhere in the aisle.
        :param brand1: str
        :param brand2: str
        :return: bool
        """
        for shelf in self.shelves:
            for i in range(1, len(shelf)-1):
                # if any([name fobrand1 in shelf[i].description]):
                if self.helper(brand1, shelf[i].description):
                    if self.helper2(brand2, [shelf[i-1].description, shelf[i+1].description]):
                        return False

        return True

    def is_at_eye_level(self, brand):
        """
        Returns whether brand is at eye level.
        :param brand: str
        :return: bool
        """
        for shelf in self.shelves:
            if shelf[0].shelf_height < 65.4 and shelf[0].shelf_height > 48: #change eye level in inches here
                for item in shelf:
                    if self.helper(brand, item.description):
                        return True

        return False

    def is_on_top_shelf(self, brand):
        """
        Returns whether brand is on the top shelf.
        :param brand: str
        :return: bool
        """
        for item in self.shelves[0]:
            if self.helper(brand, item.description):
                return True

        return False

    def is_in_vertical_block(self, brand):
        """
        Returns whether a brand is on every shelf in a consecutive vertical line.
        :param brand: str
        :return: bool
        """
        start_position = 0
        end_position = 0
        for i in range(len(self.shelves[0])): #Goes through top shelf looking for brand and identifies the start and
                                                #end position of that brand block
            if self.helper(brand, self.shelves[0][i].description):
                start_position = self.shelves[0][i].start_position
                end_position = self.shelves[0][i].end_position
                if self.length != end_position:
                    i += 1
                else:
                    break
                while i < len(self.shelves[0]) - 1 and self.helper(brand, self.shelves[0][i].description): #Ensures that the entire brand block is accounted for
                    end_position = self.shelves[0][i].end_position
                    if self.length != end_position:
                        i += 1
                    else:
                        break #assuming there is only one block per brand, we don't need to keep looking for more blocks on that shelf
                break

        if end_position == 0: #Tests if product is not on the top shelf
            return False

        for shelf in self.shelves[1:]:
            entered = False
            for i in range(len(shelf)):
                if self.helper(brand, shelf[i].description):
                    entered = True
                    #Brand block in the above shelf is stored in old start and end position below
                    old_start_position = start_position
                    old_end_position = end_position
                    start_position = shelf[i].start_position
                    end_position = shelf[i].end_position
                    i += 1
                    while i < len(shelf) - 1 and self.helper(brand, shelf[i].description): #Ensures the whole brand block is accounted for
                        end_position = shelf[i].end_position
                        if self.length != end_position:
                            i += 1
                        else:
                            break
                    if ((start_position >= old_start_position and start_position <= old_end_position) or
                        (end_position >= old_start_position and end_position <= old_end_position) or
                        start_position <= old_start_position and end_position >= old_end_position):
                    #Tests if the brand block above overlaps the current brand block in any way
                        break
                    else:
                        return False
            if not entered: #Tests to see if the brand existed on this shelf
                return False
        return True

    # def is_in_between(self, inner_brand, outer_brand1, outer_brand2):
    #     """
    #     Returns if inner_brand is in between outer_brand1 and outer_brand2 horizontally.
    #     :param inner_brand: str
    #     :param outer_brand1: str
    #     :param outer_brand2: str
    #     :return: bool
    #     """
    #     for shelf in self.shelves:
    #         if shelf[0].brand == inner_brand or shelf[-1].brand == inner_brand:
    #             return False
    #     for shelf in self.shelves:
    #         for i in range(1, len(shelf) - 1):
    #             left_brand = shelf[i-1].brand
    #             if shelf[i].brand == inner_brand:
    #                 if left_brand not in [outer_brand1, outer_brand2]:
    #                     return False
    #                 other_brand = ""
    #                 if left_brand == outer_brand1:
    #                     other_brand = outer_brand2
    #                 else:
    #                     other_brand = outer_brand1
    #                 i += 1
    #                 while shelf[i].brand == inner_brand:
    #                     i += 1
    #                 if shelf[i].brand != other_brand:
    #                     return False
    #                 else:
    #                     break
    #
    #     return True

    def is_not_in_between(self, inner_brand, outer_brand1, outer_brand2):
        """
        Returns if inner_brand is not in between outer_brand1 and outer_brand2 horizontally.
        :param inner_brand: str
        :param outer_brand1: str
        :param outer_brand2: str
        :return: bool
        """
        for shelf in self.shelves:
            for i in range(len(shelf)):
                if self.helper(outer_brand1, shelf[i].description):
                    other_brand = outer_brand2
                elif self.helper(outer_brand2, shelf[i].description):
                    other_brand = outer_brand1
                else:
                    continue
                i += 1
                if len(shelf) != i and self.helper(inner_brand, shelf[i].description):
                    while len(shelf) != i and self.helper(inner_brand, shelf[i].description):
                        i += 1
                    if len(shelf) == i:
                        break
                    if self.helper(other_brand, shelf[i].description):
                        return False
                continue
        return True

    def has_color_river(self, upcs):
        """
        Returns whether a color is on every shelf in a consecutive vertical line.
        :param color_number: list of str
        :return: bool
        """

        #Implemented same way as is_in_for vertical_block except color number instead of brand

        start_position = 0
        end_position = 0
        for i in range(len(self.shelves[0])):
            if str(int(self.shelves[0][i].upc)) in upcs:
                start_position = self.shelves[0][i].start_position
                end_position = self.shelves[0][i].end_position
                if self.length != end_position:
                    i += 1
                else:
                    break
                while i < len(self.shelves[0]) - 1 and str(int(self.shelves[0][i].upc)) in upcs:
                    end_position = self.shelves[0][i].end_position
                    if self.length != end_position:
                        i += 1
                    else:
                        break
                break

        if end_position == 0:
            return False

        for shelf in self.shelves[1:]:
            entered = False
            for i in range(len(shelf)):
                start_index = i
                if str(int(shelf[i].upc)) in upcs:
                    entered = True
                    old_start_position = start_position
                    old_end_position = end_position
                    start_position = shelf[i].start_position
                    end_position = shelf[i+1].end_position
                    i += 1
                    while str(int(shelf[i].upc)) in upcs:
                        end_position = shelf[i].end_position
                        if self.length != end_position:
                            i += 1
                        else:
                            break
                    if ((start_position >= old_start_position and start_position <= old_end_position) or
                            (end_position >= old_start_position and end_position <= old_end_position) or
                            (start_position <= old_start_position and end_position >= old_end_position)):
                        break
                    else:
                        return False
            if not entered:
                return False
        return True

    def upcs_on_shelf(self, upcs, shelf):
        """
        Tests to see if the specified upcs are on the specified shelf number
        :param upcs: list of str
        :param shelf: int
        :return: bool
        """
        for i in range(len(self.shelves)):
            for item in self.shelves[i]:
                if i != shelf and str(int(item.upc)) in upcs:
                    return False

        return True

    def upcs_not_on_shelf(self, upcs, shelf):
        """
        Tests to see if the specified upcs are on the specified shelf number
        :param upcs: list of str
        :param shelf: int
        :return: bool
        """
        for item in self.shelves[shelf]:
            if str(int(item.upc)) in upcs:
                return False

        return True

    def has_color_hotspot(self, upcs):
        """
        Tests for a rectangle or square of specified upcs.
        :param upcs: list of str
        :return: bool
        """
        vertical_shelves = 0
        start_position = 0
        end_position = 0
        for i in range(len(self.shelves[0])):
            if str(int(self.shelves[0][i].upc)) in upcs:
                vertical_shelves += 1
                start_position = self.shelves[0][i].start_position
                end_position = self.shelves[0][i].end_position
                if self.length != end_position:
                    i += 1
                else:
                    break
                while i < len(self.shelves[0]) - 1 and str(int(self.shelves[0][i].upc)) in upcs:
                    end_position = self.shelves[0][i].end_position
                    if self.length != end_position:
                        i += 1
                    else:
                        break
                break

        for shelf in self.shelves[1:]:
            entered = False
            for i in range(len(shelf)):
                start_index = i
                if str(int(shelf[i].upc)) in upcs:
                    vertical_shelves += 1
                    entered = True
                    old_start_position = start_position
                    old_end_position = end_position
                    start_position = shelf[i].start_position
                    try:
                        end_position = shelf[i + 1].end_position
                        i += 1
                    except:
                        pass
                    i += 1
                    while i < len(shelf) and str(int(shelf[i].upc)) in upcs:
                        end_position = shelf[i].end_position
                        if self.length != end_position:
                            i += 1
                        else:
                            break
                    if ((start_position >= old_start_position and start_position <= old_end_position) or
                            (end_position >= old_start_position and end_position <= old_end_position) or
                            (start_position <= old_start_position and end_position >= old_end_position)):
                        break

        horizontal = 0
        prior_min = 0
        prior_max = 0
        current_min = 0
        current_max = 0

        for shelf in self.shelves:
            for item in shelf:

                if str(int(item.upc)) in upcs:
                    horizontal += 1
                    if current_min == 0:
                        current_min = item.start_position
                        current_max = item.end_position
                    else:
                        current_max = item.end_position
                    if horizontal >= max(4, vertical_shelves):
                        return True
                    if ((current_min >= prior_min and current_min <= prior_max) or
                            (current_max >= prior_min and current_max <= prior_max) or
                            (current_min <= prior_min and current_max >= prior_max) and horizontal >= 2):
                        return True
                else:
                    horizontal = 0
                    prior_min = current_min
                    prior_max = current_max

        return False

    def is_leading_aisle(self, brand):
        """
        Returns if brand is the first brand on any of the shelves.
        :param brand: str
        :return: bool
        """
        for shelf in self.shelves:
            if self.helper(brand, shelf[0].description):
                return True

        return False

    def is_terminating_aisle(self, brand):
        """
        Returns if brand is the last brand on any of the shelves.
        :param brand: str
        :return: bool
        """
        for shelf in self.shelves:
            if self.helper(brand, shelf[-1].description):
                return True

        return False

    # def is_ordered_by_subcollection(self, brand, collections):
    #     """
    #     Returns if brand is organized from top to bottom by collections.
    #     :param brand: str
    #     :param collections: list of str
    #     :return: bool
    #     """
    #     item_flag = False
    #     brand_shelf = 0
    #     for shelf in self.shelves:
    #         for item in shelf:
    #             if self.helper(brand, item.description):
    #                 item_flag = True
    #                 if item.collection != collections[brand_shelf]:
    #                     return False
    #         if brand_shelf == len(collections) - 1:
    #             return True
    #         if item_flag:
    #             brand_shelf += 1

    # def is_in_regimen(self, brand, gender, first_form, second_form):
    #     """
    #     Returns if all brand regimens are shelved horizontally next to each other.
    #     :param brand: str
    #     :return: bool
    #     """
    #     for shelf in self.shelves:
    #         for i in range(len(shelf) - 1):
    #             right_item = shelf[i+1]
    #             if (shelf[i].brand == brand and shelf[i].gender == gender and
    #                 shelf[i].form == first_form):
    #                 if not(right_item.brand == brand and right_item.gender == gender and
    #                        right_item.form == second_form):
    #                     return False
    #
    #     return True

    def percentage_at_eye_level(self, percentage, brand):
        """
        Returns whether brand is at at least percentage at eye level.
        :param percentage: float
        :param brand: str
        :return: bool
        """
        total_product = 0
        eye_level = 0
        for shelf in self.shelves:
            for item in shelf:
                if self.helper(brand, item.description):
                    total_product += 1
                    if item.shelf_height <= 65.4 and item.shelf_height >= 48:
                        eye_level += 1

        return eye_level/total_product >= percentage

    def is_percentage_of_brand(self, subbrands, brand, percentage):
        """
        Returns whether subbrand is greater than percentage of brand in the aisle
        :param subbrand: list of str
        :param brand: str
        :return: bool
        """
        no_brand = 0
        no_subbrand = 0
        for shelf in self.shelves:
            for item in shelf:
                if self.helper(brand, item.description):
                    no_brand += 1
                for subbrand in subbrands:
                    if self.helper(subbrand, item.description):
                        no_subbrand += 1
        try:
            return no_subbrand/no_brand > 0.5
        except:
            return False

    def is_on_third_shelf(self, brand):
        """
        Returns whether brand is on the third shelf.
        :param brand: str
        :return: bool
        """
        flag = False
        for item in self.shelves[2]:
            if self.helper(brand, item.description):
                flag = True
        if not flag:
            return False
        for shelf in self.shelves[:1]:
            for item in shelf:
                if self.helper(brand, item.description):
                    return False
        for shelf in self.shelves[3:]:
            for item in shelf:
                if self.helper(brand, item.description):
                    return False

        return True

    def is_on_fourth_shelf(self, brand):
        """
        Returns whether brand is on the third shelf.
        :param brand: str
        :return: bool
        """
        flag = False
        for item in self.shelves[3]:
            if self.helper(brand, item.description):
                flag = True
        if not flag:
            return False
        for shelf in self.shelves[:2]:
            for item in shelf:
                if self.helper(brand, item.description):
                    return False
        for shelf in self.shelves[4:]:
            for item in shelf:
                if self.helper(brand, item.description):
                    return False

        return True

    def is_on_second_shelf(self, brand):
        """
        Returns whether brand is on the second shelf.
        :param brand: str
        :return: bool
        """
        flag = False
        for item in self.shelves[1]:
            if self.helper(brand, item.description):
                flag = True
        if not flag:
            return False
        for shelf in self.shelves[:2]:
            for item in shelf:
                if self.helper(brand, item.description):
                    return False
        for shelf in self.shelves[4:]:
            for item in shelf:
                if self.helper(brand, item.description):
                    return False

        return True

    def is_on_bottom_shelf(self, brand):
        """
        Returns whether brand is on the top shelf.
        :param brand: str
        :return: bool
        """
        for item in self.shelves[-1]:
            if self.helper(brand, item.description):
                return True

        return False

    def is_on_shelf(self, brand):
        """
        Returns whether brand is on the shelf.
        :param brand: str
        :return: bool
        """
        for shelf in self.shelves:
            for item in shelf:
                if self.helper(brand, item.description):
                    return True

        return False