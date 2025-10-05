# 🚀 QUICK START GUIDE - CCR Data Scraper

## ✅ READY TO SCRAPE ALL DATA!

Your scraper is fully configured and tested. Here's what you need to know:

---

## 📊 SCRAPING STATISTICS

Based on our test run:
- **Rate**: ~50 records/minute (varies with internet speed)
- **Total Records**: ~764,242 records (152,849 pages)
- **Estimated Time**: ~255 hours (~10.6 days) of continuous running
- **File Size**: Approximately 100-150 MB for full dataset

---

## 🎯 THREE WAYS TO RUN

### Option 1: QUICK TEST (Recommended First)
Test with 100 pages to verify everything works:
```powershell
# Edit config.json and set max_pages to 100
python scraper_bulk.py
```

### Option 2: PARTIAL SCRAPE
Scrape a specific number of pages (e.g., 10,000 pages = ~50,000 records):
```powershell
# Edit config.json and set max_pages to 10000
python scraper_bulk.py
```

### Option 3: FULL SCRAPE (ALL DATA)
⚠️ **Warning**: This will run for ~10 days continuously!
```powershell
# Already configured in config.json with max_pages = 200000
python scraper_bulk.py
```

---

## 📁 OUTPUT FILES

The scraper automatically saves:

1. **Checkpoint Files** (every 10 pages):
   - `ccr_checkpoint_page10_YYYYMMDD_HHMMSS.xlsx`
   - `ccr_checkpoint_page20_YYYYMMDD_HHMMSS.xlsx`
   - etc.

2. **Final File** (at the end):
   - `ccr_final_YYYYMMDD_HHMMSS.xlsx`

3. **If Interrupted** (Ctrl+C):
   - `ccr_interrupted_pageXXX_YYYYMMDD_HHMMSS.xlsx`

---

## 🔧 IMPORTANT SETTINGS

### In `config.json`:

```json
{
  "page_load_delay": 2,        // Seconds to wait between pages (increase if errors)
  "max_pages": 200000,          // Maximum pages to scrape
  "format": "excel"             // "excel" or "csv"
}
```

### In `scraper_bulk.py`:

```python
self.checkpoint_interval = 10  // Save every N pages (line 27)
```

---

## ⚠️ TIPS FOR LONG RUNS

1. **Stable Internet**: Ensure your internet won't disconnect
2. **Power Settings**: Disable sleep mode on your computer
3. **Start Small**: Test with 100 pages first
4. **Monitor Progress**: Check the terminal output regularly
5. **Checkpoint Files**: Don't delete them - they're your backup!
6. **Run Overnight**: Start before going to bed for uninterrupted scraping

### Disable Sleep Mode (Windows):
```powershell
powercfg /change standby-timeout-ac 0
powercfg /change monitor-timeout-ac 30
```

---

## 🛑 HOW TO STOP SAFELY

Press `Ctrl + C` in the terminal. The scraper will:
1. Stop immediately
2. Save all collected data to an "interrupted" file
3. Close the browser cleanly

You can resume later by starting from where you left off (manually adjust start page).

---

## 📊 DATA COLUMNS

Your exported Excel file will have these columns:

| Column | Arabic Name | Description |
|--------|-------------|-------------|
| 1 | رقم التسجيل | Registration Number |
| 2 | المحافظة | Governorate |
| 3 | تاريخ التسجيل | Registration Date |
| 4 | مالك المؤسسة | Institution Owner |
| 5 | العنوان التجاري | Commercial Address |
| 6 | الإسم التجاري | Trade Name |
| 7 | رأس المال الحالي | Current Capital |
| 8 | الحالة | Status |
| 9 | الإجراء | Action |

---

## 🔍 VIEW YOUR DATA

To quickly check any Excel file:
```powershell
python view_data.py
```

---

## 🐛 TROUBLESHOOTING

### Problem: Browser keeps closing
**Solution**: Increase `page_load_delay` in config.json to 3 or 4

### Problem: "Stale element" errors
**Solution**: This is normal, the scraper handles it automatically

### Problem: No data extracted
**Solution**: The website might be down. Wait and try again.

### Problem: Very slow scraping
**Solution**: 
- Close other applications
- Check your internet speed
- Reduce `page_load_delay` to 1 (if stable)

---

## 📞 PROGRESS TRACKING

The terminal shows live progress:
```
[Page 1,234/200,000] ✓ Got 8 records | Total: 5,456
```

Every 10 pages, you'll see:
```
💾 CHECKPOINT SAVED: ccr_checkpoint_page50_20251004_120000.xlsx
   📊 Total records: 220
   ⏱️  Time elapsed: 4.5 minutes
   📈 Rate: 48.9 records/minute
```

---

## 🎯 RECOMMENDED WORKFLOW

### Day 1: Test Run
```powershell
# Set max_pages to 100 in config.json
python scraper_bulk.py
# Verify data looks good
python view_data.py
```

### Day 2: Overnight Run
```powershell
# Set max_pages to 10000 (will take ~3-4 hours)
python scraper_bulk.py
# Let it run overnight
```

### Day 3+: Full Run
```powershell
# Set max_pages to 200000
python scraper_bulk.py
# Let it run for ~10 days
# Check checkpoint files daily
```

---

## ✅ FINAL CHECKLIST

Before starting the full scrape:

- [ ] Tested with 100 pages successfully
- [ ] Checked output Excel file
- [ ] Disabled computer sleep mode
- [ ] Stable internet connection
- [ ] Enough disk space (~500 MB free)
- [ ] Terminal window stays open
- [ ] Boss approved the timeline 😊

---

## 🚀 START SCRAPING NOW!

```powershell
python scraper_bulk.py
```

**Good luck! The scraper will handle everything automatically.**

---

## 📝 Files Summary

- `scraper_bulk.py` - Main scraper (use this one!)
- `config.json` - Configuration
- `view_data.py` - Quick data viewer
- `README.md` - Full documentation
- `requirements.txt` - Dependencies

---

**Created: October 4, 2025**
**Status: ✅ READY TO USE**
