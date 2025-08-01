#!/usr/bin/env python3
"""
Small Business Chatbot - Demo Script (Standalone)
This script demonstrates the core functionality of the chatbot without external dependencies
"""

import random

class SmallBusinessChatbotDemo:
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
            ]
        }
        
        self.name_prefixes = ["Smart", "Quick", "Pro", "Elite", "Prime", "Fresh", "Bright", "Swift"]
        self.name_suffixes = ["Hub", "Lab", "Works", "Studio", "Co", "Plus", "Pro", "Express"]
        self.funny_adjectives = ["Quirky", "Witty", "Snappy", "Peppy", "Zesty", "Bubbly", "Spunky", "Cheeky"]

    def categorize_business(self, business_idea):
        if any(word in business_idea for word in ["restaurant", "cafe", "food", "bakery", "bar"]):
            return "restaurant"
        else:
            return "service"

    def generate_business_names(self, business_idea, count=3):
        names = []
        key_words = [word.title() for word in business_idea.split() if len(word) > 3]
        
        for _ in range(count):
            if random.choice([True, False]) and key_words:
                name = f"{random.choice(self.funny_adjectives)} {random.choice(key_words)} {random.choice(self.name_suffixes)}"
            elif key_words:
                name = f"{random.choice(self.name_prefixes)} {random.choice(key_words)} {random.choice(self.name_suffixes)}"
            else:
                name = f"{random.choice(self.name_prefixes)} Business {random.choice(self.name_suffixes)}"
            names.append(name)
        
        return names

    def generate_business_steps(self, business_idea):
        category = self.categorize_business(business_idea.lower())
        return self.business_steps.get(category, self.business_steps["service"])

    def generate_innovative_ideas(self, business_idea):
        base_ideas = [
            "Implement a customer loyalty program with gamification elements",
            "Create a mobile app for easier customer interaction",
            "Partner with complementary local businesses for cross-promotion",
            "Offer subscription-based services for regular customers",
            "Use social media for behind-the-scenes content and customer stories",
            "Implement eco-friendly practices and market them as a unique selling point"
        ]
        return random.sample(base_ideas, min(3, len(base_ideas)))

def demo_chatbot():
    """Demonstrate the chatbot functionality"""
    print("🤖 Small Business Assistant Chatbot - Demo")
    print("=" * 60)
    
    chatbot = SmallBusinessChatbotDemo()
    
    demo_ideas = [
        "coffee shop",
        "online tutoring service", 
        "handmade jewelry business",
        "food truck"
    ]
    
    for idea in demo_ideas:
        print(f"\n🚀 Business Idea: {idea.title()}")
        print("-" * 40)
        
        # Generate business steps
        print("\n📋 Business Steps:")
        steps = chatbot.generate_business_steps(idea)
        for i, step in enumerate(steps[:4], 1):
            print(f"  {step}")
        print(f"  ... and {len(steps)-4} more comprehensive steps")
        
        # Generate business names
        print(f"\n🏷️ Creative Business Names:")
        names = chatbot.generate_business_names(idea, count=4)
        for name in names:
            print(f"  • {name}")
        
        # Generate innovative ideas
        print(f"\n💡 Innovation Ideas:")
        ideas = chatbot.generate_innovative_ideas(idea)
        for i, innovation in enumerate(ideas, 1):
            print(f"  {i}. {innovation}")
        
        print("\n" + "="*60)
    
    print("\n✨ Demo completed! The full chatbot includes:")
    print("• 📋 Step-by-step business plans (customized by industry)")
    print("• 🏷️ Creative and humorous business names")
    print("• 🎨 Logo design prompts for AI generators")
    print("• 📱 Social media content (LinkedIn, Instagram, Facebook)")
    print("• 💡 Industry-specific innovative ideas")
    print("• 🎯 Interactive web interface with beautiful UI")
    print("• 🚀 Real-time chat experience")
    
    print(f"\n🌐 To run the full web application:")
    print(f"   1. Install dependencies: python3 run.py")
    print(f"   2. Access at: http://localhost:3000")
    print(f"\n🎉 Transform your business ideas into reality!")

if __name__ == "__main__":
    demo_chatbot()