"""
Bulk Scraper with Progress Saving
This version saves data every N pages to prevent data loss
"""

import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
import json
from datetime import datetime
import os


class CCRBulkScraper:
    """Bulk scraper with checkpoint saving"""
    
    COLUMN_MAPPING = {
        0: "رقم التسجيل",
        1: "المحافظة",
        2: "تاريخ التسجيل",
        3: "مالك المؤسسة",
        4: "العنوان التجاري",
        5: "الإسم التجاري",
        6: "رأس المال الحالي",
        7: "الحالة",
        8: "الإجراء",
    }
    
    def __init__(self, config_file='config.json'):
        self.config = self.load_config(config_file)
        self.driver = None
        self.data = []
        self.checkpoint_interval = 10  # Save every 10 pages
        self.start_time = datetime.now()
        
    def load_config(self, config_file):
        if os.path.exists(config_file):
            with open(config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def setup_driver(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--start-maximized')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, self.config.get('wait_timeout', 15))
        print("✓ WebDriver initialized")
    
    def navigate_and_search(self):
        print(f"Navigating to {self.config['url']}...")
        self.driver.get(self.config['url'])
        time.sleep(self.config.get('page_load_delay', 3))
        
        # Click search button
        search_btn = self.wait.until(EC.element_to_be_clickable((By.ID, "pt1:pt_region0:1:b1")))
        search_btn.click()
        time.sleep(self.config.get('page_load_delay', 3))
        print("✓ Search executed")
    
    def extract_page_data(self):
        time.sleep(2)
        
        try:
            main_table = self.driver.find_element(By.ID, "pt1:pt_region0:1:t4")
            rows = main_table.find_elements(By.TAG_NAME, "tr")
            
            page_data = []
            for row in rows[2:]:
                try:
                    cells = row.find_elements(By.TAG_NAME, "td")
                    if not cells or len(cells) < 3:
                        continue
                    
                    row_data = {}
                    for i in range(min(9, len(cells))):
                        try:
                            cell_text = cells[i].text.strip()
                            column_name = self.COLUMN_MAPPING.get(i, f"Column_{i+1}")
                            row_data[column_name] = cell_text
                        except:
                            continue
                    
                    if row_data.get("رقم التسجيل") and row_data["رقم التسجيل"] not in ['', 'عرض']:
                        page_data.append(row_data)
                        
                except:
                    continue
            
            return page_data
        except Exception as e:
            print(f"Error extracting: {e}")
            return []
    
    def click_next(self):
        try:
            # Strategy 1: Direct ID for next button
            try:
                next_btn = self.driver.find_element(By.ID, "pt1:pt_region0:1:t4::nb_nx")
                if next_btn.is_displayed() and next_btn.is_enabled():
                    # Check if not disabled
                    if 'p_AFDisabled' not in next_btn.get_attribute('class'):
                        next_btn.click()
                        return True
            except:
                pass
            
            # Strategy 2: Look for "الصفحة التالية" (Next Page)
            try:
                next_links = self.driver.find_elements(By.XPATH, 
                    "//a[@title='الصفحة التالية' or @aria-label='الصفحة التالية']")
                for link in next_links:
                    if link.is_displayed() and 'p_AFDisabled' not in link.get_attribute('class'):
                        link.click()
                        return True
            except:
                pass
            
            # Strategy 3: JavaScript click
            try:
                script = """
                var nextBtn = document.getElementById('pt1:pt_region0:1:t4::nb_nx');
                if (nextBtn && !nextBtn.className.includes('p_AFDisabled')) {
                    nextBtn.click();
                    return true;
                }
                return false;
                """
                result = self.driver.execute_script(script)
                if result:
                    return True
            except:
                pass
            
            return False
        except Exception as e:
            return False
    
    def save_checkpoint(self, page_num, filename_prefix="ccr_checkpoint"):
        if not self.data:
            return
        
        df = pd.DataFrame(self.data)
        df = df.fillna('')
        
        # Remove duplicates
        df = df.drop_duplicates(subset=['رقم التسجيل'], keep='first')
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{filename_prefix}_page{page_num}_{timestamp}.xlsx"
        df.to_excel(filename, index=False, engine='openpyxl')
        
        elapsed = (datetime.now() - self.start_time).total_seconds()
        rate = len(df) / (elapsed / 60) if elapsed > 0 else 0
        
        print(f"\n💾 CHECKPOINT SAVED: {filename}")
        print(f"   📊 Total records: {len(df):,}")
        print(f"   ⏱️  Time elapsed: {elapsed/60:.1f} minutes")
        print(f"   📈 Rate: {rate:.1f} records/minute\n")
    
    def run(self):
        try:
            print("\n" + "="*70)
            print("  BULK SCRAPER - Commercial Companies Registry")
            print("="*70 + "\n")
            
            self.setup_driver()
            self.navigate_and_search()
            
            max_pages = self.config['pagination']['max_pages']
            print(f"🎯 Target: {max_pages:,} pages\n")
            
            page = 1
            consecutive_failures = 0
            
            while page <= max_pages:
                print(f"[Page {page:,}/{max_pages:,}] ", end='', flush=True)
                
                page_data = self.extract_page_data()
                
                if page_data:
                    self.data.extend(page_data)
                    print(f"✓ Got {len(page_data)} records | Total: {len(self.data):,}")
                    consecutive_failures = 0
                    
                    # Checkpoint save
                    if page % self.checkpoint_interval == 0:
                        self.save_checkpoint(page)
                    
                    # Try next page
                    if page < max_pages:
                        if self.click_next():
                            time.sleep(self.config.get('page_load_delay', 2))
                            page += 1
                        else:
                            print("\n⚠️  Cannot find next button")
                            break
                    else:
                        break
                else:
                    consecutive_failures += 1
                    print(f"✗ No data (failure {consecutive_failures}/3)")
                    if consecutive_failures >= 3:
                        break
                    page += 1
            
            # Final save
            if self.data:
                print("\n" + "="*70)
                df = pd.DataFrame(self.data)
                df = df.fillna('')
                df = df.drop_duplicates(subset=['رقم التسجيل'], keep='first')
                
                final_filename = f"ccr_final_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
                df.to_excel(final_filename, index=False, engine='openpyxl')
                
                print(f"✅ FINAL DATA SAVED: {final_filename}")
                print(f"📊 Total unique records: {len(df):,}")
                print(f"📄 Total pages scraped: {page}")
                print(f"⏱️  Total time: {(datetime.now() - self.start_time).total_seconds()/60:.1f} minutes")
                print("="*70 + "\n")
            
        except KeyboardInterrupt:
            print("\n\n⚠️  INTERRUPTED BY USER - Saving data...")
            if self.data:
                self.save_checkpoint(page, "ccr_interrupted")
        except Exception as e:
            print(f"\n✗ Error: {e}")
            if self.data:
                self.save_checkpoint(page, "ccr_error")
        finally:
            if self.driver:
                self.driver.quit()


if __name__ == "__main__":
    scraper = CCRBulkScraper()
    scraper.run()
