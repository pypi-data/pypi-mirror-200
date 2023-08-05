import logging
from aws_cost_optimization_13.utils import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


class elb:
    def elb_costing(self, data: dict) -> dict:
        """
        :param data:
        :return:
        """
        logger.info(" ---Inside _elb_costing :: elb :: elb_costing()--- ")

        region = data['Metadata']['Region']

        resolved_region = self.aws_region_map[region]

        filters = lambda elb_type: [
            {
                'Type': 'TERM_MATCH',
                'Field': 'productFamily',
                'Value': elb_type
            },
            {
                'Type': 'TERM_MATCH',
                'Field': 'location',
                'Value': resolved_region
            }
        ]
        elbtype = data['Metadata']['Type']
        if elbtype == 'application':
            filter_elb_type = filters('Load Balancer-Application')
        elif elbtype == filters('network'):
            filter_elb_type = 'Load Balancer-Network'
        elif elbtype == 'gateway':
            filter_elb_type = filters('Load Balancer-Gateway')
        else:
            return {
                'Current Cost': 0,
                'Effective Cost': 0,
                'Savings': 0,
                'Savings %': 0
            }

        price = get_pricing(self.session, region, 'AWSELB', filter_elb_type, service_name='elb')

        print(price)