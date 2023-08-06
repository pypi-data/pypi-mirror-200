class Utils:
    @staticmethod
    def get_s3_paths_from_assets(assets):
        return [asset['models'][0]['path'] for asset in assets if asset['models']]
