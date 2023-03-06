from time import sleep
import wave
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


# login function
def login(driver, url):
    driver.get(url)
    assert driver.title == "True-bark"
    sleep(1)
    # input name
    driver.find_element(
        By.XPATH, "/html/body/div/div/main/div/form/div[1]/div[2]/div[2]/div[1]/div/input").send_keys("jani")
    sleep(1)

    # input password
    driver.find_element(
        By.XPATH, "/html/body/div/div/main/div/form/div[1]/div[2]/div[2]/div[2]/div/input").send_keys("mIqrfAx490@6")
    sleep(1)

    # press login
    driver.find_element(
        By.XPATH, "/html/body/div[1]/div/main/div/form/div[2]/div/button").click()
    sleep(1)

    # go to homepage
    driver.find_element(
        By.XPATH, "/html/body/div/div/main/div/form/button").click()
    sleep(1)


# play audio function
def playAudio(driver, path):
    # press v zivo
    driver.find_element(
        By.XPATH, "/html/body/div[1]/div/main/div/div[1]/div/div/button[1]").click()

    with wave.open(path) as mywav:
        frames = mywav.getnframes()
        rate = mywav.getframerate()
        duration = frames / float(rate)
        sleep(duration)

    # stop recording
    driver.find_element(
        By.XPATH, "/html/body/div[1]/div/main/div/div[3]/div/div/div/div/div[2]/div[2]/button").click()
    sleep(1)


# main function
def test_audio():
    audio = "\\Audio files\\input.wav"
    audioPath = os.getcwd() + audio
    chrome = "\\Webdriver\\chromedriver.exe"
    driverPath = os.getcwd() + chrome

    opt = Options()
    opt.add_argument("--use-fake-device-for-media-stream")
    opt.add_argument("--use-fake-ui-for-media-stream")
    opt.add_argument("--use-file-for-fake-audio-capture={0}".format(audioPath))
    opt.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver_service = Service(
        executable_path="{0}".format(driverPath))

    driver = webdriver.Chrome(service=driver_service, options=opt)

    aplikacijaUrl = "https://staging-editor.true-bar.si/"

    login(driver, aplikacijaUrl)
    playAudio(driver, audioPath)
    print("Test uspešno izveden")
    driver.quit()


test_audio()
