# CCR Web Scraper - Commercial Companies Registry

A Python web scraper for extracting data from the Jordanian Commercial Companies Registry website.

## 🌐 Target Website

**URL**: https://ccr.mit.gov.jo/mitq/faces/HomePage

**Description**: Automated data extraction tool for commercial company records in Jordan.

---

## ✨ Features

- ✅ **Automated Scraping**: Extracts data from all pages automatically
- ✅ **Smart Pagination**: Handles website navigation seamlessly
- ✅ **Checkpoint System**: Saves progress every 10 pages to prevent data loss
- ✅ **Arabic Support**: Properly handles Arabic text and column names
- ✅ **Error Handling**: Robust error recovery and retry mechanisms
- ✅ **Progress Tracking**: Live progress updates in terminal
- ✅ **Multiple Export Formats**: Excel (.xlsx) and CSV support
- ✅ **Configurable**: Easy configuration via JSON file

---

## 📊 Data Collected

The scraper extracts the following information for each company:

| Column | Arabic Name | Description |
|--------|-------------|-------------|
| Registration Number | رقم التسجيل | Unique company registration ID |
| Governorate | المحافظة | Location/region |
| Registration Date | تاريخ التسجيل | Date of registration |
| Institution Owner | مالك المؤسسة | Owner name |
| Commercial Address | العنوان التجاري | Business address |
| Trade Name | الإسم التجاري | Company trade name |
| Current Capital | رأس المال الحالي | Current capital amount |
| Status | الحالة | Company status |
| Action | الإجراء | Available actions |

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Google Chrome browser
- Stable internet connection

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd data
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

### Basic Usage

**Run the scraper:**
```bash
python scraper_bulk.py
```

That's it! The scraper will start collecting data automatically.

---

## ⚙️ Configuration

Edit `config.json` to customize scraping behavior:

```json
{
  "url": "https://ccr.mit.gov.jo/mitq/faces/HomePage",
  "wait_timeout": 10,
  "page_load_delay": 2,
  "pagination": {
    "scrape_all_pages": true,
    "max_pages": 200000
  },
  "output": {
    "format": "excel",
    "filename": "ccr_data_{date}.xlsx"
  }
}
```

### Configuration Options

- **`wait_timeout`**: Maximum seconds to wait for page elements (default: 10)
- **`page_load_delay`**: Seconds to wait between page loads (default: 2)
- **`max_pages`**: Maximum number of pages to scrape (default: 200000)
- **`format`**: Output format - "excel" or "csv"
- **`filename`**: Output filename pattern (use {date} for timestamp)

---

## 📈 Performance

Based on testing:
- **Scraping Rate**: ~50 records per minute
- **Total Records**: ~764,242 records across 152,849 pages
- **Estimated Time**: ~255 hours (~10.6 days) for complete dataset
- **Output File Size**: ~100-150 MB for full dataset

---

## 📁 Output Files

### Automatic Saves

1. **Checkpoint Files** (every 10 pages):
   - `ccr_checkpoint_page10_YYYYMMDD_HHMMSS.xlsx`
   - `ccr_checkpoint_page20_YYYYMMDD_HHMMSS.xlsx`
   - Prevents data loss if scraper is interrupted

2. **Final Output**:
   - `ccr_final_YYYYMMDD_HHMMSS.xlsx`
   - Complete dataset with all records

3. **Interrupted Saves**:
   - `ccr_interrupted_pageXXX_YYYYMMDD_HHMMSS.xlsx`
   - Saved automatically if you stop the scraper (Ctrl+C)

---

## 🛠️ Project Structure

```
data/
├── scraper_bulk.py          # Main production scraper
├── scraper_final.py         # Alternative scraper version
├── config.json              # Configuration file
├── requirements.txt         # Python dependencies
├── view_data.py             # Data viewer utility
├── README.md                # This file
└── START_HERE.md            # Detailed usage guide
```

---

## 📖 Usage Examples

### Example 1: Test Run (100 pages)

```bash
# Edit config.json, set "max_pages": 100
python scraper_bulk.py
```

### Example 2: Partial Scrape (10,000 pages)

```bash
# Edit config.json, set "max_pages": 10000
python scraper_bulk.py
```

### Example 3: Full Scrape (All Data)

```bash
# Edit config.json, set "max_pages": 200000
python scraper_bulk.py
```

### Example 4: View Scraped Data

