import src
import numpy as np
import matplotlib.pyplot as plt
import math 

from PyQt6.QtWidgets import QWidget, QApplication, QVBoxLayout, QScrollArea, QSizePolicy, QLabel, QGridLayout, QTableWidget, QTableWidgetItem, QMenuBar, QDialog, QDialogButtonBox, QButtonGroup, QCheckBox, QPushButton, QComboBox, QListWidget, QFileDialog, QFormLayout, QLineEdit
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QFont, QAction, QKeySequence, QShortcut

import sys

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure


class My_Window(QWidget):
    def __init__(self, prog):
        super().__init__()
        self.setWindowTitle("Visningsprogram")
        self.prog = prog
        # Create the menu bar
        menu_bar = QMenuBar(self)
        
        # Create the File menu
        file_menu = menu_bar.addMenu('File')

        # Add actions to the File menu
        new_action = QAction('New', self)
        open_action = QAction('Open', self)
        save_action = QAction('Save', self)
        exit_action = QAction('Exit', self)

        file_menu.addAction(new_action)
        file_menu.addAction(open_action)
        file_menu.addAction(save_action)
        file_menu.addSeparator()  # Add a separator line
        file_menu.addAction(exit_action)

        # Connect the open action to the load file method
        open_action.triggered.connect(self.load_file)
        
        # Connect the exit action to the close method
        exit_action.triggered.connect(self.close)
        # Connect the new action to open the competition details dialog
        new_action.triggered.connect(self.open_competition_details_dialog)
        # Create the Edit menu
        edit_menu = menu_bar.addMenu('Edit')

        # Add actions to the Edit menu
        cut_action = QAction('Cut', self)
        copy_action = QAction('Copy', self)
        paste_action = QAction('Paste', self)

        edit_menu.addAction(cut_action)
        edit_menu.addAction(copy_action)
        edit_menu.addAction(paste_action)
        
        self.layout = QVBoxLayout(self)
        self.layout.setMenuBar(menu_bar)
        self.canvases = {}
        
        relay_menu = menu_bar.addMenu('Relay')
        
        change_relaybutton = QAction('Change Relay', self)
        
        relay_menu.addAction(change_relaybutton)
        
        change_relaybutton.triggered.connect(self.change_relay)
        
        # Create the Documents menu
        documents_menu = menu_bar.addMenu('Documents')
        create_startlist_button = QAction('Create Startlist', self)
        create_result_button = QAction('Create Result', self)
        documents_menu.addAction(create_startlist_button)
        documents_menu.addAction(create_result_button)
        create_startlist_button.triggered.connect(self.create_startlist_dialog)
        create_result_button.triggered.connect(self.create_result_dialog)
        
        # Create the Slave Mode menu
        slave_menu = menu_bar.addMenu('Slave Mode')
        toggle_slave_action = QAction('Toggle Slave Mode', self)
        slave_menu.addAction(toggle_slave_action)
        toggle_slave_action.triggered.connect(self.toggle_slave_mode)
        
        # Create the View menu for fullscreen mode
        view_menu = menu_bar.addMenu('View')
        fullscreen_action = QAction('Toggle Fullscreen', self)
        view_menu.addAction(fullscreen_action)
        fullscreen_action.triggered.connect(self.toggle_fullscreen)
        
        add_relay_action = QAction('Add Relay', self)  # New action to add relay
        relay_menu.addAction(add_relay_action)  # Add the new action to the menu
        add_relay_action.triggered.connect(self.add_relay_dialog)  # Connect action to method

        add_shooter_action = QAction("Add Shooter", self)
        add_shooter_action.triggered.connect(self.add_shooter_dialog)
        relay_menu.addAction(add_shooter_action)
        
        add_shooter_to_relay_action = QAction("Add Shooter to Relay", self)
        add_shooter_to_relay_action.triggered.connect(self.add_shooter_to_relay_dialog)
        relay_menu.addAction(add_shooter_to_relay_action)
        
        # Add the following in the Relay menu section
        remove_shot_action = QAction("Remove Shot", self)
        relay_menu.addAction(remove_shot_action)
        remove_shot_action.triggered.connect(self.open_remove_shot_dialog)
        
        # Create scoreboard table for top half
        self.scoreboard_table = QTableWidget()
        self.scoreboard_table.setColumnCount(4)  # Number of columns
        self.scoreboard_table.setHorizontalHeaderLabels(["Name", "Series Score", "Total Score", "Diff"])
        """
        # Create a placeholder widget for the top half
        self.top_placeholder = QLabel("Top Half Placeholder")
        self.top_placeholder.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        """
        # Set size policy for the table to expand horizontally
        self.scoreboard_table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
       
       # Set default column widths (adjust as needed)
        self.scoreboard_table.setColumnWidth(0, 200)  # Name column
        self.scoreboard_table.setColumnWidth(1, 100)  # Total Score column
        self.scoreboard_table.setColumnWidth(2, 400)  # Series Score colum
        self.scoreboard_table.setColumnWidth(3, 100)  # Series Score colum
       
       # Set default row height and add spacing between rows
        self.scoreboard_table.verticalHeader().setDefaultSectionSize(50)  # Adjust row height (default is 30)
       
        # Set up a QScrollArea to hold the canvases in a grid
        self.scroll_area = QScrollArea()
        self.scroll_content = QWidget()
        self.scroll_layout = QGridLayout(self.scroll_content)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.scroll_content)

         # Add both widgets to the layout with stretch factors
        self.layout.addWidget(self.scoreboard_table, 1)
        self.layout.addWidget(self.scroll_area, 1)
        self.setLayout(self.layout)  # Set the layout once during initialization
        
        self.update_scoreboard()
        self.update_canvas()  # Update canvas when initializing the window
        # Set up a QTimer to call update_canvas periodically
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_canvas)
        self.timer.timeout.connect(self.update_scoreboard)
        self.timer.start(1000)  # Update every 1000 milliseconds (1 second)
        
        self.resizeEvent = self.adjust_sizes
        self.showNormal()
    
    def open_remove_shot_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Remove Shot")

        layout = QVBoxLayout(dialog)

        # Shooter selection
        layout.addWidget(QLabel("Select Shooter:"))
        shooter_combo = QComboBox()
        for shooter in self.prog.competition.shooters.values():
            if prog.active_relay in shooter.relays.keys():
                shooter_combo.addItem(shooter.firstname + " " + shooter.lastname)
        layout.addWidget(shooter_combo)

        # Series selection
        layout.addWidget(QLabel("Select Series:"))
        series_combo = QComboBox()
        layout.addWidget(series_combo)

        # Shot selection
        layout.addWidget(QLabel("Select Shot:"))
        shot_combo = QComboBox()
        layout.addWidget(shot_combo)

        # Populate series and shot based on shooter selection
        def update_series():
            shooter_name = shooter_combo.currentText()
            shooter = next(s for s in self.prog.competition.shooters.values() if (s.firstname + " " + s.lastname) == shooter_name)
            series_combo.clear()
            for series_name in shooter.relays[self.prog.active_relay]["series"].keys():
                series_combo.addItem(series_name)
            update_shots()  # Update shots when series changes

        def update_shots():
            shooter_name = shooter_combo.currentText()
            series_name = series_combo.currentText()
            shooter = next(s for s in self.prog.competition.shooters.values() if (s.firstname + " " + s.lastname) == shooter_name)
            series = shooter.relays[self.prog.active_relay]["series"][series_name]
            shot_combo.clear()
            for shot in series.keys():
                if "Shot" in shot:
                    shot_combo.addItem(str(shot))

        shooter_combo.currentTextChanged.connect(update_series)
        series_combo.currentTextChanged.connect(update_shots)
        update_series()  # Initial population

        # Add Delete Shot button
        delete_button = QPushButton("Delete Shot")
        layout.addWidget(delete_button)

        def delete_shot():
            shooter_name = shooter_combo.currentText()
            series_name = series_combo.currentText()
            shot = shot_combo.currentText()
            shooter = next(s for s in self.prog.competition.shooters.values() if (s.firstname + " " + s.lastname) == shooter_name)
            shooter.remove_shot(self.prog.active_relay, series_name, shot)
            dialog.accept()

        delete_button.clicked.connect(delete_shot)

        dialog.setLayout(layout)
        dialog.exec()
    
    def add_shooter_to_relay_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Add Shooter to Relay")

        form_layout = QFormLayout(dialog)

        # Create a drop-down menu for selecting the shooter
        shooter_combo = QComboBox()
        for shooter in self.prog.competition.shooters.values():
            shooter_combo.addItem(shooter.firstname + " " + shooter.lastname)

        # Create a drop-down menu for selecting the relay
        relay_combo = QComboBox()
        for relay in self.prog.competition.relays.keys():
            relay_combo.addItem(relay)

        # Create input fields for discipline and league
        discipline_input = QLineEdit()
        league_input = QLineEdit()
        
        # Create optional input fields for result, inner tens, and lane
        result_input = QLineEdit()
        inner_tens_input = QLineEdit()
        lane_input = QLineEdit()

        form_layout.addRow("Shooter:", shooter_combo)
        form_layout.addRow("Relay:", relay_combo)
        form_layout.addRow("Discipline:", discipline_input)
        form_layout.addRow("League:", league_input)
        form_layout.addRow("Result (Optional):", result_input)
        form_layout.addRow("Inner Tens (Optional):", inner_tens_input)
        form_layout.addRow("Lane (Optional):", lane_input)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(lambda: self.add_shooter_to_relay(shooter_combo.currentText(), relay_combo.currentText(), discipline_input.text(), league_input.text(), result_input.text(), inner_tens_input.text(), lane_input.text(), dialog))
        buttons.rejected.connect(dialog.reject)

        form_layout.addWidget(buttons)

        dialog.exec()

    def add_shooter_to_relay(self, shooter_name, relay_name, discipline, league, result, inner_tens, lane, dialog):
        shooter = next((s for s in self.prog.competition.shooters.values() if (s.firstname + " " +  s.lastname) == shooter_name), None)
        print(shooter.firstname + " " + shooter.lastname)
        if shooter and relay_name in self.prog.competition.relays.keys():
            #relay = self.prog.competition.relays[relay_name]
            #relay.add_shooter(shooter, discipline, league, result, inner_tens, lane)
            if result == "":
                result = 0
            if inner_tens == "":
                inner_tens = 0
            self.prog.competition.add_shooter_to_relay(shooter.startnumber, discipline, league, relay_name, int(result), int(inner_tens), lane)
        dialog.accept()
    """ 
    def add_shooter_to_relay_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Add Shooter to Relay")

        form_layout = QFormLayout(dialog)

        # Create a drop-down menu for selecting the shooter
        shooter_combo = QComboBox()
        for shooter in self.prog.competition.shooters.values():
            shooter_combo.addItem(shooter.firstname + shooter.lastname)

        # Create a drop-down menu for selecting the relay
        relay_combo = QComboBox()
        for relay in self.prog.competition.relays.keys():
            relay_combo.addItem(relay)

        form_layout.addRow("Shooter:", shooter_combo)
        form_layout.addRow("Relay:", relay_combo)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(lambda: self.add_shooter_to_relay(shooter_combo.currentText(), relay_combo.currentText(), dialog))
        buttons.rejected.connect(dialog.reject)

        form_layout.addWidget(buttons)

        dialog.exec()

    def add_shooter_to_relay(self, shooter_name, relay_name, dialog):
        shooter = next((s for s in self.prog.competition.get_shooters() if s.name == shooter_name), None)
        if shooter and relay_name in self.prog.competition.relays:
            self.prog.competition.relays[relay_name].add_shooter(shooter)
        dialog.accept()
    """
    def toggle_fullscreen(self):
        if self.isFullScreen:
            self.showNormal()
        else:
            self.showFullScreen()
        self.isFullScreen = not self.isFullScreen

    
    def toggle_slave_mode(self):
        #if not hasattr(self.prog, 'competition') or not hasattr(self.prog.competition, 'slave_mode'):
         #   return  # No slave mode attribute found in prog.competition

        self.prog.slave_mode = not self.prog.slave_mode  # Toggle the slave mode

        # Optionally, you can display a message or update the UI to reflect the change in slave mode
        if self.prog.slave_mode:
            self.setWindowTitle("Visningsprogram (Slave Mode Enabled)")
        else:
            self.setWindowTitle("Visningsprogram (Slave Mode Disabled)")
            prog.setup_socket()
            prog.competition.create_import(r"C:\Sius\SiusData", False)
    
    def load_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open Competition File", "", "HDF5 Files (*.hdf5);;All Files (*)")
        if path:
            self.prog.create_competition(path)
            self.prog.competition.import_from_hdf5(path)
            self.prog.slave_mode = True
    
    def change_relay(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Change Relay")

        dialog_layout = QVBoxLayout()
        dialog.setLayout(dialog_layout)

        relay_buttons = QButtonGroup(dialog)
        relay_buttons.setExclusive(True)

        for relay in self.prog.competition.relays.keys():
            checkbox = QCheckBox(relay)
            relay_buttons.addButton(checkbox)
            dialog_layout.addWidget(checkbox)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(lambda: self.set_active_relay(dialog, relay_buttons))
        buttons.rejected.connect(dialog.reject)

        dialog_layout.addWidget(buttons)

        dialog.exec()

    def set_active_relay(self, dialog, relay_buttons):
        for button in relay_buttons.buttons():
            if button.isChecked():
                self.prog.active_relay = button.text()
                break
        dialog.accept()
    
    def create_startlist_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Create Startlist")

        dialog_layout = QVBoxLayout()
        dialog.setLayout(dialog_layout)

        relay_buttons = QButtonGroup(dialog)
        relay_buttons.setExclusive(True)

        for relay in self.prog.competition.relays.keys():
            checkbox = QCheckBox(relay)
            relay_buttons.addButton(checkbox)
            dialog_layout.addWidget(checkbox)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(lambda: self.create_startlist(dialog, relay_buttons))
        buttons.rejected.connect(dialog.reject)

        dialog_layout.addWidget(buttons)

        dialog.exec()

    def create_startlist(self, dialog, relay_buttons):
        for button in relay_buttons.buttons():
            if button.isChecked():
                path = prog.document_path + self.prog.competition.competition_name + "_startlista_" + button.text() + ".pdf"
                self.prog.competition.create_startlist(path, button.text())
                break
        dialog.accept()

    def create_result_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Create Result")

        dialog_layout = QVBoxLayout()
        dialog.setLayout(dialog_layout)

        # Create a button group for selecting "Relay" or "League"
        result_type_group = QButtonGroup(dialog)
        result_type_group.setExclusive(False)

        relay_button = QCheckBox("Relay")
        league_button = QCheckBox("League")

        result_type_group.addButton(relay_button)
        result_type_group.addButton(league_button)

        dialog_layout.addWidget(relay_button)
        dialog_layout.addWidget(league_button)

        # Create a list widget for selecting the specific relays
        list_widget = QListWidget()
        dialog_layout.addWidget(list_widget)

        def update_list_widget():
            list_widget.clear()
            if relay_button.isChecked():
                list_widget.addItems(self.prog.competition.relays.keys())
            elif league_button.isChecked():
                list_widget.addItems(self.prog.competition.leagues.keys())

        relay_button.toggled.connect(update_list_widget)
        league_button.toggled.connect(update_list_widget)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(lambda: self.create_result(dialog, list_widget, relay_button.text))
        buttons.rejected.connect(dialog.reject)

        dialog_layout.addWidget(buttons)

        dialog.exec()

    def create_result(self, dialog, list_widget, button_text):
        selected_items = []
        
        for item in list_widget.selectedItems():
            selected_items.append(item.text())
        if selected_items:
            for item in selected_items:
                if item in self.prog.competition.relays:
                    path = prog.document_path + self.prog.competition.competition_name + "_resultat_" + item + ".pdf"
                    self.prog.competition.create_result(path, "relay", item)
                elif item in self.prog.competition.leagues:
                    self.prog.create_result(league=item)
        dialog.accept()
        """ 
        for index in range(combo_box.count()):
            if combo_box.itemCheckState(index) == Qt.CheckState.Checked:
                selected_items.append(combo_box.itemText(index))
        if selected_items:
            for item in selected_items:
                if item in self.prog.competition.relays:
                    path = prog.document_path + self.prog.competition.competition_name + "_resultat_" + item + ".pdf"
                    self.prog.create_result(path, "relay" ,relay=item)
                elif item in self.prog.competition.leagues:
                    self.prog.create_result(league=item)
        dialog.accept()
        """
    def adjust_sizes(self, event):
        # Calculate font size based on window width
        window_height = self.height()
        window_width = self.width()
        font_size = window_height // 50  # Adjust divisor as needed
        
        # Calculate column widths based on window width
        col_width_name = window_width // 4  # Adjust divisor as needed
        col_width_total = window_width // 4  # Adjust divisor as needed
        col_width_series = window_width // 4  # Adjust divisor as needed
        col_width_diff = window_width // 4  # Adjust divisor as needed
        
        self.scoreboard_table.verticalHeader().setDefaultSectionSize(window_height // 19)  # Adjust row height (default is 30)
        
        # Update font for scoreboard table items
        font = QFont()
        font.setPointSize(font_size)
        self.scoreboard_table.setFont(font)
        
        # Update column widths for scoreboard table
        self.scoreboard_table.setColumnWidth(0, col_width_name)
        self.scoreboard_table.setColumnWidth(1, col_width_total)
        self.scoreboard_table.setColumnWidth(2, col_width_series)
        self.scoreboard_table.setColumnWidth(3, col_width_diff)
        """ 
        # Redraw canvas widgets (if needed)
        for canvas in self.canvases.values():
            canvas.draw()
        """
        
    def update_scoreboard(self):
        # Populate and sort scoreboard with shooter data
        try:
            relay = prog.active_relay
            scoreboard_data = []
            
            for shooter in self.prog.competition.shooters.values():
                if relay in shooter.relays:
                    score_dict = {
                        "Name": f"{shooter.firstname} {shooter.lastname}",
                        "Tot": shooter.relays[relay]["result"],
                        "NumShots": shooter.relays[relay]["num_shots"],
                        "Score": []
                    }
                    for serie in shooter.relays[relay]["series"]:
                        if "Serie" in serie:
                            score_dict["Score"].append(shooter.relays[relay]["series"][serie]["Tot"])
                    
                    # Calculate average score per shot
                    if score_dict["NumShots"] > 0:
                        score_dict["AvgScorePerShot"] = score_dict["Tot"] / score_dict["NumShots"]
                    else:
                        score_dict["AvgScorePerShot"] = 0
                    
                    scoreboard_data.append(score_dict)
            
            # Sort scoreboard data based on total score
            scoreboard_data.sort(key=lambda x: x["Tot"], reverse=True)
            
            # Calculate score differences from the top shooter
            if scoreboard_data:
                max_total_score = scoreboard_data[0]["Tot"]
                for data in scoreboard_data:
                    data["ScoreDifference"] = round(max_total_score - data["Tot"], 1)
            else:
                for data in scoreboard_data:
                    data["ScoreDifference"] = 0
            
            # Clear existing data in the scoreboard
            self.scoreboard_table.setRowCount(0)
            
            # Populate scoreboard table with sorted data
            for row_position, data in enumerate(scoreboard_data):
                self.scoreboard_table.insertRow(row_position)
                
                # Name column
                name_item = QTableWidgetItem(data["Name"])
                self.scoreboard_table.setItem(row_position, 0, name_item)
                
                # Series scores column
                series_scores_str = ", ".join(map(str, data["Score"]))
                series_scores_item = QTableWidgetItem(series_scores_str)
                self.scoreboard_table.setItem(row_position, 1, series_scores_item)
                
                # Total score column
                total_score_item = QTableWidgetItem(str(data["Tot"]))
                self.scoreboard_table.setItem(row_position, 2, total_score_item)
                
                # Score difference column
                score_diff_item = QTableWidgetItem(str(data["ScoreDifference"]))
                self.scoreboard_table.setItem(row_position, 3, score_diff_item)
            
        except Exception as e:
            print(f"Error, {e}")
    
    
    """
    def update_scoreboard(self):
        # Populate and sort scoreboard with shooter data
        try:
            relay = prog.active_relay
            scoreboard_data = []
            for shooter in self.prog.competition.shooters.values():
                if relay in shooter.relays:
                    score_dict = {
                        "Name": f"{shooter.firstname} {shooter.lastname}",
                        "Tot": shooter.relays[relay]["result"],
                        "NumShots": shooter.relays[relay]["num_shots"],
                        "Score": []
                    }
                    for serie in shooter.relays[relay]["series"]:
                        if "Serie" in serie:
                            score_dict["Score"].append(shooter.relays[relay]["series"][serie]["Tot"])
                    
                    # Calculate average score per shot
                    if score_dict["NumShots"] > 0:
                        score_dict["AvgScorePerShot"] = score_dict["Tot"] / score_dict["NumShots"]
                    else:
                        score_dict["AvgScorePerShot"] = 0
                    
                    scoreboard_data.append(score_dict)
            
            # Sort scoreboard data based on average score per shot
            scoreboard_data.sort(key=lambda x: x["AvgScorePerShot"], reverse=True)
            
            # Clear existing data in the scoreboard
            self.scoreboard_table.setRowCount(0)
            
            # Populate scoreboard table with sorted data
            for row_position, data in enumerate(scoreboard_data):
                self.scoreboard_table.insertRow(row_position)
                
                # Name column
                name_item = QTableWidgetItem(data["Name"])
                self.scoreboard_table.setItem(row_position, 0, name_item)
                
                # Series scores column (Switched with Total score)
                series_scores_str = ", ".join(map(str, data["Score"]))
                series_scores_item = QTableWidgetItem(series_scores_str)
                self.scoreboard_table.setItem(row_position, 1, series_scores_item)
                
                # Total score column (Switched with Series score)
                total_score_item = QTableWidgetItem(str(data["Tot"]))
                self.scoreboard_table.setItem(row_position, 2, total_score_item)
        except Exception as e:
            print(f"Error, {e}")
    """
    def update_canvas(self):
        try:
            if prog.slave_mode:
                statement = prog.competition.import_from_hdf5(prog.competition.hdf5path)
            else:
                statement = prog.update_competitions()
            if statement:
                #prog.update_competitions()
                #print(self.prog.competition.shooters["100"])
                relay = prog.active_relay
                row, col = 0, 0
                max_cols = math.ceil(self.prog.competition.get_number_of_shooters_in_relay(relay)/2)  # Set the maximum number of columns for the grid
                for shooter in self.prog.competition.shooters.values():  
                    if relay in shooter.relays:
                        #fig, ax = src.plot(shooter.relays[relay]["series"][shooter.active_serie])
                        score_dict = {"Name": shooter.firstname + " " + shooter.lastname, "Tot": shooter.relays[relay]["result"], "Score": []}  # Example scoreboard data
                        for serie in shooter.relays[relay]["series"]:
                            if "Serie" in serie:
                                score_dict["Score"].append(shooter.relays[relay]["series"][serie]["Tot"])
                        fig, ax = src.plot(shooter.relays[relay]["series"][shooter.active_serie], score_dict)
                        if not shooter.startnumber in self.canvases.keys():
                            canvas = FigureCanvasQTAgg(fig)
                            canvas.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
                            self.canvases[shooter.startnumber] = canvas
                            self.scroll_layout.addWidget(canvas, row, col)
                            
                            col += 1
                            if col >= max_cols:
                                col = 0
                                row += 1
                        else:
                            plt.close(self.canvases[shooter.startnumber].figure)
                            self.canvases[shooter.startnumber].figure = fig
                            self.canvases[shooter.startnumber].draw()
                            #self.canvas.draw()
                #print(self.prog.competition.shooters)
                
                self.scroll_content.setLayout(self.scroll_layout)
                self.scroll_content.updateGeometry()
                self.scroll_content.adjustSize()
        except Exception as e:
            print(f"Exception: {e}")
            
    def open_competition_details_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Enter Competition Details")

        form_layout = QFormLayout()

        name_input = QLineEdit()
        date_input = QLineEdit()
        host_input = QLineEdit()
        discipline_input = QLineEdit()
        first_lane_input = QLineEdit()
        last_lane_input = QLineEdit()
        logo_pic_input = QLineEdit()
        sponsor_pic_input = QLineEdit()
        hdf5_directory_input = QLineEdit()

        form_layout.addRow("Competition Name:", name_input)
        form_layout.addRow("Date:", date_input)
        form_layout.addRow("Host:", host_input)
        form_layout.addRow("Discipline:", discipline_input)
        form_layout.addRow("First Lane:", first_lane_input)
        form_layout.addRow("Last Lane:", last_lane_input)
        form_layout.addRow("Logo Pic:", logo_pic_input)
        form_layout.addRow("Sponsor Pic:", sponsor_pic_input)
        form_layout.addRow("HDF5 Directory:", hdf5_directory_input)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(lambda: self.save_competition_details(
            name_input.text(),
            date_input.text(),
            host_input.text(),
            discipline_input.text(),
            first_lane_input.text(),
            last_lane_input.text(),
            logo_pic_input.text(),
            sponsor_pic_input.text(),
            hdf5_directory_input.text(),
            dialog
        ))
        buttons.rejected.connect(dialog.reject)

        form_layout.addWidget(buttons)
        dialog.setLayout(form_layout)

        dialog.exec()

    def save_competition_details(self, name, date, host, discipline, first_lane, last_lane, logo_pic, sponsor_pic, hdf5_directory, dialog):
        # Here you can add your logic to save these details to your program
        print(f"Competition Name: {name}")
        print(f"Date: {date}")
        print(f"Host: {host}")
        print(f"Discipline: {discipline}")
        print(f"First Lane: {first_lane}")
        print(f"Last Lane: {last_lane}")
        print(f"Logo Pic: {logo_pic}")
        print(f"Sponsor Pic: {sponsor_pic}")
        print(f"HDF5 Directory: {hdf5_directory}")

        # Assuming prog has a method to set competition details
        self.prog.create_competition(name, date, host, discipline, first_lane, last_lane, logo_pic, sponsor_pic, hdf5_directory, just_load = False)
        
        dialog.accept()
        
    def add_relay_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Add Relay")

        form_layout = QFormLayout()

        relay_name_input = QLineEdit()
        time_input = QLineEdit()  # Adjust this input type as per your application's logic

        form_layout.addRow("Relay Name:", relay_name_input)
        form_layout.addRow("Time:", time_input)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(lambda: self.add_relay(
            relay_name_input.text(),
            time_input.text(),
            dialog
        ))
        buttons.rejected.connect(dialog.reject)

        form_layout.addWidget(buttons)
        dialog.setLayout(form_layout)

        dialog.exec()

    def add_relay(self, relay_name, time, dialog):
        # Implement your logic to add a relay here
        print(f"Adding relay: {relay_name} with time: {time}")

        # Assuming prog has a method to add relays
        self.prog.competition.add_relay(time, relay_name)

        dialog.accept()
    
    def add_shooter_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Add Shooter")

        form_layout = QFormLayout()

        shooter_first_name_input = QLineEdit()
        shooter_last_name_input = QLineEdit()
        shooter_team_input = QLineEdit()  # Adjust this input type as per your application's logic
        
        form_layout.addRow("Shooter firstname:", shooter_first_name_input)
        form_layout.addRow("Shooter lastname:", shooter_last_name_input)
        form_layout.addRow("Team:", shooter_team_input)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(lambda: self.add_shooter(
            shooter_first_name_input.text(),
            shooter_last_name_input.text(),
            shooter_team_input.text(),
            dialog
        ))
        buttons.rejected.connect(dialog.reject)

        form_layout.addWidget(buttons)
        dialog.setLayout(form_layout)

        dialog.exec()

    def add_shooter(self, shooter_first_name, shooter_last_name, team, dialog):
        # Implement your logic to add a shooter here
        print(f"Adding shooter: {shooter_first_name} {shooter_last_name} to team: {team}")

        # Assuming prog has a method to add shooters
        self.prog.competition.add_shooter(shooter_first_name, shooter_last_name, team)
        self.prog.competition.number_of_shooters += 1

        dialog.accept()
        
        


if __name__ == "__main__":
    logopic = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSMCeGz4Xab3Rxzhs8Hl3bBU9Iafs8FX4PIHg&s"
    sponsorpic = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSvI9l2PnRlWMs5wbvUc-HDNSE7FXth9p83Rg&s"
    
    prog = src.Program()
    app = QApplication(sys.argv)
    window = My_Window(prog)
    window.show()
    
    sys.exit(app.exec())
    #prog.create_competition("Dubbeltest Juli 2024", "20/7-2024", "Nyköpings Skyttegille", 
    #                       "FR60PR", "6", "20", logopic, sponsorpic, "competitions")
    #prog.competition.add_relay("10:00", "")
    #prog.competition.add_relay("12:00", "")
    #
    #prog.competition.add_shooter("Emil", "Alakulju", "Nyköpings Skyttegille",)
    #prog.competition.add_shooter_to_relay("100", "FR60PR", "Herr", 0, 0, "1")
    #prog.competition.add_shooter_to_relay("100", "FR60PR", "Herr", 0, 0, "2")
    #
    #prog.competition.add_shooter("Erik", "Alakulju", "Södermalm och Liljeholmens Skytteförening")
    #prog.competition.add_shooter("Alexander", "Devell", "Nyköping")
    #prog.competition.add_shooter("Testshooter 1", "Lastname", "Nyköping")
    #prog.competition.add_shooter("Testshooter 2", "Lastname", "Nyköping")
    #prog.competition.add_shooter("Testshooter 3", "Lastname", "Nyköping")
    #prog.competition.add_shooter("Testshooter 4", "Lastname", "Nyköping")
    #prog.competition.add_shooter("Testshooter 5", "Lastname", "Nyköping")
    #
    #prog.competition.add_shooter_to_relay("100", "FR60PR", "Herr", 0, 0, "1")
    #prog.competition.add_shooter_to_relay("100", "FR60PR", "Herr", 0, 0, "2")
    #prog.competition.add_shooter_to_relay("101", "FR60PR", "Herr", 0, 0, "1")
    #prog.competition.add_shooter_to_relay("101", "FR60PR", "Herr", 0, 0, "2")
    #prog.competition.add_shooter_to_relay("102", "FR60PR", "HJ", 0, 0, "1")
    #prog.competition.add_shooter_to_relay("102", "FR60PR", "HJ", 0, 0, "2")
    #prog.competition.add_shooter_to_relay("103", "FR60PR", "Herr", 0, 0, "1")
    #prog.competition.add_shooter_to_relay("104", "FR60PR", "Herr", 0, 0, "1")
    #prog.competition.add_shooter_to_relay("105", "FR60PR", "Herr", 0, 0, "1")
    #prog.competition.add_shooter_to_relay("106", "FR60PR", "Herr", 0, 0, "1")
    #prog.competition.add_shooter_to_relay("107", "FR60PR", "Herr", 0, 0, "1")
    #
    #
    #prog.competition.create_import(r"C:\Sius\SiusData", False)
    #prog.setup_socket()
    
    #prog.create_competition()
    #prog.competition.import_from_hdf5(r"/home/emil/privata_proj/viewerprogram/competitions/Koxängtest.hdf5")
    #prog.competition.export_to_hdf5()
    #prog.competition.create_result("restest.pdf", "relay", "1")    
    
    #comp = src.competition()
    #comp.import_from_hdf5(r"C:\Users\emila\OneDrive - Linköpings universitet\Desktop\Nya skytteprogrammet\viewerprogram\competitions\Dubbeltest Juli 2024_old.hdf5")
    #   print("Test: ")
    #comp.export_to_hdf5()
    
    
    
    #prog.competition.shooters["100"]["1"]["series"][prog.competition.shooters["100"].active_serie]
    
    #window.update_canvas()
    
    while True:
        prog.competition.import_from_hdf5("competitions/Koxängtest.hdf5")
        #prog.competition.export_to_hdf5()
        for shooter in prog.competition.shooters.values(): 
            fig, ax = src.plot(shooter.relays["1"]["series"][shooter.active_serie])
            
            window.canvas = FigureCanvasQTAgg(fig)
        
        input("\nType Ctrl+C to exit. Press Enter to continue...")
        
        sys.exit(app.exec_())
    
    
    
    