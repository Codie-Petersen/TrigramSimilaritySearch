from trigram.utils import get_trigram_model, infer, levenshtein_distance, weighted_average, deviation_scores
from typing import Dict
import json
import uuid

class Entry:
    """Entry class for the trigram database."""
    def __init__(self, data: str):
        self.data = data
        self.trigram_model = get_trigram_model(data)
    
    def compare(self, text: str, iterations: int = 5):
        """Use the trigram model to get the levenshtein distance for the given text."""
        text_iterations = infer(text, self.trigram_model, iterations=iterations)
        distances = [levenshtein_distance(text_iterations[i], text_iterations[i+1]) for i in range(len(text_iterations)-1)]
        score = weighted_average(distances, [0.5, 0.25, 0.125, 0.075, 0.05])
        return score

class TrigramVDB:

    def __init__(self, save_path, iterations=5, weights=[0.5, 0.25, 0.125, 0.075, 0.05]):
        self.save_path = save_path
        self.iterations = iterations
        self.weights = weights
        self.entries: Dict[str, Entry] = {}
    
    def add(self, data: str):
        """Add a new entry to the database."""
        try:
            entry = Entry(data)
            key = str(uuid.uuid4())
            self.entries[key] = entry
        except Exception as e:
            raise Exception(f"Error adding entry. {e}")
        return key

    def delete(self, key: str):
        """Delete an entry from the database."""
        try :
            del self.entries[key]
        except Exception as e:
            raise Exception(f"Key not found. {e}")
    
    def get(self, key: str):
        """Get an entry from the database."""
        try:
            return self.entries[key]
        except Exception as e:
            raise Exception(f"Key not found. {e}")
    
    def update(self, key: str, data: str):
        """Update an entry in the database."""
        try:
            assert key in self.entries
            entry = Entry(data)
            self.entries[key] = entry
        except AssertionError as e:
            raise Exception(f"Key not found. {e}")
        except Exception as e:
            raise Exception(f"Error updating entry. {e}")
    
    def search(self, text: str):
        """Check the database for the closest match to the given text."""
        try:
            keys = []
            scores = []
            for key in self.entries:
                entry = self.entries[key]
                score = entry.compare(text, iterations=self.iterations)
                keys.append(key)
                scores.append(score)
            scores = deviation_scores(scores)
            scores, keys = zip(*sorted(zip(scores, keys), reverse=True)) #sort the scores and keys in descending order.
            score_map = {key: score for key, score in zip(keys, scores)}
            return score_map
        except Exception as e:
            raise Exception(f"Error searching database. {e}")
    
    def save(self):
        """Save the database to disk."""
        #TODO: Add iterations and weights to the save file.
        try:
            with open(self.save_path, "w") as f:
                json.dump(self.entries, f)
        except Exception as e:
            raise Exception(f"Error saving database. {e}")
    
    def load(self):
        """Load the database from disk."""
        #TODO: Add iterations and weights to the save file.
        try:
            with open(self.save_path, "r") as f:
                self.entries = json.load(f)
        except Exception as e:
            raise Exception(f"Error loading database. {e}")
