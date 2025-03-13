from pydantic import BaseModel, Field
from agents import Agent, Runner
from typing import Dict, List, Optional
import asyncio


class Recipe(BaseModel):
    name: str
    ingredients: list[str]
    steps: list[str]
    prep_time: str
    cook_time: str
    servings: int


class NutritionalInfo(BaseModel):
    calories: int
    protein: float = Field(description="Protein in grams")
    carbs: float = Field(description="Carbohydrates in grams")
    fat: float = Field(description="Fat in grams")


class RecipeAnalysis(BaseModel):
    recipe: Recipe
    nutrition: NutritionalInfo
    difficulty_level: str
    cuisine_type: str
    dietary_tags: List[str]
    estimated_cost: str


# Specialized agents for different culinary tasks
recipe_extraction_agent = Agent(
    name="recipe_extraction_agent",
    instructions="Extract detailed recipe information from text, including name, ingredients, steps, preparation time, cooking time, and number of servings.",
    output_type=Recipe,
)

nutrition_analysis_agent = Agent(
    name="nutrition_analysis_agent",
    instructions="Calculate detailed nutritional information based on recipe ingredients, including calories, protein, carbs, and fat content.",
    output_type=NutritionalInfo,
)

recipe_analysis_agent = Agent(
    name="recipe_analysis_agent",
    instructions="""
    Analyze recipes to determine difficulty level, cuisine type, dietary considerations, and estimated cost.
    Provide a comprehensive evaluation of the recipe's characteristics.
    """,
    output_type=RecipeAnalysis,
)

# Culinary orchestrator agent that delegates to specialized agents
culinary_orchestrator = Agent(
    name="culinary_orchestrator",
    instructions="""
    You are a culinary management system that determines which specialized agent should handle a food-related request.
    
    - For recipe extraction requests, delegate to the recipe_extraction_agent
    - For nutritional information requests, delegate to the nutrition_analysis_agent
    - For recipe analysis requests, delegate to the recipe_analysis_agent
    
    Ensure the request is routed to the most appropriate specialized agent.
    """,
    handoffs=[recipe_extraction_agent, nutrition_analysis_agent, recipe_analysis_agent],
)


async def process_culinary_request():
    """Process a culinary request using the orchestrator pattern with a detailed recipe."""
    detailed_recipe = """
    Recipe: Classic Spaghetti Bolognese
    Ingredients:
    - 200g spaghetti
    - 100g ground beef
    - 1 onion, finely chopped
    - 2 cloves garlic, minced
    - 400g canned tomatoes
    - 2 tbsp tomato paste
    - 1 carrot, diced
    - 1 celery stick, diced
    - Salt and pepper to taste
    - Olive oil for cooking
    Preparation Steps:
    1. Boil the spaghetti according to package instructions.
    2. In a pan, heat olive oil and sauté the onions, garlic, carrot, and celery until softened.
    3. Add the ground beef and cook until it is browned.
    4. Stir in the canned tomatoes and tomato paste; let it simmer for 15-20 minutes.
    5. Season with salt and pepper.
    Cooking Time: 30 minutes
    Preparation Time: 10 minutes
    Servings: 2
    """
    result = await Runner.run(starting_agent=culinary_orchestrator, input=detailed_recipe)
    return result.raw_responses , result.final_output


# Example usage
if __name__ == "__main__":
        result, output = asyncio.run(process_culinary_request())
        print(f"Result: {result}")
        print(f"Output: {output}")
