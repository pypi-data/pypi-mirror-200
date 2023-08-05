# coding=utf-8

from customate.api_resources.abstract.domain import Domain

class OpenBankingToWalletMandate(Domain):

    def __init__(self, customate, base_url, domain, version ,**kwargs):
        """
        Initialize the Open bank Mandate Domain
        """
        super(OpenBankingToWalletMandate, self).__init__(customate)
        self.base_url = base_url
        self.domain = domain
        self.version = version


    def __repr__(self):
        """
        Provide a friendly representation
        :returns: Machine friendly representation
        :rtype: str
        """
        return '<Customate.OpenBankingToWalletMandate>'
