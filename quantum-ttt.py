import random

class QuantumTicTacToe:
    def __init__(self):
        self.board = [None] * 9  # Represents the 9 squares on the board for classical particles (X, O)
        self.entanglements = {}  # Stores entanglements: box_index -> [entangled_box1, entangled_box2, ...]
        self.placed_particles = [] # Stores (player_lowercase, (box1, box2)) for each placed quantum particle
        self.current_player = 'X' # Tracks the current player (X or O) for placing quantum particles
        self.game_over = False
        self.winner = None

    def display_board(self):
        print("\nQuantum Tic-Tac-Toe Board:")
        for i in range(9):
            if self.board[i]:
                # Display classical particles in uppercase
                print(f"[{self.board[i].upper()}]", end="")
            else:
                # Display entangled particles in lowercase
                display_content = ""
                for player_lc, entangled_boxes in self.placed_particles:
                    if i in entangled_boxes:
                        display_content += player_lc.lower() # Use lowercase for entangled particles
                if display_content:
                    print(f"[{display_content}]", end="")
                else:
                    print(f"[{i}]", end="") # Show index if empty
            if (i + 1) % 3 == 0:
                print()
        print("\nEntanglements:")
        if not self.entanglements:
            print("  No entanglements yet.")
        for box in sorted(self.entanglements.keys()):
            entangled_with_boxes = sorted(self.entanglements[box])
            if entangled_with_boxes:
                print(f"  Box {box} entangled with: {entangled_with_boxes}")

    def place_particle(self, box1, box2):
        if not (0 <= box1 < 9 and 0 <= box2 < 9):
            print("Invalid box numbers. Please choose between 0 and 8.")
            return False
        if box1 == box2:
            print("Boxes must be different.")
            return False

        # Check if either box is already occupied by a classical particle
        if self.board[box1] is not None:
            print(f"Box {box1} is already occupied by a classical '{self.board[box1]}'. Cannot place an entangled particle here.")
            return False
        if self.board[box2] is not None:
            print(f"Box {box2} is already occupied by a classical '{self.board[box2]}'. Cannot place an entangled particle here.")
            return False

        # Check if an entanglement already exists between these two specific boxes
        for _, existing_boxes in self.placed_particles:
            if tuple(sorted([box1, box2])) == existing_boxes:
                print("That entanglement already exists.")
                return False

        # Store the current player's particle (e.g., 'x' or 'o') entangled between the two boxes
        particle_boxes_tuple = tuple(sorted([box1, box2]))
        self.placed_particles.append((self.current_player.lower(), particle_boxes_tuple))

        # Add entanglements symmetrically
        self.entanglements.setdefault(box1, []).append(box2)
        self.entanglements.setdefault(box2, []).append(box1)

        print(f"{self.current_player} placed a particle entangled between boxes {box1} and {box2}.")

        if self.check_for_loop():
            print("\n!!! An entanglement loop has formed! Waveform collapse initiated. !!!")
            self.display_board()
            self.collapse_waveform()
        else:
            self.switch_player()
        return True

    def check_for_loop(self):
        visited = set()
        recursion_stack = set()

        for node in self.entanglements.keys():
            if node not in visited:
                if self._dfs_cycle_detect(node, -1, visited, recursion_stack):
                    return True
        return False

    def _dfs_cycle_detect(self, current_node, parent, visited, recursion_stack):
        visited.add(current_node)
        recursion_stack.add(current_node)

        for neighbor in self.entanglements.get(current_node, []):
            if neighbor == parent:
                continue

            if neighbor in recursion_stack:
                return True

            if neighbor not in visited:
                if self._dfs_cycle_detect(neighbor, current_node, visited, recursion_stack):
                    return True

        recursion_stack.remove(current_node)
        return False

    def collapse_waveform(self):
        last_particle_info = self.placed_particles[-1]
        last_particle_player_lowercase, last_particle_boxes = last_particle_info
        box_a, box_b = last_particle_boxes

        print(f"\nLast placed particle ({last_particle_player_lowercase.upper()} - the player who placed it): between {box_a} and {box_b}.")

        collapse_chooser = 'O' if self.current_player == 'X' else 'X'
        print(f"Player {collapse_chooser} gets to choose how the collapse unfolds!")

        print("Choose how the collapse unfolds:")
        print(f"1. {last_particle_player_lowercase.upper()}'s particle resolves to box {box_a}")
        print(f"2. {last_particle_player_lowercase.upper()}'s particle resolves to box {box_b}")

        initial_resolved_box_choice = -1 # Sentinel value
        while True:
            try:
                choice_input = input("Enter your choice (1 or 2): ")
                choice = int(choice_input)
                if choice == 1:
                    initial_resolved_box_choice = box_a
                    break
                elif choice == 2:
                    initial_resolved_box_choice = box_b
                    break
                else:
                    print("Invalid choice. Please enter 1 or 2.")
            except ValueError:
                print("Invalid input. Please enter a number.")

        # --- Core Collapse Logic ---
        # This will store the final classical positions after this collapse event.
        # We'll use a temporary dictionary to manage resolutions *within this collapse*,
        # then apply them to the main board.
        current_collapse_resolutions = {} # particle_info -> final_classical_box_index

        # The classical mark for the particle that triggered this collapse
        classical_player_mark = self.current_player.upper()

        # Step 1: Resolve the chosen particle
        # Check if the chosen box is free. If not, try the other box. If both are occupied,
        # the player's choice leads to a conflict for this particle.
        resolved_last_particle_to_box = -1
        if self.board[initial_resolved_box_choice] is None:
            resolved_last_particle_to_box = initial_resolved_box_choice
        else:
            print(f"Warning: Chosen resolution box {initial_resolved_box_choice} for {classical_player_mark} is already occupied by '{self.board[initial_resolved_box_choice]}'.")
            other_box = box_b if initial_resolved_box_choice == box_a else box_a
            if self.board[other_box] is None:
                print(f"Attempting to resolve {classical_player_mark}'s particle to its other box: {other_box}.")
                resolved_last_particle_to_box = other_box
            else:
                print(f"Both chosen boxes for {classical_player_mark}'s particle ({box_a}, {box_b}) are occupied.")
                print("This particle cannot resolve as chosen due to existing classical marks.")
                # If the triggering particle can't resolve, this collapse choice is effectively invalid
                # or leads to an incomplete collapse. For simplicity, we'll proceed without it resolving.
                # A more complex rule might force the player to choose again or declare a draw.
                pass # This particle will not be resolved in this collapse

        if resolved_last_particle_to_box != -1:
            current_collapse_resolutions[last_particle_info] = resolved_last_particle_to_box
            # Start propagation from this resolved particle
            propagation_queue = [(last_particle_info, resolved_last_particle_to_box)]
        else:
            propagation_queue = [] # No initial particle to propagate from if it couldn't resolve

        # Step 2: Propagate the collapse
        # We need a copy of placed_particles because it might change during iteration
        particles_to_process = list(self.placed_particles)

        while propagation_queue:
            current_particle_info, current_resolved_box = propagation_queue.pop(0)
            current_particle_player_lc, current_particle_boxes = current_particle_info

            # Find all other particles that were entangled with current_resolved_box
            # We iterate through all quantum particles to see if any are affected
            for other_particle_info in particles_to_process:
                # Skip if it's the same particle or already processed in this collapse
                if other_particle_info == current_particle_info or other_particle_info in current_collapse_resolutions:
                    continue

                other_player_lc, other_boxes = other_particle_info

                if current_resolved_box in other_boxes:
                    # This `other_particle` is forced out of `current_resolved_box`
                    # It must resolve to its *other* entangled box
                    forced_to_box = other_boxes[0] if other_boxes[1] == current_resolved_box else other_boxes[1]

                    # Only resolve if the target box is currently empty on the classical board
                    if self.board[forced_to_box] is None:
                        # Only resolve if not already resolved in *this* collapse event
                        if other_particle_info not in current_collapse_resolutions:
                            current_collapse_resolutions[other_particle_info] = forced_to_box
                            propagation_queue.append((other_particle_info, forced_to_box))
                    else:
                        print(f"Conflict: Quantum particle {other_player_lc.upper()} from {other_boxes} cannot resolve to box {forced_to_box} because it's already occupied by '{self.board[forced_to_box]}'.")
                        # This particle remains unresolved or might require a more complex rule.
                        # For now, it simply won't get placed.

        # Apply all resolutions from this collapse event to the main board
        for particle_info, final_box in current_collapse_resolutions.items():
            player_lc, _ = particle_info
            # Ensure the box is still empty *before* placing, as conflicts might have occurred
            # or another part of the propagation might have filled it.
            if self.board[final_box] is None:
                self.board[final_box] = player_lc.upper()
            else:
                # This should ideally not happen if propagation queue handles things correctly,
                # but it's a safeguard for complex interactions.
                print(f"Warning: Attempted to place {player_lc.upper()} in box {final_box}, but it was already occupied.")


        # After resolving particles for this collapse, remove them from placed_particles
        # We must iterate over a copy of the list or use a list comprehension
        resolved_particle_infos = current_collapse_resolutions.keys()
        self.placed_particles = [p for p in self.placed_particles if p not in resolved_particle_infos]

        # Clear entanglements for all resolved particles.
        # It's safer to rebuild `self.entanglements` only from remaining `self.placed_particles`.
        new_entanglements = {}
        for player_lc, (b1, b2) in self.placed_particles:
            new_entanglements.setdefault(b1, []).append(b2)
            new_entanglements.setdefault(b2, []).append(b1)
        self.entanglements = new_entanglements


        self.display_board()
        self.check_win()

        if not self.game_over:
            self.switch_player()

    def switch_player(self):
        self.current_player = 'O' if self.current_player == 'X' else 'X'

    def check_win(self):
        winning_combinations = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Rows
            (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Columns
            (0, 4, 8), (2, 4, 6)              # Diagonals
        ]
        for combo in winning_combinations:
            s1, s2, s3 = combo
            if self.board[s1] and self.board[s1] == self.board[s2] and self.board[s1] == self.board[s3]:
                self.winner = self.board[s1]
                self.game_over = True
                print(f"\nPlayer {self.winner} wins!")
                return
        # A draw occurs if all *classical* squares are filled and no one has won.
        if all(self.board[i] is not None for i in range(9)) and not self.game_over:
            self.game_over = True
            print("\nIt's a draw!")

    def play_game(self):
        print("Welcome to Quantum Tic-Tac-Toe!")
        print("Goal: Place your entangled particles so that, when the waveform collapses, you’re left with three in a row.")
        print("To place a particle, mark a pair of boxes (0-8) to entangle them.")
        print("When a loop forms, the waveform collapses. The player who didn't complete the loop chooses the collapse outcome.")
        print("Entangled particles are denoted by **lowercase 'x' or 'o'**, while classical (resolved) particles are denoted by **uppercase 'X' or 'O'**.")
        print("\nBoxes are numbered 0 to 8:")
        print("[0][1][2]")
        print("[3][4][5]")
        print("[6][7][8]")

        while not self.game_over:
            self.display_board()
            print(f"\nIt's Player {self.current_player}'s turn.")
            try:
                box1 = int(input("Enter first box number (0-8): "))
                box2 = int(input("Enter second box number (0-8): "))
                if not self.place_particle(box1, box2):
                    continue
            except ValueError:
                print("Invalid input. Please enter numbers.")
                continue

if __name__ == "__main__":
    game = QuantumTicTacToe()
    game.play_game()