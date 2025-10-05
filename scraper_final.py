"""
Final Production Scraper for CCR
This version includes proper column naming and better data extraction
"""

import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
import json
from datetime import datetime
import os


class CCRScraperFinal:
    """Production-ready Scraper for Commercial Companies Registry"""
    
    # Column mapping based on the website structure
    COLUMN_MAPPING = {
        0: "رقم التسجيل",  # Registration Number
        1: "المحافظة",  # Governorate
        2: "تاريخ التسجيل",  # Registration Date
        3: "مالك المؤسسة",  # Institution Owner
        4: "العنوان التجاري",  # Commercial Address
        5: "الإسم التجاري",  # Trade Name
        6: "رأس المال الحالي",  # Current Capital
        7: "الحالة",  # Status
        8: "الإجراء",  # Action
    }
    
    def __init__(self, config_file='config.json'):
        """Initialize the scraper with configuration"""
        self.config = self.load_config(config_file)
        self.driver = None
        self.data = []
        
    def load_config(self, config_file):
        """Load configuration from JSON file"""
        if os.path.exists(config_file):
            with open(config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return self.get_default_config()
    
    def get_default_config(self):
        """Return default configuration"""
        return {
            "url": "https://ccr.mit.gov.jo/mitq/faces/HomePage",
            "wait_timeout": 15,
            "page_load_delay": 4,
            "search_params": {
                "registration_number": "",
                "national_id_investor": "",
                "trade_name": "",
                "national_id_establishment": ""
            },
            "pagination": {
                "scrape_all_pages": True,
                "max_pages": 100
            },
            "output": {
                "format": "excel",
                "filename": "ccr_data_{date}.xlsx"
            }
        }
    
    def setup_driver(self):
        """Setup Chrome WebDriver"""
        options = webdriver.ChromeOptions()
        options.add_argument('--start-maximized')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        # Uncomment to run headless
        # options.add_argument('--headless')
        
        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, self.config['wait_timeout'])
        print("✓ WebDriver initialized successfully")
    
    def navigate_to_page(self):
        """Navigate to the main page"""
        print(f"Navigating to {self.config['url']}...")
        self.driver.get(self.config['url'])
        time.sleep(self.config['page_load_delay'])
        print("✓ Page loaded successfully")
    
    def click_search(self):
        """Click the search button"""
        print("Clicking search button...")
        
        try:
            search_btn = self.wait.until(
                EC.element_to_be_clickable((By.ID, "pt1:pt_region0:1:b1"))
            )
            search_btn.click()
            print("✓ Search button clicked")
            time.sleep(self.config['page_load_delay'])
            return True
        except Exception as e:
            print(f"✗ Error clicking search button: {e}")
            return False
    
    def extract_table_data(self):
        """Extract data from the results table"""
        print("Extracting table data...")
        
        try:
            # Wait for dynamic content to load
            time.sleep(3)
            
            # Find the main data table
            main_table = self.driver.find_element(By.ID, "pt1:pt_region0:1:t4")
            
            # Get all rows
            rows = main_table.find_elements(By.TAG_NAME, "tr")
            print(f"Found {len(rows)} total rows in table")
            
            page_data = []
            
            # Extract data - skip first 2 rows (filter row and header row)
            for row_idx, row in enumerate(rows[2:], start=2):
                try:
                    cells = row.find_elements(By.TAG_NAME, "td")
                    
                    if not cells or len(cells) < 3:
                        continue
                    
                    # Extract text from first 9 columns (the main data columns)
                    row_data = {}
                    for i in range(min(9, len(cells))):
                        try:
                            cell_text = cells[i].text.strip()
                            column_name = self.COLUMN_MAPPING.get(i, f"Column_{i+1}")
                            row_data[column_name] = cell_text
                        except (StaleElementReferenceException, IndexError):
                            continue
                    
                    # Only add rows with registration number
                    if row_data.get("رقم التسجيل") and row_data["رقم التسجيل"] not in ['', 'عرض']:
                        page_data.append(row_data)
                        
                except StaleElementReferenceException:
                    continue
                except Exception as e:
                    continue
            
            print(f"✓ Extracted {len(page_data)} valid rows")
            return page_data
            
        except Exception as e:
            print(f"✗ Error extracting table data: {e}")
            return []
    
    def get_pagination_info(self):
        """Get total pages and current page info"""
        try:
            # Look for pagination text like "الصفحة 1 من (المجموع) 11848 (من 5-1) جزء"
            pagination_elements = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'الصفحة') or contains(text(), 'من')]")
            for elem in pagination_elements:
                text = elem.text
                if 'الصفحة' in text or 'من' in text:
                    print(f"Pagination info: {text}")
                    # Try to extract total pages
                    import re
                    match = re.search(r'من\s*\(المجموع\)\s*(\d+)', text)
                    if match:
                        total = int(match.group(1))
                        return total
            return None
        except:
            return None
    
    def click_next_page(self):
        """Click the next page button"""
        try:
            # Strategy 1: Look for "›" or next arrow in the pagination area
            next_links = self.driver.find_elements(By.XPATH, "//a[contains(text(), '›') or contains(text(), '>')]")
            for link in next_links:
                # Check if it's visible and clickable
                if link.is_displayed() and link.is_enabled():
                    # Check if not disabled
                    parent_class = link.get_attribute('class') or ''
                    if 'disabled' not in parent_class.lower():
                        link.click()
                        return True
            
            # Strategy 2: Look for elements with specific navigation classes
            nav_elements = self.driver.find_elements(By.XPATH, 
                "//a[contains(@id, 'next') or contains(@id, 'Next') or contains(@class, 'next')]")
            for elem in nav_elements:
                if elem.is_displayed() and elem.is_enabled():
                    elem.click()
                    return True
            
            # Strategy 3: JavaScript click on pagination
            # Find the table and look for its pagination controls
            try:
                script = """
                var tables = document.querySelectorAll('div[id*="t4"]');
                for (var i = 0; i < tables.length; i++) {
                    var nextBtns = tables[i].querySelectorAll('a');
                    for (var j = 0; j < nextBtns.length; j++) {
                        if (nextBtns[j].innerText.includes('›') || nextBtns[j].innerText.includes('>')) {
                            nextBtns[j].click();
                            return true;
                        }
                    }
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
            print(f"Error clicking next page: {e}")
            return False
    
    def handle_pagination(self):
        """Handle pagination to scrape all pages"""
        page_number = 1
        max_pages = self.config['pagination']['max_pages']
        consecutive_failures = 0
        
        # Get total pages info
        total_pages = self.get_pagination_info()
        if total_pages:
            print(f"\n📊 Total pages detected: {total_pages:,}")
            print(f"⚙️  Configured max pages: {max_pages:,}")
            if max_pages < total_pages:
                print(f"⚠️  Will scrape first {max_pages:,} pages only (change config to scrape more)")
        
        while page_number <= max_pages:
            print(f"\n--- Page {page_number}/{max_pages if max_pages < 99999 else '?'} ---")
            
            # Extract current page data
            page_data = self.extract_table_data()
            
            if not page_data:
                consecutive_failures += 1
                print(f"⚠️  No data on this page (failure {consecutive_failures}/3)")
                if consecutive_failures >= 3:
                    print("✓ No more data found after 3 attempts, stopping.")
                    break
            else:
                consecutive_failures = 0  # Reset on success
                self.data.extend(page_data)
                print(f"📈 Total records so far: {len(self.data)}")
            
            # Try to go to next page
            if page_number < max_pages:
                print("Attempting to navigate to next page...")
                if self.click_next_page():
                    print("✓ Navigated to next page")
                    time.sleep(self.config['page_load_delay'])
                    page_number += 1
                else:
                    print("✓ Could not find next page button - reached end")
                    break
            else:
                print(f"✓ Reached configured maximum of {max_pages} pages")
                break
    
    def save_data(self):
        """Save scraped data to file"""
        if not self.data:
            print("⚠ No data to save")
            return None
        
        # Create DataFrame
        df = pd.DataFrame(self.data)
        
        # Clean up the data
        df = df.fillna('')
        
        # Generate filename with current date
        date_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = self.config['output']['filename'].replace('{date}', date_str)
        
        # Save based on format
        output_format = self.config['output']['format']
        
        if output_format == 'csv':
            filename = filename.replace('.xlsx', '.csv')
            df.to_csv(filename, index=False, encoding='utf-8-sig')
        else:
            df.to_excel(filename, index=False, engine='openpyxl')
        
        print(f"\n✓ Data saved to: {filename}")
        print(f"✓ Total rows: {len(df)}")
        print(f"✓ Columns: {list(df.columns)}")
        
        # Show sample data
        if len(df) > 0:
            print(f"\nSample data (first row):")
            for col in df.columns:
                value = df[col].iloc[0]
                if value:
                    print(f"  {col}: {value}")
        
        return filename
    
    def run(self):
        """Main execution method"""
        try:
            print("\n" + "="*60)
            print("  Commercial Companies Registry - Final Scraper")
            print("="*60 + "\n")
            
            # Setup
            self.setup_driver()
            self.navigate_to_page()
            
            # Click search (with empty params = all results)
            if self.click_search():
                # Scrape data
                if self.config['pagination']['scrape_all_pages']:
                    self.handle_pagination()
                else:
                    page_data = self.extract_table_data()
                    self.data.extend(page_data)
                
                # Save results
                if self.data:
                    self.save_data()
                    print("\n✓ Scraping completed successfully!")
                else:
                    print("\n⚠ No data was extracted")
            
        except Exception as e:
            print(f"\n✗ Error during scraping: {e}")
            import traceback
            traceback.print_exc()
            
        finally:
            if self.driver:
                print("\nClosing browser in 3 seconds...")
                time.sleep(3)
                self.driver.quit()


def main():
    """Main entry point"""
    scraper = CCRScraperFinal()
    scraper.run()


if __name__ == "__main__":
    main()
