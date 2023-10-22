import re

def preprocess(text):
    """Changes text to lowercase, removes special characters/punctuation."""
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)
    return text

def get_trigram_model(text):
    """Creates a probability matrix for known trigrams and its next character without wrap-around."""
    text = preprocess(text)
    probabilities = {}

    # Make list of all text indices as groups of 3 characters.
    trigram_indices = [(i, i+1, i+2) for i in range(len(text)-2) if i+2 < len(text) - 1]

    # Build dictionary of trigrams and their next character and count.
    for tri_indices in trigram_indices:
        i, j, k = tri_indices
        next_char = text[k+1]
        trigram = text[i] + text[j] + text[k]
        if trigram in probabilities:
            if next_char not in probabilities[trigram]:
                probabilities[trigram][next_char] = 0
            probabilities[trigram][next_char] += 1
        else:
            probabilities[trigram] = { next_char: 1 }
    
    # Convert counts to probabilities.
    for trigram in probabilities:
        total = sum(probabilities[trigram].values())
        for next_char in probabilities[trigram]:
            probabilities[trigram][next_char] /= total
    
    return probabilities

def infer(text, model, iterations=1):
    """Use probability matrix to infer next character similar to a 1D automata."""
    text = preprocess(text)
    text += " " # Add a space to the end of the text to wrap around.
    iteration_list = []
    
    for _ in range(iterations):
        new_text = text[:2]  # Preserve the first two characters
        for i in range(len(text) - 3): # Adjusted loop range to avoid out-of-index errors
            trigram = text[i:i+3]
            if trigram in model:
                new_text += max(model[trigram], key=model[trigram].get)
            else:
                new_text += " "
        new_text += text[-1]  # Preserve the last character
        iteration_list.append(new_text)
        text = new_text

    return iteration_list

def levenshtein_distance(s1, s2):
    """Calculate the Levenshtein distance between two strings."""
    if len(s1) > len(s2):
        s1, s2 = s2, s1

    distances = range(len(s1) + 1)
    for i2, c2 in enumerate(s2):
        distances_ = [i2+1]
        for i1, c1 in enumerate(s1):
            if c1 == c2:
                distances_.append(distances[i1])
            else:
                distances_.append(1 + min((distances[i1], distances[i1 + 1], distances_[-1])))
        distances = distances_
    return distances[-1]

def weighted_average(distances, weights):
    """Calculate the weighted average of the Levenshtein distances."""
    return sum(w * d for w, d in zip(weights, distances)) / len(distances)

def deviation_scores(scores):
    """Calculate the deviation scores."""
    mean = sum(scores) / len(scores)
    variance = sum((x - mean) ** 2 for x in scores) / len(scores)
    std_dev = variance ** 0.5
    return [((x - mean) / std_dev) for x in scores]