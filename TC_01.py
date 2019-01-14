import datetime
import unittest
import logging
import configparser
import page
import voorbereiding_UI_BP_1
import uitvoering_UI_BP_1
import os
import platform

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class TestCase_01(unittest.TestCase):
    
    def setUp(self):
        #print(platform.system())
        
        self.config = configparser.ConfigParser()
        logfile = os.environ["file_log"]
        path_to_log = os.environ["log_path"]
        path_to_ini = os.environ["ini_path"]
        
        self.config.read(path_to_ini+"init.ini")
        
        logging.basicConfig(level=logging.INFO, filename=path_to_log+logfile, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        logging.info("Setting up Driver")
        
        chromeOptions = Options()
        if platform.system()=="Linux": 
            chromeOptions.add_argument("--headless")
        chromeOptions.add_argument('--no-sandbox')
        chromeOptions.add_argument("--window-size=1920,1080")
        chromeOptions.add_argument('--disable-dev-shm-usage')
        
        if platform.system()=="Windows":
            self.driver = webdriver.Chrome(r"C:/Selenium_Jar_MR/anders/chromedriver.exe",chrome_options=chromeOptions) 
        elif platform.system()=="Linux":
            self.driver = webdriver.Chrome(r"/usr/local/bin/chromedriver",chrome_options=chromeOptions)
        

        logging.info("Setting Driver Settings")
        link = "https://acceptatie2.vos.intranet.rijkswaterstaat.nl/ivs-gui-frontend/#/mededelingen"
        driver = self.driver
        driver.get(link)
        self.addCleanup(self.driver.quit)
        self.addCleanup(self.screen_shot)
        self.driver.implicitly_wait(2)
    
    def voorbereiding_start(self):
        '''
        Ga naar de 'Sas van Gent brug'
        Zoek het schip  KTV-KAT03 op in de zoekfunctie 
        Selecteer het schip 
        Check of de status op actueel staat
        Wanneer status op beeindigd staat, zet de status op actueel en klik op publiceer reis
        Klik op het icoon (potloodje) om huidige positie te wijzigen 
        Selecteer afvarend 
        Selecteer publiceer positie 
        Klik op het kruisje om de vaartuig detailbrowser af te sluiten 
        Druk op refresh rechtsonder in beeld (GUI)
        '''
        main_page = page.MainPage(self.driver)
        data_algemeen = self.config['INITdata_algemeen']
        data_specifiek = self.config['INITdata_BP_UI_01']
        username = data_algemeen['loginnaam']
        password = data_algemeen['password']
        main_page.login(username, password)
        ivs_page = voorbereiding_UI_BP_1.IVSPage(self.driver)
        brug = data_specifiek['object']
        ivs_page.navigate(brug)
        boot = data_specifiek['test_boot']
        eni_nummer = data_specifiek['eni_nummer']
        vaarrichting = data_specifiek['vaarrichting']
        ivs_page.voorbereiding_brugplanning(boot,eni_nummer,vaarrichting )
        
    def uitvoering_start(self):
        '''
        Check of schip KTV-KAT03 in de aanbodlijst staat van de brug (rechts)
        Klik op het plusje op een nieuwe brugplanning aan te maken
        Klik op schip KTV-KAT03 en sleep dit schip naar de brugplanning (rechterhelft)
        Ga naar ingedeeld (zelfde kant als schip is ingedeeld in de brugplanning (rechts)
        Check: schip staat in de lijst ingedeeld 
        Klik op aanbod (rechterkant)
        Check: schip staat niet meer op de aanbodslijst 
        Check: schip staat in de brugplanning 
        Druk op het witte rondje om het stoplicht op groen te zetten 
        Druk op het witte rondje om het stoplicht op rood te zetten 
        Selecteer 'ja'om de brugplaning te realiseren
        Check: Schip staat weer in de aanbodlijst (rechts)
        Check: Brugplanning is verdwenen 
        Klik op (naam account bv Bert Pril )
        Selecteer uitloggen 
        '''
        data_specifiek = self.config['INITdata_BP_UI_01']
        boot = data_specifiek['test_boot']
        eni_nummer = data_specifiek['eni_nummer']

        ivs_page = uitvoering_UI_BP_1.uitvoering_UI_BP_1(self.driver)
        ivs_page.new_brugplanning(boot,eni_nummer)
        ivs_page.sleur_en_pleur(boot,eni_nummer)
        ivs_page.check(boot,eni_nummer)
        ivs_page.uitvoeren_brugplanning(boot,eni_nummer)
        main_page = page.MainPage(self.driver)
        main_page.logout()
        
    def test_uc01(self):
        self.voorbereiding_start()
        self.uitvoering_start()
        
    def screen_shot(self):
        """
        In geval van error: Maak screenshot
        
        """
        path_to_log = os.environ["log_path"]
        for error in self._outcome.errors:
            if error[1]:
                self.driver.get_screenshot_as_file(path_to_log+"screenshot_error"+datetime.datetime.today().strftime('%Y%m%d%H%M%S%f')+".png")
                
        
    def tearDown(self):
        #self.driver.close()
        pass
        

if __name__ == '__main__':
    if platform.system()=="Windows": 
        if not (os.path.exists("./logs")):
            os.mkdir("./logs")
        path_to_log = "./logs/"
        path_to_ini = "./ini/"
    elif platform.system()=="Linux":
        path_to_log = "/var/logs/"
        path_to_ini = "/var/ini/"
    
    os.environ["log_path"] = path_to_log
    os.environ["ini_path"] = path_to_ini
    os.environ["web_wait"] = '60'
    
    logfile = datetime.datetime.today().strftime('%Y%m%d%H%M%S%f') +'.log'
    os.environ["file_log"] = logfile
    log_file = 'log_file.txt'
    f = open(log_file, "a")
    runner = unittest.TextTestRunner(f)
    unittest.main(testRunner=runner,exit=False)
    f.close()
    f = open(log_file, "r")
    file = open(path_to_log+logfile, "a")
    file.write('\n')
    file.write (f.read())
    file.close()
    f.close()
    os.remove(log_file)

