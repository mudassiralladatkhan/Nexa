"""
Nexa Entertainment Module
Provides jokes, fun facts, motivational quotes, and other entertainment content
Ported and enhanced from VocalPA entertainment features
"""

import random
from typing import Dict, List, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class EntertainmentProvider:
    def __init__(self):
        # Jokes database - expanded from VocalPA
        self.jokes = [
            # Programming jokes
            "Why don't scientists trust atoms? Because they make up everything!",
            "Why did the scarecrow win an award? He was outstanding in his field!",
            "What do you call a fake noodle? An impasta!",
            "Why don't eggs tell jokes? They'd crack each other up!",
            "What do you call a sleeping bull? A bulldozer!",
            "Why don't programmers like nature? It has too many bugs!",
            "What's the best thing about Switzerland? I don't know, but the flag is a big plus!",
            "Why do Java developers wear glasses? Because they can't C#!",
            "How do you organize a space party? You planet!",
            "Why did the math book look so sad? Because it had too many problems!",
            
            # Tech jokes
            "Why was the computer cold? It left its Windows open!",
            "Why don't robots ever panic? They have nerves of steel!",
            "What do you call a computer that sings? A Dell!",
            "Why did the smartphone go to therapy? It had too many apps-iety issues!",
            "What's a computer's favorite snack? Microchips!",
            "Why don't computers take their hats off? Because they have bad CAPS LOCK!",
            "What do you call a computer superhero? A screensaver!",
            "Why was the computer tired when it got home? It had a hard drive!",
            "What do you call a computer that can pick up heavy things? A Dell-ivery truck!",
            "Why don't computers ever get hungry? They always have cookies!",
            
            # General jokes
            "What do you call a bear with no teeth? A gummy bear!",
            "Why don't scientists trust stairs? Because they're always up to something!",
            "What do you call a dinosaur that crashes his car? Tyrannosaurus Wrecks!",
            "Why don't some couples go to the gym? Because some relationships don't work out!",
            "What do you call a fish wearing a bowtie? Sofishticated!",
            "Why don't skeletons fight each other? They don't have the guts!",
            "What do you call a cow with no legs? Ground beef!",
            "Why did the bicycle fall over? Because it was two-tired!",
            "What do you call a dog magician? A labracadabrador!",
            "Why don't scientists trust atoms? Because they make up everything!",
            
            # Dad jokes
            "I'm reading a book about anti-gravity. It's impossible to put down!",
            "Did you hear about the mathematician who's afraid of negative numbers? He'll stop at nothing to avoid them!",
            "I told my wife she was drawing her eyebrows too high. She looked surprised!",
            "What do you call a factory that makes okay products? A satisfactory!",
            "I used to hate facial hair, but then it grew on me!",
            "Why don't scientists trust atoms? Because they make up everything!",
            "I'm terrified of elevators, so I'm going to start taking steps to avoid them!",
            "What do you call a belt made of watches? A waist of time!",
            "I lost my job at the bank. A woman asked me to check her balance, so I pushed her over!",
            "Why don't scientists trust atoms? Because they make up everything!"
        ]
        
        # Fun facts database
        self.fun_facts = [
            # Science facts
            "A group of flamingos is called a 'flamboyance'.",
            "Honey never spoils. Archaeologists have found pots of honey in ancient Egyptian tombs that are over 3,000 years old and still perfectly edible.",
            "A shrimp's heart is in its head.",
            "Bananas are berries, but strawberries aren't.",
            "There are more possible games of chess than there are atoms in the observable universe.",
            "A day on Venus is longer than its year.",
            "Octopuses have three hearts and blue blood.",
            "The human brain uses about 20% of the body's total energy.",
            "Lightning strikes the Earth about 100 times per second.",
            "A single cloud can weigh more than a million pounds.",
            
            # Technology facts
            "The first computer bug was an actual bug - a moth trapped in a Harvard computer in 1947.",
            "The term 'spam' for unwanted email comes from a Monty Python sketch.",
            "The first webcam was created to monitor a coffee pot at Cambridge University.",
            "Google's original name was 'BackRub'.",
            "The first YouTube video was uploaded on April 23, 2005, and was titled 'Me at the zoo'.",
            "WiFi doesn't stand for anything - it's just a made-up name.",
            "The '@' symbol was used in email for the first time in 1971.",
            "The first computer mouse was made of wood.",
            "Amazon was originally called 'Cadabra'.",
            "The first iPhone didn't have copy and paste functionality.",
            
            # Human facts
            "Humans are the only animals that blush.",
            "Your nose can remember 50,000 different scents.",
            "The human eye can distinguish about 10 million colors.",
            "You blink about 17,000 times per day.",
            "Your brain generates about 12-25 watts of electricity - enough to power a low wattage LED light.",
            "Humans shed about 8 pounds of dead skin cells each year.",
            "The average person walks the equivalent of three times around the world in their lifetime.",
            "Your heart beats about 100,000 times per day.",
            "Humans are the only animals that can draw straight lines.",
            "The human body contains about 37.2 trillion cells.",
            
            # Space facts
            "One day on Mercury lasts about 59 Earth days.",
            "Jupiter has at least 79 known moons.",
            "The Sun is so large that about 1.3 million Earths could fit inside it.",
            "A year on Neptune lasts 165 Earth years.",
            "The International Space Station orbits Earth every 90 minutes.",
            "There are more stars in the universe than grains of sand on all Earth's beaches.",
            "Saturn's moon Titan has lakes and rivers of liquid methane.",
            "The footprints on the Moon will last for millions of years because there's no wind to blow them away.",
            "Venus rotates backwards compared to most planets.",
            "Mars has the largest volcano in the solar system - Olympus Mons.",
            
            # Animal facts
            "Dolphins have names for each other.",
            "Elephants can recognize themselves in mirrors.",
            "A group of pandas is called an 'embarrassment'.",
            "Penguins propose to their mates with pebbles.",
            "Cats have a third eyelid called a nictitating membrane.",
            "A group of owls is called a 'parliament'.",
            "Butterflies taste with their feet.",
            "A group of crows is called a 'murder'.",
            "Seahorses are the only animals where the male gives birth.",
            "Polar bears have black skin under their white fur."
        ]
        
        # Motivational quotes database
        self.motivational_quotes = [
            # Success and achievement
            "The only way to do great work is to love what you do. - Steve Jobs",
            "Innovation distinguishes between a leader and a follower. - Steve Jobs",
            "The future belongs to those who believe in the beauty of their dreams. - Eleanor Roosevelt",
            "It is during our darkest moments that we must focus to see the light. - Aristotle",
            "Success is not final, failure is not fatal: it is the courage to continue that counts. - Winston Churchill",
            "The only impossible journey is the one you never begin. - Tony Robbins",
            "In the middle of difficulty lies opportunity. - Albert Einstein",
            "Believe you can and you're halfway there. - Theodore Roosevelt",
            "The way to get started is to quit talking and begin doing. - Walt Disney",
            "Don't be afraid to give up the good to go for the great. - John D. Rockefeller",
            
            # Technology and innovation
            "Technology is best when it brings people together. - Matt Mullenweg",
            "The advance of technology is based on making it fit in so that you don't really even notice it, so it's part of everyday life. - Bill Gates",
            "Any sufficiently advanced technology is indistinguishable from magic. - Arthur C. Clarke",
            "The real problem is not whether machines think but whether men do. - B.F. Skinner",
            "The Internet is becoming the town square for the global village of tomorrow. - Bill Gates",
            "Code is poetry. - WordPress motto",
            "Programs must be written for people to read, and only incidentally for machines to execute. - Harold Abelson",
            "The best way to predict the future is to invent it. - Alan Kay",
            "Software is a great combination between artistry and engineering. - Bill Gates",
            "First, solve the problem. Then, write the code. - John Johnson",
            
            # Personal growth
            "Be yourself; everyone else is already taken. - Oscar Wilde",
            "Life is what happens to you while you're busy making other plans. - John Lennon",
            "The only person you are destined to become is the person you decide to be. - Ralph Waldo Emerson",
            "Your time is limited, don't waste it living someone else's life. - Steve Jobs",
            "The greatest glory in living lies not in never falling, but in rising every time we fall. - Nelson Mandela",
            "If you want to lift yourself up, lift up someone else. - Booker T. Washington",
            "The only way to make sense out of change is to plunge into it, move with it, and join the dance. - Alan Watts",
            "Yesterday is history, tomorrow is a mystery, today is a gift of God, which is why we call it the present. - Bill Keane",
            "You miss 100% of the shots you don't take. - Wayne Gretzky",
            "Whether you think you can or you think you can't, you're right. - Henry Ford",
            
            # Wisdom and life
            "The only true wisdom is in knowing you know nothing. - Socrates",
            "Life is 10% what happens to you and 90% how you react to it. - Charles R. Swindoll",
            "The journey of a thousand miles begins with one step. - Lao Tzu",
            "It does not matter how slowly you go as long as you do not stop. - Confucius",
            "Everything you've ever wanted is on the other side of fear. - George Addair",
            "Happiness is not something ready made. It comes from your own actions. - Dalai Lama",
            "The best time to plant a tree was 20 years ago. The second best time is now. - Chinese Proverb",
            "A person who never made a mistake never tried anything new. - Albert Einstein",
            "The only limit to our realization of tomorrow will be our doubts of today. - Franklin D. Roosevelt",
            "Do not go where the path may lead, go instead where there is no path and leave a trail. - Ralph Waldo Emerson"
        ]
        
        # Riddles database
        self.riddles = [
            {
                "question": "What has keys but no locks, space but no room, and you can enter but not go inside?",
                "answer": "A keyboard"
            },
            {
                "question": "I speak without a mouth and hear without ears. I have no body, but come alive with wind. What am I?",
                "answer": "An echo"
            },
            {
                "question": "The more you take, the more you leave behind. What am I?",
                "answer": "Footsteps"
            },
            {
                "question": "What can travel around the world while staying in a corner?",
                "answer": "A stamp"
            },
            {
                "question": "What has a head, a tail, is brown, and has no legs?",
                "answer": "A penny"
            },
            {
                "question": "What gets wet while drying?",
                "answer": "A towel"
            },
            {
                "question": "What can you break, even if you never pick it up or touch it?",
                "answer": "A promise"
            },
            {
                "question": "I'm tall when I'm young, and short when I'm old. What am I?",
                "answer": "A candle"
            },
            {
                "question": "What has one eye but can't see?",
                "answer": "A needle"
            },
            {
                "question": "What has hands but can't clap?",
                "answer": "A clock"
            }
        ]
        
        # Trivia questions
        self.trivia = [
            {
                "question": "What is the largest planet in our solar system?",
                "answer": "Jupiter"
            },
            {
                "question": "Who painted the Mona Lisa?",
                "answer": "Leonardo da Vinci"
            },
            {
                "question": "What is the chemical symbol for gold?",
                "answer": "Au"
            },
            {
                "question": "Which country has the most time zones?",
                "answer": "France (12 time zones)"
            },
            {
                "question": "What is the smallest country in the world?",
                "answer": "Vatican City"
            },
            {
                "question": "Who invented the telephone?",
                "answer": "Alexander Graham Bell"
            },
            {
                "question": "What is the hardest natural substance on Earth?",
                "answer": "Diamond"
            },
            {
                "question": "Which planet is known as the Red Planet?",
                "answer": "Mars"
            },
            {
                "question": "What is the largest ocean on Earth?",
                "answer": "Pacific Ocean"
            },
            {
                "question": "Who wrote Romeo and Juliet?",
                "answer": "William Shakespeare"
            }
        ]

    def get_joke(self, category: str = None) -> Dict:
        """Get a random joke, optionally filtered by category"""
        try:
            if category:
                # Filter jokes by category (basic implementation)
                category_lower = category.lower()
                if 'tech' in category_lower or 'computer' in category_lower or 'programming' in category_lower:
                    tech_jokes = [joke for joke in self.jokes if any(word in joke.lower() for word in ['computer', 'program', 'java', 'bug', 'windows', 'robot', 'app'])]
                    if tech_jokes:
                        joke = random.choice(tech_jokes)
                    else:
                        joke = random.choice(self.jokes)
                else:
                    joke = random.choice(self.jokes)
            else:
                joke = random.choice(self.jokes)
            
            return {
                'success': True,
                'content': joke,
                'type': 'joke',
                'category': category or 'general'
            }
        except Exception as e:
            logger.error(f"Error getting joke: {str(e)}")
            return {
                'success': False,
                'message': "Sorry, I couldn't get a joke right now."
            }

    def get_fun_fact(self, category: str = None) -> Dict:
        """Get a random fun fact, optionally filtered by category"""
        try:
            if category:
                category_lower = category.lower()
                if 'science' in category_lower:
                    science_facts = [fact for fact in self.fun_facts if any(word in fact.lower() for word in ['atom', 'brain', 'heart', 'lightning', 'cloud', 'honey', 'octopus'])]
                    if science_facts:
                        fact = random.choice(science_facts)
                    else:
                        fact = random.choice(self.fun_facts)
                elif 'tech' in category_lower or 'technology' in category_lower:
                    tech_facts = [fact for fact in self.fun_facts if any(word in fact.lower() for word in ['computer', 'google', 'youtube', 'email', 'wifi', 'mouse', 'amazon'])]
                    if tech_facts:
                        fact = random.choice(tech_facts)
                    else:
                        fact = random.choice(self.fun_facts)
                elif 'space' in category_lower:
                    space_facts = [fact for fact in self.fun_facts if any(word in fact.lower() for word in ['mercury', 'jupiter', 'sun', 'neptune', 'moon', 'mars', 'venus', 'saturn'])]
                    if space_facts:
                        fact = random.choice(space_facts)
                    else:
                        fact = random.choice(self.fun_facts)
                elif 'animal' in category_lower:
                    animal_facts = [fact for fact in self.fun_facts if any(word in fact.lower() for word in ['dolphin', 'elephant', 'panda', 'penguin', 'cat', 'owl', 'butterfly', 'crow', 'seahorse', 'polar bear'])]
                    if animal_facts:
                        fact = random.choice(animal_facts)
                    else:
                        fact = random.choice(self.fun_facts)
                else:
                    fact = random.choice(self.fun_facts)
            else:
                fact = random.choice(self.fun_facts)
            
            return {
                'success': True,
                'content': fact,
                'type': 'fun_fact',
                'category': category or 'general'
            }
        except Exception as e:
            logger.error(f"Error getting fun fact: {str(e)}")
            return {
                'success': False,
                'message': "Sorry, I couldn't get a fun fact right now."
            }

    def get_motivational_quote(self, category: str = None) -> Dict:
        """Get a random motivational quote, optionally filtered by category"""
        try:
            if category:
                category_lower = category.lower()
                if 'tech' in category_lower or 'technology' in category_lower:
                    tech_quotes = [quote for quote in self.motivational_quotes if any(word in quote.lower() for word in ['technology', 'code', 'software', 'program', 'internet', 'machine'])]
                    if tech_quotes:
                        quote = random.choice(tech_quotes)
                    else:
                        quote = random.choice(self.motivational_quotes)
                elif 'success' in category_lower or 'achievement' in category_lower:
                    success_quotes = [quote for quote in self.motivational_quotes if any(word in quote.lower() for word in ['success', 'achieve', 'great', 'work', 'dream', 'future'])]
                    if success_quotes:
                        quote = random.choice(success_quotes)
                    else:
                        quote = random.choice(self.motivational_quotes)
                else:
                    quote = random.choice(self.motivational_quotes)
            else:
                quote = random.choice(self.motivational_quotes)
            
            return {
                'success': True,
                'content': quote,
                'type': 'motivational_quote',
                'category': category or 'general'
            }
        except Exception as e:
            logger.error(f"Error getting motivational quote: {str(e)}")
            return {
                'success': False,
                'message': "Sorry, I couldn't get a motivational quote right now."
            }

    def get_riddle(self) -> Dict:
        """Get a random riddle"""
        try:
            riddle = random.choice(self.riddles)
            return {
                'success': True,
                'question': riddle['question'],
                'answer': riddle['answer'],
                'type': 'riddle'
            }
        except Exception as e:
            logger.error(f"Error getting riddle: {str(e)}")
            return {
                'success': False,
                'message': "Sorry, I couldn't get a riddle right now."
            }

    def get_trivia(self) -> Dict:
        """Get a random trivia question"""
        try:
            trivia = random.choice(self.trivia)
            return {
                'success': True,
                'question': trivia['question'],
                'answer': trivia['answer'],
                'type': 'trivia'
            }
        except Exception as e:
            logger.error(f"Error getting trivia: {str(e)}")
            return {
                'success': False,
                'message': "Sorry, I couldn't get a trivia question right now."
            }

    def get_daily_content(self) -> Dict:
        """Get daily entertainment content (joke, fact, quote)"""
        try:
            # Use date as seed for consistent daily content
            today = datetime.now().strftime('%Y-%m-%d')
            random.seed(today)
            
            joke = random.choice(self.jokes)
            fact = random.choice(self.fun_facts)
            quote = random.choice(self.motivational_quotes)
            
            # Reset random seed
            random.seed()
            
            return {
                'success': True,
                'date': today,
                'joke': joke,
                'fun_fact': fact,
                'motivational_quote': quote,
                'type': 'daily_content'
            }
        except Exception as e:
            logger.error(f"Error getting daily content: {str(e)}")
            return {
                'success': False,
                'message': "Sorry, I couldn't get daily content right now."
            }

    def search_content(self, query: str, content_type: str = None) -> List[Dict]:
        """Search for specific content"""
        results = []
        query_lower = query.lower()
        
        try:
            # Search jokes
            if not content_type or content_type == 'joke':
                for joke in self.jokes:
                    if query_lower in joke.lower():
                        results.append({
                            'content': joke,
                            'type': 'joke',
                            'relevance': joke.lower().count(query_lower)
                        })
            
            # Search fun facts
            if not content_type or content_type == 'fact':
                for fact in self.fun_facts:
                    if query_lower in fact.lower():
                        results.append({
                            'content': fact,
                            'type': 'fun_fact',
                            'relevance': fact.lower().count(query_lower)
                        })
            
            # Search quotes
            if not content_type or content_type == 'quote':
                for quote in self.motivational_quotes:
                    if query_lower in quote.lower():
                        results.append({
                            'content': quote,
                            'type': 'motivational_quote',
                            'relevance': quote.lower().count(query_lower)
                        })
            
            # Sort by relevance
            results.sort(key=lambda x: x['relevance'], reverse=True)
            
            return results[:10]  # Return top 10 results
            
        except Exception as e:
            logger.error(f"Error searching content: {str(e)}")
            return []

