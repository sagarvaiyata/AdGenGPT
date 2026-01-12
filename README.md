# AdGenGPT

## What is AdGenGPT?

AdGenGPT is an Advertise Generative AI Automation. The main usecase of this application is to generate Custom Advertisements for customers. Customers can be business owners who want to post advertisements on Various Platforms.

## How does it work?

-> Customer Fills a form

    --> Customer Name
    --> Customer Email
    --> Business Name
    --> Brand Logo
    --> Digital Identity (Primary Color, Accent Color, etc.)
    --> Brand Tone (Minimalist, Modern/Contemporary, Traditional/Classic, Bold and Graphic, Flat Design, Retro/Vintage, Typography-focused, Illustrative, Photographic/Lifestyle )
    --> Social Media Selection (Meta-Facebook/Instagram, GoogleAds, Blogs, Twitter/X)
    --> Custom Template (if any)
   --> Schedule (1 post per day, 3 posts per week, Custom Schedule)

-> Successful Entry will be made on AWS RDS MySQL Database and AWS Bucket.

-> Admin will check if the subscription is active.

-> For the active users, cron job will be made by llm for the schedule and saved on redis cache.

-> Cron Job will trigger llm and it will generate an advertisement prompt and caption with hastags according to the customer's needs.

-> Generated Prompts will be used to generate an image on gemini nano banana pro and openai image model 2.

-> Total of 4 images and captions will be sent to the user based on the schedule.

## Technologies used

--> FASTAPI
--> OpenAI and Google Gemini APIs
--> AWS Relational Database MySQL
--> AWS Storage Bucket
--> Redis Cache
