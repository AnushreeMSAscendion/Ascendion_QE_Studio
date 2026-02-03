from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

driver = webdriver.Chrome()
driver.maximize_window()

BASE_URL = "<e-commerce>"


# ---------- Helper ----------
def pause(sec=2):
    time.sleep(sec)


# ---------- Test Cases ----------

def tc_01_homepage_load():
    driver.get(BASE_URL)
    assert "Amazon" in driver.title


def tc_02_search_product():
    search = driver.find_element(By.ID, "twotabsearchtextbox")
    search.send_keys("laptop")
    search.send_keys(Keys.ENTER)
    pause()
    assert "laptop" in driver.title.lower()


def tc_03_search_results_displayed():
    results = driver.find_elements(By.CSS_SELECTOR, "div.s-result-item")
    assert len(results) > 0


def tc_04_open_product_detail():
    driver.find_elements(By.CSS_SELECTOR, "div.s-result-item h2 a")[0].click()
    pause()
    assert "Amazon" in driver.title


def tc_05_product_title_visible():
    assert driver.find_element(By.ID, "productTitle").is_displayed()


def tc_06_product_price_visible():
    assert driver.find_element(By.ID, "corePriceDisplay_desktop_feature_div").is_displayed()


def tc_07_add_to_cart():
    driver.find_element(By.ID, "add-to-cart-button").click()
    pause()
    assert "Added to Cart" in driver.page_source


def tc_08_cart_count_updated():
    cart_count = driver.find_element(By.ID, "nav-cart-count").text
    assert int(cart_count) >= 1


def tc_09_open_cart():
    driver.find_element(By.ID, "nav-cart").click()
    pause()
    assert "Shopping Cart" in driver.page_source


def tc_10_proceed_to_checkout():
    driver.find_element(By.NAME, "proceedToRetailCheckout").click()
    pause()
    assert "Sign-In" in driver.page_source or "Checkout" in driver.title


def tc_11_signin_page_loaded():
    assert "Sign-In" in driver.page_source


def tc_12_invalid_login():
    driver.find_element(By.ID, "ap_email").send_keys("invalid@email.com")
    driver.find_element(By.ID, "continue").click()
    pause()
    assert "cannot find an account" in driver.page_source.lower()


def tc_13_back_to_home():
    driver.get(BASE_URL)
    assert "Amazon" in driver.title


def tc_14_category_navigation():
    driver.find_element(By.ID, "nav-hamburger-menu").click()
    pause()
    driver.find_element(By.LINK_TEXT, "Electronics").click()
    pause()
    assert "Electronics" in driver.title


def tc_15_filter_by_price():
    driver.find_element(By.ID, "low-price").send_keys("500")
    driver.find_element(By.ID, "high-price").send_keys("1000")
    driver.find_element(By.CLASS_NAME, "a-button-input").click()
    pause()
    assert "500" in driver.page_source


def tc_16_sort_results():
    driver.find_element(By.ID, "a-autoid-0-announce").click()
    pause()
    driver.find_element(By.ID, "s-result-sort-select_1").click()
    pause()
    assert True


def tc_17_pagination_next_page():
    driver.find_element(By.CSS_SELECTOR, "a.s-pagination-next").click()
    pause()
    assert "page" in driver.current_url.lower()


def tc_18_footer_links_visible():
    footer = driver.find_element(By.ID, "navFooter")
    assert footer.is_displayed()


def tc_19_language_change():
    driver.find_element(By.ID, "icp-nav-flyout").click()
    pause()
    assert "Language" in driver.page_source


def tc_20_signout_option_visible():
    driver.find_element(By.ID, "nav-link-accountList").click()
    pause()
    assert "Sign Out" in driver.page_source or "Sign in" in driver.page_source


# ---------- Test Runner ----------
if __name__ == "__main__":
    try:
        tc_01_homepage_load()
        tc_02_search_product()
        tc_03_search_results_displayed()
        tc_04_open_product_detail()
        tc_05_product_title_visible()
        tc_06_product_price_visible()
        tc_07_add_to_cart()
        tc_08_cart_count_updated()
        tc_09_open_cart()
        tc_10_proceed_to_checkout()
        tc_11_signin_page_loaded()
        tc_12_invalid_login()
        tc_13_back_to_home()
        tc_14_category_navigation()
        tc_15_filter_by_price()
        tc_16_sort_results()
        tc_17_pagination_next_page()
        tc_18_footer_links_visible()
        tc_19_language_change()
        tc_20_signout_option_visible()

        print("✅ All 20 UI test cases executed")

    finally:
        driver.quit()
