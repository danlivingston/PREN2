import requests

def send_end_command(url, team_id, auth_token):
    headers = {'Auth': auth_token}
    post_url = f"{url}/cubes/{team_id}/end"
    response = requests.post(post_url, headers=headers)
    print(response.text)

send_end_command('http://52.58.217.104:5000', 'team12', 'IhrTokenHier')
