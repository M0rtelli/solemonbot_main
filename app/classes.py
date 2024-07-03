from aiogram.fsm.state import State, StatesGroup

class selectUser(StatesGroup):
    userId = State()
    startDB = State()

class giveSell(StatesGroup):
    userId = State()
    countSell = State()

class giveDiscount(StatesGroup):
    userId = State()
    discount = State()

class sellPod(StatesGroup):
    namePod = State()
    statusPod = State()
    pricePod = State()
    photoPod = State()    

class toMarketPlace(StatesGroup):
    chooseMenu = State()

    selectTypeViewAd = State()

    TypeViewAd_minprice = State()
    TypeViewAd_maxprice = State()
    TypeViewAd_price_view = State()
    TypeViewAd_price_view_max = State()
    TypeViewAd_price_view_min = State()

    TypeViewAd_all = State()
    TypeViewAd_all_item = State()

    TypeViewAd_list = State()
    TypeViewAd_list_item = State()


    namePod = State()
    statusPod = State()
    pricePod = State()
    photoPod = State()
    commentPod = State()

    chooseMyAd = State()
    selectedAd = State()

    addAdName = State()
    addAdStatus = State()
    addAdPrice = State()
    addAdPhoto = State()
    addAdComment = State()

    editAd = State()
    editAdName = State()
    editAdStatus = State()
    editAdPrice = State()
    editAdComment = State()
    editAdPhoto = State()

    confirmDeleteAd = State()