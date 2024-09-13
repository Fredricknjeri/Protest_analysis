import tweepy
import openai

# Set up your API keys here
TWITTER_API_KEY = "your-twitter-api-key"
TWITTER_API_SECRET = "your-twitter-api-secret"
TWITTER_ACCESS_TOKEN = "your-twitter-access-token"
TWITTER_ACCESS_TOKEN_SECRET = "your-twitter-access-token-secret"
TWITTER_BEARER_TOKEN = "your-bearer-token"

# Set up OpenAI API key
OPENAI_API_KEY = "your-openai-api-key"
openai.api_key = OPENAI_API_KEY

# Define the Twitter stream class
class MyStream(tweepy.StreamingClient):
    
    def on_tweet(self, tweet):
        tweet_text = tweet.text
        print(f"New tweet found: {tweet_text}")
        
        # Check if the tweet contains the word "protest"
        if "protest" in tweet_text.lower():
            print(f"Tweet contains 'protest': {tweet_text}")
            
            # Analyze the tweet with OpenAI GPT-3 API
            analysis = analyze_tweet(tweet_text)
            print(f"Analysis: {analysis}")
        
    def on_error(self, status_code):
        if status_code == 420:
            print("Rate limit reached. Disconnected.")
            return False

def analyze_tweet(tweet_text):
    """
    Function to analyze a tweet using OpenAI GPT API.
    """
    prompt = f"""
    You are an AI trained for real-time crisis response. Analyze the following tweet and determine:
    1. Is this tweet reporting a protest or urgent situation in Nairobi?
    2. If yes, what action is required?
    
    Tweet: "{tweet_text}"
    """

    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=100,
            temperature=0.7,
        )

        return response.choices[0].text.strip()
    except Exception as e:
        return f"Error analyzing tweet: {e}"

# Create the stream and start it
def create_stream():
    stream = MyStream(bearer_token=TWITTER_BEARER_TOKEN)
    
    # Add rules to filter tweets containing the word "protest" in the Nairobi area
    # Delete any existing rules (optional)
    existing_rules = stream.get_rules().data
    if existing_rules is not None:
        rule_ids = [rule.id for rule in existing_rules]
        stream.delete_rules(rule_ids)
    
    # Add a rule to track "protest" in tweets
    stream.add_rules(tweepy.StreamRule("protest"))

    # Start streaming tweets (Nairobi coordinates: [36.605, -1.328, 37.065, -1.068])
    stream.filter(tweet_fields=["text"], expansions="geo.place_id")

if __name__ == "__main__":
    print("Starting Twitter stream for real-time protest analysis in Nairobi...")
    create_stream()
