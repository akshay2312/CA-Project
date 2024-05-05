from selenium import webdriver
import time
import datetime
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import random


def scrape_imdb_reviews(movie):
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    browser = webdriver.Chrome(options=options)

    try:
        browser.get("https://www.imdb.com")
        time.sleep(2)
        browser.find_element(By.XPATH, '//*[@id="suggestion-search"]').send_keys(movie)
        browser.find_element(By.XPATH, '//*[@id="suggestion-search-button"] ').click()
        browser.find_element(By.XPATH,
                             '//*[@id="__next"]/main/div[2]/div[3]/section/div/div[1]/section[2]/div[2]/ul/li[1]/div[2]/div/a').click()

        # Navigate to the "User Reviews" section
        browser.find_element(By.XPATH,
                             '//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[1]/div/div[2]/ul/li[2]/a').click()

        # Scroll to load more reviews
        reviews_count = 0
        while reviews_count < 200:
            try:
                # Scroll down to load more reviews
                browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)  # Wait for reviews to load
                # Check if "Load More" button exists
                load_more_button = browser.find_element(By.XPATH,
                                                        '//*[@id="load-more-trigger"]')
                if load_more_button:
                    load_more_button.click()
                    time.sleep(2)  # Wait for more reviews to load
                reviews_count = len(browser.find_elements(By.CLASS_NAME, 'review-container'))
            except NoSuchElementException:
                break  # Break the loop if "Load More" button is not found or if all reviews are loaded

        # Extract reviews
        reviews = browser.find_elements(By.CLASS_NAME, 'review-container')

        review_data_list = []
        random_reviews=[]

        for review in reviews:
            review_title = review.find_element(By.CLASS_NAME, 'title').text
            review_content = review.find_element(By.CLASS_NAME, 'content').text

            # Try to get the review rating if available
            try:
                review_rating = review.find_element(By.CLASS_NAME, 'rating-other-user-rating').text
            except NoSuchElementException:
                review_rating = 'N/A'

            review_date_str = review.find_element(By.CLASS_NAME, 'review-date').text
            review_date = datetime.datetime.strptime(review_date_str, '%d %B %Y')

            review_user = review.find_element(By.CLASS_NAME, 'display-name-link').text

            review_data_list.append({
                'title': review_title,
                'content': review_content,
                'rating': review_rating,
                'date': review_date,
                'user': review_user
            })

        random_reviews=random.sample(review_data_list,100)

        return random_reviews
    finally:
        browser.quit()


if __name__ == "__main__":
    movie = 'dune'
    reviews = scrape_imdb_reviews(movie)
    print(reviews)

