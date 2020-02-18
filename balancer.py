#!/usr/bin/python

import requests
from uuid import uuid4

# Your token with the following: balance:read, savings-goal:read, savings-goal-transfer:read, savings-goal-transfer:create
secret = ''
# Amount to keep main at in pence
amount_to_balance = 10000
# UUID of main use commands in setup to get this
main_uuid = ''
# UUID of pot use commands in setup to get this
pot_uuid = ''

def setup():
  # This is the first time you do this you need to get these values
  # curl -H 'Authorization: Bearer $me' https://api.starlingbank.com/api/v2/accounts/
  ## Take the account uuid and add it in here
  # curl -H 'Authorization: Bearer $me' https://api.starlingbank.com/api/v2/account/<uuid>/savings-goals
  pass

def step_get_balances(data):
  print('get balances')

  headers = {"Authorization":"Bearer " + secret}
  main_request = requests.get('https://api.starlingbank.com/api/v2/accounts/' + main_uuid  + '/balance', headers=headers).json()

  pot_request = requests.get('https://api.starlingbank.com/api/v2/account/' + main_uuid + '/savings-goals/' + pot_uuid, headers=headers).json()

  return {
    'main': int(main_request['effectiveBalance']['minorUnits']),
    'pot': int(pot_request['totalSaved']['minorUnits'])
  }

def step_calculate_transfer(data):
  print('Calculating')

  balances = data['get_balance']

  # main is correct - nothing to do
  if balances['main'] == amount_to_balance:
    return {'amount': 0}

  elif balances['main'] > amount_to_balance:
    # reduce balance
    print('Calculated - need to transfer to pot')
    return {
      'to': 'pot',
      'from': 'main',
      'amount': int(balances['main'] - amount_to_balance)
    }

  else:
    # Increase balance
    print('Calulated - need to transfer to main')
    return {
      'to': 'main',
      'from': 'pot',
      'amount': int(min(balances['pot'], amount_to_balance - balances['main']))
    }

def step_transfer(data):
  print('transfer either way')
  transfer_data = data['calculate_transfer']

  if transfer_data['amount'] == 0:
    return {
      'transfer': False
    }


  direction = ""
  if transfer_data['to'] == 'pot':
    direction = "add-money"
  else:
    direction = "withdraw-money"

  headers = {"Authorization":"Bearer " + secret, "Content-Type": "application/json"}

  transfer_body = {
    'amount': {
      'currency': 'GBP',
      'minorUnits': transfer_data['amount']
    }
  }

  move_request = requests.put('https://api.starlingbank.com/api/v2/account/' + main_uuid + '/savings-goals/' + pot_uuid + '/' + direction + '/' + str(uuid4()), headers=headers, json=transfer_body).json()

  return move_request

if __name__ == '__main__':
  data = {}
  data['get_balance'] = step_get_balances(data)
  print(data['get_balance'])
  data['calculate_transfer'] = step_calculate_transfer(data)
  print(data['calculate_transfer'])
  data['transfer'] = step_transfer(data)
  print(data['transfer'])
