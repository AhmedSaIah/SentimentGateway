from langdetect import DetectorFactory, detect
from langdetect.lang_detect_exception import LangDetectException

# Setting seed to get consistent results with langdetect
DetectorFactory.seed = 0


def filter_english_reviews(reviews):
    english_reviews, english_reviews_indecies= [], []

    for index, review in enumerate(reviews):
        try:
            # Detect the language of the review
            if detect(review) == 'en':
                english_reviews.append(review)
                english_reviews_indecies.append(index)
        except LangDetectException:
            # If detection fails, skip the review
            continue

    return english_reviews, english_reviews_indecies


def match_keyword(reviews, keyword):
    matched_reviews, matched_reviews_indecies = [], []
    keyword = keyword.lower()
    for index, review in enumerate(reviews):
        if keyword in review.lower():
            matched_reviews.append(review)
            matched_reviews_indecies.append(index)

    return matched_reviews, matched_reviews_indecies
