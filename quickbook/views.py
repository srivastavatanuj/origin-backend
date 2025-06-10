from django.shortcuts import redirect
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from intuitlib.client import AuthClient
from intuitlib.enums import Scopes
from quickbooks import QuickBooks
# from quickbooks.objects.invoice import Invoice, Line, SalesItemLineDetail
from orders.models import Payment
from rest_framework.permissions import AllowAny
from .models import QuickBooksToken

from django.conf import settings


auth_client = AuthClient(
    client_id=settings.QUICKBOOK_CLIENT_ID,
    client_secret=settings.QUICKBOOK_CLIENT_SECRET,
    environment='sandbox',
    redirect_uri=settings.QUICKBOOK_REDIRECT_URI
)


class QuickBookLogin(APIView):
    def get(self, request):
        url = auth_client.get_authorization_url(
            scopes=[Scopes.ACCOUNTING])
        print(url)
        return redirect(url)


class QuickBookCallback(APIView):

    def get(self, request):
        auth_code = request.GET.get('code')
        realm_id = request.GET.get('realmId')
        auth_client.get_bearer_token(auth_code, realm_id)
        token = QuickBooksToken.objects.get(id=1)
        token.access_token = auth_client.access_token
        token.refresh_token = auth_client.refresh_token
        token.realm_id = auth_client.realm_id
        token.expires_in = auth_client.expires_in
        token.x_refresh_token_expires_in = auth_client.x_refresh_token_expires_in
        token.save()
        return Response({'message': 'QuickBooks authenticated'})


# class LogPaymentToQuickBooks(APIView):
#     def post(self, request):
#         access_token = request.session.get('access_token')
#         realm_id = request.session.get('realm_id')
#         qb_client = QuickBooks(
#             auth_client=auth_client,
#             refresh_token=auth_client.refresh_token,
#             company_id=realm_id
#         )

#         payment = Payment.objects.get(
#             payment_id=request.data.get('payment_id'))
#         line = Line()
#         line.Amount = float(payment.amount)
#         line.DetailType = "SalesItemLineDetail"
#         line.SalesItemLineDetail = SalesItemLineDetail()
#         line.SalesItemLineDetail.ItemRef = {
#             'value': "1", 'name': "Product/Service Name"}

#         invoice = Invoice()
#         invoice.Line = [line]
#         # Add logic to associate customers
#         invoice.CustomerRef = {"value": "1"}
#         invoice.save(qb=qb_client)

#         return Response({"message": "Logged in QuickBooks"})
