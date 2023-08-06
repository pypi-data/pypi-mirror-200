import boto3
from typing import List, Dict, Optional


class Ecs(object):
    def __init__(self, session: boto3.session.Session = None, region: str = None):
        """
        Creates a client using either the boto3 Session or region.
        param session: required when no region is provided
        param region: required when no session is provided
        """
        if session and region:
            raise EnvironmentError('1 of session or region must be provided')

        if session:
            self.client = session.client(
                service_name='ecs',
            )
        elif region:
            self.client = boto3.client(
                service_name='ecs',
                region_name=region
            )

    def get_clusters(self, cluster_names: List[str], include_info: Optional[List[str]] = None) -> Dict:
        response = self.client.describe_clusters(
            clusters=cluster_names,
            include=include_info
        )
        clusters = response.get('clusters', [])

        return clusters


