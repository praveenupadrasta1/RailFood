from BAAS.config import CONSUMER, RESTAURANT, DELIVERY_BOY


class GroupUtility:

    @staticmethod
    def get_group(role):
        if role == '0':
            return CONSUMER
        elif role == '1':
            return RESTAURANT
        elif role == '2':
            return DELIVERY_BOY
