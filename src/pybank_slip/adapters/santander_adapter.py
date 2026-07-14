import requests
from typing import Dict, Any, Optional
from ..interfaces import BaseBankAdapter
from ..auth import OAuthCredentials, CertificateAuth

class SantanderAdapter(BaseBankAdapter):
    """
    Bank slip adapter for Santander API.
    """

    def __init__(self, credentials: OAuthCredentials, base_url: str, cert_auth: Optional[CertificateAuth] = None):
        self.credentials = credentials
        self.base_url = base_url.rstrip('/')
        self.cert_auth = cert_auth
        self._token = None

    def _get_token(self) -> str:
        """Fetches the OAuth2 Bearer token from Santander."""
        if self._token:
            return self._token
            
        payload = {"client_id": self.credentials.client_id, "grant_type": "client_credentials"}
        
        cert_args = {}
        if self.cert_auth:
            cert_args['cert'] = (self.cert_auth.cert_path, self.cert_auth.key_path)
            cert_args['verify'] = self.cert_auth.verify
            
        response = requests.post(
            self.credentials.token_url,
            data=payload,
            auth=(self.credentials.client_id, self.credentials.client_secret),
            **cert_args
        )
        response.raise_for_status()
        self._token = response.json().get("access_token")
        return self._token

    def generate_bank_slip(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        token = self._get_token()
        workspace_id = self.credentials.workspace_id
        if not workspace_id:
            raise ValueError("Workspace ID is required for Santander bank slips.")
            
        url = f"{self.base_url}/workspaces/{workspace_id}/bank_slips"
        
        headers = {
            "Authorization": f"Bearer {token}",
            "X-Application-Key": self.credentials.client_id,
            "Accept": "*/*",
            "Content-Type": "application/json",
        }
        
        cert_args = {}
        if self.cert_auth:
            cert_args['cert'] = (self.cert_auth.cert_path, self.cert_auth.key_path)
            cert_args['verify'] = self.cert_auth.verify
            
        response = requests.post(url=url, json=payload, headers=headers, **cert_args)
        response.raise_for_status()
        return response.json()

    def list_bank_slips(self, filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        raise NotImplementedError("List bank slips is not yet implemented for Santander.")

    def cancel_bank_slip(self, bank_slip_id: str, payload: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        raise NotImplementedError("Cancel bank slip must use edit_bank_slip (patch) with the cancel payload in Santander.")

    def edit_bank_slip(self, bank_slip_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        token = self._get_token()
        workspace_id = self.credentials.workspace_id
        url = f"{self.base_url}/workspaces/{workspace_id}/bank_slips"
        
        headers = {
            "Authorization": f"Bearer {token}",
            "X-Application-Key": self.credentials.client_id,
            "Accept": "*/*",
            "Content-Type": "application/json",
        }
        
        cert_args = {}
        if self.cert_auth:
            cert_args['cert'] = (self.cert_auth.cert_path, self.cert_auth.key_path)
            cert_args['verify'] = self.cert_auth.verify
            
        response = requests.patch(url=url, json=payload, headers=headers, **cert_args)
        response.raise_for_status()
        return response.json()

    # Santander Specific Methods
    def register_workspace(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        token = self._get_token()
        url = f"{self.base_url}/workspaces"
        headers = {
            "Authorization": f"Bearer {token}",
            "X-Application-Key": self.credentials.client_id,
            "Content-Type": "application/json",
        }
        
        cert_args = {}
        if self.cert_auth:
            cert_args['cert'] = (self.cert_auth.cert_path, self.cert_auth.key_path)
            cert_args['verify'] = self.cert_auth.verify
            
        response = requests.post(url=url, json=payload, headers=headers, **cert_args)
        response.raise_for_status()
        return response.json()

    def list_workspaces(self) -> Dict[str, Any]:
        token = self._get_token()
        url = f"{self.base_url}/workspaces"
        headers = {
            "Authorization": f"Bearer {token}",
            "X-Application-Key": self.credentials.client_id,
        }
        cert_args = {}
        if self.cert_auth:
            cert_args['cert'] = (self.cert_auth.cert_path, self.cert_auth.key_path)
            cert_args['verify'] = self.cert_auth.verify
            
        response = requests.get(url=url, headers=headers, **cert_args)
        response.raise_for_status()
        return response.json()

    def delete_workspace(self, workspace_id: str) -> None:
        token = self._get_token()
        url = f"{self.base_url}/workspaces/{workspace_id}"
        headers = {
            "Authorization": f"Bearer {token}",
            "X-Application-Key": self.credentials.client_id,
        }
        cert_args = {}
        if self.cert_auth:
            cert_args['cert'] = (self.cert_auth.cert_path, self.cert_auth.key_path)
            cert_args['verify'] = self.cert_auth.verify
            
        response = requests.delete(url=url, headers=headers, **cert_args)
        response.raise_for_status()
