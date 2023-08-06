from v6e_utils.agil_connect.agil_connect import AgilConnection


class PanelOwners(AgilConnection):
    def __init__(self, url=None):
        super().__init__(url)
        self.set_api_endpoint('panel/owners')

    def get_panel_owners(self):
        url = self.ensure_url(self.gateway_url, self.api_endpoint)
        return self.get_result(url)

    def get_panel_owners_as_list(self):
        try:
            owners = self.get_panel_owners()
            options = [(owner['id'], owner['name']) for owner in owners]
        except Exception as e:
            print(f"Error: {e}")
            options = []
        return options


class PanelBanks(AgilConnection):
    def __init__(self, url=None):
        super().__init__(url)
        self.set_api_endpoint('panel/banks')

    def get_panel_banks(self, owner=None):
        url = self.ensure_url(self.gateway_url, self.api_endpoint)
        return self.post_data(url, data={'owner': owner})

    def get_panel_banks_as_list(self, owner=None):
        try:
            banks = self.get_panel_banks(owner=owner)
            options = [(bank['id'], bank['description']) for bank in banks]
        except Exception as e:
            print(f"Error: {e}")
            options = []
        return options
