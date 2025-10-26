"""
Add all 52 real Checkatrade reviews to the database with proper geocoding
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path
import uuid

# London postcode to coordinates mapping (approximate centers)
POSTCODE_COORDS = {
    'SW19': (51.4214, -0.1878),  # Wimbledon
    'SE5': (51.4794, -0.0885),   # Camberwell
    'SW2': (51.4500, -0.1167),   # Brixton
    'SW12': (51.4648, -0.1731),  # Balham
    'SW4': (51.4627, -0.1460),   # Clapham
    'SW16': (51.4325, -0.1221),  # Streatham
    'SM4': (51.3805, -0.1995),   # Morden
    'SE5': (51.4794, -0.0885),   # Camberwell
    'SW10': (51.4892, -0.1934),  # West Brompton
    'SW9': (51.4659, -0.1155),   # Stockwell
    'CR7': (51.3920, -0.0865),   # Thornton Heath
    'SW6': (51.4815, -0.1945),   # Fulham
    'SW11': (51.4647, -0.1634),  # Battersea
    'SE26': (51.4209, -0.0438),  # Sydenham
    'SE17': (51.4896, -0.0954),  # Walworth
    'SE19': (51.4184, -0.0819),  # Crystal Palace
    'SW17': (51.4322, -0.1517),  # Tooting
    'SW18': (51.4584, -0.1947),  # Wandsworth
    'N1': (51.5389, -0.1033),    # Islington
    'NW8': (51.5288, -0.1719),   # St John's Wood
    'SE22': (51.4503, -0.0689),  # East Dulwich
    'CR4': (51.3827, -0.1137),   # Mitcham
    'SE11': (51.4929, -0.1162),  # Kennington
    'SE21': (51.4430, -0.0838),  # Dulwich
    'W12': (51.5072, -0.2366),   # Shepherd's Bush
    'NW1': (51.5290, -0.1255),   # Camden
    'W9': (51.5234, -0.1896),    # Maida Vale
    'NW6': (51.5420, -0.1947),   # West Hampstead
    'SE6': (51.4341, -0.0145),   # Catford
    'SW15': (51.4574, -0.2214),  # Putney
}

async def add_all_reviews():
    ROOT_DIR = Path('/app/backend')
    load_dotenv(ROOT_DIR / '.env')
    
    mongo_url = os.environ['MONGO_URL']
    client = AsyncIOMotorClient(mongo_url)
    db = client[os.environ['DB_NAME']]
    
    reviews_data = [
        (10, "Weeding and garden clearance", "Tidied shrubs and cleared weeds. Left garden looking much better and easier to maintain. Good communicators and quick to respond. Happy to recommend.", "SW19"),
        (10, "Great work and highly recommended.", "Really good work. Very helpful, did exactly what we asked and great communication throughout. Very efficient and would use them again.", "SE5"),
        (10, "Garden cutting back", "PNM guys were working the first time when I was unable to be there. They did a great job cutting back in the garden but misunderstood that I also wanted the climbers cut back. So they returned when I was able to be there and I saw for myself how totally professional they were. They cleared gutters and untwined climbers from trellis. They cleared all the debris and even leaf blowed the lawn so that the garden looked immaculate by the time they had finished. They were polite, willing and grateful for a well deserved cuppa. I would highly recommend these friendly,efficient and willing guys.", "SW2"),
        (10, "Weeding, lawn overhaul, new turf and planting", "Marco and his team were amazing. Such a nice guy and his work was fabulous. Brilliant at communication and worked very hard and so quickly. Thank you so much Marco - we are so so happy with the result.", "SW12"),
        (10, "Great and efficient garden clearance", "Paolo and his team were fantastic. Quick to give a quote and completed the clearance of our garden quickly and professionally. Would definitely use them again and recommend them to a friend", "SW4"),
        (10, "Garden clearance and tidy", "The guys came in and did an amazing job getting my garden back into shape. I had ivy and overgrown weeds everywhere, and the PNM guys took the time and care clear it all up so I can make a fresh start on everything. It's also nice that they're just generally pleasant and nice people. The extra nice thing that I really appreciated was that during the process they made sure to keep my house as clean as possible and even took the care to vacuum up afterwards. That was unexpected but a small gesture that really made a difference.", "SW16"),
        (9.67, "Garden clearance", "Was quoted £650 to clear my garden of weeds and brambles, trim the hedges and cut the grass. They turned up on time and cleared it all out in around 3 or 4 hours, also handled the disposal of green waste. No complaints here, stellar job!", "SM4"),
        (10, "Complete garden clearance and removal of waste, laying of lawn, jet washing patio", "Great communication from start to finish. Computerised drawing was provided so we could visualise the end result. The team arrived when they said they would, worked fast and efficiently. Delighted with the end result.", "SW19"),
        (10, "Highly recommended", "Really great experience, the guys were friendly, helpful, informed and efficient. Cleared a really heavily congested garden with no issue and were very dilligent about it. Absolutely would recommend and go with again.", "SW16"),
        (10, "Dispose of thorny bush", "booked on day of posting and completed within 2 hours of booking", "SW16"),
        (9, "Small garden clearance", "PNM gardening were quick to quote from a photo and easy to communicate with. The two gardeners did a great job and cleared an overgrown garden really quickly and left no mess. Would recommend", "SW12"),
        (10, "Ivy Removal", "Very good job, good communication and would use again.", "SW10"),
        (9.33, "Good hedge trimming", "Paolo and his team arrived promptly and worked hard to sort out our and our neighbour's front hedges. They were friendly and courteous and cleaned up well afterwards. The only negative was that their ladders were not quite tall enough to really trim the tops to perfection.", "SW4"),
        (9.33, "Great gardening", "Professional- reliable. Good Job", "SW9"),
        (7.67, "Garden waste clearance", "They cleared garden waste fairly quickly.", "CR7"),
        (10, "Excellent reliable service", "Asked for a clean-up of the garden, some planting and a branch removed, really super helpful, quick and clear communication", "SW6"),
        (10, "Garden makeover", "The initial contact was to introduce ourselves, to discuss the work I needed doing, and arrange a visit to see my garden. When the work commenced I was pleased they arrived at the time agreed. They really worked hard and I found them very friendly, updating me on the work done - and what was left to do. On the whole after 3 days I was very happy with results - I've arranged another job with them and would recommend them for any gardening jobs.", "SW2"),
        (10, "Small garden clean up", "PNM were responsive, showed up on time, worked fast, were reasonably priced, and nice guys. They did a great job with the garden and I would highly recommend them. I will be hiring them again the next time I need garden work done.", "SW9"),
        (10, "Trimming holly tree", "Rapid to attend and great communication", "SW6"),
        (10, "Bamboo clearance", "The PNM team did an excellent job clearing a huge patch (three stories high) of bamboo that we inherited when we bought our house. The team worked incredibly efficiently (it took them just over a day, when we expected it would take almost a week!), reliable and easy to communicate with. Their waste clearance service was also invaluable living in London! We 100% recommend and will be using PNM again! Our dog was also a huge fan :) Thank you!", "SW11"),
        (9.67, "Garden Clearance", "Turned up on time, cleared garden very professionally, good communication.", "SE26"),
        (10, "To clear a massively overgrown garden", "PNM did a fantastic job clearing my uncle's overgrown back garden. Very reliable and polite. Did an excellent and thorough job", "SW6"),
        (10, "Gardening", "I required some garden maintenance and via Checkatrade, PNM GARDENING sent me a message. I informed them of the garden maintenance required and sent some photographs. I asked if they could attend the following day which they did. Two gardeners attended and did a great job in the garden. I was very pleased with how my garden looked after the work carried out. I would recommend PNM GARDENING as they provided an excellent service and communication.", "SW11"),
        (10, "My parent's extremely overgrown garden was cut and tidied.", "I'm always nervous about using a new service - even when reviews are good but I happy to say that PNM Gardening exceeded my expectations. They were easy to liaise with in the booking process and arrived punctually at the agreed time. The work wws done efficiently and to an extremely high standard, I will definitely be using them regularly. Highly recommend.", "SW4"),
        (10, "Garden clearance", "Nice fellas, on time job done tidy and efficient", "SE17"),
        (9, "Front and back gardening", "We had 2 gardens in a very bad shape. PNM helped us quickly,. communication was excellent, I can definitely recommend this company for all your gardening needs.", "SE19"),
        (9.67, "Planting front garden, mow lawns, trim hedges, clearing weeds, general tidy", "Super team - friendly, keen to please, needed minimal direction. Very helpful.", "SW19"),
        (9, "Garden Clearance", "The men arrived arrived on time, they even messaged me to give me an approx time of arrival. They were very professional, we did the introductions, the work started as soon as they arrived. Once the garden was cleared (it was pretty quick considering it was wild + it was raining), I was very impressed by the results, the garden is now ready for the next stage. Thank you PNM Builders Ltd for a job well done👏🏾👏🏾", "SW2"),
        (10, "Faultless - would highly recommend", "Lads did an amazing job. Best gardener work we've had completed. Professional, high quality work. Thank you", "SW17"),
        (10, "Took out my heavily weeded lawn-rotavated the top soil-some levelling-cleared & removed it all", "Quick, efficient and highly effective. Would recommend", "SW16"),
        (10, "New turf for our garden", "We are very happy with a quality of work provided by Marco, Paolo and their team - we needed to lay a new turf in our garden. From start to finish, the team was professional, knowledgeable, caring and attentive to our needs.The installation process was seamless, and the team worked efficiently while maintaining a clean worksite and answering all my questions about the installation process. The quality of the turf is great—vibrant and lush! Highly recommend and will be using them again", "SW18"),
        (10, "Weeding and pruning the garden", "We were very happy with the work carried out in our garden, Everywhere was left clean and tidy. The guys working were very friendly and helpful. I would definitely use the company again.", "SE5"),
        (10, "Garden clearance", "Friendly and efficient Quote was very competitive Would definitely use again", "SW19"),
        (10, "Two hedges were trimmed, a large plum tree cut back and general garden maintenance", "The gardeners were friendly, efficient and skilled.", "SW12"),
        (10, "Garden fence and clearance", "Paolo and his team did an absolutely fantastic job. They were extremely polite, hardworking and helpful. They stayed for as long as was needed to get the job done. I'm really grateful to them! And it was also great value for money :) Many thanks to them all!", "N1"),
        (9, "Pruning and clearing a very overgrown garden", "Great at communication, extremely polite and respectful people. Marco and his team tidied up my Mum's long neglected garden. Great job, we were very pleased and I look forward to working with them again.", "NW8"),
        (10, "Garden tidy up", "Was looking for someone to do a general tidy up of a fairly overgrown garden. Very professional and friendly and good communication. Did exactly as asked and garden looks 10x better. Thanks very much!", "SE22"),
        (9.67, "Tidying garden, removing waste, planting and jet washing decking", "The team were excellent. Polite, professional, prompt and great quality. We're really happy with the work and will definitely be using them again.", "CR4"),
        (10, "Cutting back high bushes in the front garden, collect green waste", "Marco was punctual and completed the task efficiently, taking into account all my suggestions, great service", "SE11"),
        (10, "Garden and tree cutting, tidying and maintenance", "Paolo and Marco did a great job on our garden, from the start communication was very clear and prompt, they were punctual, and worked v quickly and efficiently, the garden was very overgrown and the left it looking vastly improved and tidy, cleared away all the cutting and leaves and advised on further maintenance. We would definitely hire them again and recommend them.", "NW8"),
        (10, "Garden redesign", "I can't thank Marco and Paolo for their advice and assistance with what to do in terms of redesigning a garden which was full of weeds and nettles. They responded to queries very quickly . I was given choices of stones and fencing . They are very honest and trustworthy. I explained what I would like and they gave me advice which I am grateful for. Nelson worked so hard he absolutely transformed my garden, it looks beautiful, people walking by always comment on how lovely it looks . I would 100% recommend them, without a doubt I would go back to them for any other work I need to be done .", "SE21"),
        (10, "Garden clearing", "Lovely guys, polite, warm and friendly. Did a fantastic job, they worked so hard. Great to support a lovely family business, I wish them well. 5 stars", "W12"),
        (9, "Hedge removal and new decking", "We moved into a house where the decking had rotted away and the hedge had not been maintained for decades. PNM came and cut the hedge down to size and put in new decking just in time doe the warmer weather. Paolo, Nelson and Marco were highly professional in all their engagement. Highly recommended!", "SE26"),
        (10, "raised flowerbeds installation", "A great family business. They seem genuinely interested in customer satisfaction which makes them a pleasure to deal with & their workmanship was excellent.", "SW15"),
        (10, "Hedge and shrub reducing", "PNM were great, communication was excellent, they worked so hard reducing a monster hedge, followed all the specifications to the letter, and all this at the same time as a van was being delivered into the garden! The clearing up process was also really good, would definitely recommend. Thanks again Marco/Paulo 🙏", "SE21"),
        (10, "Removing overgrown garden materials and waste", "From the start of this job the communication was excellent Highly reliable with great expertise, and knowledgeable staff Any requests were met with a very positive can do response. Job carried out efficiently and cleanly. Highly recommend.", "N1"),
        (9.67, "Clearing garden waste (4 cubic meters) from back garden", "PNM showed up on time. PNM were very friendly and polite and got the job done well and quickly.", "NW1"),
        (10, "Garden tidy up", "Paolo and the team were super communicative, punctual to the minute and got the work done really quickly while checking I was happy with everything. Excellent service, would absolutely recommend.", "W9"),
        (10, "Incredible garden work", "Incredible garden work.", "NW6"),
        (9.33, "Plant removal", "Did a great job.", "SE6"),
        (10, "Cleared out double garden front space and side area, along with garden stairs", "This company I used for the first time today. The job was completed to a high standard. They were polite, helpful, quick and efficient. I will be using them again and would not hesitate in recommending them.", "SW15"),
        (10, "Garden Cleanup", "They completely transformed my overgrown garden. They came on time and did a great job. Will be using them again for sure!", "SW19"),
    ]
    
    # Clear existing reviews
    delete_result = await db.reviews.delete_many({})
    print(f"Deleted {delete_result.deleted_count} existing reviews")
    
    # Add all reviews
    mongo_reviews = []
    for rating, service, text, postcode in reviews_data:
        lat, lng = POSTCODE_COORDS.get(postcode, (51.5074, -0.1278))  # Default to London center
        
        review_doc = {
            'id': str(uuid.uuid4()),
            'name': 'Verified Customer',
            'rating': rating,
            'date': 'Recent',
            'text': text,
            'service': service,
            'postcode': postcode,
            'lat': lat,
            'lng': lng,
            'images': [],
            'approved': True,
            'created_at': '2024-01-01T00:00:00'
        }
        
        mongo_reviews.append(review_doc)
    
    # Insert all reviews
    if mongo_reviews:
        result = await db.reviews.insert_many(mongo_reviews)
        print(f"✅ Inserted {len(result.inserted_ids)} real Checkatrade reviews")
    
    # Print summary
    print(f"\n📊 Review Import Summary:")
    print(f"Total reviews: {len(mongo_reviews)}")
    avg_rating = sum(r['rating'] for r in mongo_reviews) / len(mongo_reviews)
    print(f"Average rating: {avg_rating:.2f}/10 ({avg_rating/2:.2f}/5)")
    print(f"\nUnique postcodes: {len(set(r['postcode'] for r in mongo_reviews))}")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(add_all_reviews())
