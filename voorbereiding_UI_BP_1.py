from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import logging
import re
import time
import os


class BasePage(object):
    """Base class to initialize the base page that will be called from all pages"""

    def __init__(self, driver):
        self.driver = driver
        
class IVSPage(BasePage):
    def navigate(self, brug):
        WAIT = int(os.environ["web_wait"])
        #WAIT = 30
        wait = WebDriverWait(self.driver, WAIT)
        logging.info("Going to "+brug)
        locator_login = (By.LINK_TEXT, brug)
        elem = wait.until(EC.presence_of_element_located(locator_login))
        elem = wait.until(EC.element_to_be_clickable(locator_login))
        elem.click()
        
    def voorbereiding_brugplanning(self, boot, eni_nummer, vaarrichting):
        WAIT = int(os.environ["web_wait"])
        #WAIT = 30
        wait = WebDriverWait(self.driver, WAIT)
        driver = self.driver
        #Brugplanningen opschonen
        
        
        planningen = driver.find_elements_by_css_selector('.delete-brugplanning-btn')
        if (len(planningen)>0):
            locator_prullenbak = (By.CSS_SELECTOR,'.delete-brugplanning-btn')
            wait.until(EC.element_to_be_clickable(locator_prullenbak))
            
        for planning in planningen:
            planning.click()
            bevestig = driver.find_element_by_css_selector("#btn-do-delete")
            bevestig.click()
        
        locator_plusje = (By.CSS_SELECTOR,".add-button .fa-plus")
        toevoegen = wait.until(EC.element_to_be_clickable(locator_plusje))
        toevoegen.click()
        
        logging.info("Zoek boot "+boot)
        locator_zoeken = (By.CSS_SELECTOR, "#vaartuig-search-input")
        elem = wait.until(EC.presence_of_element_located(locator_zoeken))
        elem.send_keys(boot)
        
        locator_window = (By.TAG_NAME, "ivs-overlay-window")
        window = wait.until(EC.presence_of_element_located(locator_window))
        
        locator_sub_venster = (By.CSS_SELECTOR, ".vaartuig-search-result-container")
        venster = wait.until(EC.presence_of_element_located(locator_sub_venster))
        
        #boten = []
        boten = venster.find_elements_by_css_selector('.vaartuig-identifier')
        for boot in boten:
            if (boot.text == eni_nummer):
                boot.click()
                break
                
        locator_boot = (By.CSS_SELECTOR,"[type='button'][aria-haspopup='true']")
        elem = wait.until(EC.presence_of_element_located(locator_boot))
        
        logging.info("Zet de status van de boot naar Actueel")
        
        locator_drop_down = (By.CSS_SELECTOR,".controle-and-acties [type='button'][aria-haspopup='true']")
        drop_down = wait.until(EC.presence_of_element_located(locator_drop_down))
        if (drop_down!='Actueel'):
            logging.info("De status van de boot is niet Actueel")
            drop_down.click()
            locator_menu = (By.CSS_SELECTOR, '[aria-labelledby="vaarreisSegment-status"]')
            elem = wait.until(EC.presence_of_element_located(locator_menu))
            options = []
            options = elem.find_elements_by_css_selector('.ng-star-inserted')
            for option in options:
                #print (option.text)
                if(option.text == 'Actueel'): 
                    option.click()
                    locator_publiceer = (By.CSS_SELECTOR,'#publiceer-reis-button')
                    elem = wait.until(EC.presence_of_element_located(locator_publiceer))
                    logging.info("De nieuwe status wordt gepubliceerd")
                    elem.click()
                    #Hier krijgen we meuk
                    
                    break
           
        locator_positie = (By.CSS_SELECTOR,'#invoeren-positie')
        elem = wait.until(EC.presence_of_element_located(locator_positie))
        logging.info("De positie van de boot veranderen")
        action=ActionChains(driver)
        action.move_to_element(elem).perform()
        elem.click() 
        locator_submenu = (By.CSS_SELECTOR,"[aria-labelledby='vaarreis-muteren-positie-vaarrichting']")
        elem = wait.until(EC.presence_of_element_located(locator_submenu))
        
        if (vaarrichting == 'afvarend'):
            logging.info("Selecteer afvarend")
            locator_afvarend = (By.CSS_SELECTOR,'.dropdown-item[translate="VTS_GEBIEDSLIJST.AFVAREND"]')
            elem = wait.until(EC.presence_of_element_located(locator_afvarend)) 
            elem.click()
        elif (vaarrichting == 'opvarend'):
            locator_opvarend = (By.CSS_SELECTOR,'.dropdown-item[translate="VTS_GEBIEDSLIJST.OPVAREND"]')
            elem = wait.until(EC.presence_of_element_located(locator_opvarend)) 
            elem.click()
            
        locator_publiceren = (By.CSS_SELECTOR,'.btn-success')
        elem = wait.until(EC.presence_of_element_located(locator_publiceren))
        #time.sleep(1)
        elem.click()
        locator_kruisje = (By.CSS_SELECTOR,".btn-delete[container='body']")
        elem = wait.until(EC.presence_of_element_located(locator_kruisje))
        elem.click()
        locator_ververs = (By.CSS_SELECTOR,'.navbar-dark #sector-refresh-btn')
        logging.info("Hoofdscherm verversen")
        elem = wait.until(EC.presence_of_element_located(locator_ververs))
        elem.click()

