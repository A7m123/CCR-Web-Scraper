# CCR Web Scraper

Automated data extraction tool for the Jordanian Commercial Companies Registry.

## Quick Start

```bash
pip install -r requirements.txt
python scraper_bulk.py
```

## Features

- ✅ Automated scraping with pagination
- ✅ Checkpoint system (saves every 10 pages)
- ✅ Arabic text support
- ✅ Progress tracking
- ✅ ~50 records/minute

## Configuration

Edit `config.json`:
- `max_pages`: Number of pages to scrape
- `format`: "excel" or "csv"
- `page_load_delay`: Seconds between pages

## Output

Files are saved as:
- `ccr_checkpoint_pageN_TIMESTAMP.xlsx` (every 10 pages)
- `ccr_final_TIMESTAMP.xlsx` (final output)

## Documentation

- See `START_HERE.md` for detailed guide
- See `README_FULL.md` for complete documentation

## Tech Stack

Python 3.8+ | Selenium | Pandas | Chrome WebDriver

---

**Target**: ~764,000 records | **Rate**: ~50 records/min | **Time**: ~10 days
