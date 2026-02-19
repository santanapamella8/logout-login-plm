from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

# ===== CONFIGURAÇÃO =====
options = UiAutomator2Options()
options.platform_name = "Android"
options.device_name = "Android"
options.app_package = "br.com.zaruc.plmandroid"
options.automation_name = "UiAutomator2"
options.no_reset = True
options.full_reset = False

driver = webdriver.Remote("http://localhost:4723", options=options)
wait = WebDriverWait(driver, 10)

# ===== SCROLL ATÉ LOGOUT =====
logout_btn = wait.until(
    EC.presence_of_element_located(
        (AppiumBy.ANDROID_UIAUTOMATOR,
         'new UiScrollable(new UiSelector().scrollable(true))'
         '.scrollIntoView(new UiSelector().text("Logout"));')
    )
)

# ===== LOGOUT (long press) =====
driver.execute_script("mobile: longClickGesture", {
    "elementId": logout_btn.id,
    "duration": 1500
})

# ===== OK - Confirma logout =====
wait.until(
    EC.element_to_be_clickable(
        (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("OK")')
    )
).click()

# ===== OK - Usuario deslogado =====
wait.until(
    EC.element_to_be_clickable(
        (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("OK")')
    )
).click()

print("Logout realizado com sucesso.")

# ===== LOGIN =====

# 🔐 Pegando usuário e senha das variáveis de ambiente
usuario = os.getenv("PLM_USER")
senha = os.getenv("PLM_PASS")

if not usuario or not senha:
    raise Exception("Variáveis PLM_USER e PLM_PASS não configuradas.")

campos = wait.until(
    EC.presence_of_all_elements_located(
        (AppiumBy.CLASS_NAME, "android.widget.EditText")
    )
)

campos[0].clear()
campos[0].send_keys(usuario)

campos[1].clear()
campos[1].send_keys(senha)

wait.until(
    EC.element_to_be_clickable(
        (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Entrar")')
    )
).click()

# ===== NÃO - Login Offline =====
wait.until(
    EC.element_to_be_clickable(
        (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("NÃO")')
    )
).click()

# ===== Selecionar Unidade =====
wait.until(
    EC.element_to_be_clickable(
        (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("47-PRODUCAO ZARUC")')
    )
).click()

print("Login realizado com sucesso!")

driver.quit()
