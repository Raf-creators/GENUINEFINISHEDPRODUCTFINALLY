import asyncio
import json
from playwright.async_api import async_playwright
from datetime import datetime

async def scrape_checkatrade_reviews():
    """
    Scrape all reviews from PNM Gardening's Checkatrade page
    Handles dynamic loading via 'Load more' button
    """
    reviews = []
    
    async with async_playwright() as p:
        # Launch browser
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        # Navigate to the reviews page
        url = "https://www.checkatrade.com/trades/pnmgardening/reviews"
        print(f"Navigating to {url}...")
        await page.goto(url, wait_until="domcontentloaded", timeout=60000)
        
        # Wait for initial reviews to load
        await page.wait_for_selector('[data-testid="review-card"]', timeout=15000)
        
        # Click "Load more" button repeatedly until no more reviews
        load_more_count = 0
        max_attempts = 20  # Safety limit
        
        while load_more_count < max_attempts:
            try:
                # Look for the "Load more reviews" button
                load_more_button = page.locator('button:has-text("Load more reviews")')
                
                # Check if button exists and is visible
                if await load_more_button.count() > 0 and await load_more_button.is_visible():
                    print(f"Clicking 'Load more' (attempt {load_more_count + 1})...")
                    await load_more_button.click()
                    # Wait for new content to load
                    await asyncio.sleep(2)
                    load_more_count += 1
                else:
                    print("No more 'Load more' button found. All reviews loaded.")
                    break
            except Exception as e:
                print(f"Error clicking load more: {e}")
                break
        
        # Extract all reviews
        print("Extracting review data...")
        review_cards = await page.locator('[data-testid="review-card"]').all()
        
        print(f"Found {len(review_cards)} reviews")
        
        for idx, card in enumerate(review_cards):
            try:
                review_data = {}
                
                # Extract rating
                rating_elem = card.locator('[data-testid="review-rating"]')
                if await rating_elem.count() > 0:
                    rating_text = await rating_elem.text_content()
                    review_data['rating'] = int(rating_text.strip()) if rating_text else 10
                else:
                    review_data['rating'] = 10
                
                # Extract title/service
                title_elem = card.locator('h3')
                if await title_elem.count() > 0:
                    review_data['service'] = await title_elem.text_content()
                else:
                    review_data['service'] = "General Service"
                
                # Extract date
                date_elem = card.locator('text=/Posted.*ago|Posted.*[0-9]{1,2} (January|February|March|April|May|June|July|August|September|October|November|December)/')
                if await date_elem.count() > 0:
                    review_data['date'] = await date_elem.text_content()
                else:
                    review_data['date'] = "Unknown"
                
                # Extract review text
                review_text_elem = card.locator('p').nth(0)
                if await review_text_elem.count() > 0:
                    review_data['text'] = await review_text_elem.text_content()
                else:
                    review_data['text'] = ""
                
                # Extract customer name
                name_elem = card.locator('[data-testid="reviewer-name"]')
                if await name_elem.count() > 0:
                    review_data['customer_name'] = await name_elem.text_content()
                else:
                    # Try alternate selector
                    name_alt = card.locator('text=/^[A-Z][a-z]+ [A-Z]/')
                    if await name_alt.count() > 0:
                        review_data['customer_name'] = await name_alt.text_content()
                    else:
                        review_data['customer_name'] = "Anonymous"
                
                # Extract postcode/location
                location_elem = card.locator('text=/Job location: [A-Z]{1,2}[0-9]{1,2}/')
                if await location_elem.count() > 0:
                    location_text = await location_elem.text_content()
                    # Extract just the postcode
                    postcode = location_text.replace("Job location: ", "").strip()
                    review_data['postcode'] = postcode
                else:
                    review_data['postcode'] = "SW11"  # Default to Balham area
                
                # Extract images
                images = []
                img_elements = await card.locator('img[src*="storage.googleapis.com"]').all()
                for img in img_elements:
                    img_src = await img.get_attribute('src')
                    if img_src and 'thumb' in img_src:
                        # Convert thumbnail to full size
                        full_img = img_src.replace('.thumb.', '.')
                        images.append(full_img)
                
                review_data['images'] = images
                
                # Add to list
                reviews.append(review_data)
                print(f"Extracted review {idx + 1}: {review_data['service'][:50]}...")
                
            except Exception as e:
                print(f"Error extracting review {idx + 1}: {e}")
                continue
        
        await browser.close()
    
    return reviews

async def main():
    print("Starting Checkatrade scraping...")
    reviews = await scrape_checkatrade_reviews()
    
    # Save to JSON file
    output_file = "/app/backend/checkatrade_reviews.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(reviews, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Successfully scraped {len(reviews)} reviews")
    print(f"📁 Saved to: {output_file}")
    
    # Print summary
    print("\n📊 Review Summary:")
    print(f"Total reviews: {len(reviews)}")
    print(f"Reviews with images: {sum(1 for r in reviews if r.get('images'))}")
    postcodes = set(r['postcode'] for r in reviews)
    print(f"Unique postcodes: {len(postcodes)}")
    print(f"Postcodes: {', '.join(sorted(postcodes))}")

if __name__ == "__main__":
    asyncio.run(main())
