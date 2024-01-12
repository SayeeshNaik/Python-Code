import requests
import sys
sys.path.append("D:\PythonCodes\WebScrapping Projects\CaptchaSolver")
import captcha_solver


captcha_php_url = "	https://karnatakajudiciary.kar.nic.in/repository/captcha.php"
captcha = captcha_solver.captcha_solver_php(captcha_php_url)
print("Captcha = ",captcha)

headers = {
    'Cookie': '{}'.format(captcha),
}

response = requests.post('https://karnatakajudiciary.kar.nic.in/repository/rep_judgment_details.php', headers=headers)
print(response.text)

