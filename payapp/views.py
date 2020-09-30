from django.shortcuts import render
from django.contrib.auth import authenticate, login as auth_login
from django.conf import settings
from .models import Transaction
from .paytm import generate_checksum, verify_checksum
from django.views.decorators.csrf import csrf_exempt
import cgi
from django.http import HttpResponse


def initiate_payment(request):
    if request.method == "GET":
        return render(request, 'payapp/pay.html')
    try:
        username = request.POST['username']
        password = request.POST['password']
        amount = int(request.POST['amount'])
        user = authenticate(request, username=username, password=password)
        if user is None:
            raise ValueError
        auth_login(request=request, user=user)
    except:
        return render(request, 'payapp/pay.html', context={'error': 'Wrong Accound Details or amount'})

    transaction = Transaction.objects.create(made_by=user, amount=amount)
    transaction.save()
    # merchant_key = settings.PAYTM_SECRET_KEY

    # params = (
    #     ('MID', settings.PAYTM_MERCHANT_ID),
    #     ('ORDER_ID', str(transaction.order_id)),
    #     ('CUST_ID', str(transaction.made_by.email)),
    #     ('TXN_AMOUNT', str(transaction.amount)),
    #     ('CHANNEL_ID', settings.PAYTM_CHANNEL_ID),
    #     ('WEBSITE', settings.PAYTM_WEBSITE),
    #     # ('EMAIL', request.user.email),
    #     # ('MOBILE_N0', '9911223388'),
    #     ('INDUSTRY_TYPE_ID', settings.PAYTM_INDUSTRY_TYPE_ID),
    #     ('CALLBACK_URL', 'http://127.0.0.1:8000/callback/'),
    #     # ('PAYMENT_MODE_ONLY', 'NO'),
    # )
    # requestParams = {
    #     'command' => 'AUTHORIZATION',
    #     'access_code' => 'zx0IPmPy5jp1vAz8Kpg7',
    #     'merchant_identifier' => 'CycHZxVj',
    #     'merchant_reference' => 'XYZ9239-yu898',
    #     'amount' => '10000',
    #     'currency' => 'AED',
    #     'language' => 'en',
    #     'customer_email' => 'test@payfort.com',
    #     'signature' => '7cad05f0212ed933c9a5d5dffa31661acf2c827a',
    #     'order_description' => 'iPhone 6-S',
    # }
    requestParams = {
        ('command', settings.COMMAND,)
        ('merchant_identifier', settings.MERCHANT_IDENTIFIER,)
        ('merchant_reference', settings.MERCHANT_REFERENCE,)
        ('currency', settings.CURRENCY,)
        ('language', settings.LANGUAGE,)
        ('access_code', settings.ACCESS_CODE,)
        ('customer_email', settings.CUSTOMER_EMAIL,)
        ('order_description', settings.ORDER_DESCRIPTION,)
    }

    redirectUrl = 'https://sbcheckout.payfort.com/FortAPI/paymentPage'
    print (HttpResponse("<html xmlns='https://www.w3.org/1999/xhtml'>\n<head></head>\n<body>\n"))
    print ("<form action='redirectUrl' method='post' name='frm'>\n")
    for (slug,title) in requestParams:
        print ("\t<input type='hidden' name='"+ cgi.escape(slug)+"' value='"+ cgi.escape(title)+"'>\n")

    print ("</form>")
    print ("\t<script type='text/javascript'>\n")
    print ("\t\tdocument.frm.submit();\n")
    print ("\t</script>\n")
    print ("\n</body>\n</html>")
    # paytm_params = dict(params)
    # checksum = generate_checksum(paytm_params, merchant_key)

    # transaction.checksum = checksum
    # transaction.save()

    # paytm_params['CHECKSUMHASH'] = checksum
    # print('SENT: ', checksum)
    # return render(request, 'payapp/redirect.html', context=paytm_params)

@csrf_exempt
def callback(request):
    if request.method == 'POST':
        received_data = dict(request.POST)
        paytm_params = {}
        # paytm_checksum = received_data['CHECKSUMHASH'][0]
        # for key, value in received_data.items():
        #     if key == 'CHECKSUMHASH':
        #         paytm_checksum = value[0]
        #     else:
        #         paytm_params[key] = str(value[0])
        # # Verify checksum
        # is_valid_checksum = verify_checksum(paytm_params, settings.PAYTM_SECRET_KEY, str(paytm_checksum))
        # if is_valid_checksum:
        received_data['message'] = "Checksum Matched"
        # else:
        #     received_data['message'] = "Checksum Mismatched"
        #     return render(request, 'payapp/callback.html', context=received_data)
        return render(request, 'payapp/callback.html', context=received_data)
