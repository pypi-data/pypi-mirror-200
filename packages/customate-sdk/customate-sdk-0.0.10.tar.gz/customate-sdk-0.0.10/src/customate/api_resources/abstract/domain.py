
class Domain(object):
    """
    Abstract class used in each domain/endpoint

    Makes an HTTP request to this domain.
        :param dict params: Query parameters.
        :param object data: The request body.
        :param dict headers: The HTTP headers.
        :param tuple auth: Basic auth tuple of (api_key, secret)
    """
    def __init__(self, customate):
        self.customate = customate

    def post(self, params=None, data=None, headers=None, auth=None, profile_id=None, domain_id=None, domain_action=None):
        return self.customate.request(
            'post',
            self.base_url,
            self.domain,
            self.version,
            params=params,
            data=data,
            headers=headers,
            auth=auth,
            profile_id=profile_id,
            domain_id=domain_id,
            domain_action=domain_action
        )

    def get(self, params=None, data=None, headers=None, auth=None, profile_id=None, domain_id=None, domain_action=None):
        return self.customate.request(
            'get',
            self.base_url,
            self.domain,
            self.version,
            params=params,
            data=data,
            headers=headers,
            auth=auth,
            profile_id=profile_id,
            domain_id=domain_id,
            domain_action=domain_action
        )

    def put(self, params=None, data=None, headers=None, auth=None, profile_id=None, domain_id=None, domain_action=None):
        return self.customate.request(
            'put',
            self.base_url,
            self.domain,
            self.version,
            params=params,
            data=data,
            headers=headers,
            auth=auth,
            profile_id=profile_id,
            domain_id=domain_id,
            domain_action=domain_action
        )

    def delete(self, params=None, data=None, headers=None, auth=None, profile_id=None, domain_id=None, domain_action=None):
        return self.customate.request(
            'delete',
            self.base_url,
            self.domain,
            self.version,
            params=params,
            data=data,
            headers=headers,
            auth=auth,
            profile_id=profile_id,
            domain_id=domain_id,
            domain_action=domain_action
        )

