from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

# ===== CONFIGURAÇÃO =====
options = UiAutomator2Options()
options.platform_name = "Android"
options.device_name = "Android"
options.app_package = "br.com.zaruc.plmandroid"
options.automation_name = "UiAutomator2"
options.no_reset = True
options.full_reset = False

driver = webdriver.Remote("http://localhost:4723", options=options)
wait = WebDriverWait(driver, 15)

try:
    # ==============================
    # ===== LOGOUT (SE ESTIVER LOGADO)
    # ==============================
    try:
        logout_btn = wait.until(
            EC.presence_of_element_located(
                (AppiumBy.ANDROID_UIAUTOMATOR,
                 'new UiScrollable(new UiSelector().scrollable(true))'
                 '.scrollIntoView(new UiSelector().text("Logout"));')
            )
        )

        driver.execute_script("mobile: longClickGesture", {
            "elementId": logout_btn.id,
            "duration": 1500
        })

        # Confirma logout
        wait.until(
            EC.element_to_be_clickable(
                (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("OK")')
            )
        ).click()

        wait.until(
            EC.element_to_be_clickable(
                (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("OK")')
            )
        ).click()

        print("Logout realizado com sucesso.")

    except TimeoutException:
        print("Usuário já estava deslogado.")

    # ==============================
    # ===== LOGIN
    # ==============================

    # 🔐 ALTERE AQUI QUANDO QUISER
    usuario = "seu_usuario"
    senha = "sua_senha"

    # Aguarda campos de login
    campos = wait.until(
        EC.presence_of_all_elements_located(
            (AppiumBy.CLASS_NAME, "android.widget.EditText")
        )
    )

    if len(campos) < 2:
        raise Exception("Campos de login não encontrados.")

    campos[0].clear()
    campos[0].send_keys(usuario)

    campos[1].clear()
    campos[1].send_keys(senha)

    # Clicar em Entrar
    wait.until(
        EC.element_to_be_clickable(
            (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Entrar")')
        )
    ).click()

    # ==============================
    # ===== LOGIN OFFLINE (se aparecer)
    # ==============================
    try:
        wait.until(
            EC.element_to_be_clickable(
                (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("NÃO")')
            )
        ).click()
        print("Login offline recusado.")
    except TimeoutException:
        pass

    # ==============================
    # ===== SELECIONAR UNIDADE
    # ==============================
    wait.until(
        EC.element_to_be_clickable(
            (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("47-PRODUCAO ZARUC")')
        )
    ).click()

    print("Login realizado com sucesso!")

except Exception as e:
    print("Erro durante execução:", e)
    driver.save_screenshot("erro_login.png")
    print("Print salvo como erro_login.png")

finally:
    time.sleep(2)
    driver.quit()
