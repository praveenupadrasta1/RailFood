OTP_EXPIRY_MINUTES_LIMIT = 7   # mins
PASSWORD_MIN_LENGTH = 8   # mins
TRAIN_DETAILS_UPDATE_INTERVAL = 1440   # mins or 24 hours
TRAIN_LIVE_STATUS_UPDATE_INTERVAL = 10  # mins
CANCELLED_TRAIN_DETAILS_UPDATE_INTERVAL = 360 # mins or 6 hours
RESCHEDULED_TRAIN_DETAILS_UPDATE_INTERVAL = 360 # mins or 6 hours
PNR_DETAILS_UPDATE_INTERVAL = 120 # mins or 2 hours

OTP_FAIL_ATTEMPTS_THRESHOLD = 3

########################### Railway API JSON keys ####################################

# PNR Details JSON Keys
RESPONSE_CODE_KEY = 'response_code'
PNR_KEY = 'pnr'
PNR_NO_KEY = 'pnr_no'
FROM_STATION_KEY = 'from_station'
TO_STATION_KEY = 'to_station'
RESERVATION_UPTO_KEY = 'reservation_upto'
BOARDING_POINT_KEY = 'boarding_point'
DESTINATION_STATION_KEY = 'destination_station'

STATION_LNG_KEY = 'lng'
STATION_LAT_KEY = 'lat'
STATION_NAME_KEY = 'name'
STATION_CODE_KEY = 'code'

PASSENGERS_KEY = 'passengers'
CURRENT_STATUS_KEY = 'current_status'
BOOKING_STATUS_KEY = 'booking_status'
DOJ_KEY = 'doj'
CHART_PREPARED_KEY = 'chart_prepared'

SEAT_CURRENT_STATUS_KEY = 'current_status'
SEAT_COACH_KEY = 'coach'
SEAT_NUMBER_KEY = 'seat_no'
IS_TICKET_CANCELLED = 'is_cancelled'

# Train details JSON Keys

TRAIN_KEY = 'train'
TRAIN_NAME_KEY = 'name'
TRAIN_NUMBER_KEY = 'number'
TRAIN_ROUTE_KEY = 'route'
STATION_KEY = 'station'
SCHARRIVAL_KEY = 'scharr'
SCHDEPT_KEY = 'schdep'
STATION_DISTANCE_KEY = 'distance'
TRAIN_DAY_NUMBER_KEY = 'day'
IS_TRAIN_CANCELLED_KEY = 'is_train_cancelled'
IS_TRAIN_RESCHEDULED_KEY = 'is_train_rescheduled'

SOURCE_VALUE = 'SOURCE'
DEST_VALUE = 'DEST'

# Cancelled Trains JSON Keys

TRAINS_KEY = 'trains'

# Rescheduled Trains JSON Keys

RESCHEDULED_TO_TIME_KEY = 'rescheduled_time'
RESCHEDULED_TO_DATE_KEY = 'rescheduled_date'

# Train Live Status Keys

TRAIN_LIVE_STATUS = 'train_live_status'

######################################################################################


########################## Google maps API JSON keys ###################################

RESULTS_KEY = 'results'
ADDRESS_COMPONENTS_KEY = 'address_components'
TYPES_KEY = 'types'
ADMIN_AREA_LEVEL_1_KEY = 'administrative_area_level_1'
SHORT_NAME_KEY = 'short_name'
STATE_SHORT_NAME_KEY = 'state_short_name'

#######################################################################################


######################### Miscellaneous API keys ###########################################

DETAILS_KEY = 'details'
STATUS_KEY = 'status'
STATUS_CODE_KEY = 'status_code'
DATA_KEY = 'data'
TRAIN_ARRIVAL_DETAILS_KEY = 'train_arrival_details'
CANCELLED_STATUS ='CAN'
CONFIRMED_STATUS = 'CNF'
PNR_DETAILS_KEY = 'pnr_details'
SEAT_DETAILS_KEY = 'seat_details'
TRAIN_DETAILS_KEY = 'train_details'
SERVER_DATETIME_UTC_KEY = 'server_datetime_utc'
PNR_DETAILS_UPDATE_INTERVAL_KEY = 'pnr_details_update_interval'
LAST_UPDATED_UTC_KEY = 'last_updated_utc'
IS_LIVE_STATUS = 'is_live_status'
EMAIL_KEY = 'email'
USER_KEY = 'user'
PASSWORD_KEY = 'password'
OTP_KEY = 'otp'
TOKEN_KEY = 'token'
USERNAME_KEY = 'username'
CATEGORY_KEY = 'category'
ERRORS_KEY = 'errors'
ROLE_KEY = 'role'
IS_EMAIL_VERIFIED = 'is_email_verified'
IS_MOBILE_VERIFIED = 'is_mobile_verified'

