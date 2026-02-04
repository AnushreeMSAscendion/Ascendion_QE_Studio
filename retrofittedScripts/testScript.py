from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

driver = webdriver.Chrome()
driver.maximize_window()

BASE_URL = "<e-commerce>"
LOGIN_URL = "<login-page-url>"  # Login page URL placeholder


# ---------- Helper ----------
def pause(sec=2):
    time.sleep(sec)


# ---------- Login Test Cases (NEW) ----------

def navigate_to_login_screen():
    """Helper function to navigate to login screen"""
    driver.get(LOGIN_URL)
    pause()
    assert "Login" in driver.page_source or "Sign" in driver.page_source


def tc_login_001_invalid_credentials():
    """Test Case TC_LOGIN_001: Verify error message for invalid login credentials"""
    # Step 2: Navigate to the login screen
    navigate_to_login_screen()
    assert "Login" in driver.page_source or "Sign" in driver.page_source
    
    # Step 3: Enter invalid username and/or password
    try:
        username_field = driver.find_element(By.ID, "username")
        password_field = driver.find_element(By.ID, "password")
        login_button = driver.find_element(By.ID, "login-button")
        
        username_field.send_keys("invalid_user")
        password_field.send_keys("invalid_password")
        login_button.click()
        pause()
        
        # Expected result: Error message displayed
        error_message = driver.find_element(By.CLASS_NAME, "error-message").text
        assert "Invalid username or password" in error_message or "Please try again" in error_message
    except Exception as e:
        print(f"TC_LOGIN_001 failed: {str(e)}")
        raise


def tc_login_002_remember_me_checkbox():
    """Test Case TC_LOGIN_002: Verify 'Remember Me' checkbox is not present"""
    # Step 2: Navigate to the login screen
    navigate_to_login_screen()
    assert "Login" in driver.page_source or "Sign" in driver.page_source
    
    # Step 3: Check for the presence of 'Remember Me' checkbox
    try:
        remember_me_elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'Remember Me')]")
        remember_me_checkbox = driver.find_elements(By.ID, "remember-me")
        
        # Expected result: 'Remember Me' checkbox is not present
        assert len(remember_me_elements) == 0 and len(remember_me_checkbox) == 0, "Remember Me checkbox should not be present"
    except AssertionError:
        raise
    except Exception as e:
        print(f"TC_LOGIN_002 failed: {str(e)}")
        raise


def tc_login_003_forgot_username_workflow():
    """Test Case TC_LOGIN_003: Verify 'Forgot Username' workflow"""
    # Step 2: Navigate to the login screen
    navigate_to_login_screen()
    assert "Login" in driver.page_source or "Sign" in driver.page_source
    
    # Step 3: Click on 'Forgot Username' link
    try:
        forgot_username_link = driver.find_element(By.LINK_TEXT, "Forgot Username")
        forgot_username_link.click()
        pause()
        
        # Expected result: 'Forgot Username' workflow is initiated
        assert "Forgot Username" in driver.page_source or "Username Recovery" in driver.page_source
        
        # Step 4: Follow the instructions to recover username
        email_field = driver.find_element(By.ID, "recovery-email")
        email_field.send_keys("user@example.com")
        
        submit_button = driver.find_element(By.ID, "submit-recovery")
        submit_button.click()
        pause()
        
        # Expected result: Username recovery instructions are followed
        assert "instructions" in driver.page_source.lower() or "sent" in driver.page_source.lower()
    except Exception as e:
        print(f"TC_LOGIN_003 failed: {str(e)}")
        raise


# ---------- E-Commerce Test Cases (EXISTING) ----------

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
        # Execute Login Test Cases
        print("\n=== Executing Login Test Cases ===")
        tc_login_001_invalid_credentials()
        print("✅ TC_LOGIN_001 passed")
        
        tc_login_002_remember_me_checkbox()
        print("✅ TC_LOGIN_002 passed")
        
        tc_login_003_forgot_username_workflow()
        print("✅ TC_LOGIN_003 passed")
        
        # Execute E-Commerce Test Cases
        print("\n=== Executing E-Commerce Test Cases ===")
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

        print("\n✅ All 23 UI test cases executed (3 Login + 20 E-Commerce)")

    finally:
        driver.quit()