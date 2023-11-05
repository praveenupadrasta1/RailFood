from BAAS.config import TRAIN_KEY, TRAIN_NUMBER_KEY


def get_train_number_from_pnr_details(pnr_details):
    train_details = pnr_details.get(TRAIN_KEY)
    return int(train_details.get(TRAIN_NUMBER_KEY))