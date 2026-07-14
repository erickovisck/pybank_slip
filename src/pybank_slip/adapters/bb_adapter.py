import requests
from typing import Dict, Any, Optional
from ..interfaces import BaseBankAdapter
from ..auth import CertificateAuth, OAuthCredentials
from requests.auth import HTTPBasicAuth

class BancoDoBrasilAdapter(BaseBankAdapter):
    def _set_urls(self):
        if self.environment == 'sandbox':
            self.base_url = "https://api.hm.bb.com.br"
            self.token_url = "https://oauth.hm.bb.com.br/oauth/token"
        else:
            self.base_url = "https://api.bb.com.br"
            self.token_url = "https://oauth.bb.com.br/oauth/token"
            
        self.route_bank_slips = "/cobrancas/v2/boletos"

    """
    Bank slip adapter for Banco do Brasil API V2.
    """

    def __init__(self, credentials: OAuthCredentials, environment: str = 'production', cert_auth: Optional[CertificateAuth] = None):
        super().__init__(credentials, environment, cert_auth)
        self._token = None

    def _get_token(self) -> str:
        """Fetches the OAuth2 Bearer token from Banco do Brasil."""
        if self._token:
            return self._token

        payload = {"grant_type": "client_credentials", "scope": "cobrancas.boletos-info cobrancas.boletos-requisicao"}
        
        response = requests.post(
            self.token_url,
            data=payload,
            auth=HTTPBasicAuth(self.credentials.client_id, self.credentials.client_secret),
            cert=(self.cert_auth.cert_path, self.cert_auth.key_path),
            verify=self.cert_auth.verify,
        )
        response.raise_for_status()
        self._token = response.json().get("access_token")
        return self._token

    def generate_bank_slip(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        token = self._get_token()
        # Ensure the query string uses the correct app_key variable as defined in the credentials
        app_key_qs = f"?gw-dev-app-key={self.credentials.app_key}"
        url = f"{self.base_url}/boletos{app_key_qs}"
        
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        
        response = requests.post(
            url=url,
            json=payload,
            headers=headers,
            cert=(self.cert_auth.cert_path, self.cert_auth.key_path),
            verify=self.cert_auth.verify,
        )
        response.raise_for_status()
        return response.json()

    def list_bank_slips(self, filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        token = self._get_token()
        app_key_qs = f"?gw-dev-app-key={self.credentials.app_key}"
        url = f"{self.base_url}/boletos{app_key_qs}"
        
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
        }
        
        response = requests.get(
            url=url,
            params=filters,
            headers=headers,
            cert=(self.cert_auth.cert_path, self.cert_auth.key_path),
            verify=self.cert_auth.verify,
        )
        response.raise_for_status()
        return response.json()

    def cancel_bank_slip(self, bank_slip_id: str, payload: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        token = self._get_token()
        url = f"{self.base_url}/boletos/{bank_slip_id}/baixar"
        
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        
        if not payload:
            payload = {"numeroConvenio": ""} # Must be filled by the caller
            
        response = requests.post(
            url=url,
            json=payload,
            headers=headers,
            cert=(self.cert_auth.cert_path, self.cert_auth.key_path),
            verify=self.cert_auth.verify,
        )
        response.raise_for_status()
        return response.json()

    def edit_bank_slip(self, bank_slip_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        token = self._get_token()
        app_key_qs = f"?gw-dev-app-key={self.credentials.app_key}"
        url = f"{self.base_url}/boletos/{bank_slip_id}{app_key_qs}"
        
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        
        response = requests.patch(
            url=url,
            json=payload,
            headers=headers,
            cert=(self.cert_auth.cert_path, self.cert_auth.key_path),
            verify=self.cert_auth.verify,
        )
        response.raise_for_status()
        return response.json()
