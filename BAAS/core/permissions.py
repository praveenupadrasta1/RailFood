from user_authentication.models import User
from ticket_details.models import TicketDetails
from train_details.models import TrainLiveStatus
from restaurant.models import RestaurantProfile, RestaurantBankDetails, RestaurantMembershipDetails, Cuisines
from BAAS.config import CONSUMER, RESTAURANT, DELIVERY_BOY

# Each permission has 4 fields,
# 1. the codename field, entered in the index 0
# 2. the name field, entered in the index 1
# 3. The model the permission belongs to, entered in the index 2
# 4. The app name, entered in the index 3

# User model
CHANGE_USER = ('change_user', 'Can change user', User, 'user')

# Ticket Details model
ADD_TICKETDETAILS = ('add_ticketdetails', 'Can add ticket details', TicketDetails, 'ticket_details')
DELETE_TICKETDETAILS = ('delete_ticketdetails', 'Can delete ticket details', TicketDetails, 'ticket_details')
CAN_GET_MY_JOURNEYS = ('can_get_my_journeys', 'Can get My Journeys', TicketDetails, 'ticket_details')

# Train Live status model
CAN_GET_TRAIN_LIVE_STATUS_CONSUMER = ('can_get_train_live_status_consumer', 'Can get train live status for consumer',
                                      TrainLiveStatus, 'train_details')

# Restaurant Profile model
CAN_CREATE_RESTAURANT_PROFILE = ('add_restaurantprofile', 'Can add restaurant profile', RestaurantProfile,
                                 'restaurant')
CAN_UPDATE_RESTAURANT_PROFILE = ('change_restaurantprofile', 'Can change restaurant profile', RestaurantProfile,
                                 'restaurant')
CAN_GET_RESTAURANT_PROFILE = ('get_restaurant_profile', 'Can get restaurant profile', RestaurantProfile,
                                 'restaurant')

# Restaurant Bank Details model
CAN_ADD_BANK_DETAILS = ('add_restaurantbankdetails', 'Can add restaurant bank details', RestaurantBankDetails, 'restaurant')
CAN_UPDATE_BANK_DETAILS = ('change_restaurantbankdetails', 'Can change restaurant bank details', RestaurantBankDetails, 'restaurant')
CAN_GET_BANK_DETAILS = ('get_restaurantbankdetails', 'Can get restaurant bank details', RestaurantBankDetails, 'restaurant')

# Restaurant Membership model
CAN_OPT_MEMBERSHIP = ('can_opt_membership', 'Can opt membership', RestaurantMembershipDetails, 'restaurant')
CAN_GET_MEMBERSHIP = ('get_memberships', 'Can get memberships', RestaurantMembershipDetails, 'restaurant')

# Cuisines model
CAN_GET_CUISINES = ('get_cuisines', 'Can get Cuisines', Cuisines, 'restaurant')


########################### ASSIGN PERMISSIONS HERE ###########################################

USER_PERMISSIONS = {CONSUMER :[CHANGE_USER,
                                ADD_TICKETDETAILS,
                                DELETE_TICKETDETAILS,
                                CAN_GET_MY_JOURNEYS,
                                CAN_GET_TRAIN_LIVE_STATUS_CONSUMER,
                                CAN_GET_RESTAURANT_PROFILE],

                    RESTAURANT : [CHANGE_USER,
                                  CAN_CREATE_RESTAURANT_PROFILE,
                                  CAN_UPDATE_RESTAURANT_PROFILE,
                                  CAN_ADD_BANK_DETAILS,
                                  CAN_UPDATE_BANK_DETAILS,
                                  CAN_OPT_MEMBERSHIP,
                                  CAN_GET_MEMBERSHIP,
                                  CAN_GET_BANK_DETAILS,
                                  CAN_GET_CUISINES],

                    DELIVERY_BOY : [],
                    }

##################################################################################################