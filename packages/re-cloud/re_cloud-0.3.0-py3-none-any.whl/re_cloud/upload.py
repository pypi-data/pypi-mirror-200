from re_cloud.config.utils import read_re_data_config
import requests
import json
import time
import base64
import Crypto.Signature.PKCS1_v1_5 as PKCS1_v1_5
import Crypto.PublicKey.RSA as RSA
import Crypto.Hash.SHA256 as SHA256
import mimetypes
from rich import print
from os import path
import click

DEFAULT_BASE_URL = "https://cloud.getre.io"


def get_id_token(service_account_path, iap_client_id):
    oauth_token_uri = "https://www.googleapis.com/oauth2/v4/token"
    with open(service_account_path, "r") as f:
        service_account = json.load(f)
    private_key_id = service_account.get("private_key_id")
    client_email = service_account.get("client_email")
    private_key = service_account.get("private_key")
    issued_at = time.time()
    expires_at = issued_at + 3600
    header = f"{{'alg':'RS256','typ':'JWT','kid':'{private_key_id}'}}"
    header_base64 = base64.urlsafe_b64encode(header.encode("utf-8")).decode("utf-8")
    payload = f"{{'iss':'{client_email}','aud':'{oauth_token_uri}','exp':{expires_at},'iat':{issued_at},'sub':'{client_email}','target_audience':'{iap_client_id}'}}"
    payload_base64 = base64.urlsafe_b64encode(payload.encode("utf-8")).decode("utf-8")
    key = RSA.importKey(private_key)
    # Create an PKCS1_v1_5 object
    signer = PKCS1_v1_5.new(key)
    msg_hash = SHA256.new((header_base64 + "." + payload_base64).encode("utf-8"))
    signature_base64 = base64.urlsafe_b64encode(signer.sign(msg_hash)).decode("utf-8")
    jwt_complete = (
        header_base64 + "." + payload_base64 + "." + signature_base64
    ).encode("utf-8")
    data = {
        "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
        "assertion": jwt_complete,
    }
    r = requests.post(url="https://accounts.google.com/o/oauth2/token", data=data)
    r = r.json()
    return r.get("id_token")


def upload_files(upload_type, dir_path, file_paths=None, **kwargs):
    channel_name_or_id = kwargs.get("channel_name_or_id")
    config_dir = kwargs.get("config_dir")
    name = kwargs.get("name")

    config = read_re_data_config(config_dir)

    re_cloud_config = config.get("re_cloud")
    BASE_URL = re_cloud_config.get("base_url") or DEFAULT_BASE_URL
    API_KEY = re_cloud_config.get("api_key")
    PROJECT_ID = re_cloud_config.get("project_id")
    SERVICE_ACCOUNT_PATH = re_cloud_config.get("service_account_path")
    IAP_CLIENT_ID = re_cloud_config.get("iap_client_id")
    is_staging_environment = BASE_URL.startswith("https://staging.getre.io")
    headers = {"Content-Type": "application/json"}
    if is_staging_environment:
        print("Staging environment detected, attempting to retrieve IAP id_token")
        signed_jwt = get_id_token(SERVICE_ACCOUNT_PATH, IAP_CLIENT_ID)
        print("Retrieved IAP id_token")
        headers["Authorization"] = f"Bearer {signed_jwt}"

    request_data = {
        "api_key": API_KEY,
        "project_id": PROJECT_ID,
        "upload_type": upload_type,
        "channel_name_or_id": channel_name_or_id,
    }
    if name:
        request_data["name"] = name
    request_data["file_paths"] = file_paths

    r = requests.post(f"{BASE_URL}/uploads", json=request_data, headers=headers)
    if r.status_code != 200:
        print(f"Upload failed. Status code is {r.status_code}")
        print(r.text)
        return
    response = r.json()
    response_data = response.get("data")
    if response.get("status") != "success":
        print("Upload failed")
        print(r.text)
        return
    upload_data = response_data.get("upload") or {}
    upload_urls = response_data.get("upload_urls") or {}

    print("Uploading report to re_cloud")

    if not file_paths:
        raise click.ClickException(
            "No files to upload found at the expected path: {}".format(dir_path)
        )

    for f in file_paths:
        target = path.join("" if not dir_path else dir_path, f)
        upload_file(target, upload_urls.get(f))
        print(f"Uploading {f} done")

    request_data = {"api_key": API_KEY}
    r = requests.put(
        f"{BASE_URL}/uploads/{upload_data['id']}/", json=request_data, headers=headers
    )
    if r.status_code != 200:
        print("Upload failed")
        print(r.text)
        return

    target_url = f"{BASE_URL}/uploads/{upload_data['id']}/"
    print(
        f"Upload complete. You can view your report here! [link={target_url}]{target_url}[/link]"
    )


def upload_file(target_file, upload_url):
    mimetype = mimetypes.guess_type(target_file)[0] or "application/octet-stream"
    with open(target_file, "rb") as f:
        data = f.read()
        res = requests.put(
            url=upload_url, data=data, headers={"Content-Type": mimetype}
        )
        _ = f"""
            Status code is {res.status_code}

            Uploaded {target_file} successfully!
        """