# Restaurant Profile API JSON Keys
NAME_KEY = 'name'
MOBILE_NUM_KEY = 'mobile_number'
ADDRESS_KEY = 'address'
IMAGE_URL_KEY = 'image_url'
ORDER_OPEN_TIMING_FROM_KEY = 'order_open_timing_from'
ORDER_OPEN_TIMING_TO_KEY = 'order_open_timing_to'
CONVEINIENCE_FEE_KEY = 'conveinience_fee'
COMMISSION_PERCENTAGE_KEY = 'commission_percentage'
RESTAURANT_ID_KEY = 'restaurant_id'
RESTAURANT_RATING_KEY = 'rating'
RESTAURANT_NUMBER_REVIEWS_KEY = 'n_reviews'
RESTAURANT_CUISINES_KEY = 'cuisines'
RESTAURANT_HAS_OFFER_KEY = 'has_offer'

#Cuisine API JSON Keys
CUISINE_NAME_KEY = 'name'
CUISINE_ID_KEY = 'id'

# Restaurant Bank Details API JSON Keys
ACCOUNT_NAME_KEY = 'account_name'
ACCOUNT_NUMBER_KEY = 'account_number'
BANK_NAME_KEY = 'bank_name'
IFSC_CODE_KEY = 'IFSC_code'

# Membership details API JSON Keys
PRICE_KEY = 'price'
VALIDITY_KEY = 'validity'
TYPE_KEY = 'type'

#######################################################################################


########################### HTTP API Versioning #####################################

HTTP_API_VERSION_KEY = 'HTTP_API_VERSION'
BETA_VERSION_KEY = 'beta'

######################################################################################


################################### PHRASES ##########################################

PNR_ADDED_SUCCESSFULLY = 'PNR no. added successfully'
PNR_DETAILS_ALREADY_EXISTS = 'PNR no. already exists'
INVALID_PNR_NUMBER = 'Invalid PNR no.! Please try again'
INVALID_API_VERSION = 'Invalid API Version'
INVALID_CREDENTIALS = 'Invalid Credentials!'
USER_DEACTIVATED = 'This user has been deactivated.'
OTP_IS_REQUIRED = 'OTP is required'
CATEGORY_IS_REQUIRED = 'Category is required'
INVALID_EMAIL_ADDRESS = 'Invalid Email address!'
ERROR_DELETING_CANCELLED_TRAIN_RECORDS = 'Error deleting cancelled train records'
ERROR_DELETING_RESCHEDULED_TRAIN_RECORDS = 'Error deleting rescheduled train records'
NO_JOURNEYS_EXIST = 'There are no journey(s)'
INVALID_TRAIN_NUMBER = 'Invalid train number'
OTP_EXPIRED = 'OTP Expired!'
INCORRECT_OTP = 'Incorrect OTP'
OTP_SENT_SUCCESSFULLY = 'OTP sent to your {0} successfully'
BAD_CATEGORY = 'Bad category'
INVALID_REQUEST = 'Invalid request'
NEW_PASSWORD_SET_MESSAGE = 'A new password has been sent to your email'
VERIFY_EMAIL = 'Verify your email to reset your password'
INVALID_MOBILE_NUMBER = 'Invalid Mobile Number!'
INVALID_STATION = 'Invalid Station!'
INVALID_CUISINE = 'Invalid Cuisine!'
PROFILE_ALREADY_EXISTS = 'Profile already exists!'
PROFILE_DOESNT_EXISTS = 'Profile doesn\'t exists!'
BANK_DETAILS_ALREADY_EXIST = 'Bank details already exists!'
BANK_DETAILS_DOESNT_EXIST = 'Bank details doesn\'t exists!'

########################################################################################

################################## Group Names ########################################

CONSUMER = 'CONSUMER'
RESTAURANT = 'RESTAURANT'
DELIVERY_BOY = 'DELIVERY BOY'

#######################################################################################

################################ Choice fields ######################################

VEGETARIAN = 'VEGETARIAN'
NON_VEGETARIAN = 'NON_VEGETARIAN'
MULTI_CUISINE = 'MUTLI_CUISINE'

BRONZE_MEMBERSHIP = 'BRONZE_MEMBERSHIP'
SILVER_MEMBERSHIP = 'SILVER_MEMBERSHIP'
GOLD_MEMBERSHIP = 'GOLD_MEMBERSHIP'
PLATINUM_MEMBERSHIP = 'PLATINUM_MEMBERSHIP'

BRONZE_MEMBERSHIP_CODE = 'B'
SILVER_MEMBERSHIP_CODE = 'S'
GOLD_MEMBERSHIP_CODE = 'G'
PLATINUM_MEMBERSHIP_CODE = 'P'

#######################################################################################


############################### Membership details #################################

BRONZE_MEMBERSHIP_MONTHS_VALIDITY = 1
SILVER_MEMBERSHIP_MONTHS_VALIDITY = 3
GOLD_MEMBERSHIP_MONTHS_VALIDITY = 6
PLATINUM_MEMBERSHIP_MONTHS_VALIDITY = 12

BRONZE_MEMBERSHIP_PRICING = 1000
SILVER_MEMBERSHIP_PRICING = 2500
GOLD_MEMBERSHIP_PRICING = 4500
PLATINUM_MEMBERSHIP_PRICING = 8500

#####################################################################################