```bash
python view_data.py
```

---

## 🎯 Scraping Workflow

```
1. Load Website → 2. Click Search → 3. Extract Page Data
                                              ↓
        6. Save Final File ← 5. Next Page ← 4. Save Checkpoint
                                 ↓
                            (Repeat 3-5)
```

---

## ⚠️ Important Notes

### For Long-Running Scrapes

1. **Disable Sleep Mode**: Prevent computer from sleeping
   ```bash
   powercfg /change standby-timeout-ac 0
   ```

2. **Stable Internet**: Ensure reliable connection

3. **Monitor Progress**: Check terminal output regularly

4. **Keep Checkpoint Files**: They're your backup if something goes wrong

### Stopping Safely

Press `Ctrl + C` to stop. The scraper will:
- Save all collected data
- Create an "interrupted" file
- Close browser cleanly

---

## 🔍 Data Viewing

View your scraped data quickly:

```bash
python view_data.py
```

Output:
```
Reading: ccr_final_20251004_144851.xlsx

Total rows: 44
Total columns: 9

Columns:
  1. رقم التسجيل
  2. المحافظة
  3. تاريخ التسجيل
  ...
```

---

## 🐛 Troubleshooting

### Issue: Browser closes unexpectedly
**Solution**: Increase `page_load_delay` in config.json to 3-4 seconds

### Issue: "Stale element" errors
**Solution**: Normal behavior, scraper handles this automatically

### Issue: Slow scraping speed
**Solution**: 
- Close unnecessary applications
- Check internet connection
- Reduce `page_load_delay` to 1 (if connection is stable)

### Issue: No data extracted
**Solution**: Website might be down or blocking. Wait and retry.

---

## 📊 Sample Output

| رقم التسجيل | المحافظة | تاريخ التسجيل | مالك المؤسسة | رأس المال الحالي | الحالة |
|------------|---------|--------------|-------------|----------------|--------|
| 100160 | عمان | 09/06/1997 | محمود عبدالفتاح | 500 | مفسوخه |
| 100506 | عمان | 02/07/1997 | محمود عبدالفتاح | 500 | قائمه |
| 399576 | عمان | 30/10/2017 | مراد غالب | 1,000 | قائمة / محجوزة |

---

## 🔐 Legal & Ethical Use

- This scraper is for **legitimate data collection** purposes only
- Respect the website's terms of service
- Avoid excessive request rates that could impact server performance
- Use collected data responsibly and in compliance with local regulations

---

## 🤝 Contributing

Improvements and suggestions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## 📝 Technical Details

### Technologies Used

- **Selenium**: Web automation and browser control
- **Pandas**: Data manipulation and Excel export
- **OpenPyXL**: Excel file handling
- **Chrome WebDriver**: Browser automation driver

### Browser Requirements

- Google Chrome (latest version recommended)
- ChromeDriver (automatically managed by webdriver-manager)

---

## 📞 Support

For issues or questions:
1. Check `START_HERE.md` for detailed guide
2. Review troubleshooting section above
3. Check terminal output for error messages

---

## 📅 Version History

### Version 1.0 (October 2025)
- Initial release
- Bulk scraping with checkpoint system
- Arabic text support
- Configurable via JSON
- Progress tracking
- Multiple export formats

---

## ⚡ Performance Tips

1. **Internet Speed**: Faster connection = faster scraping
2. **Page Delay**: Reduce to 1-2 seconds if connection is stable
3. **Checkpoint Interval**: Adjust in `scraper_bulk.py` (line 27)
4. **Headless Mode**: Uncomment in code for slightly better performance

---

## 📦 Dependencies

```
selenium>=4.15.0
pandas>=2.0.0
openpyxl>=3.1.0
webdriver-manager>=4.0.0
```

See `requirements.txt` for complete list.

---

## 🎓 Learning Resources

- [Selenium Documentation](https://selenium-python.readthedocs.io/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Web Scraping Best Practices](https://www.scrapehero.com/web-scraping-best-practices/)

---

## ✅ Tested On

- Windows 10/11
- Python 3.8, 3.9, 3.10, 3.11, 3.13
- Chrome 120+

---

## 📄 License

This project is provided as-is for data collection purposes. Please ensure compliance with local laws and website terms of service when using this tool.

---

**Built with ❤️ for efficient data collection**

**Last Updated**: October 5, 2025
