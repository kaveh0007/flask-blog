from typing import Set
from urllib.parse import urlparse
from secrets import token_hex
from flask import current_app, flash
from werkzeug.datastructures import FileStorage
from PIL import Image
import jwt
from datetime import datetime, timezone, timedelta

def check_url_scheme_and_authority(url: str, allowed_hosts: Set[str]) -> bool:
    """
    Used to prevent open redirects in the flask application.\n
    Allowed arguments:
    - url : The URL string you want to check (full url or authority).
    - allowed_hosts : Set of Strings of hosts you want to allow (with scheme and host and optionally with port).
    """
    if not url:
        return False

    allowed_netloc = set()

    parsed_url_target = urlparse(url)
    scheme_target = parsed_url_target.scheme
    netloc_target = parsed_url_target.netloc

    if not scheme_target and not netloc_target:
        return True

    if (not scheme_target and netloc_target) or (scheme_target and not netloc_target):
        return False

    if scheme_target not in ["http", "https"]:
        return False

    for host in allowed_hosts:
        parsed_url_host = urlparse(host)
        netloc_host = parsed_url_host.netloc
        allowed_netloc.add(netloc_host) if netloc_host else allowed_netloc.add(host)

    return netloc_target in allowed_netloc

def handle_pfp_uploads(image_file: FileStorage) -> str:
    """
    Used to handle image uploads in requests to change the profile picture of the user account.\n
    Allowed Arguments:
    - image_file : A `werkzeug.datastructures.FileStorage` object.
    """
    expected_size = (125, 125)
    name_on_disk = token_hex(8)
    _, extension = image_file.filename.split(".")

    filename = ".".join([name_on_disk, extension])
    location_on_disk = f"{current_app.config['UPLOAD_FOLDER']}/{filename}"

    resized_image_file = Image.open(image_file.stream)
    resized_image_file.thumbnail(expected_size)

    resized_image_file.save(location_on_disk)
    return filename

def create_jwt(user_id: int) -> str:
    """
    Generates a time bound JSON Web Token (JWT) to be sent to password reset emails.\n
    Allowed Arguments:
    - user_id : The `id` field of an ORM instance for `User`
    """
    expiration_time = datetime.now(timezone.utc)+timedelta(seconds=180)
    token = jwt.encode(payload={"exp" : expiration_time, "user_id" : user_id}, \
                       key=current_app.config['SECRET_KEY'], \
                        algorithm="HS256")
    return token

def verify_jwt(token) -> int|None:
    """
    Authenticates the JSON Web Token (JWT) and returns the `id` field of an ORM instance for `User`.\n
    Allowed Arguments:
    - token : A JSON Web Token (JWT)
    """
    try:
        data = jwt.decode(jwt=token, key=current_app.config['SECRET_KEY'], algorithms=["HS256"])
        return data.get('user_id')
    except jwt.ExpiredSignatureError:
        flash("Request timed out, please try again", "warning")
        return None
    except jwt.InvalidSignatureError:
        flash("Authentication Failed", "danger")
        return None
    except jwt.DecodeError:
        flash("Invalid Token Format", "danger")