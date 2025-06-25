import tkinter as tk
from tkinter import messagebox
import math

class QuantumTicTacToe:
    def __init__(self, master, info_label, entanglement_listbox):
        self.master = master
        self.info_label = info_label
        self.entanglement_listbox = entanglement_listbox

        self.board = [None] * 9  # Classical particles (X, O)
        self.entanglements = {}  # Entanglements: box_index -> [entangled_box1, entangled_box2, ...]
        self.placed_particles = [] # (player_lowercase, (box1, box2)) for quantum particles
        self.current_player = 'X' # Current player for placing quantum particles
        self.game_over = False
        self.winner = None

        self.selected_boxes = [] # Stores two boxes selected for entanglement

        # Define colors for players and UI elements
        self.player_colors = {'X': '#0000FF', 'O': '#FF0000'} # Blue for X, Red for O (Classical)
        # Paler shades for entangled particles
        self.quantum_player_colors = {'x': '#87CEFA', 'o': '#FFA07A'} # LightSkyBlue for x, LightSalmon for o
        # Arc colors - a bit darker than quantum particle colors to stand out
        self.arc_colors = {'X': '#4169E1', 'O': '#CD5C5C'} # RoyalBlue for X arcs, IndianRed for O arcs
        self.default_bg = '#F0F0F0' # Light gray background for window/frames
        self.cell_normal_bg = '#FFFFFF' # White for normal cells
        self.cell_selected_bg = '#FFFFCC' # Light yellow for selected cells
        self.box_number_fg = 'gray' # Color for the small box numbers
        self.hover_overlay_color = '#E0E0E0' # Light gray for hover effect

        # Board dimensions
        self.cell_size = 100
        self.padding = 2 # Padding between cells
        self.board_canvas_width = (self.cell_size + self.padding * 2) * 3
        self.board_canvas_height = (self.cell_size + self.padding * 2) * 3

        self.setup_game_ui()
        self.reset_game()

    def setup_game_ui(self):
        # Create a single Canvas for the entire board drawing
        self.board_drawing_canvas = tk.Canvas(self.master, width=self.board_canvas_width, height=self.board_canvas_height,
                                             bg=self.default_bg, highlightthickness=0)
        self.board_drawing_canvas.grid(row=0, column=0, columnspan=2, pady=10, padx=10)

        # Bind click and hover events to the main drawing canvas
        self.board_drawing_canvas.bind("<Button-1>", self.on_board_click)
        self.board_drawing_canvas.bind("<Motion>", self.on_canvas_motion)
        self.board_drawing_canvas.bind("<Leave>", self.on_canvas_leave)

        # Collapse choice buttons (initially hidden)
        self.collapse_choice_frame = tk.Frame(self.master, bg=self.default_bg)
        self.collapse_choice_frame.grid(row=1, column=0, columnspan=2, pady=(0,10))
        self.collapse_choice_frame.grid_remove()

        self.choice1_button = tk.Button(self.collapse_choice_frame, text="", font=("Arial", 12, "bold"),
                                         bg="#E0FFFF", relief=tk.FLAT, command=lambda: self.make_collapse_choice(1))
        self.choice1_button.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5, pady=5)

        self.choice2_button = tk.Button(self.collapse_choice_frame, text="", font=("Arial", 12, "bold"),
                                         bg="#FFE4E1", relief=tk.FLAT, command=lambda: self.make_collapse_choice(2))
        self.choice2_button.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5, pady=5)

        # Reset button
        reset_button = tk.Button(self.master, text="Reset Game", font=("Arial", 12),
                                 bg="#ADD8E6", relief=tk.FLAT, command=self.reset_game)
        reset_button.grid(row=2, column=0, columnspan=2, pady=(0,10))

        self.hovered_cell_index = -1 # To track which cell is currently hovered over

    def reset_game(self):
        self.board = [None] * 9
        self.entanglements = {}
        self.placed_particles = []
        self.current_player = 'X'
        self.game_over = False
        self.winner = None
        self.selected_boxes = []

        self.update_board_display() # This will draw all elements
        self.update_entanglement_display()
        self.update_info_label(f"Welcome! It's Player {self.current_player}'s turn. Select two boxes to entangle.")
        self.collapse_choice_frame.grid_remove()
        self.enable_board_interaction()

    # Helper to get cell coordinates and center
    def get_cell_coords(self, index):
        row = index // 3
        col = index % 3
        x1 = col * (self.cell_size + self.padding * 2) + self.padding
        y1 = row * (self.cell_size + self.padding * 2) + self.padding
        x2 = x1 + self.cell_size
        y2 = y1 + self.cell_size
        center_x = x1 + self.cell_size / 2
        center_y = y1 + self.cell_size / 2
        return (x1, y1, x2, y2, center_x, center_y)

    def update_board_display(self):
        self.board_drawing_canvas.delete("all") # Clear everything for redraw

        # --- Draw Cell Backgrounds, Numbers, and Particles ---
        for i in range(9):
            x1, y1, x2, y2, center_x, center_y = self.get_cell_coords(i)

            # Draw cell background
            bg_color = self.cell_normal_bg
            if i in self.selected_boxes:
                bg_color = self.cell_selected_bg
            self.board_drawing_canvas.create_rectangle(x1, y1, x2, y2, fill=bg_color, outline="gray", tags=f"cell_{i}")

            # Draw box number
            self.board_drawing_canvas.create_text(x2 - 8, y1 + 8, text=str(i), anchor="ne",
                               font=("Arial", 9), fill=self.box_number_fg, tags=f"cell_{i}_number")

            # Draw particle (if any)
            if self.board[i]:
                # Classical particle
                self.board_drawing_canvas.create_text(center_x, center_y,
                                   text=self.board[i].upper(), font=("Arial", 32, "bold"),
                                   fill=self.player_colors[self.board[i]], tags=f"cell_{i}_particle")
            else:
                # Quantum particle(s) or empty
                entangled_particles_in_cell = []
                for player_lc, entangled_boxes in self.placed_particles:
                    if i in entangled_boxes:
                        entangled_particles_in_cell.append(player_lc.lower())
                entangled_particles_in_cell.sort() # Sort for consistent display order (e.g., 'xo' instead of 'ox')

                if entangled_particles_in_cell:
                    # Draw each character individually for correct coloring
                    approx_char_width = 20 # Approximate width of one character in pixels for font size 32
                    total_chars = len(entangled_particles_in_cell)
                    
                    # Calculate starting X position to center the group of characters
                    start_x = center_x - (total_chars * approx_char_width / 2)
                    
                    for char_idx, char in enumerate(entangled_particles_in_cell):
                        char_color = self.quantum_player_colors[char] # Get the specific color for 'x' or 'o'
                        # Position each character relative to the start_x
                        x_pos = start_x + (char_idx * approx_char_width) + (approx_char_width / 2)
                        
                        self.board_drawing_canvas.create_text(x_pos, center_y,
                                           text=char, font=("Arial", 32, "bold"),
                                           fill=char_color, tags=f"cell_{i}_particle_part_{char_idx}")
        
        # --- Draw Entanglement Arcs (AFTER cells are drawn) ---
        drawn_entanglements = set() # To avoid drawing duplicate arcs (A-B and B-A)
        for player_lc, boxes_tuple in self.placed_particles:
            b1, b2 = boxes_tuple
            
            # Ensure we only draw each unique entanglement once
            normalized_pair = tuple(sorted((b1, b2)))
            if normalized_pair in drawn_entanglements:
                continue
            drawn_entanglements.add(normalized_pair)

            _, _, _, _, cx1, cy1 = self.get_cell_coords(b1)
            _, _, _, _, cx2, cy2 = self.get_cell_coords(b2)

            # Determine arc color based on the player who placed it
            arc_color = self.arc_colors[player_lc.upper()]

            # Calculate mid-point and offset for the arc
            mid_x = (cx1 + cx2) / 2
            mid_y = (cy1 + cy2) / 2

            # Vector between centers
            dx = cx2 - cx1
            dy = cy2 - cy1

            # Perpendicular vector (rotated 90 degrees) for offset
            # Normalize and scale for consistent offset strength
            vector_length = math.sqrt(dx**2 + dy**2)
            offset_strength = 0.2 * self.cell_size # Adjust this value for arc height
            
            if vector_length != 0:
                # Rotate the vector (dx, dy) by 90 degrees to get (-dy, dx)
                # Then scale it by offset_strength / vector_length
                offset_vec_x = -dy * (offset_strength / vector_length)
                offset_vec_y = dx * (offset_strength / vector_length)
            else: # Should not happen for two distinct boxes, but safeguard
                offset_vec_x, offset_vec_y = 0, 0

            # Control point for the arc
            arc_control_x = mid_x + offset_vec_x
            arc_control_y = mid_y + offset_vec_y

            # Create the curved line using multiple points for smoothness
            points = [cx1, cy1, arc_control_x, arc_control_y, cx2, cy2]
            
            self.board_drawing_canvas.create_line(points, smooth=True, splinesteps=20,
                                                  fill=arc_color, width=2, tags="entanglement_arc")

        # After drawing all arcs and cells, bring all cell-related tags to the front
        # This will ensure arcs are visible above background but below text/numbers
        # The previous tag_lower was indeed the issue.
        self.board_drawing_canvas.tag_raise("entanglement_arc")


    def on_canvas_motion(self, event):
        if self.game_over or self.collapse_choice_frame.winfo_ismapped():
            return
        
        # Determine which cell is currently being hovered over
        x, y = event.x, event.y
        current_hover_index = -1
        for i in range(9):
            x1, y1, x2, y2, _, _ = self.get_cell_coords(i)
            if x1 <= x < x2 and y1 <= y < y2:
                current_hover_index = i
                break

        if current_hover_index != self.hovered_cell_index:
            # Clear previous hover if any
            if self.hovered_cell_index != -1 and self.board[self.hovered_cell_index] is None:
                self.board_drawing_canvas.delete(f"hover_rect_{self.hovered_cell_index}")
            
            # Apply new hover if valid and not a classical cell
            if current_hover_index != -1 and self.board[current_hover_index] is None:
                x1, y1, x2, y2, _, _ = self.get_cell_coords(current_hover_index)
                self.board_drawing_canvas.create_rectangle(x1, y1, x2, y2,
                                                           fill=self.hover_overlay_color, stipple="gray50", outline="",
                                                           tags=f"hover_rect_{current_hover_index}")
                # Ensure hover is below numbers/particles but above cell background
                self.board_drawing_canvas.tag_lower(f"hover_rect_{current_hover_index}", f"cell_{current_hover_index}_number")
            
            self.hovered_cell_index = current_hover_index

    def on_canvas_leave(self, event):
        # Clear hover effect when mouse leaves the entire canvas
        if self.hovered_cell_index != -1:
            self.board_drawing_canvas.delete(f"hover_rect_{self.hovered_cell_index}")
        self.hovered_cell_index = -1

    def update_info_label(self, message):
        self.info_label.config(text=message)

    def update_entanglement_display(self):
        self.entanglement_listbox.delete(0, tk.END)
        self.entanglement_listbox.insert(tk.END, "--- Current Entanglements ---")
        if not self.entanglements:
            self.entanglement_listbox.insert(tk.END, "No entanglements yet.")
            return

        displayed_entanglements = set()
        for box in sorted(self.entanglements.keys()):
            for connected_box in sorted(self.entanglements[box]):
                pair = tuple(sorted((box, connected_box)))
                if pair not in displayed_entanglements:
                    particle_owner = '?'
                    for player_lc, boxes_tuple in self.placed_particles:
                        if boxes_tuple == pair:
                            particle_owner = player_lc.upper()
                            break
                    self.entanglement_listbox.insert(tk.END, f"  {particle_owner}: ({pair[0]}, {pair[1]})")
                    displayed_entanglements.add(pair)

    def on_board_click(self, event):
        # Determine which cell was clicked based on event coordinates
        x, y = event.x, event.y
        clicked_index = -1
        for i in range(9):
            x1, y1, x2, y2, _, _ = self.get_cell_coords(i)
            if x1 <= x < x2 and y1 <= y < y2:
                clicked_index = i
                break
        
        if clicked_index == -1: # Clicked outside any cell
            return

        # Rest of the logic remains similar to previous on_board_click
        if self.game_over or self.collapse_choice_frame.winfo_ismapped():
            return

        if self.board[clicked_index] is not None:
            self.update_info_label(f"Box {clicked_index} is already occupied by a classical '{self.board[clicked_index]}'. Please choose an empty box.")
            return

        if len(self.selected_boxes) < 2:
            if clicked_index in self.selected_boxes:
                self.selected_boxes.remove(clicked_index)
                self.update_board_display() # Redraw to remove selection highlight
                self.update_info_label(f"Deselected box {clicked_index}. Select two boxes to entangle.")
                return

            self.selected_boxes.append(clicked_index)
            self.update_board_display() # Redraw to show selection highlight

            if len(self.selected_boxes) == 1:
                self.update_info_label(f"Selected box {self.selected_boxes[0]}. Select a second box.")
            elif len(self.selected_boxes) == 2:
                box1, box2 = self.selected_boxes[0], self.selected_boxes[1]
                self.selected_boxes = [] # Clear selected boxes immediately for visual feedback
                if self.place_particle(box1, box2):
                    self.update_board_display()
                    self.update_entanglement_display()
                else:
                    self.update_board_display() # Update to remove selection highlights

    def place_particle(self, box1, box2):
        if box1 == box2:
            self.update_info_label("Boxes must be different.")
            return False

        for _, existing_boxes in self.placed_particles:
            if tuple(sorted([box1, box2])) == existing_boxes:
                self.update_info_label("That entanglement already exists.")
                return False

        particle_boxes_tuple = tuple(sorted([box1, box2]))
        self.placed_particles.append((self.current_player.lower(), particle_boxes_tuple))

        self.entanglements.setdefault(box1, []).append(box2)
        self.entanglements.setdefault(box2, []).append(box1)

        self.update_info_label(f"Player {self.current_player} placed a particle entangled between boxes {box1} and {box2}.")

        if self.check_for_loop():
            self.update_info_label("!!! An entanglement loop has formed! Waveform collapse initiated. !!!")
            self.initiate_collapse_choice()
        else:
            self.switch_player()
            self.update_info_label(f"It's Player {self.current_player}'s turn. Select two boxes to entangle.")
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

    def initiate_collapse_choice(self):
        self.disable_board_interaction()
        self.collapse_choice_frame.grid()

        last_particle_info = self.placed_particles[-1]
        last_particle_player_lowercase, last_particle_boxes = last_particle_info
        box_a, box_b = last_particle_boxes

        collapse_chooser = 'O' if self.current_player == 'X' else 'X'
        self.update_info_label(f"Player {collapse_chooser} chooses collapse! Last particle ({last_particle_player_lowercase.upper()}): {box_a} <-> {box_b}")

        self.choice1_button.config(text=f"Resolve {last_particle_player_lowercase.upper()} to {box_a}")
        self.choice2_button.config(text=f"Resolve {last_particle_player_lowercase.upper()} to {box_b}")

        self._collapse_info = {
            "last_particle_info": last_particle_info,
            "box_a": box_a,
            "box_b": box_b,
            "classical_player_mark": self.current_player.upper()
        }

    def make_collapse_choice(self, choice):
        self.collapse_choice_frame.grid_remove()
        self.enable_board_interaction()

        last_particle_info = self._collapse_info["last_particle_info"]
        box_a = self._collapse_info["box_a"]
        box_b = self._collapse_info["box_b"]
        classical_player_mark = self._collapse_info["classical_player_mark"]

        initial_resolved_box_choice = box_a if choice == 1 else box_b

        current_collapse_resolutions = {}
        resolved_last_particle_to_box = -1

        if self.board[initial_resolved_box_choice] is None:
            resolved_last_particle_to_box = initial_resolved_box_choice
        else:
            self.update_info_label(f"Warning: Chosen box {initial_resolved_box_choice} for {classical_player_mark} is occupied. Trying other box.")
            other_box = box_b if initial_resolved_box_choice == box_a else box_a
            if self.board[other_box] is None:
                resolved_last_particle_to_box = other_box
            else:
                self.update_info_label(f"Both chosen boxes ({box_a}, {box_b}) for {classical_player_mark}'s particle are occupied. Particle cannot resolve.")
                pass

        if resolved_last_particle_to_box != -1:
            current_collapse_resolutions[last_particle_info] = resolved_last_particle_to_box
            propagation_queue = [(last_particle_info, resolved_last_particle_to_box)]
        else:
            propagation_queue = []

        particles_to_process = list(self.placed_particles)

        while propagation_queue:
            current_particle_info, current_resolved_box = propagation_queue.pop(0)
            current_particle_player_lc, current_particle_boxes = current_particle_info

            for other_particle_info in particles_to_process:
                if other_particle_info == current_particle_info or other_particle_info in current_collapse_resolutions:
                    continue

                other_player_lc, other_boxes = other_particle_info
                classical_mark_for_other_particle = other_player_lc.upper()

                if current_resolved_box in other_boxes:
                    forced_to_box = other_boxes[0] if other_boxes[1] == current_resolved_box else other_boxes[1]

                    if other_particle_info not in current_collapse_resolutions:
                        if self.board[forced_to_box] is None:
                            current_collapse_resolutions[other_particle_info] = forced_to_box
                            propagation_queue.append((other_particle_info, forced_to_box))
                        else:
                            self.update_info_label(f"Conflict: Quantum particle {classical_mark_for_other_particle} from {other_boxes} cannot resolve to box {forced_to_box} (occupied).")
                            pass

        for particle_info, final_box in current_collapse_resolutions.items():
            player_lc, _ = particle_info
            if self.board[final_box] is None:
                self.board[final_box] = player_lc.upper()
            else:
                self.update_info_label(f"Warning: Attempted to place {player_lc.upper()} in box {final_box}, but it was already occupied.")


        resolved_particle_infos = current_collapse_resolutions.keys()
        self.placed_particles = [p for p in self.placed_particles if p not in resolved_particle_infos]

        new_entanglements = {}
        for player_lc, (b1, b2) in self.placed_particles:
            new_entanglements.setdefault(b1, []).append(b2)
            new_entanglements.setdefault(b2, []).append(b1)
        self.entanglements = new_entanglements


        self.update_board_display()
        self.update_entanglement_display()
        self.check_win()

        if not self.game_over:
            self.switch_player()
            self.update_info_label(f"Collapse complete. It's Player {self.current_player}'s turn. Select two boxes to entangle.")

    def disable_board_interaction(self):
        self.board_drawing_canvas.config(state=tk.DISABLED)

    def enable_board_interaction(self):
        if self.game_over:
            self.board_drawing_canvas.config(state=tk.DISABLED)
            return
        self.board_drawing_canvas.config(state=tk.NORMAL)

    def switch_player(self):
        self.current_player = 'O' if self.current_player == 'X' else 'X'

    def check_win(self):
        winning_combinations = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Rows
            (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Columns
            (0, 4, 8), (2, 4, 6)              # Diagonals
        ]

        x_wins = False
        o_wins = False

        for combo in winning_combinations:
            s1, s2, s3 = combo
            # Check for X win
            if self.board[s1] == 'X' and self.board[s1] == self.board[s2] and self.board[s1] == self.board[s3]:
                x_wins = True
            # Check for O win
            if self.board[s1] == 'O' and self.board[s1] == self.board[s2] and self.board[s1] == self.board[s3]:
                o_wins = True
        
        # --- New Win/Draw Logic ---
        if x_wins and o_wins:
            self.winner = "Both" # Indicate a simultaneous win for draw purposes
            self.game_over = True
            self.update_info_label("It's a draw! Both players achieved three in a row.")
            messagebox.showinfo("Game Over", "It's a draw! Both players achieved three in a row.")
        elif x_wins:
            self.winner = 'X'
            self.game_over = True
            self.update_info_label(f"Player {self.winner} wins!")
            messagebox.showinfo("Game Over", f"Player {self.winner} wins!")
        elif o_wins:
            self.winner = 'O'
            self.game_over = True
            self.update_info_label(f"Player {self.winner} wins!")
            messagebox.showinfo("Game Over", f"Player {self.winner} wins!")
        elif all(self.board[i] is not None for i in range(9)): # Standard draw if board is full
            self.game_over = True
            self.update_info_label("It's a draw! No more moves possible.")
            messagebox.showinfo("Game Over", "It's a draw! No more moves possible.")
        
        if self.game_over:
            self.disable_board_interaction() # Disable interaction once game is over




