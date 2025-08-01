from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json
import random
import re
from datetime import datetime
import openai
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize OpenAI (you'll need to set your API key)
openai.api_key = os.getenv('OPENAI_API_KEY')

class SmallBusinessChatbot:
    def __init__(self):
        self.business_steps = {
            "restaurant": [
                "1. Conduct market research and identify your target audience",
                "2. Create a detailed business plan with financial projections",
                "3. Secure funding through loans, investors, or personal savings",
                "4. Choose and lease a suitable location with foot traffic",
                "5. Obtain necessary licenses (business license, food service permit, liquor license if needed)",
                "6. Design your menu and pricing strategy",
                "7. Purchase equipment and furniture",
                "8. Hire and train staff",
                "9. Develop marketing strategies and brand identity",
                "10. Plan your grand opening event"
            ],
            "retail": [
                "1. Research your market and competition thoroughly",
                "2. Define your unique selling proposition",
                "3. Create a comprehensive business plan",
                "4. Secure initial funding and working capital",
                "5. Find the right location or set up e-commerce platform",
                "6. Register your business and obtain necessary permits",
                "7. Set up supplier relationships and inventory management",
                "8. Design your store layout and customer experience",
                "9. Hire and train employees",
                "10. Launch marketing campaigns and build customer base"
            ],
            "service": [
                "1. Define your service offerings and target market",
                "2. Analyze competitors and pricing strategies",
                "3. Create a detailed business plan",
                "4. Set up business structure and legal requirements",
                "5. Obtain necessary certifications and licenses",
                "6. Set up your workspace (home office or commercial space)",
                "7. Develop service packages and pricing",
                "8. Create marketing materials and online presence",
                "9. Build a network and referral system",
                "10. Launch and continuously improve your services"
            ],
            "tech": [
                "1. Validate your idea through market research and MVP testing",
                "2. Create a detailed technical and business plan",
                "3. Secure funding (bootstrapping, angel investors, or VCs)",
                "4. Build your development team",
                "5. Develop your minimum viable product (MVP)",
                "6. Set up legal structure and intellectual property protection",
                "7. Test and iterate based on user feedback",
                "8. Plan your go-to-market strategy",
                "9. Scale your product and team",
                "10. Focus on customer acquisition and retention"
            ]
        }
        
        self.name_prefixes = [
            "Smart", "Quick", "Pro", "Elite", "Prime", "Fresh", "Bright", "Swift", 
            "Bold", "Zen", "Peak", "Pure", "Edge", "Spark", "Nova", "Ace"
        ]
        
        self.name_suffixes = [
            "Hub", "Lab", "Works", "Studio", "Co", "Plus", "Pro", "Express",
            "Central", "Point", "Zone", "Spot", "Base", "House", "Corner"
        ]
        
        self.funny_adjectives = [
            "Quirky", "Witty", "Snappy", "Peppy", "Zesty", "Bubbly", "Spunky",
            "Cheeky", "Jolly", "Funky", "Zippy", "Bouncy", "Perky", "Sassy"
        ]

    def generate_business_steps(self, business_type, business_idea):
        """Generate customized business steps based on the business idea"""
        business_category = self.categorize_business(business_idea.lower())
        base_steps = self.business_steps.get(business_category, self.business_steps["service"])
        
        # Customize steps based on specific business idea
        customized_steps = []
        for step in base_steps:
            if "restaurant" in business_idea.lower() and "menu" not in step:
                if "marketing" in step.lower():
                    customized_steps.append(step + " (focus on food photography and reviews)")
                else:
                    customized_steps.append(step)
            elif "online" in business_idea.lower() or "e-commerce" in business_idea.lower():
                if "location" in step.lower():
                    customized_steps.append(step.replace("location", "e-commerce platform and website"))
                else:
                    customized_steps.append(step)
            else:
                customized_steps.append(step)
        
        return customized_steps

    def categorize_business(self, business_idea):
        """Categorize business idea into predefined categories"""
        if any(word in business_idea for word in ["restaurant", "cafe", "food", "bakery", "bar"]):
            return "restaurant"
        elif any(word in business_idea for word in ["retail", "store", "shop", "boutique", "selling"]):
            return "retail"
        elif any(word in business_idea for word in ["app", "software", "tech", "website", "platform"]):
            return "tech"
        else:
            return "service"

    def generate_business_names(self, business_idea, count=5):
        """Generate creative and humorous business names"""
        names = []
        business_words = business_idea.replace(" ", "").title()
        
        # Extract key words from business idea
        key_words = [word.title() for word in business_idea.split() if len(word) > 3]
        
        for _ in range(count):
            if random.choice([True, False]):
                # Funny combination
                name = f"{random.choice(self.funny_adjectives)} {random.choice(key_words)} {random.choice(self.name_suffixes)}"
            else:
                # Professional combination
                name = f"{random.choice(self.name_prefixes)} {random.choice(key_words)} {random.choice(self.name_suffixes)}"
            
            names.append(name)
        
        # Add some creative combinations
        if key_words:
            names.append(f"The {key_words[0]} Collective")
            names.append(f"{key_words[0]}ify" if len(key_words[0]) > 4 else f"{key_words[0]} & Co")
        
        return list(set(names))  # Remove duplicates

    def generate_logo_prompt(self, business_name, business_idea):
        """Generate a detailed prompt for logo creation"""
        business_category = self.categorize_business(business_idea.lower())
        
        style_suggestions = {
            "restaurant": "warm colors, food-related icons, elegant typography",
            "retail": "modern, clean design, shopping-related elements",
            "tech": "sleek, minimalist, digital-friendly colors like blue or green",
            "service": "professional, trustworthy, clean lines"
        }
        
        style = style_suggestions.get(business_category, "professional and modern")
        
        return f"Create a professional logo for '{business_name}', a {business_idea} business. Style: {style}. The logo should be memorable, scalable, and work well in both color and black & white."

    def generate_social_media_content(self, platform, business_name, business_idea):
        """Generate social media content for different platforms"""
        content = {
            "linkedin": {
                "format": "Professional LinkedIn Post",
                "content": f"🚀 Excited to introduce {business_name}! \n\nWe're revolutionizing {business_idea} with innovative solutions that put our customers first. Our mission is to deliver exceptional value while building lasting relationships in our community.\n\n✨ What sets us apart:\n• Customer-centric approach\n• Quality-driven solutions\n• Community-focused values\n• Innovation at our core\n\nReady to experience the difference? Let's connect and explore how we can serve you better!\n\n#SmallBusiness #Innovation #CustomerFirst #CommunityBusiness #Entrepreneurship"
            },
            "instagram": {
                "format": "Instagram Post with Hashtags",
                "content": f"✨ Meet {business_name}! ✨\n\nYour new go-to for {business_idea} 🎯\n\nWe believe in:\n🌟 Quality over quantity\n💫 Customer happiness\n🚀 Innovation that matters\n💝 Community love\n\nReady to join our journey? \nDM us or visit our link in bio! 👆\n\n#SmallBusiness #{business_name.replace(' ', '')} #Local #Quality #Innovation #CustomerLove #NewBusiness #Entrepreneur #Community #Excellence #Service"
            },
            "facebook": {
                "format": "Facebook Ad Copy",
                "content": f"🎉 Welcome to {business_name}! 🎉\n\nLooking for exceptional {business_idea}? You've found the right place!\n\nWhy choose us?\n✅ Personalized service\n✅ Competitive pricing\n✅ Local expertise\n✅ Customer satisfaction guaranteed\n\n🎁 SPECIAL LAUNCH OFFER: Contact us this month for exclusive deals!\n\n📞 Get in touch today and discover the {business_name} difference!\n\n#LocalBusiness #QualityService #SpecialOffer #CustomerFirst"
            }
        }
        
        return content.get(platform.lower(), {"format": "General Social Media", "content": f"Check out {business_name} for amazing {business_idea}!"})

    def generate_innovative_ideas(self, business_idea):
        """Generate innovative ideas related to the business"""
        base_ideas = [
            "Implement a customer loyalty program with gamification elements",
            "Create a mobile app for easier customer interaction",
            "Partner with complementary local businesses for cross-promotion",
            "Offer subscription-based services for regular customers",
            "Use social media for behind-the-scenes content and customer stories",
            "Implement eco-friendly practices and market them as a unique selling point",
            "Create educational content related to your industry",
            "Offer virtual consultations or services",
            "Develop a referral program with attractive incentives",
            "Use data analytics to personalize customer experiences"
        ]
        
        # Customize ideas based on business type
        business_category = self.categorize_business(business_idea.lower())
        
        if business_category == "restaurant":
            base_ideas.extend([
                "Create signature dishes with local ingredients",
                "Offer cooking classes or food workshops",
                "Implement a farm-to-table concept",
                "Create themed dining experiences"
            ])
        elif business_category == "retail":
            base_ideas.extend([
                "Offer personal shopping services",
                "Create seasonal product bundles",
                "Implement AR try-before-you-buy features",
                "Host community events in your store"
            ])
        elif business_category == "tech":
            base_ideas.extend([
                "Implement AI-powered customer support",
                "Create API integrations with popular tools",
                "Offer white-label solutions",
                "Build a community platform for users"
            ])
        
        return random.sample(base_ideas, min(6, len(base_ideas)))

chatbot = SmallBusinessChatbot()

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    message = data.get('message', '').lower()
    business_idea = data.get('business_idea', '')
    
    response = {
        'message': '',
        'type': 'text',
        'data': None
    }
    
    if 'steps' in message or 'plan' in message or 'how to start' in message:
        if not business_idea:
            response['message'] = "I'd love to help you create a business plan! Could you tell me more about your business idea?"
        else:
            steps = chatbot.generate_business_steps('general', business_idea)
            response['message'] = f"Here's a comprehensive step-by-step plan for your {business_idea} business:"
            response['type'] = 'steps'
            response['data'] = steps
    
    elif 'name' in message and ('suggest' in message or 'generate' in message):
        if not business_idea:
            response['message'] = "I'd be happy to suggest some creative names! What's your business idea?"
        else:
            names = chatbot.generate_business_names(business_idea)
            response['message'] = f"Here are some creative and catchy names for your {business_idea} business:"
            response['type'] = 'names'
            response['data'] = names
    
    elif 'logo' in message:
        business_name = data.get('business_name', '')
        if not business_name or not business_idea:
            response['message'] = "To create a logo, I'll need your business name and idea. Could you provide both?"
        else:
            logo_prompt = chatbot.generate_logo_prompt(business_name, business_idea)
            response['message'] = f"Here's a detailed prompt for creating your logo. You can use this with AI image generators like DALL-E, Midjourney, or Stable Diffusion:"
            response['type'] = 'logo_prompt'
            response['data'] = logo_prompt
    
    elif any(platform in message for platform in ['linkedin', 'instagram', 'facebook', 'social media']):
        business_name = data.get('business_name', business_idea.title() + ' Business')
        platform = 'linkedin' if 'linkedin' in message else 'instagram' if 'instagram' in message else 'facebook' if 'facebook' in message else 'linkedin'
        
        if not business_idea:
            response['message'] = "I'd love to create social media content for you! What's your business idea?"
        else:
            content = chatbot.generate_social_media_content(platform, business_name, business_idea)
            response['message'] = f"Here's your {content['format']}:"
            response['type'] = 'social_media'
            response['data'] = content
    
    elif 'ideas' in message or 'innovative' in message or 'suggestions' in message:
        if not business_idea:
            response['message'] = "I'd be happy to suggest innovative ideas! What's your business concept?"
        else:
            ideas = chatbot.generate_innovative_ideas(business_idea)
            response['message'] = f"Here are some innovative ideas to enhance your {business_idea} business:"
            response['type'] = 'ideas'
            response['data'] = ideas
    
    else:
        response['message'] = """Welcome to your Small Business Assistant! 🚀

I'm here to help you turn your business idea into reality. Here's what I can do for you:

📋 **Business Planning**: Get step-by-step guidance for starting your business
🏷️ **Name Generation**: Creative and catchy business names
🎨 **Logo Creation**: Detailed prompts for logo design
📱 **Social Media**: LinkedIn posts, Instagram ads, and Facebook content
💡 **Innovation**: Fresh ideas to make your business stand out

Just tell me your business idea and what you'd like help with!

Examples:
- "I want to start a coffee shop, give me the steps"
- "Suggest names for my online tutoring business"
- "Create a LinkedIn post for my consulting firm"
- "Give me innovative ideas for my bakery"
"""
    
    return jsonify(response)

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)