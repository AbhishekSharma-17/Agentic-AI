import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize the client
client = OpenAI()

# ============================================================
# EXAMPLE 1: Basic Streaming for Chat Completions
# ============================================================
def basic_chat_streaming():
    """
    Demonstrates the most basic way to stream chat completions
    """
    print("=== BASIC CHAT STREAMING ===")
    
    # Make a streaming request
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": "Write a short poem about coding"}],
        stream=True
    )
    
    # Process the streaming response
    for chunk in response:
        if chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end="", flush=True)
    print("\n")

# ============================================================
# EXAMPLE 2: Streaming with the Responses API
# ============================================================
def responses_api_streaming():
    """
    Demonstrates streaming with the Responses API (more modern approach)
    """
    print("=== RESPONSES API STREAMING ===")
    
    response = client.responses.create(
        model="gpt-4o",
        input=[{
            "role": "user",
            "content": [
                {"type": "input_text", "text": "Write a short poem about coding"},
            ]
        }],
        stream=True
    )
    
    # Process the streaming response
    for event in response:
        if hasattr(event, 'delta') and event.delta.text:
            print(event.delta.text, end="", flush=True)
        # For handling different event types
        elif event.type == "stream_end":
            print("\n[Stream ended]")
    print("\n")

# ============================================================
# EXAMPLE 3: Streaming with Async/Await
# ============================================================
async def async_streaming():
    """
    Demonstrates how to use streaming with async/await
    """
    print("=== ASYNC STREAMING ===")
    
    from openai import AsyncOpenAI
    
    # Create async client
    async_client = AsyncOpenAI()
    
    # Make an async streaming request
    response = await async_client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": "Write a short poem about coding"}],
        stream=True
    )
    
    # Process the streaming response asynchronously
    async for chunk in response:
        if chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end="", flush=True)
    print("\n")

# ============================================================
# EXAMPLE 4: Streaming with Web/UI Integration
# ============================================================
def web_ui_streaming_example():
    """
    Pseudo-code example showing how to integrate streaming with a web UI
    """
    print("=== WEB UI STREAMING (PSEUDOCODE) ===")
    
    print("""
# In a Flask/FastAPI app:

@app.route('/stream')
def stream_response():
    # Set up streaming response headers
    def generate():
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": request.args.get('prompt')}],
            stream=True
        )
        
        for chunk in response:
            if chunk.choices[0].delta.content:
                yield f"data: {chunk.choices[0].delta.content}\\n\\n"
        yield "data: [DONE]\\n\\n"
    
    return Response(generate(), mimetype='text/event-stream')

# In JavaScript:
const eventSource = new EventSource('/stream?prompt=your_prompt_here');
eventSource.onmessage = function(event) {
    if (event.data === '[DONE]') {
        eventSource.close();
    } else {
        // Append the text to your UI
        document.getElementById('response').innerHTML += event.data;
    }
};
    """)
    print("\n")

# ============================================================
# EXAMPLE 5: Streaming with Custom Processing
# ============================================================
def streaming_with_processing():
    """
    Shows how to process streaming chunks while building a complete response
    """
    print("=== STREAMING WITH PROCESSING ===")
    
    # Initialize containers for tracking
    complete_response = ""
    word_count = 0
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": "Write a short poem about coding"}],
        stream=True
    )
    
    print("Processing stream: ", end="")
    
    for chunk in response:
        if chunk.choices[0].delta.content:
            content = chunk.choices[0].delta.content
            complete_response += content
            print(content, end="", flush=True)
            
            # Count words in this chunk
            new_words = len(content.split())
            if new_words > 0:
                word_count += new_words
    
    print(f"\n\nStats: {word_count} words, {len(complete_response)} characters\n")
    
    return complete_response

# ============================================================
# EXAMPLE 6: Streaming Vision API with Image Input
# ============================================================
def vision_streaming():
    """
    Example of streaming with vision API and image input
    """
    print("=== VISION API STREAMING ===")
    
    import base64
    
    # Function to encode the image
    def encode_image(image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    
    # Path to your image
    image_path = "Openai_vision/tesco-shopping-receipt-CNTYDX.jpg"
    
    # Getting the base64 string
    base64_image = encode_image(image_path)
    
    # Creating the data URL
    image_url = f"data:image/jpeg;base64,{base64_image}"
    
    response = client.responses.create(
        model="gpt-4o",
        input=[{
            "role": "user",
            "content": [
                {"type": "input_text", "text": "Describe what you see in this image"},
                {
                    "type": "input_image",
                    "image_url": image_url,
                },
            ],
                
        }],
        stream=True
    )
    
    print("Processing vision stream: ", end="")
    
    for event in response:
        # Different handling for Responses API
        if hasattr(event, 'delta') and event.delta.text:
            print(event.delta.text, end="", flush=True)
    
    print("\n")

# ============================================================
# EXAMPLE 7: Handling Streaming Errors
# ============================================================
def error_handling_streaming():
    """
    Shows how to handle errors in streaming responses
    """
    print("=== ERROR HANDLING IN STREAMING ===")
    
    try:
        # Deliberately causing an error with an invalid model
        response = client.chat.completions.create(
            model="invalid-model-name",
            messages=[{"role": "user", "content": "This will cause an error"}],
            stream=True
        )
        
        for chunk in response:
            if chunk.choices[0].delta.content:
                print(chunk.choices[0].delta.content, end="")
                
    except Exception as e:
        print(f"Caught an error: {str(e)}")
        # Implement proper error handling based on the type of error
        
        # For API errors
        if hasattr(e, 'status_code'):
            if e.status_code == 429:
                print("Rate limit exceeded. Please try again later.")
            elif e.status_code == 401:
                print("Authentication error. Check your API key.")
            else:
                print(f"API Error: Status {e.status_code}")
    
    print("\n")

# ============================================================
# Run the examples
# ============================================================

if __name__ == "__main__":
    print("OpenAI API Streaming Examples\n")
    print("Choose an example to run:")
    print("1. Basic Chat Streaming")
    print("2. Responses API Streaming")
    print("3. Async Streaming (requires running in an async context)")
    print("4. Web/UI Integration Example (pseudocode)")
    print("5. Streaming with Custom Processing")
    print("6. Vision API Streaming")
    print("7. Error Handling in Streaming")
    print("8. Run All Examples (except async)")
    
    choice = input("\nEnter your choice (1-8): ")
    
    if choice == '1':
        basic_chat_streaming()
    elif choice == '2':
        responses_api_streaming()
    elif choice == '3':
        print("Async example needs to be run in an async context.")
        print("To run it, you would need to use:")
        print("```")
        print("import asyncio")
        print("asyncio.run(async_streaming())")
        print("```")
    elif choice == '4':
        web_ui_streaming_example()
    elif choice == '5':
        streaming_with_processing()
    elif choice == '6':
        vision_streaming()
    elif choice == '7':
        error_handling_streaming()
    elif choice == '8':
        basic_chat_streaming()
        responses_api_streaming()
        web_ui_streaming_example()
        streaming_with_processing()
        vision_streaming()
        error_handling_streaming()
    else:
        print("Invalid choice")
