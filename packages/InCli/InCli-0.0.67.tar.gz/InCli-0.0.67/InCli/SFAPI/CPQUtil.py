from . import restClient,CPQ,account,timeStats

def create_cart_with_promotion(cartName,accountName,pricelistName,promoName,ts:timeStats=None):
#    restClient.setLoggingLevel()
#    cartName = 'testa_4'

    cartId = CPQ.getCartId(f"name:{cartName}")
    if cartId != None:
        CPQ.deleteCart(cartId)

    accountId = account.createAccount_Id(f'Name:{accountName}',recordTypeName='Consumer')
    cartId = CPQ.createCart(accountF= accountId, pricelistF=f'Name:{pricelistName}',name=cartName,checkExists=True)
    if ts!=None: ts.time('createCart')
    #print(restClient.getLastCallElapsedTime())

   # promoName = 'NOS4u 100Mb + Móvel'
    promo = CPQ.getCartPromotions(cartId,query=promoName,onlyOne=True)

    res = CPQ.postCartsPromoItems_api(cartId,promo['Id'])
    print(restClient.getLastCallElapsedTime())

    all = CPQ.getCartItems_api(cartId,fields='vlocity_cmt__ServiceAccountId__c,vlocity_cmt__BillingAccountId__c',price=False,validate=False,includeAttachment=False)
    print(restClient.getLastCallElapsedTime())