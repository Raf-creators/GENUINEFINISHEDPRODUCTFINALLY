"""
Parse reviews from the markdown content we scraped
"""
import json
import re

# The markdown content from crawl_tool
markdown_reviews = """
- 10

### Back yard transformed!



Posted 4 days ago




Spectacular workmanship and customer service. A great bunch of helpful friendly characters. My Garden is fully patiod now, and they have carried out useful clean up work in the area for our neighbours too. I look forward to looking outside to my back yard now.



![review attachment](https://storage.googleapis.com/core-media-service-production/user-media/01K7RXWKWR7Y9YPFG5G617TF1G.1000073101.thumb.heic?GoogleAccessId=app-core-media-service%40capi-production-21756.iam.gserviceaccount.com&Expires=1766257348&Signature=XVhNTevurp%2BMCnMlGAzt9PHQ6vuWTA8i4Bwk5JldXFIxyOKL6PDpgtzopELnj3eqKaHiip5NW1cWg02%2F9GutpgA9w9YW5TXUC4d7jUWk%2FZrWJa%2FckuiLvekfgaTyr34bzhmi2bUMPldT0OXOYlyzBiMLmIBnoO6AqvmYa5RfU7Tx7wi4Gb4KuL4eabXSDKYwJF4qA8wi000dRvpL46wzkd74PyovlHOqc0Gt0s4LBsSpZPetnow34%2FR14bORr2peuuSQP3AbGp4kfSohlrzlAPGr8Tz1Ncii6ls6pzFUZdQUVqBGLSMG2cwqOjcWO2skLkmCJsjFo77sPylpyqoGJw%3D%3D)![review attachment](https://storage.googleapis.com/core-media-service-production/user-media/01K7RXWM3TVY54Z3V6QWK0YM04.1000073100.thumb.heic?GoogleAccessId=app-core-media-service%40capi-production-21756.iam.gserviceaccount.com&Expires=1766257348&Signature=YkyEKz%2BFKuL0GV6cm4%2Bf3Em8sFG2hF15n%2FgSWg5gEFSIUF9zu48X4kiqgF7w1OvBFh06%2Fj%2FgcSozXtoKQKlqrx%2BaD2s3c%2Fi%2BNYt91OzKY8oDRy%2FZq%2Fm6tCpnIYXuj0U2EO4Yyf%2BSzT9BQ2j1NcJO4si2vxsglzrbvjH4ZGpGqw4VKJoAE9Cxt6g3z05Z2b%2FuLN9dzBUl1fblO4dtbd7YRXeGmwxLCdBuHr2SNgQ0tjWRZ0L9WdlGTbyhPlCup55z4z4X1kNpV%2BDB7ILDqNayQYSrrMv88bql1jbvBVrqw5%2BYEo2OuLydBrCt%2B5i9VcyVfEKkglbVbTNFO6m8Iia8Ww%3D%3D)![review attachment](https://storage.googleapis.com/core-media-service-production/user-media/01K7RXWM9Y7HK6AMRD0TK3WMEJ.1000073010.thumb.jpg?GoogleAccessId=app-core-media-service%40capi-production-21756.iam.gserviceaccount.com&Expires=1766257348&Signature=YkDdomq07Sdqp%2Bv4A8X7fj2FKwoSEJ%2FE1TfyBngxUcqHhc4pFuFZgLVidTmW4h9YtLTaz5Sp9t8gzHNsqtdiTEz4ewYSlWSOseZZnJNBN8zN2j15bH7LDxp2FG54NKEJQFKQ7USRTN8InowAPl6X7dtrvm1wy9UrjEeeoP2Dc5nwIFbcGQUb0nritcGku6EqE6aCYpBuuIOIJlbLih39RRSPV2yKOFX2yzMBl2duU%2FFGTKudAu7CB9ag7jFPVx7GHPOSssU2E%2FgNeOX67Iaw%2FjLGnoelp%2BEo0JNUIpj1itBgobFLzoWN4B1%2F0Q5wXPUt%2BwM4min2s%2BhBIVKfu7y5aQ%3D%3D)

Verified reviewer
Job location: CR4
- [P\\
Peter B](https://www.checkatrade.com/profile/068c8134-9051-73af-9720-a6d5167f61c2) 8.67

### New garden fence , garden maintenance, planting winter bulbs



Posted 6 days ago




The guys were so willingly to please and to ensure our wishes were met. We are most pleased and would recommend.



Verified reviewer
Job location: SW18
- 10

### Excellent work!



Posted 11 October




The guys were excellent! They worked hard and did a great job of the hedge. Tidied up properly and checked I was happy with the work. Will definitely use again, highly recommend. 5 \*



![review attachment](https://storage.googleapis.com/core-media-service-production/user-media/01K7AGCCC2XMNWEKZ1738KPWHH.IMG_1941.thumb.jpeg?GoogleAccessId=app-core-media-service%40capi-production-21756.iam.gserviceaccount.com&Expires=1766257348&Signature=PMaSbLA5D9VrGH957Mieu4rIFa0%2B3ogh5mog1HWgB16nuDSbeweoJP1oQe1kaUb0bc66qCor5KHk%2BjvdFLauxLLzce3L2fJ0FEGz32H%2F3rBwj%2FBT8DMk4vlmGCUT2f6m1mjtfesDDf5AS%2BCR1oTv6qjHJl6jdRGpvvJFiNeEtlLQmxmkI1xEd9iDbESvuovQZ%2FTWBTRx%2Ff6YaMMQYLJIkF3CZuR6B9G835wEtpyE%2BPnar7Ur3EDnkSkfdDUJN7vWX3fP07lmkBVGMoG2J7aua3mulfThsB2xXPlZinrZ%2FTW%2FcKUasM5iuXMIF%2Ffjh2TDioCJBV6M6GF%2BnNg8JH4eyQ%3D%3D)![review attachment](https://storage.googleapis.com/core-media-service-production/user-media/01K7AGCCTEFXEF3ZEY4XAXVA34.IMG_1940.thumb.jpeg?GoogleAccessId=app-core-media-service%40capi-production-21756.iam.gserviceaccount.com&Expires=1766257348&Signature=oUvZLUiDU0PS4t7Xp1MkHitlTmoz4QkO12riPLE1H7nlLDg3h778IpGoS4BVfslaKaOB29ynlks25KXAWK%2B1oIAHdNOXGci6lxmeQLPXRibQh%2BqWFo13fgEM81Heff5LGR7KOZNxiJrmYOpsKpVDjXuo3NhDEUd3btk78GT0UBnEkvIF4AnjaeMi%2Bhm7h61pRqKTHa2kxtzkHr0HZ1w66CdSk9B2%2Fih2q87%2F8R50nJMHrSTbyBxTmfMn3IgfCoFEaXnYFhBdErRpkdPlXPUxvWsrQmOuxI9MSjwdlh84PCJSL%2BzfRDAGgkgfQiwEUK35j0qvlNkoBQomdS5GQBgLNA%3D%3D)![review attachment](https://storage.googleapis.com/core-media-service-production/user-media/01K7AGCD17M56J82WEDMMWDBN4.IMG_1938.thumb.jpeg?GoogleAccessId=app-core-media-service%40capi-production-21756.iam.gserviceaccount.com&Expires=1766257348&Signature=Z9zTkBSM78DCA%2BDtTCJOa71JHKGzeHAS6%2BzMLrSvEPXu3KdKqxDHZldYuOAtSCOaURJeMmaCFRin7nRX4OLaC3LxXcTsUsg6HZQLHK3T%2F9f3dVtU6GhrC6goul8YLrlrr5h9q5Sf%2FVN%2F9h%2BkdHjocm8nwDk8BP0L1LObEmHsY10stmAc68gYfmi4tE%2B9PeuF9igO0EbJqirhcjY2eUhkZjrZ6PThfinhcWow9tNtW%2Bndt75oivYkjJsvMZfzWUGq0mtEKspYlKYRAAQopJyjUsvDUzSLJxywKCBB3Qyj90%2BT9vNu9sx7efq6dxhaCba5mVYp%2F%2FapSH1tueH%2FhJbVHw%3D%3D)![review attachment](https://storage.googleapis.com/core-media-service-production/user-media/01K7AGCD7J00P1Q35DFMXHFWJF.IMG_2033.thumb.jpeg?GoogleAccessId=app-core-media-service%40capi-production-21756.iam.gserviceaccount.com&Expires=1766257348&Signature=PO%2BhU3Kzdi35VgnaMvzAJXtXs94lO9RLrPNwMv68vI%2BKXPd4Eh5l20TtWSP3Lm7Ra%2F0%2BjMXnhHBV9KxWnyouahejtc6Ev6oNgOwKbrsQHY58dFDSeEt41RpyGS5g4nZKD3jals%2FFwV0BXATKmQfJu0RMhD38GnB5k5VegHtyxIskwI4uQ%2FWyB7zJslpDNUUwkGQ%2FImKXf7DcpENaz1lySXACdafRsqLLRU2L174sKz9HtLq2HtAiH%2Fg7rDasO3vCbi%2BsYvWn9P0CfF50HD2M2xQNoJjZ24vBKMYifQvo8In5M4rCJSvjs5stD1gaygOr%2B5FNlMKAirhNzR3twNCbDQ%3D%3D)![review attachment](https://storage.googleapis.com/core-media-service-production/user-media/01K7AGCDDGH8T1JNWVABXCBHPD.IMG_2030.thumb.jpeg?GoogleAccessId=app-core-media-service%40capi-production-21756.iam.gserviceaccount.com&Expires=1766257348&Signature=fiDPHekiIalHMrMn%2BD6AvGGDoSmSrOCE4hBblTA0MezfBb4yARDOsS%2FKELGJMZqoeMVTUG1xU772TKx2tA8tx8ISpxbko%2B1FPrXay4lzW04X5mnn64piT%2FMvqZKD9EatzWl%2FhFmtBmW5m7%2FbZkNd1p%2FeO2XyEZWdHq%2FRZe1fHCzIOGYB3NU2zAIJbFo1AYQ54OCkjAnPbEUx3%2FZb33ii3mEMvbBFc65FY73tj2XRD1LaV%2BViJL4PaoVMUGeyARAdujavlBYa0%2Bt90xQn4YdPkz9yvzNpwRupNSLs31FWWr9vN1XEcuWuW36py01S%2BU0Z%2FKddFmtpQFpvklqrz7sKbQ%3D%3D)

Verified reviewer
Job location: SW2
- 10

### Mews path & garden cutting back & removing overgrown bushes



Posted 22 September




Great communication from the start & throughout from Paolo.
Marco & Gonzalo worked tirelessly cutting back & removing bushes that had gone wild up to the top of the house over many years. Swept and cleared all leaves. They then proceeded to cut back trees in the garden and all bushes. Again removed all leaves. Leaving everything looking spotless. My neighbour even asked if they could assist her with cutting back while they were there which they happily did.
A really wonderful service. Would highly recommend without hesitation. I'll definitely be using again.... and again! Thank you



![review attachment](https://storage.googleapis.com/core-media-service-production/user-media/01K5S21T0KB53EV2KGAVRN0G6R.IMG_9066.thumb.jpg?GoogleAccessId=app-core-media-service%40capi-production-21756.iam.gserviceaccount.com&Expires=1766257348&Signature=YjCp3TpcQ12jh3AI3baGsP3DcgdMGWXnYN9WnetC0ydZFafgl%2BBmGq7h97GI4DpPv4opMt7zOmJw1yxykY6anQByqfA5WN7iflNl7hnS%2FnMcyFEzeksanMKXupPKKUKlNkmBy7aSbPUeu9lWcA%2FXzEU2rXHvyLyf7PyuWNdDtG7jvLlDoCFvjxm8%2FgvVxkknv7KW6kNnTVCyB4OBzEcO6myQnUf903AUObH0UsZ41%2B9xCxzszB%2Bq4tQTfLALTLtLag5B3dL9oLUNAvgbjiLmO32nN3g1C1cOpa01x6BcVuuEAMi1dV5puO56jA7AN7UkLEZ7yVFzcaHKQMll3yGOtA%3D%3D)![review attachment](https://storage.googleapis.com/core-media-service-production/user-media/01K5S21TF7X1BFJEWYRYXS52G4.IMG_9065.thumb.jpg?GoogleAccessId=app-core-media-service%40capi-production-21756.iam.gserviceaccount.com&Expires=1766257348&Signature=DFDF7H6c1qjKJCaRzCopvlNUZAZwXIVkOGYgCRL3koimIdmptQQ0igPtlMV5usKr20Nn9R4T88e%2BuIWsoVgmjYRoRWCTnRo7jQe0gcdl8US0%2BupzExMp6MtDKKUsJtwTid0LKjVhvKmvVCdH4kyI65f%2BkojRdadjB06MZ7vl4IiPniawCjac6v3kaoSXZqgBsXrKh0DfBjuT5w9MLwjXtDV1sIsiV%2Bjgakz5Di9qP2%2FAEqmVmfASFHPIlJ4THzNmXQdr6l9j7A4%2B9iL231kaynwdWWxQVG%2FOvwexlPftuJ%2BrBoek22bwOqw7zFhnUPugRxGSL%2BWRZ5sHeiCXIMKrWQ%3D%3D)![review attachment](https://storage.googleapis.com/core-media-service-production/user-media/01K5S21TNBGHEZM1APSC17V0C4.IMG_9063.thumb.HEIC?GoogleAccessId=app-core-media-service%40capi-production-21756.iam.gserviceaccount.com&Expires=1766257348&Signature=i4tfszDRUhs28hTh35%2FK%2BXAcDs7f8b4a%2F%2FH2JjHDZpzZParc28l1w4OQEJzVpyF4Ma%2FlT%2B0ixm2ENGc8tXe%2BdTrEk4xsCIIM1TIsq3OHk7gXIbDwuXc%2BZe2SrnCY4%2B%2FZHhDAGjYkxVHa3tC9EqYaX%2FcNg0Sqqcc25uzrlacPFxCsROBWHkGTfjxb9m0%2FLDXALPydWO%2FRDMpwExxaSqsHebqKiA1Gm6BYmH4mdCG2HYHQmqhjxcK1IckTncA3o92nPvUxoMflOOKA9ElYylOaR9FUv71glErRX4gkamMxc0LyTZeyIPOiU%2BnTt9da6iZm9skkAcRm7pFoL7wJZjOhfw%3D%3D)![review attachment](https://storage.googleapis.com/core-media-service-production/user-media/01K5S21TXDX85ZFBFGVKE7CZW7.IMG_9057.thumb.HEIC?GoogleAccessId=app-core-media-service%40capi-production-21756.iam.gserviceaccount.com&Expires=1766257348&Signature=L%2B7ud8yO9GyF6OY46QeiMcmBy%2FD67DO67rbCwjExIJV3UQRz8HTGWPur5xyaPmHbU57wBiMfhVgxcx7CPEMiTJFolxe0JixEZxHYQ6FOfeDhj1Uwqd7SBC4lXmAoSZ128Mqc0h56dLHuDypdbhTkqIS8Kzuxw1JaLRjEe%2B4odb%2B6Ylcx9p4Y%2BuJFdaqJ%2BM6f9U5AMq0%2BUT%2Fv2hkvMxDlwOoYdTEioKKQmKtsH5kQ3TEoTcMa6sOOW3xWaRv0MzJRwWKLp8ZlzYMOC7P8Maro%2Fjlq7XS2MmmwCvm%2FDLaYWog57Q3HA5xAJ8AshRwZtU%2BUGrYhfjYuWIQwisIX6%2B2fKQ%3D%3D)

Verified reviewer
Job location: SW4
- 10

### Total garden clearance (wedding & trimming)



Posted 20 September




Amazing work from the guys, beforehand the team were super communicative and clear with me which was great. The entire team on the day (4x people) were all friendly and diligent and did a brilliant (and very quick) job of clearing the garden and removing all the debris. Exactly what I was hoping for - would highly recommend.



![review attachment](https://storage.googleapis.com/core-media-service-production/user-media/01K5KG1A0F98BWH9TVMAHET0PA.IMG_1772%202.thumb.HEIC?GoogleAccessId=app-core-media-service%40capi-production-21756.iam.gserviceaccount.com&Expires=1766257348&Signature=BVzJ4OAN%2BHj3eI3kT8ZDtiUVcfhEo52280UdelDomekrUc%2FFOrIVoOHjE0FViF%2FHpNUr41lzkPv1TYWqjg46IUUVlItUbAQS%2Fzkx322IqwM5%2FLB%2BT7CxMAYiEjoyjDJ89cIxldGC271xxpMGy4KXBG2qwpHv5kDiE%2BMTWdatMOZBfMCkSVvPoeTmbd8MIcBR6LcJrQ2kUYAzuz83SC0QmlLTPLlQKLEs%2BjyVK2gGrmJfj3DmL91yASif8xLQAyib46fBXV8JAUsA0Ur%2B%2BSwN2xsQ8oLG4ar%2FS7KdcfT0geGRQCS8VoADA8Q2W6gEbsV0ltg9XPSL4Ffc1E8fZCrLYQ%3D%3D)![review attachment](https://storage.googleapis.com/core-media-service-production/user-media/01K5KG1AAPS849Q330X3N2XM8N.IMG_2123.thumb.HEIC?GoogleAccessId=app-core-media-service%40capi-production-21756.iam.gserviceaccount.com&Expires=1766257348&Signature=XyVEU4Dr54qyW1UG3CrysjqLy7OmRsPnBJ3xslxS6KJ%2FJ27vrK0AWy9W%2Bny9tMWnGfUTbc0nOcoHXdGFU%2BgcfvNLtl6xEEPaUteN0z1eYkCRVFtR%2BOkyrLdZqRuhaSd%2BupT2vCeTBMVaabbhVlTbrSlRwQqBbhWTpsAAxidIf%2BDAoUv2juJsH%2FBPfEU%2BWr2EGI5UT7%2BcI3Mm%2BdCg2rwo0N82puOMwdo7TeEpn7E1E7rSOA%2FYLTX5JG8BehZJ4Wibb8FjQWfdTguk%2FOBGiw0TD%2FwlOYgprBF3uZmWfsnVTqOaMO3PGzs0Qe%2B55OahZ9eeGcDlPLX1KziOUCcpicL%2ByQ%3D%3D)

Verified reviewer
Job location: SW4
- [J\\
James W](https://www.checkatrade.com/profile/0679f568-4a72-786d-a620-9928ad81a35d) 10

### Hedge/tree trimming



Posted 13 September




The PNM Gardening team did a wonderful job trimming some overgrown hedges/trees in my garden. Communication was clear and prompt, with scope and price agreed in advance. They turned up on time, were extremely friendly and polite, and executed with efficiency and precision. They took the waste away with them and left the garden looking neat and tidy. Many thanks, guys - appreciate you doing such a great job!



![review attachment](https://storage.googleapis.com/core-media-service-production/user-media/01K51H7KH40944PZ4944C4JT6N.011D20EA-B5AB-4A1B-A585-17AE7AB2F3F7.thumb.jpeg?GoogleAccessId=app-core-media-service%40capi-production-21756.iam.gserviceaccount.com&Expires=1766257348&Signature=AVitGgrfbY6WlmINmEay7yBhxxex%2FvNjGIveCe%2FUFyJN0cA2%2B0r6JIVJZcaxyCSMWVD4XjVEgV%2FLnsBgdMn6q193MGRuGTjdr7U4yCNXKPHWf8JSwYd0SW%2BC3J5A9D4HI%2Fc2IP17w9U54KL0%2F4ngLVniR4CmjXntC7zxEo%2Fs78gnXZOBvZ173HQXibVNRIBUuFt60Z1bm5fzYpjssfrxBw9l1e8l0d%2B%2Fj88abuEB185IZxsDQdqqDs3GnOsBIGoN9EDrYFD4Of4qHovhS%2B8nuU%2FgNvHb%2BJHF3o8R45TMje2NlKhrghrdRrBRvIbnhVGt96HUSv0T0T5XoB76HX%2BWrQ%3D%3D)

Verified reviewer
Job location: SW19

Load more reviews
"""

