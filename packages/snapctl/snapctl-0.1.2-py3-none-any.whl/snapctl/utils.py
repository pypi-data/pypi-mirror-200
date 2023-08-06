import base64
import subprocess

def check_docker() -> bool:
  try:
    subprocess.run([
      "docker", "--version"
    ], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    return True
  except:
    return False

def get_token_values(token: str) -> None | list:
  try:
    input_token = base64.b64decode(token).decode('ascii')
    token_parts = input_token.split('|')
    # web_app_token|service_id|ecr_repo_url|ecr_repo_username|ecr_repo_token
    if len(token_parts) == 5:
      #token_parts[2] = 'http://131164543756.dkr.ecr.us-west-2.amazonaws.com/adhoc-c1a8eb1f-ee36-4313-bda5-046039ea06b3'
      return token_parts
    if len(token_parts) == 4:
      #token_parts[1] = 'http://131164543756.dkr.ecr.us-west-2.amazonaws.com/adhoc-c1a8eb1f-ee36-4313-bda5-046039ea06b3'
      token_parts.insert(0, '')
      return token_parts
  except Exception:
    pass
  return None

# TOKEN_ENV_VAR_NAME = 'SNP_TOKEN'
# def check_token_env_var() -> bool:
#   if TOKEN_ENV_VAR_NAME in os.environ and os.environ[TOKEN_ENV_VAR_NAME] != '':
#     return True
#   return False

# def get_token() -> str:
#   if TOKEN_ENV_VAR_NAME in os.environ and os.environ[TOKEN_ENV_VAR_NAME] != '':
#     return os.environ[TOKEN_ENV_VAR_NAME]
#   return ''
