import os
import subprocess
import typer
from typing import Optional

from snapctl.echo import error, success, info
from snapctl.utils import get_token_values, check_docker
from rich.progress import Progress, SpinnerColumn, TextColumn

app = typer.Typer()

# Constants
VALID_COMMANDS = {
  'byosnap': ['upload']
}
# TOKEN="eyJwYXlsb2FkIjoiZTQ0dEo2dDNnSGhaOVRlYThRcmFyWFhQdVZVMWhxTmpnS0tJcGdDNUMvR3JzNEZadkhhTC8vSmlDR2hSNlFrNzZ5d1JkVFhDRVAzTTJhK3dGYmp1VUJCNnJzWU91SVUrelhVOXdvdFF0dWlCZENnOXBLVHcySGt4ODlNUmlEUFhvaU9wN0lHaTlXcUtGUVl3YmovYTN4OXcvNUxJaDFUZzlTYnRtQ3BXeGlINDYyZUJHZzFTOHVranVSNlV4YTNtWWsrb3FBcTk0TmVHNUlxM1g3bTFBc2ovU1R4Wk5DTFI3OGpNRnhBZUFsTE5FYk45aTRIYnpSNk5Gdk56SDVrKytoVE1VNVNrbERvWlhFcVV2VzNhVTJ3L2JIRkd4d1Y0RG9PN2MrYUtWai9mNWlER2xLMkJkMG83VUxsVnBZcDYvQ3JON213RFN3b2phSFV4YTBZOEpJdHpHY3lCK1ZnRW9TTUdMaWc0bDIrMjVUVXpSK1pxVXBmeUhhTmV5L05ic1l3MUhya0h3Tko2ZzlIa1FNd1NXeDVYRmNnY3E1UmpKUjROQkJCWGFqRXdPMXQrMkphZjVxa0FieFdKckJ0TUxwcytGYll6Y3p2VS9iSDRQaTZIOGFzSGwrM0lGQzJ3R1ZpRDBwSkU4amhzRTRuakpmZjJVbnplUDAvRnVET2plMzNXOVpsK1kxRjdUWEJNZVRDRXVWendkVk9Vd3JNRDZ1L1ZqQVcyOWFZdXJSR3dHTHJnTzhTYzhteDY4WCs5b05leXljOW9JL2hNUnk4VG5DTHNZTk5xZG5CZnNRZW5MWEwyL20zS1BxMmZNaWJ4akF0bE9xTUpMK2Nxd2JrSHZhRUZtMnlNQTFOYnVtOTNUTHEwdFRRZkZBSGl1UXFvd0R5NittcHAvZmZLZXUzclEwRFE5UHZib3JUbDBlV2M2YmdxUXdRUU1HOFQvcnJMZXRUZW4zSnNucVpZWk1zQ1lqM3NSZ1F3ZG1LcjU5dUpyNmREOENKN0M2bUllTWRXajhHalhvVlFXcmViOU5jU0xwbVFsZyt3RUZQRXo2Zjlsd2h5WlNNRUFYUkVMbHRnNS9FTkkyajluYTJFQlJMUUhkcUp3K2QyM1NWRDNLWXJjWE41MzJjRjcrYUZhWndMNWhyV3JkRFdIbjZuOFlTSTNGYVNGb2haRmRzMXdTcW1DR1NIbTAvcEFld2toaGt4M2krTXA5aDk1UGtqaUZpUmtRQ21LSzBxQzh6NHZ6d0tvTnBEN1p1OXRvY296bExNL0E0ZDRYUzc1cmk4MThxeVRaS2d1ZHcyNnpMSTkwcUlPSFRRaGdOalNDeTI4elI0SUtqeGEzUE5LMFZrelAwYW5kcmRoVHV6M2VIbDlUNUE5VzExdEhnNlBzdzNPS0RlR2J6NmZnK0N5YStUNHlFOEFkYWphTTJRcDcrL2o5NUR4RXBxNVI0cmFyQ01RbzRBZjBBOG9xRnNwNko1ekRJU3ducXNXcy9TVGtQYkJ2ODBVUUMyTW51NVlJazRPYUZ5enZ1ZGdmaHNJWWNVMk04RWdoZkFEdjR3MTU4UWhiRjcvUHlEV3kwc3k4Q3luRm9mbldlWThnNEVaNkV4cEg0RUJYKzB4T2RyZG9YOHh3RVpXbG13dVcwa0pxdXpHdy9pZDlLd21UeFEyK3RFUHJ3dlVNQ1N4QjN1OWVFNVlzSWhXRCtSd25JTEE0Qkk5R3BySnpkcUhRcHNVaW1SRjluUWRTdTV1N0Zad2FUQmlUd0JHaXJDWXM0Szl3aklTeURxY090cDBWWHIzaFpkYlg5K0xsV3F3VXZseGNXWjFqWnFLRFlmemh2WEVOYmpkaXVYclJrRWo5bWNWMkhJRmtkSEJweS8wNzQ9IiwiZGF0YWtleSI6IkFRRUJBSGo2bGM0WElKdy83bG4wSGMwMERNZWs2R0V4SENiWTRSSXBUTUNJNThJblV3QUFBSDR3ZkFZSktvWklodmNOQVFjR29HOHdiUUlCQURCb0Jna3Foa2lHOXcwQkJ3RXdIZ1lKWUlaSUFXVURCQUV1TUJFRURJZjN6bERvelJEeVpScTYvUUlCRUlBN1ZsUURQbzBMaFUyU0dwREpSREFrdXg1L1pDWVE0RVVCMWVuV2M5cGtZdHF2R2J0cC9aTzFRY2kwNzBPSGpneWhDY0JCdzIwSGZZaW54Uk09IiwidmVyc2lvbiI6IjIiLCJ0eXBlIjoiREFUQV9LRVkiLCJleHBpcmF0aW9uIjoxNjc4NTAzMjc0fQ=="
# BASE_REPO= '131164543756.dkr.ecr.us-west-2.amazonaws.com'
# REPO_NAME="sandbox-multi-tools"
# ECR_PATH=f"{BASE_REPO}/{REPO_NAME}"

