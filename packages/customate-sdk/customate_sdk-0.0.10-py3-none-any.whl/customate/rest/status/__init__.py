# coding=utf-8

from customate.api_resources.abstract.domain import Domain

class Status(Domain):

    def __init__(self, customate, base_url, domain, version, **kwargs):
        """
        Initialize the Status Domain
        """
        super(Status, self).__init__(customate)
        self.base_url = base_url
        self.domain = domain
        self.version = version


    def __repr__(self):
        """
        Provide a friendly representation
        :returns: Machine friendly representation
        :rtype: str
        """
        return '<Customate.Status>'
