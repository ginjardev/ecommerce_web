from intasend import APIService


API_PUBLISHABLE_KEY = 'ISPubKey_test_e005a552-9557-4ee5-b2a2-414656a6193f'
API_TOKEN = 'ISSecretKey_test_202da626-23bb-4715-875e-2b5b3ceb83ce'
PAYLINK = 'https://sandbox.intasend.com/pay/b4e7da7c-d004-4906-be98-275e5526ae42/'


service = APIService(publishable_key=API_PUBLISHABLE_KEY, token=API_TOKEN, test=True)

create_order = service.payment_links.create(
    title='E-commerce Website Order',
    amount=10 + 200,
    currency='USD',
    description='Order from E-commerce Website',
    customer_email='admin@gmail.com',
    redirect_url=PAYLINK
)

print(create_order)