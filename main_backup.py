#!/usr/bin/env python3
"""
AI Post Bot for Telegram - Render.com Web Service
Generates 20 daily posts with AI content and nano banana images using Google Gemini models
Optimized for Render.com Web Service deployment with nano banana metaphor
"""

import os
import time
import schedule
import random
import requests
import threading
from datetime import datetime, timezone
from io import BytesIO
import logging
import base64
import json

# Core libraries
import google.generativeai as genai
from PIL import Image, ImageDraw, ImageFont
from flask import Flask, jsonify

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AIPostBot:
    def __init__(self):
        self.google_api_key = os.getenv('GOOGLE_API_KEY')
        self.telegram_bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.telegram_channel_id = os.getenv('TELEGRAM_CHANNEL_ID')
        
        # Store missing vars for later validation
        self.missing_vars = []
        if not self.google_api_key:
            self.missing_vars.append('GOOGLE_API_KEY')
        if not self.telegram_bot_token:
            self.missing_vars.append('TELEGRAM_BOT_TOKEN')
        if not self.telegram_channel_id:
            self.missing_vars.append('TELEGRAM_CHANNEL_ID')
            
        if self.missing_vars:
            logger.warning(f"Missing environment variables: {', '.join(self.missing_vars)}. Bot functionality will be limited.")
            return  # Don't initialize AI services without API keys
        
        # Initialize Google AI
        genai.configure(api_key=self.google_api_key)
        self.text_model = genai.GenerativeModel('gemini-1.5-flash-latest')
        
        # Initialize Telegram API URL
        self.telegram_api_url = f"https://api.telegram.org/bot{self.telegram_bot_token}"
        
        # Qiziqarli AI mavzulari va promptlari
        self.ai_topics = [
            "🎯 Prompt engineering sirli formulasi — AI dan 10x yaxshi natija olish yo'llari",
            "💸 AI bilan pul ishlash — real misollar va bosqichma-bosqich yo'riqnoma",
            "🎨 Midjourney va DALL-E dan ajoyib rasmlar — professional promptlar va triklar",
            "💻 ChatGPT bilan dasturlash — zero dan hero gacha yo'l",
            "📈 AI bilan biznes-ideya yaratish — startup uchun 100 ta fikr 1 daqiqada",
            "📝 CV yozishda AI mahorati — HR ni hayratda qoldiradigan resume yaratish",
            "🎬 AI video yaratish — YouTube uchun kontentni 5 daqiqada tayyorlash",
            "📚 O'zbek tilida AI — ChatGPT ga o'zbekcha qanday gaplashish o'rgatish?",
            "🔥 AI xatolarini bartaraf etish — nima uchun javob noto'g'ri va qanday tuzatish?",
            "🚀 AI bilan startup ochish — texnologiya orqali biznes qurish sirlari",
            "📸 AI rasm promptlari kolleksiyasi — har kuni yangi tasvirlar yaratish",
            "💡 Neural tarmoqlar oddiy tilda — 5 yoshli bolaga tushuntirish mumkin!",
            "⚡ GPT-4 vs Gemini vs Claude — qaysi biri eng zo'ri? Real test natijalar",
            "🎵 AI musiqa yaratish — hit qo'shiq yozish uchun professional yo'riqnoma",
            "🎮 AI bilan o'yin yaratish — kodlashmasdan o'yin yasash mumkinmi?",
            "📊 AI bilan ma'lumot tahlili — Excel dan 100x tezroq ishlash usullari",
            "🌍 AI tarjimon — 100+ tilda professional tarjima qilish sirlari",
            "📱 AI chat-bot yaratish — Telegram uchun aqlli assistant qurish",
            "🎪 AI bilan kreativ yozish — hikoya, she'r, ssenariy yaratish mahorati",
            "💼 AI bilan marketing — reklama matni va strategiya yaratish formulasi",
            "🔮 AI kelajak bashorati — 2025-yilda qanday imkoniyatlar ochiladi?",
            "🏆 AI olimpiada — kim eng zo'r prompt yoza oladi? Musobaqa boshlanadi!",
            "🎭 AI roleplay — ChatGPT ni Elon Musk, Steve Jobs kabi qilish sirlari",
            "📈 AI trading — kriptovalyuta va aksiyalarda AI yordamchisi"
        ]
        
        print("🤖 AI Post Bot Render.com Web Service da ishga tushdi. 7:00-21:00 UTC oralig'ida 20 ta post jo'natiladi.")
    
    def generate_uzbek_text(self, topic):
        """Generate Uzbek text content about AI topics using Gemini 1.5 Flash"""
        try:
            prompt = f"""O'zbek tilida, juda amaliy va o'rgatuvchi post yoz. Mavzu: {topic}

MAJBURIY TALABLAR:
🔥 ANIQ PROMPT MISOLLARI:
- Kamida 3-5 ta to'liq, ishlaydignan prompt berish
- Har birini "PROMPT:" deb belgilab, copy-paste qilib foydalanish mumkin bo'lgan formatda yozish
- Real natijalar va konkret misollar ko'rsatish

📋 BATAFSIL YO'RIQNOMA:
- Har bir bosqichni raqamlab, aniq ko'rsatma berish
- "Qanday qilish kerak" dan "Nima yozish kerak" gacha barchasini tushuntirish
- Xatolar va ulardan qanday qochishni ko'rsatish

🎯 AMALIY MASHQLAR:
- Foydalanuvchi darhol sinab ko'rishi mumkin bo'lgan vazifalar berish
- Boshlang'ich dan professional darajagacha turli variantlar
- Natijani qanday yaxshilash mumkinligini tushuntirish

📊 BATAFSIL STRUKTURA:
1. Hayratlanarli fakt/statistika (raqamlar bilan)
2. "Lekin muammo shunda..." - real muammo
3. "Mana yechim!" - aniq yo'riqnoma
4. PROMPT MISOLLARI (kamida 3-5 ta):
   - PROMPT 1: [aniq prompt matni]
   - PROMPT 2: [aniq prompt matni] 
   - va hokazo...
5. BOSQICHMA-BOSQICH YO'RIQNOMA:
   - 1-bosqich: [aniq harakat]
   - 2-bosqich: [aniq harakat]
   - va hokazo...
6. PRO MASLAHATLAR (kamida 3 ta konkret maslahat)
7. "HOZIROQ SINAB KO'RING!" - amaliy vazifa
8. Savol (o'quvchini faollashtirish uchun)

MISOLLAR FORMATI:
PROMPT: "Aniq va to'liq prompt matni shu yerda yoziladi, uni copy qilib paste qilish mumkin bo'lishi kerak"

NATIJA: Bu prompt qanday natija berishini tasvirlab bering

So'nggi qatorga: "➡️ https://t.me/nanobanananews kanaliga obuna bo'ling!" yozing.

MUHIM: Har doim aniq, amaliy va copy-paste qilib foydalanish mumkin bo'lgan promptlarni bering. Umumiy gap-so'z emas, aniq yo'riqnomalar kerak!
            
            logger.info(f"Generating Uzbek text for topic: {topic}")
            response = self.text_model.generate_content(prompt)
            
            if response and hasattr(response, 'text') and response.text:
                generated_text = response.text.strip()
                logger.info(f"Successfully generated {len(generated_text)} characters of Uzbek text")
                return generated_text
            else:
                return self._get_fallback_text(topic)
                
        except Exception as e:
            logger.error(f"Error generating Uzbek text: {e}")
            return self._get_fallback_text(topic)
    
    def _get_fallback_text(self, topic):
        """Generate fallback text when Gemini fails"""
        topic_simple = topic.replace('—', '-') if '—' in topic else topic
        
        text_parts = [
            f"AI AMALIY YO'RIQNOMA: {topic_simple}",
            "",
            "Bilasizmi, professional promptlarni yozish - bu san'at! Keling, aniq misollar orqali o'rganamiz.",
            "",
            "AMALIY PROMPT MISOLLARI:",
            "",
            'PROMPT 1: "Menga [mavzu] haqida batafsil va tushunarli tarzda tushuntir. 5 yoshli bolaga tushuntirgandek oddiy tildan foydalanib, misollar kel"',
            "",
            "NATIJA: Har qanday murakkab mavzuni osonroq tushunasiz",
            "",
            'PROMPT 2: "Quyidagi matnni professional va rasmiy tarzda qayta yoz: [matn]. Ishbilarmon email uchun mos shaklda tayyorla"',
            "",
            "NATIJA: Har qanday matnni professional ko'rinishga keltiradi",
            "",
            f'PROMPT 3: "Menga {topic_simple.split("-")[0].strip() if "-" in topic_simple else topic_simple} bo\'yicha 10 ta konkret maslahat ber. Har biri amaliy va darhol qo\'llash mumkin bo\'lsin"',
            "",
            "NATIJA: To'g'ridan-to'g'ri amaliyotga tatbiq qilish mumkin",
            "",
            "PRO MASLAHAT:",
            "- Har doim aniq va konkret so'rov qiling",
            '- Kontekst bering ("...uchun", "...maqsadida")',
            '- Format ko\'rsating ("ro\'yxat shaklida", "bosqichma-bosqich")',
            "",
            "HOZIROQ SINAB KO'RING: Yuqoridagi birorta promptni copy qilib, o'z mavzungiz bilan sinang!",
            "",
            "Siz qaysi promptni sinab ko'rdingiz va qanday natija oldingiz?",
            "",
            "https://t.me/nanobanananews kanaliga obuna bo'ling!"
        ]
        
        return "\n".join(text_parts)
    
    def generate_topic_image(self, topic):
        """Generate topic-related image using Gemini 2.5 Flash Image Preview (no text in image)"""
        try:
            logger.info(f"Generating topic-related image with Gemini 2.5 Flash Image Preview for topic: {topic}")
            
            image_model = genai.GenerativeModel('gemini-2.5-flash-image-preview')
            
            # Generate image related to the topic without any text
            prompt = f"""Create a high-quality, professional image related to: '{topic}'. 