# Commands
@app.callback()
def callback():
  """
  Snapser CLI Tool
  """

# command: Optional[str] = typer.Argument(None)
@app.command()
def byosnap(
  command: str = typer.Argument(..., help="Bring your own Commands: " + ", ".join(VALID_COMMANDS['byosnap']) + "."),
  path: str = typer.Argument(..., help="Path to your snap code"),
  tag: str = typer.Argument(..., help="Tag for your snap"),
  token: str = typer.Argument(..., help="Copy the token from the Web App"),
  docker_file: str = typer.Option("Dockerfile", help="Dockerfile name to use")
):
  """
  Bring your own code
  """
  token_list = []
  # Error checking
  with Progress(
    SpinnerColumn(),
    TextColumn("[progress.description]{task.description}"),
    transient=True,
  ) as progress:
    progress.add_task(description=f'Checking dependencies...', total=None)
    if not check_docker():
      return error('Docker not present')
    if not command in VALID_COMMANDS['byosnap']:
      error_message: str = 'Invalid command. Valid commands are ' + ', '.join(VALID_COMMANDS['byosnap']) + '.'
      return error(error_message)
    token_list = get_token_values(token)
    if token_list is None:
      error_message: str = 'Invalid token. Please reach out to your support team.'
      return error(error_message)

  success('Dependencies Verified')

  # Extract details from the token
  web_app_token = token_list[0]
  service_id = token_list[1]
  ecr_repo_url = token_list[2]
  ecr_repo_username = token_list[3]
  ecr_repo_token = token_list[4]

  try:

    # Login to Snapser Registry
    with Progress(
      SpinnerColumn(),
      TextColumn("[progress.description]{task.description}"),
      transient=True,
    ) as progress:
      progress.add_task(description=f'Logging into Snapser Image Registry...', total=None)
      response = subprocess.run([
        f'echo "{ecr_repo_token}" | docker login --username {ecr_repo_username} --password-stdin {ecr_repo_url}'
      ], shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
      if response.returncode:
        return error('Unable to connect to the Snapser Container Repository. Please get the latest token from the Web app.')
    success('Login Successful')

    # Build your snap
    with Progress(
      SpinnerColumn(),
      TextColumn("[progress.description]{task.description}"),
      transient=True,
    ) as progress:
      progress.add_task(description=f'Building your snap...', total=None)
      response = subprocess.run([
        #f"docker build --no-cache -t {tag} {path}"
        f"docker build --platform linux/arm64 -t {service_id}.{tag} {path}"
      ], shell=True, )#stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
      if response.returncode:
        return error('Unable to build docker.')
    success('Build Successfull')

    # Tag the repo
    with Progress(
      SpinnerColumn(),
      TextColumn("[progress.description]{task.description}"),
      transient=True,
    ) as progress:
      progress.add_task(description=f'Tagging your snap...', total=None)
      response = subprocess.run([
        f"docker tag {service_id}.{tag} {ecr_repo_url}:{service_id}.{tag}"
      ], shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
      if response.returncode:
        return error('Unable to tag your snap.')
    success('Tag Successfull')

    # Push the image
    with Progress(
      SpinnerColumn(),
      TextColumn("[progress.description]{task.description}"),
      transient=True,
    ) as progress:
      progress.add_task(description=f'Pushing your snap...', total=None)
      response = subprocess.run([
        f"docker push {ecr_repo_url}:{service_id}.{tag}"
      ], shell=True, )#stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
      if response.returncode:
        return error('Unable to push your snap.')
    success('Snap Upload Successfull')

  # white_check_mark thumbsup love-you_gesture

  except Exception as e:
    return error('CLI Error')
  success(f"BYOSnap " + command + ' complete :oncoming_fist:')


@app.command()
def byow():
  """
  Bring your own workstation
  """
  typer.echo("Connecting to your cluster")