def extract_image_urls(text):
    """Extract all image URLs from markdown image links"""
    pattern = r'!\[.*?\]\((https://storage\.googleapis\.com/[^)]+)\)'
    urls = re.findall(pattern, text)
    # Remove .thumb. from URLs to get full-size images
    return [url.replace('.thumb.', '.') for url in urls]

def parse_reviews(markdown_text):
    """Parse markdown text into structured review data"""
    reviews = []
    
    # Split by rating indicators (lines starting with "- 10" or "- [number]")
    parts = re.split(r'\n- (?:\d+\.?\d*|\[)', markdown_text)
    
    for part in parts[1:]:  # Skip first empty part
        try:
            lines = part.strip().split('\n')
            if not lines:
                continue
            
            # Extract rating from first line  
            rating_match = re.match(r'^(\d+\.?\d*)', lines[0])
            rating = float(rating_match.group(1)) if rating_match else 10
            
            # Find service title (### header)
            service = "Garden Service"
            for line in lines:
                if line.startswith('###'):
                    service = line.replace('###', '').strip()
                    break
            
            # Find date
            date = "Unknown"
            for line in lines:
                if 'Posted' in line:
                    date = line.strip()
                    break
            
            # Find review text (paragraph after date)
            review_text = ""
            date_found = False
            for line in lines:
                if date_found and line.strip() and not line.startswith('!') and not line.startswith('Verified') and not line.startswith('Job location'):
                    review_text += line.strip() + " "
                if 'Posted' in line:
                    date_found = True
            
            # Find postcode
            postcode = "SW11"  # Default Balham
            for line in lines:
                postcode_match = re.search(r'Job location: ([A-Z]{1,2}\d{1,2})', line)
                if postcode_match:
                    postcode = postcode_match.group(1)
                    break
            
            # Find customer name
            customer_name = "Anonymous"
            name_match = re.search(r'\[([A-Z][a-z]+\s+[A-Z])\]', part)
            if name_match:
                customer_name = name_match.group(1)
            
            # Extract images
            images = extract_image_urls(part)
            
            review = {
                'rating': int(rating),
                'service': service,
                'date': date,
                'text': review_text.strip(),
                'postcode': postcode,
                'customer_name': customer_name,
                'images': images
            }
            
            reviews.append(review)
            
        except Exception as e:
            print(f"Error parsing review: {e}")
            continue
    
    return reviews

if __name__ == "__main__":
    reviews = parse_reviews(markdown_reviews)
    
    # Save to JSON
    output_file = "/app/backend/checkatrade_reviews.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(reviews, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Successfully parsed {len(reviews)} reviews")
    print(f"📁 Saved to: {output_file}")
    
    # Print summary
    for i, review in enumerate(reviews, 1):
        print(f"\n{i}. {review['service'][:50]}")
        print(f"   Rating: {review['rating']}/10")
        print(f"   Location: {review['postcode']}")
        print(f"   Images: {len(review['images'])}")
        print(f"   Date: {review['date']}")