class QuantumTicTacToeGUI:
    def __init__(self, master):
        self.master = master
        master.title("Quantum Tic-Tac-Toe")
        master.geometry("520x720")
        master.resizable(False, False)
        master.config(bg="#F0F0F0") # Soft light gray background for the window

        # Info Label
        self.info_label = tk.Label(master, text="Welcome to Quantum Tic-Tac-Toe!", font=("Arial", 12, "bold"),
                                   wraplength=480, fg="#333333", bg=master["bg"])
        self.info_label.grid(row=3, column=0, columnspan=2, pady=(15, 5), padx=10, sticky="ew")

        # Entanglement Listbox
        entanglement_frame = tk.LabelFrame(master, text="Current Entanglements", font=("Arial", 10, "bold"),
                                           fg="#333333", bg=master["bg"])
        entanglement_frame.grid(row=4, column=0, columnspan=2, pady=(10, 0), padx=10, sticky="ew")

        self.entanglement_listbox = tk.Listbox(entanglement_frame, height=6, font=("Consolas", 10),
                                               bg="#FFFFFF", fg="#444444", selectbackground="#D0D0D0", selectforeground="#444444",
                                               highlightthickness=0, borderwidth=0)
        self.entanglement_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Game rules explanation
        rules_label = tk.Label(master, text="Rules: 'x'/'o' are quantum, 'X'/'O' are classical. Form a loop, then the other player chooses collapse to win! Entanglements are shown with arced lines.",
                               font=("Arial", 9, "italic"), wraplength=480, fg="#555555", bg=master["bg"])
        rules_label.grid(row=5, column=0, columnspan=2, pady=(10, 15), padx=10, sticky="ew")

        self.game = QuantumTicTacToe(master, self.info_label, self.entanglement_listbox)


if __name__ == "__main__":
    root = tk.Tk()
    app = QuantumTicTacToeGUI(root)
    root.mainloop()
