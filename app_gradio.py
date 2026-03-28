import random
import os
import gradio as gr

# Use local model cache so the pre-downloaded model is found in production
os.environ.setdefault('SENTENCE_TRANSFORMERS_HOME', './model_cache')

from sentence_transformers import SentenceTransformer, util

# =====================
# CHATBOT CLASS WITH EMBEDDINGS
# =====================
class Chatbot:

    def __init__(self):
        self.intents_responses = {}
        self.patterns = {}
        self.intents = []

        # Load intents and precompute embeddings
        self._load_intents()

        # Load sentence-transformer model
        self.embed_model = SentenceTransformer('all-MiniLM-L6-v2')

        # Precompute embeddings for all patterns per intent
        self.intent_embeddings = {}
        for tag, patterns_list in self.patterns.items():
            self.intent_embeddings[tag] = self.embed_model.encode(patterns_list, convert_to_tensor=True)

    def _load_intents(self):
        intents_data = {
            "intents": [
                {
                    "tag": "greeting",
                    "patterns": [
                        "hi",
                        "hello",
                        "hey",
                        "good morning",
                        "good afternoon",
                        "good evening"
                    ],
                    "responses": [
                        "Hello! I can help with business questions."
                    ]
                },
                {
                    "tag": "startup_steps",
                    "patterns": [
                        "how to start a business",
                        "steps to start a company",
                        "startup process",
                        "new business formation",
                        "launching a startup",
                        "first steps for a business",
                        "create a new company"
                    ],
                    "responses": [
                        "Starting a business involves several key steps: market research, business planning, securing funding, legal registration, and developing your product/service.",
                        "Key steps include defining your business idea, conducting market research, writing a business plan, finding funding, choosing a legal structure, registering your business, and building your team."
                    ]
                },
                {
                    "tag": "business_plan",
                    "patterns": [
                        "what is a business plan",
                        "create a business plan",
                        "components of a business plan",
                        "why do I need a business plan",
                        "business plan outline",
                        "how to write a business plan",
                        "importance of business planning"
                    ],
                    "responses": [
                        "A business plan is a formal document outlining a company's goals, strategies, marketing and sales plans, and financial forecasts. It serves as a roadmap for the business.",
                        "It typically includes an executive summary, company description, market analysis, organization and management, service or product line, marketing and sales strategy, funding request, and financial projections."
                    ]
                },
                {
                    "tag": "funding",
                    "patterns": [
                        "how to get funding for a startup",
                        "startup funding options",
                        "raise capital",
                        "sources of business funding",
                        "venture capital",
                        "angel investors",
                        "bootstrapping",
                        "small business loans",
                        "seed funding",
                        "funding for new business"
                    ],
                    "responses": [
                        "Funding options for startups include bootstrapping, angel investors, venture capital, crowdfunding, and small business loans.",
                        "The best funding source depends on your business stage, capital needs, and growth potential."
                    ]
                },
                {
                    "tag": "idea_validation",
                    "patterns": [
                        "validate business idea",
                        "test startup idea",
                        "is my idea good"
                    ],
                    "responses": [
                        "Validate your idea by researching demand, testing with customers, and building a prototype."
                    ]
                },
                {
                    "tag": "minimum_viable_product",
                    "patterns": [
                        "what is MVP",
                        "build MVP",
                        "minimum viable product meaning"
                    ],
                    "responses": [
                        "An MVP is a simple version of your product used to test demand."
                    ]
                },
                {
                    "tag": "finding_customers",
                    "patterns": [
                        "how to get customers",
                        "find customers",
                        "first customers startup"
                    ],
                    "responses": [
                        "Find customers through marketing, networking, and online platforms."
                    ]
                },
                {
                    "tag": "marketing_strategy",
                    "patterns": [
                        "marketing strategy",
                        "promote company"
                    ],
                    "responses": [
                        "Marketing strategy involves targeting the right audience and promoting value."
                    ]
                },
                {
                    "tag": "digital_marketing",
                    "patterns": [
                        "digital marketing",
                        "online marketing",
                        "SEO marketing"
                    ],
                    "responses": [
                        "Digital marketing promotes businesses online using SEO, ads, and social media."
                    ]
                },
                {
                    "tag": "sales_strategy",
                    "patterns": [
                        "sales strategy",
                        "increase sales",
                        "sell more products"
                    ],
                    "responses": [
                        "Sales increase by understanding customers and providing value."
                    ]
                },
                {
                    "tag": "pricing_strategy",
                    "patterns": [
                        "price product",
                        "pricing strategy",
                        "set price"
                    ],
                    "responses": [
                        "Pricing depends on costs, competitors, and customer value."
                    ]
                },
                {
                    "tag": "branding",
                    "patterns": [
                        "branding",
                        "build brand",
                        "brand identity"
                    ],
                    "responses": [
                        "Branding shapes how customers see your company."
                    ]
                },
                {
                    "tag": "profit",
                    "patterns": [
                        "what is profit",
                        "profit meaning"
                    ],
                    "responses": [
                        "Profit is revenue minus expenses."
                    ]
                },
                {
                    "tag": "revenue",
                    "patterns": [
                        "what is revenue",
                        "revenue meaning"
                    ],
                    "responses": [
                        "Revenue is total income from sales."
                    ]
                },
                {
                    "tag": "expenses",
                    "patterns": [
                        "business expenses",
                        "company costs"
                    ],
                    "responses": [
                        "Expenses are costs required to operate a business."
                    ]
                },
                {
                    "tag": "lean_startup",
                    "patterns": [
                        "what is lean startup",
                        "lean startup methodology",
                        "how to implement lean startup",
                        "lean startup process"
                    ],
                    "responses": [
                        "The Lean Startup methodology focuses on quickly developing products using iterative cycles, testing assumptions with minimal resources, and learning from customer feedback. It helps startups reduce risks and improve chances of success by avoiding wasted effort and building products that customers actually want."
                    ]
                },
                {
                    "tag": "crowdfunding",
                    "patterns": [
                        "how to crowdfund a project",
                        "crowdfunding platforms",
                        "raise money through crowdfunding",
                        "crowdfunding tips"
                    ],
                    "responses": [
                        "Crowdfunding is raising funds from a large number of people, usually via online platforms, to finance a business or project. It requires presenting a clear value proposition, creating engaging campaigns, and communicating effectively with backers to achieve funding goals."
                    ]
                },
                {
                    "tag": "business_analytics",
                    "patterns": [
                        "what is business analytics",
                        "how to analyze business data",
                        "data-driven decisions",
                        "business intelligence"
                    ],
                    "responses": [
                        "Business analytics uses data to inform business decisions, identify trends, and improve performance."
                    ]
                }
            ]
        }

        for intent in intents_data["intents"]:
            tag = intent["tag"]
            self.intents.append(tag)
            self.patterns[tag] = intent["patterns"]
            self.intents_responses[tag] = intent["responses"]

    def ask_llm(self, question):
        try:
            import requests
            url = "https://api.duckduckgo.com/"
            params = {
                "q": question,
                "format": "json"
            }
            response = requests.get(url, params=params).json()
            if response.get("AbstractText"):
                return response["AbstractText"]
            else:
                return "I searched the internet but couldn't find a clear answer."
        except:
            return "Internet connection required for this feature."

    def process_message(self, message):
        # Embed user message
        input_embedding = self.embed_model.encode(message, convert_to_tensor=True)

        # Compare with all intent patterns
        best_tag = None
        best_score = -1
        for tag, embeddings in self.intent_embeddings.items():
            # cosine similarity
            scores = util.cos_sim(input_embedding, embeddings)
            max_score = scores.max().item()
            if max_score > best_score:
                best_score = max_score
                best_tag = tag

        # If similarity is high enough, return a response
        if best_score >= 0.4:
            return random.choice(self.intents_responses[best_tag])
        else:
            # Fallback to internet or default answer
            return self.ask_llm(message)


# Initialize bot
bot = Chatbot()

# Create Gradio interface
def chat_interface(message):
    return bot.process_message(message)

# Create the interface for Hugging Face Spaces
demo = gr.Interface(
    fn=chat_interface,
    inputs="text",
    outputs="text",
    title="Business Chatbot",
    description="Ask me anything about starting and running a business!",
    examples=[
        ["What is a business plan?"],
        ["How to start a business?"],
        ["What is the lean startup methodology?"]
    ]
)

if __name__ == "__main__":
    demo.launch()
