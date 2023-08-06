import boto3
from typing import List, Dict


class Config(object):
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
                service_name='config',
            )
        elif region:
            self.client = boto3.client(
                service_name='config',
                region_name=region
            )

    def describe_config_rules(self) -> List:
        """
        Returns a list with details about all Config rules
        :return:
        """

        response = self.client.describe_config_rules()
        next_token = response.get('NextToken')
        rules = response.get('ConfigRules', [])

        while next_token:
            response = self.client.get_resources(
                NextToken=response.get('NextToken'),
            )
            next_token = response.get('NextToken')
            rules += response.get('ConfigRules', [])

        return rules

    def get_rule_compliance_status(self, rule_name: str) -> str:
        """
        Returns whether the specified Config rule is compliant
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Client.describe_compliance_by_config_rule
        :param rule_name: the name of the config rule to describe
        :return:describe_compliance response
        """
        response = self.client.describe_compliance_by_config_rule(
            ConfigRuleNames=[
                rule_name,
            ],
        )
        compliance = response.get('ComplianceByConfigRules')[0]['Compliance']['ComplianceType']

        return compliance

    def get_rule_compliance_details(self, rule_name: str) -> List:
        """
        Returns the evaluation results for the specified Config rule.
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Client.get_compliance_details_by_config_rule
        :rule_name: The name of the config rule
        :return: get_rule_compliance_details response
        """

        response = self.client.get_compliance_details_by_config_rule(ConfigRuleName=rule_name)
        eval_results = response.get('EvaluationResults', [])
        next_token = response.get('NextToken')

        while next_token:
            response = self.client.get_compliance_details_by_config_rule(
                ConfigRuleName=rule_name,
                NextToken=response.get('NextToken'),
                Limit=100
            )
            next_token = response.get('NextToken')
            eval_results += response.get('EvaluationResults', [])

        return eval_results

    def start_config_rules_evaluation(self, rule_names: List[str]) -> Dict:
        """
        On-demand evaluation for the specified rules against the last known configuration state of the resources
        Can only be run from ACCOUNTADMIN or higher
        :param rule_names: the names of the rules to evaluation in a list
        :return: start_config_rules_evaluation response
        """
        response = self.client.start_config_rules_evaluation(
            ConfigRuleNames=rule_names
        )

        return response