Show relevant objects, scenes, technology, or illustrations that represent this AI topic.
Style: modern, clean, professional, educational, suitable for social media.
NO TEXT, NO WORDS, NO LETTERS in the image - only visual elements.
16:9 aspect ratio, high detail, good lighting, colorful and engaging.
Examples of what to show:
- For ChatGPT/AI models: robot, computer brain, neural networks
- For image generation: artist tools, creative scenes, digital art
- For programming: code symbols, computers, development setup
- For learning AI: books, brain, lightbulb, education symbols
Background should be clean and modern."""
            
            response = image_model.generate_content(prompt)
            
            if response and hasattr(response, 'parts') and response.parts:
                for part in response.parts:
                    if hasattr(part, 'inline_data') and part.inline_data and hasattr(part.inline_data, 'data'):
                        image_data_b64 = part.inline_data.data
                        if isinstance(image_data_b64, str):
                            image_data = base64.b64decode(image_data_b64)
                        else:
                            image_data = image_data_b64
                        
                        if len(image_data) > 0:
                            logger.info(f"Successfully generated topic image: {len(image_data)} bytes")
                            return BytesIO(image_data)
            
            logger.warning("No valid image data found in Gemini 2.5 Flash Image Preview response")
            return None
            
        except Exception as e:
            logger.error(f"Error generating topic image with Gemini 2.5 Flash Image Preview: {e}")
            return None
    
    def generate_dynamic_image_prompt(self, topic):
        """Generate dynamic and varied prompts for different topics"""
        # Define topic categories and their visual elements
        topic_visuals = {
            'chatgpt': ['robot head', 'chat bubbles', 'brain neural networks', 'conversation interface'],
            'prompt': ['lightbulb', 'command terminal', 'magic wand', 'speech bubble with code'],
            'midjourney': ['artist palette', 'digital brush', 'creative scene', 'art studio'],
            'rasm': ['camera', 'image gallery', 'creative tools', 'design studio'],
            'python': ['snake logo', 'code blocks', 'programming setup', 'terminal window'],
            'cv': ['document', 'professional profile', 'resume template', 'office desk'],
            'video': ['film camera', 'video editing', 'movie clapper', 'screen recording'],
            'matn': ['typewriter', 'documents', 'writing desk', 'keyboard'],
            'o\'qish': ['books', 'education symbols', 'student desk', 'learning environment'],
            'blog': ['laptop', 'writing', 'publish button', 'content creation'],
            'xato': ['warning signs', 'debug symbols', 'error fixing', 'troubleshooting'],
            'sarlavha': ['title design', 'headline text', 'newspaper', 'content header'],
            'dastur': ['code editor', 'software development', 'programming languages', 'app interface'],
            'tarjima': ['language symbols', 'translation interface', 'global communication', 'multilingual'],
            'musiqa': ['musical notes', 'sound waves', 'audio studio', 'headphones'],
            'o\'yin': ['game controller', 'pixel art', 'game development', 'gaming setup'],
            'biznes': ['charts', 'business meeting', 'innovation', 'startup environment'],
            'reja': ['calendar', 'planning board', 'schedule', 'time management'],
            'o\'rganish': ['graduation cap', 'study materials', 'research', 'knowledge symbols']
        }
        
        # Color schemes for variety
        color_schemes = [
            ['#667eea', '#764ba2'],  # Purple-blue
            ['#f093fb', '#f5576c'],  # Pink-red
            ['#4facfe', '#00f2fe'],  # Blue-cyan
            ['#43e97b', '#38f9d7'],  # Green-teal
            ['#fa709a', '#fee140'],  # Pink-yellow
            ['#a8edea', '#fed6e3'],  # Mint-pink
            ['#ff9a9e', '#fecfef'],  # Coral-pink
            ['#a18cd1', '#fbc2eb']   # Purple-pink
        ]
        
        # Find matching visual elements
        visual_elements = ['technology symbols', 'modern interface', 'digital elements']
        for key in topic_visuals:
            if key in topic.lower():
                visual_elements = topic_visuals[key]
                break
        
        # Random selection for variety
        import random
        selected_elements = random.sample(visual_elements, min(2, len(visual_elements)))
        selected_colors = random.choice(color_schemes)
        
        # Background styles
        backgrounds = [
            'clean gradient background',
            'modern geometric background',
            'abstract technological background',
            'minimalist professional background',
            'futuristic digital background'
        ]
        
        selected_bg = random.choice(backgrounds)
        
        # Generate dynamic prompt
        prompt = f"""Create a modern, professional illustration featuring {', '.join(selected_elements)}. 
