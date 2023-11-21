
from chatbot_model import respond_to_text, create_chatbot_model

# creation of models should be outside the loop due to computational efficiency
encoder_model, decoder_model = create_chatbot_model()

while True:
    input_text = input("You: ")
    output_text = respond_to_text(input_text, encoder_model, decoder_model)
    print("Bot: ", output_text)