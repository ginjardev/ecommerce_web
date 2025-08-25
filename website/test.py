from intasend import APIService


API_PUBLISHABLE_KEY = 'ISPubKey_test_e005a552-9557-4ee5-b2a2-414656a6193f'
API_TOKEN = 'ISSecretKey_test_202da626-23bb-4715-875e-2b5b3ceb83ce'
PAYLINK = 'https://sandbox.intasend.com/pay/d27c15a8-bd40-47d4-b0b4-d739a95b462d/'


service = APIService(publishable_key=API_PUBLISHABLE_KEY, token=API_TOKEN, test=True)
payload = {}
payload["title"] = 'E-commerce Website Order'
payload["currency"] = 'USD'
payload["amount"] = 10 + 200
payload["mobile_tarrif"] = 'BUSINESS-PAYS'
payload["card_tarrif"] = 'BUSINESS-PAYS'
payload["is_active"] = True

# create_order = service.payment_links.create(
#     title='E-commerce Website Order',
#     amount=10 + 200,
#     currency='USD',
#     description='Order from E-commerce Website',
#     mobile_tarrif="BUSINESS-PAYS", 
#     card_tarrif="BUSINESS-PAYS",
#     redirect_url=PAYLINK,
#     payload=payload
# )

payment = service.collect.checkout(email='admin@gmail.com', amount=10 + 200, currency='USD')

print(payment['invoice'].status)