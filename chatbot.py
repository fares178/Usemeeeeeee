import random
import os

# Use local model cache so the pre-downloaded model is found in production
os.environ.setdefault('SENTENCE_TRANSFORMERS_HOME', './model_cache')

from sentence_transformers import SentenceTransformer, util
from flask import Flask, render_template, request, jsonify

# Import for sentence-transformers


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
                        "Business analytics involves using data, statistical methods, and technology to analyze trends, identify patterns, and make informed decisions. It helps companies optimize operations, improve customer experience, and increase profitability through evidence-based insights."
                    ]
                },
                {
                    "tag": "supply_chain",
                    "patterns": [
                        "what is supply chain management",
                        "supply chain optimization",
                        "how to manage supply chain",
                        "supply chain process"
                    ],
                    "responses": [
                        "Supply chain management is the coordination of production, logistics, and distribution to ensure that products reach customers efficiently. Optimizing the supply chain reduces costs, improves delivery times, and increases overall business efficiency."
                    ]
                },
                {
                    "tag": "franchising",
                    "patterns": [
                        "how to start a franchise",
                        "franchise opportunities",
                        "buy a franchise",
                        "franchising business"
                    ],
                    "responses": [
                        "Franchising allows individuals to operate a business under an established brand using its products, systems, and support. Starting a franchise involves selecting a suitable brand, understanding legal agreements, training, and following the franchise model to ensure success."
                    ]
                },
                {
                    "tag": "corporate_social_responsibility",
                    "patterns": [
                        "what is corporate social responsibility",
                        "CSR in business",
                        "business social responsibility",
                        "ethical business practices"
                    ],
                    "responses": [
                        "Corporate social responsibility (CSR) is a business approach that focuses on creating positive social, environmental, and economic impact. Companies engage in CSR to improve community welfare, enhance brand reputation, and build sustainable long-term growth."
                    ]
                },
                {
                    "tag": "business_valuation",
                    "patterns": [
                        "how to value a business",
                        "business valuation methods",
                        "company worth",
                        "calculate business value"
                    ],
                    "responses": [
                        "Business valuation is the process of determining the economic value of a company. Methods include analyzing assets, revenue, market conditions, and future earning potential. Accurate valuation is crucial for investors, mergers, acquisitions, and funding."
                    ]
                },
                {
                    "tag": "pivoting",
                    "patterns": [
                        "what is business pivot",
                        "how to pivot a startup",
                        "changing business strategy",
                        "pivoting ideas"
                    ],
                    "responses": [
                        "Pivoting is when a business changes its strategy, product, or target market to adapt to customer needs or market conditions. A successful pivot requires analyzing feedback, identifying opportunities, and executing changes effectively to improve chances of success."
                    ]
                },
                {
                    "tag": "remote_work_management",
                    "patterns": [
                        "manage remote team",
                        "remote work strategies",
                        "virtual team management",
                        "working remotely"
                    ],
                    "responses": [
                        "Managing a remote team involves using technology to communicate, track progress, and maintain engagement. Key strategies include setting clear expectations, regular check-ins, collaboration tools, and fostering a culture of accountability and trust."
                    ]
                },
                {
                    "tag": "business_mentorship",
                    "patterns": [
                        "business mentor",
                        "how to find a mentor",
                        "mentorship benefits",
                        "startup mentorship"
                    ],
                    "responses": [
                        "Business mentorship connects entrepreneurs with experienced professionals who provide guidance, advice, and insights. Mentorship can help avoid common mistakes, accelerate learning, and provide valuable networking opportunities."
                    ]
                },
                {
                    "tag": "cash_flow",
                    "patterns": [
                        "cash flow",
                        "cash flow meaning"
                    ],
                    "responses": [
                        "Cash flow tracks money entering and leaving business."
                    ]
                },
                {
                    "tag": "break_even",
                    "patterns": [
                        "break even point",
                        "break even meaning"
                    ],
                    "responses": [
                        "Break-even is when revenue equals expenses."
                    ]
                },
                {
                    "tag": "competitive_advantage",
                    "patterns": [
                        "competitive advantage",
                        "beat competitors"
                    ],
                    "responses": [
                        "Competitive advantage makes your business unique."
                    ]
                },
                {
                    "tag": "scaling",
                    "patterns": [
                        "scale business",
                        "grow startup"
                    ],
                    "responses": [
                        "Scaling increases revenue while maintaining efficiency."
                    ]
                },
                {
                    "tag": "leadership",
                    "patterns": [
                        "leadership skills",
                        "be a leader"
                    ],
                    "responses": [
                        "Leadership involves guiding and motivating teams."
                    ]
                },
                {
                    "tag": "team_building",
                    "patterns": [
                        "build team",
                        "hire employees"
                    ],
                    "responses": [
                        "Hire skilled people aligned with your mission."
                    ]
                },
                {
                    "tag": "customer_service",
                    "patterns": [
                        "customer service",
                        "customer support"
                    ],
                    "responses": [
                        "Good service builds trust and loyalty."
                    ]
                },
                {
                    "tag": "negotiation",
                    "patterns": [
                        "negotiate deal",
                        "negotiation skills"
                    ],
                    "responses": [
                        "Negotiation helps achieve beneficial agreements."
                    ]
                },
                {
                    "tag": "risk_management",
                    "patterns": [
                        "business risks",
                        "manage risk"
                    ],
                    "responses": [
                        "Risk management minimizes losses."
                    ]
                },
                {
                    "tag": "ecommerce",
                    "patterns": [
                        "start ecommerce",
                        "online store"
                    ],
                    "responses": [
                        "Ecommerce sells products online."
                    ]
                },
                {
                    "tag": "passive_income",
                    "patterns": [
                        "passive income",
                        "earn passive income"
                    ],
                    "responses": [
                        "Passive income generates earnings automatically."
                    ]
                },
                {
                    "tag": "entrepreneurship",
                    "patterns": [
                        "entrepreneur meaning",
                        "what is entrepreneurship"
                    ],
                    "responses": [
                        "Entrepreneurship is creating and managing businesses."
                    ]
                },
                {
                    "tag": "business_ethics",
                    "patterns": [
                        "business ethics",
                        "ethical business"
                    ],
                    "responses": [
                        "Ethics ensure responsible business behavior."
                    ]
                },
                {
                    "tag": "time_management",
                    "patterns": [
                        "manage time",
                        "time management business"
                    ],
                    "responses": [
                        "Time management improves productivity."
                    ]
                },
                {
                    "tag": "productivity",
                    "patterns": [
                        "increase productivity",
                        "work efficiency"
                    ],
                    "responses": [
                        "Productivity improves through planning and focus."
                    ]
                },
                {
                    "tag": "networking",
                    "patterns": [
                        "business networking",
                        "professional networking"
                    ],
                    "responses": [
                        "Networking builds relationships and opportunities."
                    ]
                },
                {
                    "tag": "innovation",
                    "patterns": [
                        "business innovation",
                        "innovative ideas"
                    ],
                    "responses": [
                        "Innovation creates competitive advantage."
                    ]
                },
                {
                    "tag": "decision_making",
                    "patterns": [
                        "business decisions",
                        "decision making"
                    ],
                    "responses": [
                        "Good decisions rely on data and analysis."
                    ]
                },
                {
                    "tag": "customer_retention",
                    "patterns": [
                        "retain customers",
                        "customer loyalty"
                    ],
                    "responses": [
                        "Retention builds long-term success."
                    ]
                },
                {
                    "tag": "market_research",
                    "patterns": [
                        "market research",
                        "study market"
                    ],
                    "responses": [
                        "Market research helps understand customers."
                    ]
                },
                {
                    "tag": "marketing",
                    "patterns": [
                        "what is marketing",
                        "marketing strategies",

                        "how to market my product",
                        "tell me about marketing"
                    ],
                    "responses": [
                        "Marketing helps businesses attract customers."
                    ]
                },
                {
                    "tag": "finance",
                    "patterns": [
                        "what is profit",
                        "what is revenue",
                        "finance basics",
                        "explain financial terms",
                        "how does finance work"
                    ],
                    "responses": [
                        "Profit = revenue - expenses."
                    ]
                },
                {
                    "tag": "sales",
                    "patterns": [
                        "increase sales",
                        "sales techniques",
                        "how to sell more",
                        "boosting sales",
                        "grow sales"
                    ],
                    "responses": [
                        "Understand customer needs to increase sales."
                    ]
                },
                {
                    "tag": "operations",
                    "patterns": [
                        "manage operations",
                        "logistics",
                        "supply chain management",
                        "operational efficiency",
                        "how to run operations"
                    ],
                    "responses": [
                        "Operations management focuses on efficiency in production and delivery.",
                        "Logistics is key to a smooth supply chain."
                    ]
                },
                {
                    "tag": "customer_service",
                    "patterns": [
                        "customer support",
                        "handle complaints",
                        "customer satisfaction",
                        "how to improve customer service",
                        "dealing with customers"
                    ],
                    "responses": [
                        "Good customer service builds loyalty.",
                        "Resolving complaints promptly is essential for customer satisfaction."
                    ]
                },
                {
                    "tag": "human_resources",
                    "patterns": [
                        "HR questions",
                        "human resources",
                        "staffing",
                        "recruitment",
                        "employee management",
                        "what is HR"
                    ],
                    "responses": [
                        "Human Resources manages employee relations, recruitment, and benefits.",
                        "Effective staffing is crucial for business success."
                    ]
                },
                {
                    "tag": "product_development",
                    "patterns": [
                        "new product ideas",
                        "product design",
                        "development cycle",
                        "innovation",
                        "how to develop a product",
                        "product innovation"
                    ],
                    "responses": [
                        "Product development involves ideation, design, and launch of new products.",
                        "Innovation is key to staying competitive in product development."
                    ]
                },
                {
  "tag": "business_definition",
  "patterns": [
    "What is a business?",
    "Define business",
    "Business meaning",
    "Explain business",
    "What does business mean?"
  ],
  "responses": [
    "A business is an organization that provides goods or services to customers in exchange for money. Its main aim is usually to earn profit while satisfying customer needs."
  ]
},
                {
  "tag": "business_purpose",
  "patterns": [
    "What is the purpose of a business?",
    "Why do businesses exist?",
    "What is the goal of a business?",
    "Business objective"
  ],
  "responses": [
    "The purpose of a business is to provide goods or services that meet customer needs while generating profit and contributing to the economy."
  ]
},
                {
  "tag": "business_profit",
  "patterns": [
    "How do businesses make money?",
    "How does a business earn profit?",
    "How do companies make money?",
    "Where does business money come from?"
  ],
  "responses": [
    "Businesses make money by selling products or services. They earn revenue from customers and make profit after subtracting costs and expenses."
  ]
},
         {
  "tag": "business_success",
  "patterns": [
    "What makes a business successful?",
    "How can a business succeed?",
    "What makes companies successful?",
    "How do businesses become successful?"
  ],
  "responses": [
    "A business becomes successful by understanding customers, offering quality products, managing costs effectively, marketing properly, and continuously improving."
  ]
},
                {
  "tag": "business_how_it_works",
  "patterns": [
    "How does a business work?",
    "How does business operate?",
    "How do businesses operate?"
  ],
  "responses": [
    "A business works by identifying a need, creating a product or service to meet that need, marketing it to customers, selling it, and managing revenue and costs to generate profit."
  ]
},
                {
                  "intents": [
                    {
                      "intent": "what_is_cashier",
                      "examples": [
                        "What is a cashier?",
                        "Who is a cashier?",
                        "Explain cashier role"
                      ],
                      "responses": [
                        "A cashier is someone who handles payments, gives change, and helps customers complete purchases."
                      ]
                    },
                    {
                      "intent": "greet_customer",
                      "examples": [
                        "How should I greet a customer?",
                        "What is the proper way to welcome a customer?",
                        "Customer greeting tips"
                      ],
                      "responses": [
                        "Smile and say, 'Hello! How can I help you today?' Friendly greetings improve customer experience."
                      ]
                    },
                    {
                      "intent": "handle_cash",
                      "examples": [
                        "How do I handle cash?",
                        "Cash handling procedure",
                        "Counting money tips"
                      ],
                      "responses": [
                        "Count bills carefully, check coins, give exact change, and keep the cash drawer organized."
                      ]
                    },
                    {
                      "intent": "use_cash_register",
                      "examples": [
                        "How do I use a cash register?",
                        "Cash register steps",
                        "Operating the register"
                      ],
                      "responses": [
                        "Scan or enter items, calculate the total, accept payment, give change if needed, and issue a receipt."
                      ]
                    },
                    {
                      "intent": "train_new_employee",
                      "examples": [
                        "How do I train new employees?",
                        "Employee training steps",
                        "Teach new staff"
                      ],
                      "responses": [
                        "Explain their role clearly, demonstrate tasks step by step, supervise practice, and give feedback."
                      ]
                    },
                    {
                      "intent": "effective_training",
                      "examples": [
                        "How do I make training effective?",
                        "Tips for training employees",
                        "Employee training advice"
                      ],
                      "responses": [
                        "Use clear instructions, hands-on practice, examples, and regular feedback."
                      ]
                    },
                    {
                      "intent": "check_training_understanding",
                      "examples": [
                        "How do I check if employees understand?",
                        "Testing employee knowledge",
                        "How to see if training worked"
                      ],
                      "responses": [
                        "Ask them to perform tasks, quiz them on procedures, and observe their work."
                      ]
                    },
                    {
                      "intent": "train_cash_handling",
                      "examples": [
                        "How do I train employees to handle cash?",
                        "Cashier training tips",
                        "Teach money handling"
                      ],
                      "responses": [
                        "Show proper counting, giving change, organizing the register, and reconciling at the end of the shift."
                      ]
                    },
                    {
                      "intent": "train_customer_service",
                      "examples": [
                        "How do I train employees to handle customers?",
                        "Customer service training",
                        "Teaching customer interaction"
                      ],
                      "responses": [
                        "Teach polite greetings, active listening, problem-solving, and how to stay calm in difficult situations."
                      ]
                    },
                    {
                      "intent": "handle_training_difficulty",
                      "examples": [
                        "What if employees struggle during training?",
                        "Difficult employee training",
                        "Help employees who are struggling"
                      ],
                      "responses": [
                        "Be patient, give extra guidance, repeat instructions, and provide supportive feedback."
                      ]
                    },
                    {
                      "intent": "ongoing_training",
                      "examples": [
                        "How do I make ongoing training?",
                        "Continuous employee training",
                        "Regular training tips"
                      ],
                      "responses": [
                        "Schedule regular refreshers, update employees on new procedures, and encourage learning new skills."
                      ]
                    },
                    {
                      "intent": "prevent_register_discrepancy",
                      "examples": [
                        "How do I prevent mistakes or theft?",
                        "Avoid cash register errors",
                        "Manage cash properly"
                      ],
                      "responses": [
                        "Train the cashier properly, supervise when needed, and enforce strict cash-handling rules."
                      ]
                    },
                    {
                      "intent": "manage_cashier",
                      "examples": [
                        "How do I manage a cashier effectively?",
                        "Tips for managing cashiers",
                        "Supervise cashier"
                      ],
                      "responses": [
                        "Monitor their work, ensure they follow cash handling procedures, provide training, and check the register regularly."
                      ]
                    }
                  ]
                },

                {
                    "tag": "mange cashier",
                    "patterns": [
                        "how to manage cashier"

                    ],
                    "responses": [
                        "Monitor their work, ensure they follow cash handling procedures, provide training, and check the register regularly."
                    ]
                },

                {
                    "tag": "online business",
                    "patterns": [
                        "What is an online business?"

                    ],
                    "responses": [
                        "An online business operates on the internet, selling products or services through websites or apps."
                    ]
                },

                {
                    "tag": "risks",
                    "patterns": [
                        "what are some risks of making a business",
                        "What are the risks of starting a business?"

                    ],
                    "responses": [
                        "Risks include losing money, strong competition, low demand, and unexpected problems."
                    ]
                },
                {
                    "tag": "fall",
                    "patterns": [
                        "Why do some businesses fail?",
                        "how does businesses fall"
                        
                    ],
                    "responses": [
                        "Common reasons include poor planning, lack of customers, bad management, or not adapting to changes."
                    ]
                },

                {
                    "tag": "thanks giving",
                    "patterns": [
                        "thank you",
                        "thanks",
                        "i am gratful"
                    ],
                    "responses": [
                        "You’re welcome! If you need anything just tell me 👍"
                    ]
                },

                {
                    "tag": "ending",
                    "patterns": [
                        "bye",
                        "goodbye",
                        "see you"
                    ],
                    "responses": [
                        "Goodbye!"
                    ]
                }
            ]
        }

        for intent in intents_data["intents"]:
            if "tag" not in intent:
                continue
            tag = intent["tag"]
            self.intents.append(tag)
            self.patterns[tag] = intent["patterns"]
            self.intents_responses[tag] = intent["responses"]

    # =====================
    # INTERNET FALLBACK
    # =====================
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
        if best_score >= 0.4:  # Adjusted threshold from 0.5 to 0.4
            return random.choice(self.intents_responses[best_tag])
        else:
            # Fallback to internet or default answer
            return self.ask_llm(message)

app = Flask(__name__, template_folder='templates')

# Eagerly initialize at startup — model is cached from the build step
bot_assistant = Chatbot()

# Serve all pages
@app.route('/')
def index_root():
    return render_template('index.html')

@app.route('/index.html')
def index_html():
    return render_template('index.html')

@app.route('/about.html')
def about():
    return render_template('about.html')

@app.route('/settings.html')
def settings():
    return render_template('settings.html')

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")
    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    response = bot_assistant.process_message(user_message)
    return jsonify({"response": response})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port)
app = Flask(__name__)
bot = Chatbot()

@app.route("/")
def index():
    return render_template("chatbot.html")

@app.route("/get")
def get_bot_response():
    user_text = request.args.get('msg')
    # This calls your chatbot's logic to find the best match
    return str(bot.get_response(user_text))

if __name__ == "__main__":
    app.run(debug=True)
    
