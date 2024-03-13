import requests

def send_start_command(url, team_id, auth_token):
    headers = {'Auth': auth_token}
    post_url = f"{url}/cubes/{team_id}/start"
    response = requests.post(post_url, headers=headers)
    print(response.text)

send_start_command('http://52.58.217.104:5000', 'team12', 'IhrTokenHier')
