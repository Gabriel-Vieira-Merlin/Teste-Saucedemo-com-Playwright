from playwright.sync_api import Page, expect
import pytest

#Testa se o títle da página é Swag Labs
def test_title(page: Page):
    page.goto("https://www.saucedemo.com")
    assert page.title() == "Swag Labs"

#Teste se o site bloqueia acessos sem estar logado
def test_epicsadface(page: Page):
    page.goto("https://www.saucedemo.com/inventory.html")
    assert page.inner_text('h3') == "Epic sadface: You can only access '/inventory.html' when you are logged in."

#Verifica se um compra está sendo feita
def test_compra(page:Page):
    page.goto("https://www.saucedemo.com")

    #Faz o login e senha
    page.fill('xpath=//*[@id="user-name"]', 'standard_user')
    page.fill('xpath=//*[@id="password"]', 'secret_sauce')
    page.click('xpath=//*[@id="login-button"]')

    #Adiciona a mochila ao carrinho de compras
    page.click('xpath=//*[@id="add-to-cart-sauce-labs-backpack"]')

    #Vai até o carrinho e verifica se o produto foi adicionado
    page.click('xpath=//*[@id="shopping_cart_container"]/a')
    assert page.locator('xpath=//*[@id="item_4_title_link"]/div').inner_text() == "Sauce Labs Backpack"

    #Prossegue com a compra
    page.click('xpath=//*[@id="checkout"]')

    #Preenche nome, sobrenome e código postal e finaliza a conta
    page.fill('xpath=//*[@id="first-name"]', 'Teste')
    page.fill('xpath=//*[@id="last-name"]', 'Playwright')
    page.fill('xpath=//*[@id="postal-code"]', '12345678')
    page.click('xpath=//*[@id="continue"]')

    #Verfica se o produto está no checkout overview
    assert page.locator('xpath=//*[@id="item_4_title_link"]/div').inner_text() == "Sauce Labs Backpack"

    #Verifica se o preço está correto
    assert page.locator('xpath=//*[@id="checkout_summary_container"]/div/div[2]/div[8]').inner_text() == "Total: $32.39"

    #Finaliza a compra
    page.click('xpath=//*[@id="finish"]')

    #Verifica se a compra foi realizada
    assert page.inner_text('h2') == "Thank you for your order!"