# Global instance
entertainment = EntertainmentProvider()

# Convenience functions
def get_joke(category: str = None) -> Dict:
    """Get a random joke"""
    return entertainment.get_joke(category)

def get_fun_fact(category: str = None) -> Dict:
    """Get a random fun fact"""
    return entertainment.get_fun_fact(category)

def get_motivational_quote(category: str = None) -> Dict:
    """Get a random motivational quote"""
    return entertainment.get_motivational_quote(category)

def get_riddle() -> Dict:
    """Get a random riddle"""
    return entertainment.get_riddle()

def get_trivia() -> Dict:
    """Get a random trivia question"""
    return entertainment.get_trivia()

def get_daily_content() -> Dict:
    """Get daily entertainment content"""
    return entertainment.get_daily_content()

# Example usage and testing
if __name__ == "__main__":
    print("Testing Entertainment Module:")
    print("=" * 50)
    
    # Test joke
    joke_result = get_joke()
    print(f"Joke: {joke_result}")
    print()
    
    # Test fun fact
    fact_result = get_fun_fact('science')
    print(f"Science Fact: {fact_result}")
    print()
    
    # Test motivational quote
    quote_result = get_motivational_quote('technology')
    print(f"Tech Quote: {quote_result}")
    print()
    
    # Test riddle
    riddle_result = get_riddle()
    print(f"Riddle: {riddle_result}")
    print()
    
    # Test daily content
    daily_result = get_daily_content()
    print(f"Daily Content: {daily_result}")
