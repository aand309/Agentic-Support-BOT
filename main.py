

from src.bot import SupportBotAgent

def run_bot():
    """
    Initializes and runs the SupportBotAgent.
    """
    # Path to the document the bot will train on
    document_path = "data/faq.txt"

    # Initialize the agent
    bot = SupportBotAgent(document_path=document_path)

    # Define sample queries to test the bot
    sample_queries = [
        "How can I reset my password?",
        "What is the refund policy?",
        "How do I contact customer support?",
        "How do I fly to the moon?" # Out-of-scope query
    ]

    # Run the bot with the sample queries
    bot.run(queries=sample_queries)

if __name__ == "__main__":
    run_bot()