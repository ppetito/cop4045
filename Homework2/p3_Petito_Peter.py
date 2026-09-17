# Peter Petito - Homework 2
# Problem 3: Social Network

import csv
from typing import Dict, List, Tuple

SocialNetwork = Dict[str, Tuple[str, List[str]]]

def add_user(sn: SocialNetwork, username: str, fullname: str):
    """Add a new user with no friends to the sn. Return True if added, false if the username
    exists."""
    try:
        if username in sn:
            return False
        sn[username] = (fullname, [])
        return True
    except Exception as error:
        print(f"Error adding user '{username}': {error}")
        raise

def add_friend(sn: SocialNetwork, user1: str, user2: str):
    """Add a mutual friend link between user1 and user2 in sn. Return True if success, False
    otherwise."""
    try:
        if user1 not in sn or user2 not in sn:
            return False
        if user2 not in sn[user1][1]:
            sn[user1][1].append(user2)
        if user1 not in sn[user2][1]:
            sn[user2][1].append(user1)
        return True
    except Exception as error:
        print(f"Error adding friend link between '{user1}' and '{user2}': {error}")
        raise

def get_friends(sn:SocialNetwork, user1: str, distance: int):
    """Return all friends of user1 within the given link distance (BFS)"""
    try:
        if user1 not in sn:
            return []
        visited = {user1}
        current_level = [user1]
        result = []
        for _ in range(distance):
            next_level = []
            for u in current_level:
                for f in sn[u][1]:
                    if f not in visited:
                        visited.add(f)
                        next_level.append(f)
                        result.append(f)
            current_level = next_level
            if not current_level:
                break
            return result
    except Exception as error:
        print(f"Error getting friends of '{user1}': {error}")
        raise

def save_network(filename: str, sn: SocialNetwork):
    """Save a social network dictionary to a CSV file: username, fullname, semicolon-separated friends."""
    try:
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            for username, (fullname, friends) in sn.items():
                writer.writerow([username, fullname, ';'.join(friends)])
    except Exception as error:
        print(f"Error saving network to '{filename}': {error}")
        raise


def load_network(filename: str):
    """Load and return a social network dictionary from a CSV file saved with save_network()."""
    try:
        sn: SocialNetwork = {}
        with open(filename, 'r', newline='') as f:
            reader = csv.reader(f)
            for row in reader:
                username, fullname, friends_str = row
                friends = friends_str.split(';') if friends_str else []
                sn[username] = (fullname, friends)
        return sn
    except Exception as error:
        print(f"Error loading network from '{filename}': {error}")
        raise

def main():
    sn: SocialNetwork = {
        'alice': ('Alice Smith', ['maria']),
        'maria': ('Maria Cortez', ['alice', 'joe', 'david']),
        'joe': ('Joseph Adams', ['maria', 'eve']),
        'eve': ('Evelyn Cooper', ['joe']),
        'david': ('David Benson', ['maria']),
    }

    print("a) add_user:")
    print("  add new user 'frank':", add_user(sn, 'frank', 'Frank Ortiz'))
    print("  add existing user 'alice':", add_user(sn, 'alice', 'Alice Smith'))

    print("b) add_friend:")
    print("  link frank-eve:", add_friend(sn, 'frank', 'eve'))
    print("  link frank-unknown:", add_friend(sn, 'frank', 'unknown'))
    print("  sn:", sn)

    print("c) get_friends:")
    print("  alice, distance 1:", get_friends(sn, 'alice', 1))
    print("  alice, distance 2:", get_friends(sn, 'alice', 2))
    print("  unknown user:", get_friends(sn, 'nobody', 2))

    print("d)-e) save_network / load_network:")
    save_network('social_network.csv', sn)
    loaded = load_network('social_network.csv')
    print("  loaded == original:", loaded == sn)
    print("  loaded:", loaded)

if __name__ == "__main__":
    main()

