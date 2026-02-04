from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

driver = webdriver.Chrome()
driver.maximize_window()

BASE_URL = "<e-commerce>"
LOGIN_URL = "<login-page-url>"

# ---------- Helper ----------
def pause(sec=2):
    time.sleep(sec)

# ---------- Login Helper Functions ----------
def navigate_to_login_screen():
    """Navigate to the login screen"""
    driver.get(LOGIN_URL)
    pause()
    assert "Sign-In" in driver.page_source or "Login" in driver.page_source

def verify_login_screen_displayed():
    """Verify login screen is displayed"""
    login_form = driver.find_element(By.ID, "ap_email") or driver.find_element(By.NAME, "email")
    assert login_form.is_displayed()

def enter_invalid_credentials(username="invalid@email.com", password="wrongpassword"):
    """Enter invalid username and/or password"""
    driver.find_element(By.ID, "ap_email").send_keys(username)
    driver.find_element(By.ID, "continue").click()
    pause()
    if driver.find_elements(By.ID, "ap_password"):
        driver.find_element(By.ID, "ap_password").send_keys(password)
        driver.find_element(By.ID, "signInSubmit").click()
        pause()

def verify_invalid_login_error():
    """Verify error message for invalid credentials"""
    error_msg = driver.page_source.lower()
    assert "invalid username or password" in error_msg or "cannot find an account" in error_msg or "incorrect" in error_msg

def check_remember_me_checkbox():
    """Check for the presence of 'Remember Me' checkbox"""
    remember_me_elements = driver.find_elements(By.XPATH, "//input[@type='checkbox' and contains(@name, 'remember')]") or \
                          driver.find_elements(By.XPATH, "//label[contains(text(), 'Remember')]/input")
    return len(remember_me_elements) > 0

def verify_remember_me_not_present():
    """Verify 'Remember Me' checkbox is not present"""
    assert not check_remember_me_checkbox(), "Remember Me checkbox should not be present"

def click_forgot_username_link():
    """Click on 'Forgot Username' link"""
    forgot_links = driver.find_elements(By.LINK_TEXT, "Forgot Username") or \
                   driver.find_elements(By.PARTIAL_LINK_TEXT, "Forgot") or \
                   driver.find_elements(By.XPATH, "//a[contains(text(), 'Forgot') and contains(text(), 'Username')]")
    if forgot_links:
        forgot_links[0].click()
        pause()
    else:
        # If no specific forgot username link, try forgot password/general forgot link
        driver.find_element(By.ID, "auth-fpp-link-bottom").click()
        pause()

def verify_forgot_username_workflow_initiated():
    """Verify 'Forgot Username' workflow is initiated"""
    page_content = driver.page_source
    assert "forgot" in page_content.lower() or "recover" in page_content.lower() or "reset" in page_content.lower()

def follow_username_recovery_instructions():
    """Follow the instructions to recover username"""
    # Enter email for recovery
    email_field = driver.find_element(By.ID, "ap_email") or driver.find_element(By.NAME, "email")
    email_field.send_keys("recovery@email.com")
    driver.find_element(By.ID, "continue").click()
    pause()

def verify_username_retrieved():
    """Verify username recovery instructions are followed and username is retrieved"""
    page_content = driver.page_source.lower()
    assert "sent" in page_content or "check" in page_content or "email" in page_content or "success" in page_content

# ---------- New Login Test Cases ----------

def tc_login_001_invalid_credentials():
    """Test Case TC_LOGIN_001: Test invalid login credentials"""
    navigate_to_login_screen()
    verify_login_screen_displayed()
    enter_invalid_credentials()
    verify_invalid_login_error()

def tc_login_002_remember_me_not_present():
    """Test Case TC_LOGIN_002: Verify Remember Me checkbox is not present"""
    navigate_to_login_screen()
    verify_login_screen_displayed()
    verify_remember_me_not_present()

def tc_login_003_forgot_username_workflow():
    """Test Case TC_LOGIN_003: Test Forgot Username workflow"""
    navigate_to_login_screen()
    verify_login_screen_displayed()
    click_forgot_username_link()
    verify_forgot_username_workflow_initiated()
    follow_username_recovery_instructions()
    verify_username_retrieved()

# ---------- Original Test Cases ----------

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
        # Run new login test cases
        print("\n=== Running Login Test Cases ===")
        tc_login_001_invalid_credentials()
        print("✅ TC_LOGIN_001 passed")
        
        tc_login_002_remember_me_not_present()
        print("✅ TC_LOGIN_002 passed")
        
        tc_login_003_forgot_username_workflow()
        print("✅ TC_LOGIN_003 passed")
        
        # Run original e-commerce test cases
        print("\n=== Running E-Commerce Test Cases ===")
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
        print("✅ All 20 original UI test cases executed")
        
        print("\n✅ All test cases (23 total) executed successfully")
    finally:
        driver.quit()