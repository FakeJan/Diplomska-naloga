import wave
import os
from playwright.sync_api import Playwright, expect
from time import sleep

# playwright codegen demo.playwright.dev/todomvc


def login(page):
    # print("Logged in successfully")
    # page.goto("https://staging-editor.true-bar.si/")
    page.get_by_placeholder("Uporabniško ime").click()
    page.get_by_placeholder("Uporabniško ime").fill("jani")
    page.get_by_placeholder("Geslo").click()
    page.get_by_placeholder("Geslo").fill("mIqrfAx490@6")
    page.get_by_role("button", name="PRIJAVA").click()
    page.locator(".modal_wrapper").first.click()


def playAudio(page, path):
    '''Predvaja zvonci posnetek preko mikrofona'''
    page.get_by_role("button", name="V ŽIVO").click()

    with wave.open(path) as mywav:
        frames = mywav.getnframes()
        rate = mywav.getframerate()
        duration = frames / float(rate)
        sleep(duration)

    page.get_by_role("button").first.click()
    sleep(1)


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
    audio = "\\Audio files\\input.wav"
    audioPath = os.getcwd() + audio
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


# def test_dosnemavanje(playwright: Playwright) -> None:
#     '''Narek dosnemavanje'''
#     chromium = playwright.chromium
#     browser = chromium.launch(headless=False, args=[
#         '--use-fake-device-for-media-stream',
#         '--use-fake-ui-for-media-stream',
#         '--use-file-for-fake-audio-capture={0}'.format(path)])
#     context = browser.new_context()
#     context.grant_permissions(permissions=['microphone'])
#     page = context.new_page()

#     page.goto("https://staging-editor.true-bar.si/")
#     page.get_by_placeholder("Uporabniško ime").click()
#     page.get_by_placeholder("Uporabniško ime").fill("jani")
#     page.get_by_placeholder("Geslo").click()
#     page.get_by_placeholder("Geslo").fill("mIqrfAx490@6")
#     page.get_by_role("button", name="PRIJAVA").click()
#     page.locator(".modal_wrapper").first.click()
#     page.get_by_role("button", name="V ŽIVO").click()
#     sleep(1)
#     with wave.open(path) as mywav:
#         frames = mywav.getnframes()
#         rate = mywav.getframerate()
#         duration = frames / float(rate)
#         sleep(duration)

#     # stop speech button
#     page.get_by_role("button").first.click()

#     # dosnemavanje
#     page.locator("#footer").get_by_role("button").first.click()
#     sleep(1)
#     with wave.open(path) as mywav:
#         frames = mywav.getnframes()
#         rate = mywav.getframerate()
#         duration = frames / float(rate)
#         sleep(duration)

#     # stop recording
#     page.locator("#footer").get_by_role("button").first.click()

#     # save
#     sleep(5)
#     # name the recording
#     page.locator("input").click()
#     page.locator("input").fill("Narek dosnemavanje")
#     sleep(1)
#     page.locator("input").press("Enter")

#     page.get_by_role("button", name="KONČAJ").click()

#     page.get_by_role("button", name="ZGODOVINA").click()
#     locator = page.get_by_text("Narek dosnemavanje").first
#     expect(locator).to_have_text("Narek dosnemavanje")

#     # ---------------------
#     context.close()
#     browser.close()
