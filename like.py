import json
with open('model/required_data.json', 'r', encoding='utf-8') as f:
    required_data = json.load(f)

num_decoder_tokens = required_data['num_decoder_tokens']
max_decoder_seq_length = required_data['max_decoder_seq_length']
latent_dim = required_data['latent_dim']
input_token_index = required_data['input_token_index']
target_token_index = required_data['target_token_index']
reverse_target_char_index = required_data['reverse_target_char_index']

for i in range(len(reverse_target_char_index)):
    print(reverse_target_char_index[str(i)], end="")