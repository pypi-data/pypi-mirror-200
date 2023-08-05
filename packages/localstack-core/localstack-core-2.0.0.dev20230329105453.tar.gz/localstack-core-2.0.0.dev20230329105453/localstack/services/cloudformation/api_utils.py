import logging
import re
from urllib.parse import urlparse

from requests.structures import CaseInsensitiveDict

from localstack import config, constants
from localstack.services.s3 import s3_listener, s3_utils
from localstack.utils.aws import aws_stack
from localstack.utils.functions import run_safe
from localstack.utils.http import safe_requests
from localstack.utils.strings import to_str

LOG = logging.getLogger(__name__)


def prepare_template_body(req_data: dict) -> str | bytes | None:  # TODO: mutating and returning
    template_url = req_data.get("TemplateURL")
    if template_url:
        req_data["TemplateURL"] = convert_s3_to_local_url(template_url)
    url = req_data.get("TemplateURL", "")
    if is_local_service_url(url):
        modified_template_body = get_template_body(req_data)
        if modified_template_body:
            req_data.pop("TemplateURL", None)
            req_data["TemplateBody"] = modified_template_body
    modified_template_body = get_template_body(req_data)
    if modified_template_body:
        req_data["TemplateBody"] = modified_template_body
    return modified_template_body


def get_template_body(req_data: dict) -> str:
    body = req_data.get("TemplateBody")
    if body:
        return body
    url = req_data.get("TemplateURL")
    if url:
        response = run_safe(lambda: safe_requests.get(url, verify=False))
        # check error codes, and code 301 - fixes https://github.com/localstack/localstack/issues/1884
        status_code = 0 if response is None else response.status_code
        if response is None or status_code == 301 or status_code >= 400:
            # check if this is an S3 URL, then get the file directly from there
            url = convert_s3_to_local_url(url)
            if is_local_service_url(url):
                parsed_path = urlparse(url).path.lstrip("/")
                parts = parsed_path.partition("/")
                client = aws_stack.connect_to_service("s3")
                LOG.debug(
                    "Download CloudFormation template content from local S3: %s - %s",
                    parts[0],
                    parts[2],
                )
                result = client.get_object(Bucket=parts[0], Key=parts[2])
                body = to_str(result["Body"].read())
                return body
            raise Exception(
                "Unable to fetch template body (code %s) from URL %s" % (status_code, url)
            )
        return to_str(response.content)
    raise Exception("Unable to get template body from input: %s" % req_data)


def is_local_service_url(url: str) -> bool:
    if not url:
        return False
    candidates = (
        constants.LOCALHOST,
        constants.LOCALHOST_HOSTNAME,
        config.LOCALSTACK_HOSTNAME,
        config.HOSTNAME_EXTERNAL,
    )
    if any(re.match(r"^[^:]+://[^:/]*%s([:/]|$)" % host, url) for host in candidates):
        return True
    host = url.split("://")[-1].split("/")[0]
    return "localhost" in host


def convert_s3_to_local_url(url: str) -> str:
    url_parsed = urlparse(url)
    path = url_parsed.path

    headers = CaseInsensitiveDict({"Host": url_parsed.netloc})
    bucket_name = s3_utils.extract_bucket_name(headers, path)
    key_name = s3_utils.extract_key_name(headers, path)

    # note: make sure to normalize the bucket name here!
    bucket_name = s3_listener.normalize_bucket_name(bucket_name)
    local_url = f"{config.service_url('s3')}/{bucket_name}/{key_name}"
    return local_url
