from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
import re
import json
import os



from selenium.webdriver.support.ui import WebDriverWait

# fp = webdriver.FirefoxProfile('C:\\Users\\AndreaFrancesco\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\ia63cg2l.default-release')
# fp = webdriver.FirefoxProfile('C:\\Users\\AndreaFrancesco\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\o90bpr8r.default-release-1')
fp = webdriver.FirefoxProfile(
    'C:\\Users\\AndreaFrancesco\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\wqj7yfbe.default-release-3')

driver = webdriver.Firefox(fp)  # Chrome_Options is deprecated. So we use options instead.


driver.get('http://www.studiodazzi.it/admin')

username = driver.find_element_by_xpath('//*[@id="login-container"]/form/input[1]')
username.send_keys('nicoletta.podesta')

password = driver.find_element_by_xpath('//*[@id="login-container"]/form/input[2]')
password.send_keys('forno425')

loginButton = driver.find_element_by_xpath('//*[@id="login-container"]/form/input[3]')
loginButton.click()

windows_before = driver.current_window_handle

normalizzaLink = driver.find_element_by_link_text('Normalizza Cliente Immobiliare.it')
normalizzaLink.click()

WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))
windows_after = driver.window_handles
new_window = [x for x in windows_after if x != windows_before][0]
driver.switch_to.window(new_window)



#chrome_options = webdriver.ChromeOptions();
#chrome_options.add_experimental_option("prefs", {"download.prompt_for_download": False, "plugins.always_open_pdf_externally": True})


#
time.sleep(30)


def insertElement():
    global senzaZona
    senzaZona = False
    isToDelete = False

    global stazioni


    elementInterno = driver.find_element_by_xpath('/html/body/table/tbody/tr[3]/td/table/tbody/tr/td[1]')
    classInterno = elementInterno.text
    requestId = classInterno.split("idRichiesta=")[1].split(" DDDD")[0]
    driver.get('https://pro.immobiliare.it/v2/richieste_utente.php?idRichiesta=' + requestId)
    time.sleep(7)

    try:
        closeButton6 = driver.find_element_by_xpath('/html/body/div[6]/div/div/div/div[3]/div/button')
        if closeButton6 is not None and closeButton6.is_enabled():
            print("Element CloseButton6 found")
            closeButton6.click()
    except NoSuchElementException:
        print("Element CloseButton6 not found")

    try:
        isCloseButton2 = False
        closeButton2 = driver.find_element_by_xpath('/html/body/div[2]/div/div/div/div[3]/div/button')
        if closeButton2 is not None and closeButton2.is_enabled():
            print("Element CloseButton2 found")
            isCloseButton2 = True
            isCloseButton4 = False

    except NoSuchElementException:
        print("Element CloseButton2 not found")
    try:
        isCloseButton4 = False
        closeButton = driver.find_element_by_xpath('/html/body/div[4]/div/div/div/div[3]/div/button')
        if closeButton is not None and closeButton.is_enabled() and closeButton.text == 'STAMPA':
            print("Element CloseButton4 found")
            isCloseButton4 = True
            isCloseButton2 = False
            senzaZona = True
            #closeButton.click()
    except NoSuchElementException:
        print("Element CloseButton4 not found")
    try:
        if isCloseButton2:
            mappa = driver.find_element_by_xpath('/html/body/div[2]/div/div/div/div[2]/div/div[1]/div[2]/div[1]/img')
        else:
            mappa = driver.find_element_by_xpath('/html/body/div[4]/div/div/div/div[2]/div/div[1]/div[2]/div[1]/img')
    except NoSuchElementException:
        print("Element Mappa not found")
        senzaZona = True

    try:
        checkStazione = driver.find_element_by_xpath(
            '/html/body/div[4]/div/div/div/div[2]/div/div[1]/div[2]/div[2]/div[2]/ul/li/div')
        if 'STAZIONE' in checkStazione.text:
            stazioni = driver.find_element_by_xpath(
                '/html/body/div[4]/div/div/div/div[2]/div/div[1]/div[2]/div[2]/div[2]').text

    except NoSuchElementException:
        print("Element Stazione not found")

    time.sleep(2)
    if isCloseButton2:
        nameImm = driver.find_element_by_xpath('/html/body/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div[1]/div[2]').text
        cognomeImm = driver.find_element_by_xpath('/html/body/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div[2]/div[2]').text
        emailImm = driver.find_element_by_xpath('/html/body/div[2]/div/div/div/div[2]/div/div[2]/div[3]/div[1]/div[2]/a').text
        phoneImm = driver.find_element_by_xpath('/html/body/div[2]/div/div/div/div[2]/div/div[2]/div[3]/div[2]/div[2]').text
        messageImm = driver.find_element_by_xpath('/html/body/div[2]/div/div/div/div[2]/div/div[2]/div[4]/div/div[2]').text
    elif isCloseButton4:
        nameImm = driver.find_element_by_xpath('/html/body/div[4]/div/div/div/div[2]/div/div[2]/div[2]/div[1]/div[2]').text
        cognomeImm = driver.find_element_by_xpath('/html/body/div[4]/div/div/div/div[2]/div/div[2]/div[2]/div[2]/div[2]').text
        emailImm = driver.find_element_by_xpath('/html/body/div[4]/div/div/div/div[2]/div/div[2]/div[3]/div[1]/div[2]/a').text
        phoneImm = driver.find_element_by_xpath('/html/body/div[4]/div/div/div/div[2]/div/div[2]/div[3]/div[2]/div[2]').text
        messageImm = driver.find_element_by_xpath('/html/body/div[4]/div/div/div/div[2]/div/div[2]/div[4]/div/div[2]').text
    else:
        isToDelete = True
        print("caso strano")

    driver.execute_script("window.history.go(-1)")

    if stazioni != '':
        decidiZone()

    time.sleep(2)
    if isToDelete:
        driver.find_element_by_xpath('/html/body/table/tbody/tr[3]/td/table/tbody/tr/td[1]/form[2]/div/input').click()
        return
    nomeCognome = driver.find_element_by_xpath(
        '/html/body/table/tbody/tr[3]/td/table/tbody/tr/td[1]/form[1]/fieldset[1]/input')
    nomeCognome.clear()
    nomeCognome.send_keys(nameImm + ' ' + cognomeImm)
    email = driver.find_element_by_xpath(
        '/html/body/table/tbody/tr[3]/td/table/tbody/tr/td[1]/form[1]/fieldset[2]/input')
    email.send_keys(emailImm)
    telefono = driver.find_element_by_xpath(
        '/html/body/table/tbody/tr[3]/td/table/tbody/tr/td[1]/form[1]/fieldset[3]/input')
    telefono.send_keys(phoneImm)
    testo = driver.find_element_by_xpath(
        '/html/body/table/tbody/tr[3]/td/table/tbody/tr/td[1]/form[1]/fieldset[4]/textarea')
    testo.send_keys(messageImm)


    if isSenzaZoneSelected() and senzaZona:
        checkNessunaZona = driver.find_element_by_xpath(
            '/html/body/table/tbody/tr[3]/td/table/tbody/tr/td[1]/form[1]/fieldset[4]/input[21]'
        ).click()

    messaggio = "nome: " + nameImm + ' ' + cognomeImm + \
                " email: " + emailImm + \
                " telefono: " + phoneImm + \
                " testo: " + messageImm + \
                " request: https://pro.immobiliare.it/v2/richieste_utente.php?idRichiesta=" + requestId

    modificaButton = driver.find_element_by_name('aggiungi')
    modificaButton.click()

    print(messaggio)

    time.sleep(2)

