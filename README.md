# PyBank Slip

PyBank Slip is an independent, modern, and robust Python library designed to unify and simplify communication with bank slip (Boleto and Pix) APIs in Brazil. It manages all the complexity of authentication (OAuth2 and mTLS) and abstracts the bank routes, allowing your application (like ERPs or E-commerces) to focus solely on building the bank slip payload.

---

## 🏦 Supported Banks

The library currently supports the V2 APIs of the following institutions:
- **Banco do Brasil** (API de Cobranças V2)
- **Santander** (API de Cobrança / Workspace V2)

---

## ⚙️ How it Works?

The library adopts the **Factory/Adapter** design pattern. The core focuses on the `BankSlipManager`, which receives the global credentials and the target bank, and returns an instance (Adapter) ready for use. The Adapter handles:
1. Automatically fetching the **Access Token (Bearer)** using the credentials.
2. Attaching the **ICP-Brasil Certificate (mTLS)** required by the APIs.
3. Defensive handling against malformed payloads (`safe_json_loads`) returned by the bank servers (e.g., truncated JSONs or invalid fields).
4. Managing the selected environment (Production vs Sandbox).

---

## 📌 Required Parameters

The library requires configurations in three main areas:

### 1. `OAuthCredentials`
A structure that stores the App data created in the bank's developer portal:
- `client_id`: The Client ID (App ID).
- `client_secret`: The Client Secret.
- `app_key` (Optional): Primarily used by Banco do Brasil (gw-dev-app-key).

### 2. `CertificateAuth` (mTLS)
Digital certificate configuration for two-way SSL/TLS encryption (required by Santander and BB).
- `cert_path`: Absolute path to the `.pem` file of the client certificate (Public Key).
- `key_path`: Absolute path to the `.pem` file of the private key.

### 3. Manager/Adapter 
Parameters passed when instantiating the adapter:
- `bank`: Bank string identifier (`'bb'` or `'santander'`).
- `credentials`: Instance of `OAuthCredentials`.
- `environment`: Environment string (`'production'` or `'sandbox'`).
- `cert_auth`: Instance of `CertificateAuth`.
- `workspace_id` (Only Santander): The financial workspace ID.

---

## 🚀 Abstracted Routes and Features

Each Adapter abstracts the raw HTTP calls into the following built-in methods:

### `generate_bank_slip(payload: dict)`
Sends the bank slip registration request.
- **Banco do Brasil:** `POST /cobrancas/v2/boletos`
- **Santander:** `POST /collection_bill_management/v2/workspaces/{workspace_id}/bank_slips`

### `list_bank_slips(filters: dict)`
Queries issued bank slips using filters (Document, Date, etc).
- **Banco do Brasil:** `GET /cobrancas/v2/boletos`
- **Santander:** `GET /collection_bill_management/v2/workspaces/{workspace_id}/bank_slips`

### `cancel_bank_slip(bank_slip_id: str, payload: dict)`
Requests the cancellation/write-off of the bank slip.
- **Banco do Brasil:** `POST /cobrancas/v2/boletos/{id}/baixar`
- **Santander:** `PATCH /collection_bill_management/v2/workspaces/{workspace_id}/bank_slips/{id}`

### `edit_bank_slip(bank_slip_id: str, payload: dict)`
Allows editing conditions (Due Date, Value, Discounts) of the bank slip.
- **Banco do Brasil:** `PATCH /cobrancas/v2/boletos/{id}`
- **Santander:** `PATCH /collection_bill_management/v2/workspaces/{workspace_id}/bank_slips/{id}`

*(For Santander, there are also exclusive utility methods such as `search_workspaces` inside the Adapter).*

---

## 💻 Practical Usage Example

```python
from pybank_slip import BankSlipManager, OAuthCredentials, CertificateAuth

# 1. Setup Credentials
credentials = OAuthCredentials(
    client_id="your_client_id",
    client_secret="your_client_secret",
    app_key="bb_key"  # If using Banco do Brasil
)

# 2. Setup Certificates
cert_auth = CertificateAuth(
    cert_path="/path/to/cert.pem",
    key_path="/path/to/key.pem"
)

# 3. Generate Adapter (Factory)
adapter = BankSlipManager.get_adapter(
    bank="bb",
    credentials=credentials,
    environment="sandbox",
    cert_auth=cert_auth
)

# 4. Call the desired feature
payload_boleto = { ... } # Your JSON dictionary matching the bank's schema
response = adapter.generate_bank_slip(payload_boleto)
print(response)
```
