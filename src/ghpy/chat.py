import os
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from colorama import Fore, Style, init


# load environment variables
load_dotenv()

# initialize chat model (Azure)
llm = AzureChatOpenAI(
    #api_keys=os.getenv("AZURE_OPENAI_API_KEY"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    azure_deployment=os.getenv("AZURE_DEPLOYMENT_NAME"),
    api_version=os.getenv("API_VERSION"),
    temperature=0.5
)

# parser initialize
parser = StrOutputParser()


# recipe generation prompt template
recipe_prompt = ChatPromptTemplate.from_template(
    """
        You are a dietary expert specializing in gut health. Based on the following details:
        Gut Issues: {gut_issues}
        Food Preferences: {food_preferences}
        ingredients: {ingredients}

        Generate a recipe that addresses the gut issues and food preferences, and uses the provided ingredients.
        Include preparation instructions, cooking time, and explain how the recipe supports gut health.
    """
)

def get_user_data(promt):
    return input(promt).strip()

def print_colored_message(message, color=Fore.WHITE):
    print(f"{color}{message}{Style.RESET_ALL}")

def save_recipe(gut_issues, recipe):
    filename = f"{gut_issues.replace(' ', '_')}_recipe.txt"
    with open(filename, 'w') as file:
        file.write(recipe)
    print_colored_message(f"{Fore.LIGHTGREEN_EX}Recipe saved to {filename}{Style.BRIGHT}")

def main():
    print(f"{Fore.WHITE}----- Welcome to the Gut Health Recipe Recommendation ------{Style.BRIGHT}\n")

    # collect user's gut issues
    print_colored_message(f"{Fore.YELLOW}What gut issues are you experiencing (e.g., bloating, IBS, acidity)?{Style.RESET_ALL}")
    gut_issues = input(f"{Fore.CYAN}Your Answer: {Style.RESET_ALL}")

    # collect user's food preferences or dietery restrcitions
    print_colored_message(f"{Fore.YELLOW}Do you have any food preferences or dietery restrictions (e.g, vegan, gluten-free)?{Style.RESET_ALL}")
    food_preferences = input(f"{Fore.CYAN}Your Answer: {Style.RESET_ALL}")

    # collect user's available ingredients
    print_colored_message(f"{Fore.YELLOW}What ingredients do you have on hand?{Style.RESET_ALL}")
    ingredients = input(f"{Fore.CYAN}Your Answer: {Style.RESET_ALL}")

    # crteat prompt from user inputs
    prompt = recipe_prompt.format_messages(
        gut_issues = gut_issues,
        food_preferences = food_preferences,
        ingredients = ingredients
    )

    # retrieve recipe from model
    response = llm.invoke(prompt)

    # parse the response
    recipe = parser.invoke(response)

    # WE CAN USE | chaining too -> recipe = prompt | llm | parser and recipe.invoke()

    print(f"\n{Fore.GREEN}{recipe}{Style.RESET_ALL}")

    save_recipe(gut_issues=gut_issues,recipe=recipe)

if __name__ == "__main__":
    main()

