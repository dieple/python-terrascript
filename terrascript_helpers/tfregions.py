import boto3

ssm = boto3.client('ssm')


class Regions:
    @classmethod
    def get_regions(cls):
        short_codes = cls._get_region_short_codes()

        regions = [{
            'name': cls._get_region_long_name(sc),
            'code': sc
        } for sc in short_codes]

        regions_sorted = sorted(
            regions,
            key=lambda k: k['name']
        )

        return regions_sorted

    @classmethod
    def _get_region_long_name(cls, short_code):
        param_name = (
            '/aws/service/global-infrastructure/regions/'
            f'{short_code}/longName'
        )
        response = ssm.get_parameters(
            Names=[param_name]
        )
        return response['Parameters'][0]['Value']

    @classmethod
    def _get_region_short_codes(cls):
        output = set()
        for page in ssm.get_paginator('get_parameters_by_path').paginate(
                Path='/aws/service/global-infrastructure/regions'
        ):
            output.update(p['Value'] for p in page['Parameters'])

        return output