def isSenzaZoneSelected():

    for item in mappingZone:
        if driver.find_element_by_xpath(item['input']).is_selected():
            return False
    return True
def decidiZone():

    global stazioni
    global senzaZona
    senzaZona = True

    #stazioni = driver.find_element_by_xpath('/html/body/div[4]/div/div/div/div[2]/div/div[1]/div[2]/div[2]/div[2]').text
    for line in stazioni.splitlines():
        lineCleaned = line.replace("STAZIONE ", "").lower()

        for zone in macrozones:
            if lineCleaned in zone['child']:
                print(zone['label'])
                for item in mappingZone:
                    if item['label'] == zone['label']:
                        driver.find_element_by_xpath(item['input']).click()
                        senzaZona = False
                        break
                break
        print('none')
        stazioni = ''


def getMetroZones():
    #https://www.immobiliare.it/search/macrozones?id=8042&type=3
    global macrozones

    input_file = open('macrozones.json')
    json_array = json.load(input_file)
    macrozones = []
    for item in json_array:
        for child in item['children']:
            store_details = {"label": None, "child": None}
            store_details['label'] = item['label']
            store_details['child'] = child['label'].lower()
            macrozones.append(store_details)
    print('stop')

def getMappingZone():
    global mappingZone

    input_file = open('mappingZonezInput.json')
    json_array = json.load(input_file)
    mappingZone = []
    for item in json_array:
        store_details = {"label": None, "input": None}
        store_details['label'] = item['label']
        store_details['input'] = item['input']
        mappingZone.append(store_details)

# while True:

count = 0

macrozones = []
mappingZone = []
stazioni = ''
senzaZona = False

getMetroZones()
getMappingZone()

while (count < 200):
    insertElement()

    print('The count is:', count)
    count = count + 1

print("Good bye!")
