from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
import time
import easyocr
from pathlib import Path


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
        self.max_count = 40 # 最多打招乎次数
        self.location = '北京' # 区域
        self.salary_num = 22 # 薪资区间的最高点，没有达到这个数字就会被过滤掉
        # 要排除的公司
        self.exclude_company_list = [
            '汉克',
            '七凌',
            '法本',
            '纬创',
            '柯莱特',
            '德科',
            '数字马力',
            '金道天成',
            '慧博云通',
            '亿达',
            '软通',
            '科锐尔',
            '字节',
            '慧教研',
            '神州通誉',
            '国简科技',
            '浪潮数字',
            '六易在线',
            '微创'
        ]
    
    # 删除截出来的薪资图片
    def del_img(self, path):
        file_path = Path(path)
        try:
            file_path.unlink()
            print(f"文件 {file_path} 删除成功！")
        except FileNotFoundError:
            print(f"文件 {file_path} 不存在！")
        except PermissionError:
            print(f"没有权限删除 {file_path}！")
        except Exception as e:
            print(f"删除失败：{e}")

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
                # 职位名称
                job_name = element.find_element(By.CLASS_NAME, "job-name").text
                # 薪资元素
                salary = element.find_element(By.CLASS_NAME, "job-salary")
                salary.screenshot(f'./{job_name}.png')
                # 创建reader对象
                reader = easyocr.Reader(['ch_sim','en']) 
                # 读取图像中的薪资数字
                result = reader.readtext(f'./{job_name}.png')
                salary_str = result[0][1]
                # 取出来薪资范围中的最大值
                max_salary = salary_str.split('K')[0].split('-')[1]
                print(f'salary-->{result[0][1]}---{max_salary}')
                self.del_img(f'./{job_name}.png')
                # 公司名称
                boss_name = element.find_element(By.CLASS_NAME, "boss-name").text
                # 地址
                location = element.find_element(By.CLASS_NAME, "company-location").text
                # 按职位名称 公司名称 地址 薪资过滤
                if any(keyword in job_name for keyword in self.used_job_name_list):
                    if all(company_name not in boss_name for company_name in self.exclude_company_list):
                        if self.location in location and int(max_salary) >= self.salary_num:
                            print(f'职位名称={job_name}-公司名称={boss_name}-地址={location}--薪资={max_salary}')
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
                # self.driver.refresh()
                # # 找到职位按钮点击
                # WebDriverWait(self.driver, 5).until(
                #     EC.visibility_of_element_located((By.LINK_TEXT, "职位"))
                # ).click()
                self.driver.get("https://www.zhipin.com/web/geek/jobs?salary=405")
                time.sleep(3)
                WebDriverWait(self.driver, 5).until(
                    EC.visibility_of_element_located((By.LINK_TEXT, f"前端开发工程师({self.location})"))
                ).click()
                time.sleep(3)
                self.click_job()

            print(f'有效点击次数 -> {self.click_count}')
        except Exception as exc:
            print('error', exc)
        finally:
            time.sleep(100)
            self.driver.quit()


if __name__ == "__main__":
    job_clicker = JobClicker()
    job_clicker.start()