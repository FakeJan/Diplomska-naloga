import wave
import os
from playwright.sync_api import Playwright, expect
from time import sleep


def login(page):
    '''Prijavi se v aplikacijo'''
    page.goto("https://speech-to-text.si")
    page.get_by_placeholder("Uporabniško ime").click()
    page.get_by_placeholder("Uporabniško ime").fill("username")
    page.get_by_placeholder("Geslo").click()
    page.get_by_placeholder("Geslo").fill("password")
    page.get_by_role("button", name="PRIJAVA").click()
    page.locator(".modal_wrapper").first.click()


def playAudio(page, path):
    '''Predvaja zvocni posnetek preko mikrofona'''
    # press start
    page.get_by_role("button", name="V ŽIVO").click()

    with wave.open(path) as mywav:
        frames = mywav.getnframes()
        rate = mywav.getframerate()
        duration = frames / float(rate)
        sleep(duration)

    page.get_by_role("button").first.click()
    sleep(1)


def addRecording(page, path):
    '''Dosnemavanje'''
    page.locator("#footer").get_by_role("button").first.click()
    sleep(1)
    with wave.open(path) as mywav:
        frames = mywav.getnframes()
        rate = mywav.getframerate()
        duration = frames / float(rate)
        sleep(duration)

    # stop recording
    page.locator("#footer").get_by_role("button").first.click()


def nameRecording(page, name):
    '''Damo posnetku ime in shranimo'''
    sleep(1)
    page.locator("input").click()
    page.locator("input").fill(name)
    sleep(1)
    page.locator("input").press("Enter")
    page.get_by_role("button", name="KONČAJ").click()


def checkHistory(page, name):
    '''Pogledamo ce je posnetek v zgodovini'''
    page.get_by_role("button", name="ZGODOVINA").click()
    sleep(5)
    locator = page.get_by_text(name).first
    expect(locator).to_have_text(name)


def deleteRecording(page):
    '''Zbrise kreiran posnetek iz zgodovine'''
    page.locator(
        ".row-extender-icon-wrapper > .MuiButtonBase-root").first.click()
    page.get_by_role("button", name="delete").click()
    page.get_by_role("button", name="Izbriši").click()


def test_narekovanje(playwright: Playwright) -> None:
    audio = "input.wav"
    audioPath = os.path.join(os.getcwd(), "Audio-Files", audio)
    chromium = playwright.chromium
    browser = chromium.launch(headless=False, args=[
        '--use-fake-device-for-media-stream',
        '--use-fake-ui-for-media-stream',
        '--use-file-for-fake-audio-capture={0}'.format(audioPath)])
    context = browser.new_context()
    context.grant_permissions(permissions=['microphone'])
    page = context.new_page()

    login(page)
    playAudio(page, audioPath)
    # ---------------------
    context.close()
    browser.close()


def test_dosnemavanje(playwright: Playwright) -> None:
    '''Narek dosnemavanje'''
    audio = "input.wav"
    audioPath = os.path.join(os.getcwd(), "Audio-Files", audio)
    name = "Narek dosnemavanje"
    chromium = playwright.chromium
    browser = chromium.launch(headless=False, args=[
        '--use-fake-device-for-media-stream',
        '--use-fake-ui-for-media-stream',
        '--use-file-for-fake-audio-capture={0}'.format(audioPath)])
    context = browser.new_context()
    context.grant_permissions(permissions=['microphone'])
    page = context.new_page()

    login(page)
    playAudio(page, audioPath)
    addRecording(page, audioPath)
    nameRecording(page, name)
    checkHistory(page, name)
    deleteRecording(page)
    # ---------------------
    context.close()
    browser.close()
