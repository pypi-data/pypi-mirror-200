class Filter:
    @staticmethod
    def filter_by_number(assets, filter_criteria, greater_than=None, less_than=None):
        if greater_than is not None and less_than is not None:
            return list(
                filter(lambda asset: greater_than < asset['models'][0][filter_criteria] < less_than, assets))

        if greater_than is not None:
            return list(
                filter(lambda asset: asset['models'][0][filter_criteria] > greater_than, assets))

        if less_than is not None:
            return list(
                filter(lambda asset: asset['models'][0][filter_criteria] < less_than, assets))

        return assets

    @staticmethod
    def filter_by_string(assets, filter_criteria, equal_to):
        if filter_criteria is not None or filter_criteria != "":
            return list(
                filter(lambda asset: asset['models'][0][filter_criteria].lower() == equal_to.lower(), assets))

        return assets

