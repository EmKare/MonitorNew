

# Import the library
from lorem_text import lorem

# Generate a sentence
sentence = lorem.sentence()

# Generate a paragraph
paragraph = lorem.paragraph()

# Generate multiple paragraphs
paragraphs = lorem.paragraphs(3)  # Generate 3 paragraphs

# Generate a specific number of words
words = lorem.words(10)  # Generate 10 words

print(sentence)
print(paragraph)
print(paragraphs)
print(words)