Style: clean, minimalist, suitable for social media and educational content.
Colors: gradient from {selected_colors[0]} to {selected_colors[1]} with accent colors.
Background: {selected_bg}
NO TEXT, NO WORDS, NO LETTERS in the image - only visual symbols and elements.
Composition: balanced, centered, with good contrast and visual hierarchy.
16:9 aspect ratio, high quality, professional design."""
        
        return prompt

    def create_topic_graphic(self, topic):
        """Create varied topic-related graphics using PIL with dynamic content"""
        try:
            import random
            width, height = 1000, 562  # 16:9 aspect ratio
            
            # Generate varied color scheme
            color_schemes = [
                {'bg': ['#1a1a2e', '#16213e'], 'accent': ['#00ff88', '#ff6b6b', '#4ecdc4']},
                {'bg': ['#2d1b69', '#11998e'], 'accent': ['#ffd93d', '#ff6b6b', '#6c5ce7']},
                {'bg': ['#667eea', '#764ba2'], 'accent': ['#ffffff', '#f093fb', '#4facfe']},
                {'bg': ['#f093fb', '#f5576c'], 'accent': ['#ffffff', '#43e97b', '#4facfe']},
                {'bg': ['#4facfe', '#00f2fe'], 'accent': ['#ffffff', '#43e97b', '#ff6b6b']}
            ]
            
            scheme = random.choice(color_schemes)
            img = Image.new('RGB', (width, height), color=scheme['bg'][0])
            draw = ImageDraw.Draw(img)
            
            # Create varied gradient background
            bg_start = scheme['bg'][0].lstrip('#')
            bg_end = scheme['bg'][1].lstrip('#')
            
            start_rgb = tuple(int(bg_start[i:i+2], 16) for i in (0, 2, 4))
            end_rgb = tuple(int(bg_end[i:i+2], 16) for i in (0, 2, 4))
            
            for y in range(height):
                ratio = y / height
                r = int(start_rgb[0] + (end_rgb[0] - start_rgb[0]) * ratio)
                g = int(start_rgb[1] + (end_rgb[1] - start_rgb[1]) * ratio)
                b = int(start_rgb[2] + (end_rgb[2] - start_rgb[2]) * ratio)
                draw.line([(0, y), (width, y)], fill=(r, g, b))
            
            # Determine topic-specific elements
            center_x, center_y = width // 2, height // 2
            
            # Draw topic-specific patterns
            if 'chatgpt' in topic.lower() or 'prompt' in topic.lower():
                # Chat/conversation elements
                for i, (x, y) in enumerate([(200, 150), (600, 200), (400, 300)]):
                    color = scheme['accent'][i % len(scheme['accent'])]
                    # Chat bubble shapes
                    draw.ellipse([x-30, y-20, x+30, y+20], outline=color, width=3)
                    draw.polygon([(x-35, y), (x-25, y+10), (x-25, y-10)], fill=color)
                    
            elif 'rasm' in topic.lower() or 'midjourney' in topic.lower():
                # Creative/artistic elements
                for i in range(6):
                    x = random.randint(100, width-100)
                    y = random.randint(100, height-100)
                    color = random.choice(scheme['accent'])
                    size = random.randint(15, 40)
                    # Artistic shapes
                    if i % 3 == 0:
                        draw.ellipse([x-size, y-size, x+size, y+size], outline=color, width=2)
                    elif i % 3 == 1:
                        draw.rectangle((x-size, y-size, x+size, y+size), outline=color, width=2)
                    else:
                        points = [(x, y-size), (x+size, y+size), (x-size, y+size)]
                        draw.polygon(points, outline=color, width=2)
                        
            elif 'python' in topic.lower() or 'dastur' in topic.lower():
                # Programming elements
                for i in range(8):
                    x = 150 + (i % 4) * 200
                    y = 150 + (i // 4) * 200
                    color = scheme['accent'][i % len(scheme['accent'])]
                    # Code block representations
                    draw.rectangle((x-40, y-15, x+40, y+15), outline=color, width=2)
                    for j in range(3):
                        draw.line([x-35+j*20, y-10+j*7, x-15+j*20, y-10+j*7], fill=color, width=1)
                        
            else:
                # General AI/tech elements
                positions = [(200, 180), (500, 150), (800, 200), (300, 350), (700, 380)]
                for i, (x, y) in enumerate(positions):
                    color = scheme['accent'][i % len(scheme['accent'])]
                    # Neural network nodes
                    draw.ellipse([x-20, y-20, x+20, y+20], fill=color)
                    # Connecting lines
                    if i < len(positions) - 1:
                        next_x, next_y = positions[i+1]
                        draw.line([x, y, next_x, next_y], fill=color, width=2)
            
            # Add random decorative elements
            for _ in range(random.randint(10, 20)):
                x = random.randint(50, width-50)
                y = random.randint(50, height-50)
                color = random.choice(scheme['accent'])
                size = random.randint(2, 8)
                draw.ellipse([x-size, y-size, x+size, y+size], fill=color)
            
            # Save to BytesIO
            img_buffer = BytesIO()
            img.save(img_buffer, format='PNG', quality=95)
            img_buffer.seek(0)
            
            return img_buffer
            
        except Exception as e:
            logger.error(f"Error creating topic graphic: {e}")
            return None
    
    def post_to_telegram(self, text, image_buffer):
        """Post content to Telegram channel"""
        try:
            if image_buffer:
                image_buffer.seek(0)
                
                # Check if text is too long for caption (1024 char limit)
                if len(text) <= 1024:
                    # Send photo with full caption
                    files = {'photo': ('nano_banana_image.png', image_buffer, 'image/png')}
                    data = {
                        'chat_id': self.telegram_channel_id,
                        'caption': text
                    }
                    
                    response = requests.post(
                        f"{self.telegram_api_url}/sendPhoto",
                        files=files,
                        data=data,
                        timeout=30
                    )
                    
                    if response.status_code == 200:
                        logger.info("Posted complete content to Telegram with image")
                        return True
                    else:
                        logger.error(f"Telegram API error: {response.status_code} - {response.text}")
                        return False
                else:
                    # Text is too long, send image with short caption and full text separately
                    # Send photo with short caption
                    short_caption = "AI haqida qiziqarli ma'lumot 👇"
                    files = {'photo': ('nano_banana_image.png', image_buffer, 'image/png')}
                    data = {
                        'chat_id': self.telegram_channel_id,
                        'caption': short_caption
                    }
                    
                    photo_response = requests.post(
                        f"{self.telegram_api_url}/sendPhoto",
                        files=files,
                        data=data,
                        timeout=30
                    )
                    
                    if photo_response.status_code != 200:
                        logger.error(f"Telegram photo API error: {photo_response.status_code} - {photo_response.text}")
                        return False
                    
                    # Send full text as separate message
                    text_data = {
                        'chat_id': self.telegram_channel_id,
                        'text': text
                    }
                    
                    text_response = requests.post(
                        f"{self.telegram_api_url}/sendMessage",
                        data=text_data,
                        timeout=30
                    )
                    
                    if text_response.status_code == 200:
                        logger.info("Posted long content to Telegram with image and separate text message")
                        return True
                    else:
                        logger.error(f"Telegram text API error: {text_response.status_code} - {text_response.text}")
                        return False
            else:
                # Send text message only
                data = {
                    'chat_id': self.telegram_channel_id,
                    'text': text
                }
                
                response = requests.post(
                    f"{self.telegram_api_url}/sendMessage",
                    data=data,
                    timeout=30
                )
                
                if response.status_code == 200:
                    logger.info("Posted to Telegram (text only)")
                    return True
                else:
                    logger.error(f"Telegram API error: {response.status_code} - {response.text}")
                    return False
            
        except Exception as e:
            logger.error(f"Error posting to Telegram: {e}")
            return False
    
    def create_and_post_ai_post(self):
        """Generate AI post with topic-related image (no text in image) and detailed text"""
        try:
            # Select random topic
            topic = random.choice(self.ai_topics)
            logger.info(f"Creating AI post with image for topic: {topic}")
            
            # Generate detailed Uzbek text content
            text_content = self.generate_uzbek_text(topic)
            
            # Try to generate topic-related image (without text)
            image_buffer = self.generate_topic_image(topic)
            
            # If AI image generation failed, create topic-related graphic fallback
            if not image_buffer:
                logger.info("AI image generation failed, creating topic-related graphic fallback")
                image_buffer = self.create_topic_graphic(topic)
            
            # Post to Telegram with image and text caption
            success = self.post_to_telegram(text_content, image_buffer)
            
            if success:
                logger.info("✅ AI post with image and text published successfully")
            else:
                logger.error("❌ Failed to publish AI post")
                
        except Exception as e:
            logger.error(f"Error in create_and_post_ai_post: {e}")
    
    def setup_schedule(self):
        """Setup posting schedule - 20 posts from 7:00 to 21:00 UTC (every ~42 minutes)"""
        post_times = []
        start_hour = 7
        end_hour = 21
        
        # Calculate 20 post times evenly distributed across 14 hours
        total_minutes = (end_hour - start_hour) * 60  # 14 hours = 840 minutes
        interval = total_minutes // 19  # 19 intervals for 20 posts (42 minutes approximately)
        
        for i in range(20):
            minutes_from_start = i * interval
            hour = start_hour + (minutes_from_start // 60)
            minute = minutes_from_start % 60
            
            time_str = f"{hour:02d}:{minute:02d}"
            post_times.append(time_str)
            
            schedule.every().day.at(time_str).do(self.create_and_post_ai_post)
            logger.info(f"Scheduled nano banana post at {time_str} UTC")
        
        logger.info(f"✅ Scheduled {len(post_times)} daily nano banana posts from {post_times[0]} to {post_times[-1]} UTC")
    
    def run_scheduler(self):
        """Run scheduler in background thread"""
        logger.info("Starting nano banana scheduler thread...")
        while True:
            try:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
            except Exception as e:
                logger.error(f"Error in nano banana scheduler: {e}")
                time.sleep(60)

# Flask app setup
app = Flask(__name__)

@app.route('/')
def index():
    """Root endpoint returning JSON status"""
    return {"status": "alive"}

@app.route('/health')
def health():
    """Health check endpoint"""
    return {"status": "healthy"}

@app.route('/status')
def status():
    """Status endpoint showing environment configuration"""
    try:
        bot = AIPostBot()
        return {
            "status": "running",
            "environment_configured": len(bot.missing_vars) == 0,
            "missing_variables": bot.missing_vars,
            "scheduler_active": len(bot.missing_vars) == 0
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.route('/test_post')
def test_post():
    """Test endpoint to manually trigger a post"""
    try:
        bot = AIPostBot()
        if bot.missing_vars:
            return {"status": "error", "message": f"Missing environment variables: {', '.join(bot.missing_vars)}. Please configure them to enable bot functionality."}
        bot.create_and_post_ai_post()
        return {"status": "Test post sent successfully"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def main():
    """Main entry point"""
    try:
        # Initialize nano banana bot
        bot = AIPostBot()
        
        # Only start scheduling if we have all required environment variables
        if not bot.missing_vars:
            bot.setup_schedule()
            # Start scheduler in background thread
            scheduler_thread = threading.Thread(target=bot.run_scheduler, daemon=True)
            scheduler_thread.start()
        logger.info("Bot scheduler started successfully")
        else:
        logger.info("Bot scheduler not started due to missing environment variables")
        
        # Get port from environment (default to 5000 for Replit)
        port = int(os.getenv('PORT', 5000))  # Use port 5000 for Replit frontend
        
        # Start Flask web server (always start this for health checks)
        logger.info(f"Starting Flask web server on 0.0.0.0:{port}")
        app.run(host='0.0.0.0', port=port, debug=False)
        
    except Exception as e:
        logger.error(f"Failed to start application: {e}")
        exit(1)

if __name__ == "__main__":
    main()