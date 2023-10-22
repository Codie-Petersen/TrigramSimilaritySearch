from trigram.vdb import TrigramVDB

if __name__ == "__main__":
    db = TrigramVDB("data/trigram.json")
    db.add("Tadpoles love to eat algae and small insects such as mosquito larvae.")
    db.add("Cats are the most popular pet in the United States.")
    db.add("The Amazon rainforest is the largest rainforest in the world.")
    db.add("The first person on the moon was Neil Armstrong.")
    db.add("The Declaration of Independence was signed in 1776.")
    db.add("The capital of the United States is Washington, D.C.")
    db.add("The largest country in the world by area is Russia.")
    db.add("Dogs are descended from wolves.")
    db.add("The longest river in the world is the Nile.")
    db.add("American football is the most popular sport in the United States.")
    
    scores = db.search(input("Enter a sentence: "))
    keys = list(scores.keys())
    values = list(scores.values())
    
    for i in range(len(keys)):
        data = db.get(keys[i]).data
        print(f"{keys[i]}: {values[i]} | {data[:50]}...")