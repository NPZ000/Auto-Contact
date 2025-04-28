from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
import time


class JobClicker:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.click_count = 0
        # 只点击包含以下关键字的职位
        self.used_job_name_list = [
            '前端',
            'react',
            'React',
            'vue',
            'Vue',
            '小程序'
        ]
        self.max_count = 30 # 最多打招乎次数

    def set_cookie(self):
        cookie = {
            "name": "wt2",  # 替换为实际的 Cookie 名称
            # wt2的值粘贴到这里
            "value": "",
            "domain": ".zhipin.com",
            "path": "/",
            "httpOnly": True
        }
        self.driver.delete_all_cookies()
        time.sleep(2)
        self.driver.add_cookie(cookie)

    def click_job(self):
        try:
            box_elements = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "job-card-wrap"))
            )

            # 过滤掉不相关的职位
            filter_list = []
            for element in box_elements:
                job_name = element.find_element(By.CLASS_NAME, "job-name").text
                print(f'职位名称={job_name}')
                if any(keyword in job_name for keyword in self.used_job_name_list):
                    filter_list.append(element)

            for box in filter_list:
                try:
                    box.click()  # 点击元素
                    time.sleep(5)
                    try:
                        element = WebDriverWait(self.driver, 10).until(
                            EC.visibility_of_element_located((By.LINK_TEXT, "立即沟通"))
                        )
                        print("找到元素，准备点击...")
                        element.click()
                        self.click_count += 1
                        WebDriverWait(self.driver, 10).until(
                            EC.visibility_of_element_located((By.LINK_TEXT, "留在此页"))
                        ).click()
                    except Exception as err:
                        print(f"等待超时：未找到 '立即沟通' 或元素不可见: {err}")
                    finally:
                        continue
                except Exception as e:
                    print(f"点击失败: {e}")
                    continue
        except Exception as e:
            print(f"获取职位卡片失败: {e}")

    def start(self):
        try:
            self.driver.get("https://www.zhipin.com/beijing/?seoRefer=index")
            self.set_cookie()
            self.driver.refresh()

            while self.click_count < self.max_count:
                # 刷新页面
                self.driver.refresh()
                # 找到职位按钮点击
                WebDriverWait(self.driver, 5).until(
                    EC.visibility_of_element_located((By.LINK_TEXT, "职位"))
                ).click()
                time.sleep(5)
                # 如果有特定的求职期望，替换下面的“职位（城市）”
                WebDriverWait(self.driver, 5).until(
                    EC.visibility_of_element_located((By.LINK_TEXT, "前端开发工程师(北京)"))
                ).click()
                time.sleep(3)
                self.click_job()

            print(f'有效点击次数 -> {self.click_count}')
        except Exception as exc:
            print('error', exc)
        finally:
            time.sleep(10)
            self.driver.quit()


if __name__ == "__main__":
    job_clicker = JobClicker()
    job_clicker.start()