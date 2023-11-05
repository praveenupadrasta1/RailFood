from restaurant.models import RestaurantReviewRating


class RestaurantReviewRatingUtility:

    @staticmethod
    def get_restaurant_rating(restaurant):
        try:
            restaurant_review_ratings = RestaurantReviewRating.objects.filter(restaurant_id=restaurant)
            result_rating = 0
            for restaurant_review_rating in restaurant_review_ratings:
                result_rating = result_rating + restaurant_review_rating.rating
            return result_rating/len(restaurant_review_ratings)
        except Exception as e:
            return 0

    @staticmethod
    def get_restaurant_count_reviews(restaurant):
        try:
            restaurant_review_ratings = RestaurantReviewRating.objects.filter(restaurant_id=restaurant)
            count_reviews = 0
            for restaurant_review_rating in restaurant_review_ratings:
                if restaurant_review_rating.review is not None:
                    count_reviews += 1
            return count_reviews
        except Exception as e:
            return 0