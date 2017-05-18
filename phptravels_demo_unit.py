# Testing of phptravels.net test site with Selenium.
# Only setup to go with Chrome or Chromium's webdriver.

import unittest

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select


import time

def printdebug(string):
	print(time.strftime("[%H:%M:%S] ") + string)

__timeout__ = 5 # delay for page loads in seconds



class PHPTravelsTest(unittest.TestCase):
	@classmethod
	def setUp(inst):
		# create a new Chome session
		inst.driver = webdriver.Chrome()
		inst.driver.implicitly_wait(__timeout__)
		inst.driver.maximize_window()

	def admin_signin(self, email, password):
		self.driver.get("http://www.phptravels.net/admin")
		signedin = False

		# Check if already signed in
		signoutsfound = self.driver.find_elements_by_class_name("fa-sign-out")
		if (len(signoutsfound)):
			signedin = True
		

		if( not signedin ):
			email_field = self.driver.find_element_by_name("email")
			password_field = self.driver.find_element_by_name("password")

			email_field.send_keys(email)
			password_field.send_keys(password)
			password_field.submit()
			# Verify signed in now
			signoutsfound = self.driver.find_elements_by_class_name("fa-sign-out")
			if (len(signoutsfound)):
				signedin = True

		return signedin

	def admin_createuser(self, email, password, firstname, lastname, country):
		sidebar_menu = self.check_element_present(self.driver, By.ID, "social-sidebar-menu")
		self.assertIsNotNone(sidebar_menu, "No Admin sidebar")

		accounts_link = self.check_element_present(sidebar_menu, By.LINK_TEXT,'Accounts')
		self.assertIsNotNone(accounts_link, "No Accounts link in sidebar.")
		accounts_link.click()

		customers_link = self.check_element_present(sidebar_menu, By.LINK_TEXT,'Customers')
		self.assertIsNotNone(customers_link, "No 'Customers' link in sidebar.")
		customers_link.click()

		add_button = self.check_element_present(self.driver, By.CLASS_NAME,'add_button')
		self.assertIsNotNone(add_button, "'Customers' screen not loaded. No 'Add' button.")
		add_button.click()

		fname_field = self.check_element_present(self.driver, By.NAME,'fname')
		self.assertIsNotNone(fname_field, "No 'fname' field.")
		self.assertIsNone(fname_field.send_keys(firstname),"Sending Firstname: "+firstname)

		lname_field = self.check_element_present(self.driver, By.NAME,'lname')
		self.assertIsNotNone(lname_field, "No 'lname' field.")
		self.assertIsNone(lname_field.send_keys(lastname),"Sending Lastname: "+lastname)

		email_field = self.check_element_present(self.driver, By.NAME,'email')
		self.assertIsNotNone(email_field, "No 'email' field.")
		self.assertIsNone(email_field.send_keys(email),"Sending email: "+email)

		password_field = self.check_element_present(self.driver, By.NAME,'password')
		self.assertIsNotNone(password_field, "No 'password' field.")
		self.assertIsNone(password_field.send_keys(password),"Sending password: "+password)

		countryselector = self.check_element_present(self.driver, By.CLASS_NAME,'select2-choice')
		self.assertIsNotNone(countryselector, "No Country drop down.")
		countryselector.click()

		country_entry = self.check_element_present(self.driver, By.CLASS_NAME,'select2-input')
		self.assertIsNotNone(country_entry, "No field to enter country.")
		self.assertIsNone(country_entry.send_keys(country),"Sending country: "+country)

		country_found = self.check_element_present(self.driver, By.CLASS_NAME,'select2-match')
		self.assertIsNotNone(country_found, "Country not found in list: "+country)
		country_found.click()

		password_field.submit()

		alert = self.check_element_present(self.driver, By.CLASS_NAME,'alert-danger')
		if alert:
			self.assertIsNone(alert, "Problem creating account: "+alert.text)

		return True

	def admin_verifyuser(self, email, password, firstname, lastname, country):
		sidebar_menu = self.check_element_present(self.driver, By.ID, "social-sidebar-menu")
		self.assertIsNotNone(sidebar_menu, "No Admin sidebar")

		accounts_link = self.check_element_present(sidebar_menu, By.LINK_TEXT,'Accounts')
		self.assertIsNotNone(accounts_link, "No Accounts link in sidebar.")
		accounts_link.click()

		customers_link = self.check_element_present(sidebar_menu, By.LINK_TEXT,'Customers')
		self.assertIsNotNone(customers_link, "No 'Customers' link in sidebar.")
		customers_link.click()

		rows = self.driver.find_elements(By.CLASS_NAME, 'xcrud-row')

		self.assertIsNot(0, len(rows), "No list of users")

		found = False
		for row in rows:
			cells = row.find_elements_by_tag_name("td")
			if (cells[2].text == firstname and cells[3].text == lastname and cells[4].text == email):
				found = True
				break

		self.assertTrue(found, "User not found: "+email)
		
		# deep verify in edit
		edit_link = self.check_element_present(row, By.CLASS_NAME, 'fa-edit')
		edit_link.click()

		country_chosen = self.check_element_present(self.driver, By.CLASS_NAME,'select2-chosen')
		self.assertIsNotNone(country_chosen, "Unable to view extended details.")
		self.assertEqual(country_chosen.text, country, "Country doesn't match: "+country)

		return True

	def admin_createtour(self, tourdict):
		sidebar_menu = self.check_element_present(self.driver, By.ID, "social-sidebar-menu")
		self.assertIsNotNone(sidebar_menu, "No Admin sidebar")

		tours_link = self.check_element_present(sidebar_menu, By.LINK_TEXT,'Tours')
		self.assertIsNotNone(tours_link, "No Tours link in sidebar.")
		tours_link.click()

		add_link = self.check_element_present(sidebar_menu, By.LINK_TEXT,'Add New')
		self.assertIsNotNone(add_link, "No Add New link in sidebar.")
		add_link.click()

		# Tour Name
		tourname_field = self.check_element_present(self.driver, By.NAME,'tourname')
		self.assertIsNotNone(tourname_field, "No 'tourname' field.")
		self.assertIsNone(tourname_field.send_keys(tourdict['tourname']),"Sending Tour Name: "+tourdict['tourname'])

		# Tour Description
		tour_richframe = self.check_element_present(self.driver, By.CLASS_NAME,'cke_wysiwyg_frame')
		self.assertIsNotNone(tour_richframe, "No frame for description.")
		self.driver.switch_to.frame(tour_richframe)
		tour_description = self.check_element_present(self.driver, By.TAG_NAME,'body')
		self.assertIsNotNone(tour_description, "No body to write description in.")

		for description_line in tourdict['description']:
			tour_description.send_keys(description_line)

		self.driver.switch_to.default_content()

		# Adult Max Number
		maxadult_field = self.check_element_present(self.driver, By.NAME,'maxadult')
		self.assertIsNotNone(maxadult_field, "No 'maxadult' field.")
		self.assertIsNone(maxadult_field.send_keys(tourdict['adultquantity']))

		# Adult Price
		adultprice_field = self.check_element_present(self.driver, By.NAME,'adultprice')
		self.assertIsNotNone(adultprice_field, "No 'adultprice' field.")
		self.assertIsNone(adultprice_field.send_keys(tourdict['adultprice']))

		# Stars
		if 'stars' in tourdict:
			stars_dropdown = self.check_element_present(self.driver, By.NAME,'tourstars')
			self.assertIsNotNone(stars_dropdown, "No Stars dropdown.")
			stars_dropdown.click()
			star_option = self.check_element_present(self.driver, By.XPATH,"//select[@name='tourstars']/option[@value='"+tourdict['stars']+"']")
			self.assertIsNotNone(star_option, "No option for Star Rating: "+tourdict['stars'])
			star_option.click()

		# Total Days
		if 'days' in tourdict:
			tourdays_field = self.check_element_present(self.driver, By.NAME,'tourdays')
			self.assertIsNotNone(tourdays_field, "No 'tourdays' field.")
			self.assertIsNone(tourdays_field.send_keys(tourdict['days']))

		# Total Nights
		if 'nights' in tourdict:
			tournights_field = self.check_element_present(self.driver, By.NAME,'tournights')
			self.assertIsNotNone(tournights_field, "No 'tournights' field.")
			self.assertIsNone(tournights_field.send_keys(tourdict['nights']))

		# Tour Type
		tourtype_dropdown = self.check_element_present(self.driver, By.ID,'s2id_autogen11')
		self.assertIsNotNone(tourtype_dropdown, "No Tour Type drop down.")
		tourtype_dropdown.click()

		tourtype_entry = self.check_element_present(self.driver, By.CLASS_NAME,'select2-focused')
		self.assertIsNotNone(tourtype_entry, "No field to enter type.")
		tourtype_entry.click()
		self.assertIsNone(tourtype_entry.send_keys(tourdict['type']),"Sending type: "+tourdict['type'])

		tourtype_found = self.check_element_present(self.driver, By.CLASS_NAME,'select2-match')
		self.assertIsNotNone(tourtype_found, "Tour Type not found in list: "+tourdict['type'])
		tourtype_found.click()

		# Multiple Locations
		loci = 1
		for location in tourdict['locations']:
			locationselector = self.check_element_present(self.driver, By.ID,'s2id_locationlist'+str(loci))
			self.assertIsNotNone(locationselector, "No Location drop down: "+str(loci))
			locationselector.click()

			location_entry = self.check_element_present(self.driver, By.CLASS_NAME,'select2-focused')
			self.assertIsNotNone(location_entry, "No field to enter location.")
			location_entry.click()
			self.assertIsNone(location_entry.send_keys(location),"Sending location: "+location)

			location_found = self.check_element_present(self.driver, By.CLASS_NAME,'select2-match')
			self.assertIsNotNone(location_found, "Location not found in list: "+location)
			location_found.click()
			
			loci += 1

		# Tour Type
		done_button = self.check_element_present(self.driver, By.ID,'add')
		self.assertIsNotNone(done_button, "No Done button to add tour.")
		done_button.click()		

		return True

	def admin_verifytour(self, tourdict):
		# restart to dashboard
		dashboard_link = self.check_element_present(self.driver, By.LINK_TEXT, "Dashboard")
		self.assertIsNotNone(dashboard_link, "No Dashboard Link.")
		dashboard_link.click()

		sidebar_menu = self.check_element_present(self.driver, By.ID, "social-sidebar-menu")
		self.assertIsNotNone(sidebar_menu, "No Admin sidebar")

		tours_link = self.check_element_present(sidebar_menu, By.LINK_TEXT,'Tours')
		self.assertIsNotNone(tours_link, "No Tours link in sidebar.")
		tours_link.click()

		tours_menu = self.check_element_present(sidebar_menu, By.ID,'Tours')
		self.assertIsNotNone(tours_menu, "Tours menu did not expand.")

		tours2_link = self.check_element_present(tours_menu, By.LINK_TEXT,'Tours')
		self.assertIsNotNone(tours2_link, "No 2nd level Tours link in sidebar.")
		tours2_link.click()

		# Verify on right page
		panel_heading = self.check_element_present(self.driver, By.CLASS_NAME, 'panel-heading')
		# try again once if still on old pane 5 seconds later
		if (panel_heading.text != 'Tours Management'):
			time.sleep(5)
			panel_heading = self.check_element_present(self.driver, By.CLASS_NAME, 'panel-heading')

		self.assertEqual(panel_heading.text, 'Tours Management', 'Not on Tours Management page.')

		rows = self.driver.find_elements(By.CLASS_NAME, 'xcrud-row')

		self.assertIsNot(0, len(rows), "No list of tours")

		found = False
		for row in rows:
			cells = row.find_elements_by_tag_name("td")
			if (cells[4].text == tourdict['tourname']):
				found = True
				break

		self.assertTrue(found, "Tour not found: "+tourdict['tourname'])
		
		# deep verify in edit
		edit_link = self.check_element_present(row, By.CLASS_NAME, 'fa-edit')
		edit_link.click()

		# Tour Description
		tour_richframe = self.check_element_present(self.driver, By.CLASS_NAME,'cke_wysiwyg_frame')
		self.assertIsNotNone(tour_richframe, "No frame for description.")
		self.driver.switch_to.frame(tour_richframe)
		tour_description = self.check_element_present(self.driver, By.TAG_NAME,'body')
		self.assertIsNotNone(tour_description, "No body of description to get.")

		existing_description = tour_description.text
		for description_line in tourdict['description']:
			# Exception for short bits (the line feed)
			if (len(description_line) > 6):
				self.assertTrue(description_line in existing_description)

		self.driver.switch_to.default_content()

		# Adult Max Number
		maxadult_field = self.check_element_present(self.driver, By.NAME,'maxadult')
		self.assertIsNotNone(maxadult_field, "No 'maxadult' field.")
		self.assertEqual(maxadult_field.get_attribute('value'), tourdict['adultquantity'])

		# Adult Price
		adultprice_field = self.check_element_present(self.driver, By.NAME,'adultprice')
		self.assertIsNotNone(adultprice_field, "No 'adultprice' field.")
		self.assertEqual(adultprice_field.get_attribute('value'), tourdict['adultprice'])

		# Stars
		if 'stars' in tourdict:
			stars_dropdown = self.check_element_present(self.driver, By.NAME,'tourstars')
			self.assertIsNotNone(stars_dropdown, "No Stars dropdown.")
			self.assertEqual(Select(stars_dropdown).first_selected_option.text, tourdict['stars'])

		# Total Nights
		if 'nights' in tourdict:
			tournights_field = self.check_element_present(self.driver, By.NAME,'tournights')
			self.assertIsNotNone(tournights_field, "No 'tournights' field.")
			self.assertEqual(tournights_field.get_attribute('value'), tourdict['nights'])

		# Tour Type
		tourtype_dropdown = self.check_element_present(self.driver, By.NAME,'tourtype')
		self.assertIsNotNone(tourtype_dropdown, "No Tour Type drop down.")
		self.assertEqual(Select(tourtype_dropdown).first_selected_option.text, tourdict['type'])


		# Multiple Locations
		loci = 1
		for location in tourdict['locations']:
			locationselector = self.check_element_present(self.driver, By.ID,'s2id_locationlist'+str(loci))
			self.assertIsNotNone(locationselector, "No Location drop down: "+str(loci))

			self.assertTrue(tourdict['locations'][loci-1] in locationselector.text)
			loci += 1


		return True


	def user_book_tour(self, username, password, tourdict):
		self.driver.get("http://www.phptravels.net/")

		tours_link = self.check_element_present(self.driver, By.LINK_TEXT, "Tours")
		self.assertIsNotNone(tours_link, "No Tours Link.")
		tours_link.click()

		star_guide = self.check_element_present(self.driver,By.CLASS_NAME, "rating")
		self.assertIsNotNone(star_guide, "No Star Guide.")

		star_wanted = self.check_element_present(star_guide, By.CSS_SELECTOR, "input[name='stars'][value='"+tourdict['stars']+"']")
		self.assertIsNotNone(star_guide, "No Radio rating for: "+tourdict['stars'])

		# Get the parent, and then the floating sibling
		star_parent = self.check_element_present(star_wanted, By.XPATH, "..")
		floating_over_star = self.check_element_present(star_parent, By.TAG_NAME, 'ins')
		self.assertIsNotNone(floating_over_star, "Floating layer over rating selection now missing.")
		floating_over_star.click()

		star_wanted.submit()

		# new page load

		tours_results = self.check_element_present(self.driver, By.CLASS_NAME, "itemscontainer")

		rows = tours_results.find_elements(By.CLASS_NAME, 'itemlabel3')

		self.assertIsNot(0, len(rows), "No list of tours")

		# search for our tour in the link names
		found = False
		for row in rows:
			destinations = row.find_elements(By.XPATH, "//div[1]//h4//a")
			for link in destinations:
				# check for tour name in the tags
				if (link.text == tourdict['tourname']):
					found = link
					break
			# if found, go into the row's details
			if found:
				break

		self.assertTrue(found, "Unable to find specified tour.")
		found.click()

		# New Page Load here

		# Need a cousin of the text "Booking Options". Find text, find grand parent (booking_optioons_panel), find right cousins after that.
		booking_options_text = self.check_element_present(self.driver, By.XPATH, "//span[text()='Booking Options']")
		self.assertIsNotNone(booking_options_text, 'Unable to find "Booking Options" text.')
		booking_options_panel = self.check_element_present(booking_options_text, By.XPATH, "../..")

		# Set number of Adults
		adults_dropdown = self.check_element_present(booking_options_panel, By.ID,'selectedAdults')
		self.assertIsNotNone(adults_dropdown, "No Selected Adults dropdown.")
		adults_dropdown.click()
		adults_dropdown_value = self.check_element_present(adults_dropdown, By.XPATH,"//option[@value='"+tourdict['adultquantity']+"']")
		self.assertIsNotNone(adults_dropdown_value, "No option for number of adults: "+tourdict['adultquantity'])
		adults_dropdown_value.click()

		book_now_button = self.check_element_present(booking_options_panel, By.XPATH, "//button[text()='Book Now']")
		self.assertIsNotNone(book_now_button, 'No "Book Now" button found.')
		book_now_button.submit()

		# new Page Load here

		sign_in_button = self.check_element_present(self.driver, By.ID, 'signintab')
		self.assertIsNotNone(book_now_button, 'No "Sign In" button found (prior to credentials).')
		sign_in_button.click()

		# re-draw page

		username_field = self.check_element_present(self.driver, By.ID, 'username')
		self.assertIsNotNone(username_field, 'No username field (email) found.')
		self.assertIsNone(username_field.send_keys(username),"Sending username: "+username)
		
		password_field = self.check_element_present(self.driver, By.ID, 'password')
		self.assertIsNotNone(password_field, 'No password field found.')
		self.assertIsNone(password_field.send_keys(password),"Sending password: "+password)

		confirm_booking_button = self.check_element_present(self.driver, By.XPATH, "//button[text()='CONFIRM THIS BOOKING']")
		self.assertIsNotNone(confirm_booking_button, 'No Confirm Booking button found.')

		# Set timeout longer. Not using explicit, as that changes the Exceptions
		self.driver.implicitly_wait(20)

		confirm_booking_button.click()

		# Verify it loads up to the Invoice
		invoice_text = self.check_element_present(self.driver, By.XPATH, "//div[text()='Invoice']")
		self.assertIsNotNone(invoice_text, "Invoice did not load.")

		# and put timeout back
		self.driver.implicitly_wait(__timeout__)

		return True

	def check_element_present(self, parent_element, how, what):
		"""
		Helper method to check for an element's presence on page.
		Both will wait for and verify existance.
		:params parent_element: driver to use
		:params how: 'By' locator type
		:params what: locator what/element/name/id
		"""
		try:
			element = parent_element.find_element(by=how, value=what)
		except NoSuchElementException:
			return None
		return element

	def click_on_top_layer(self, element, xoffset, yoffset):
		try: 
			action = webdriver.common.action_chains.ActionChains(self.driver)
			action.move_to_element_with_offset(element, xoffset, yoffset)
			action.click()
			action.perform()
		except NoSuchElementException:
			return False
		return True

	def test_01_create_account(self):
		# makesure signed in as admin
		self.assertTrue(self.admin_signin('admin@phptravels.com', 'demoadmin'), "Unable to Sign In.")
		self.assertTrue(self.admin_createuser('sampleuser01@example.net', 'SamplePass01', 'Sarah', 'Sample', 'United States'), "Unable to create user.")
		self.assertTrue(self.admin_verifyuser('sampleuser01@example.net', 'SamplePass01', 'Sarah', 'Sample', 'United States'), "User wasn't created correctly.")

	def test_02_create_tour(self):
		tour = {
			'tourname' : "Iocane's Origin",
			'description' : ["Because iocane comes from Australia, as everyone knows, and Australia is entirely peopled with criminals, and criminals are used to having people not trust them, as you are not trusted by me, so I can clearly not choose the wine in front of you.",Keys.RETURN," - Vizzini"],
			'adultquantity' : '5',
			'adultprice' : '5142',
			'type' : 'Adventure',
			'locations' : ['Austral Downs'],
			'stars' : '4',
			'nights' : '6',
			'days' : '7'
		}
		self.assertTrue(self.admin_signin('admin@phptravels.com', 'demoadmin'), "Unable to Sign In.")
		self.assertTrue(self.admin_createtour(tour), "Unable to create tour.")
		self.assertTrue(self.admin_verifytour(tour), "Unable to verify tour created.")

	def test_03_join_tour(self):
		tour = {
			'tourname' : "Iocane's Origin",
			'adultquantity' : '2',
			'adultprice' : '5142',
			'type' : 'Adventure',
			'locations' : ['Austral Downs'],
			'stars' : '4',
		}
		self.assertTrue(self.user_book_tour('sampleuser01@example.net', 'SamplePass01', tour), "Unable to book tour.")

if __name__ == '__main__':
    unittest.main()

