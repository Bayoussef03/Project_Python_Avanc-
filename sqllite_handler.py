import sqlite3
import os
import json
import matplotlib.pyplot as plt


class SQLiteHandler:
    def __init__(self, db_file):
        self.abs_path = os.path.dirname(os.path.abspath(__file__))
        self.json_db_path = f"{self.abs_path}/resources/nfl.json"
        self.db_file = db_file
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            self.connection = sqlite3.connect(self.db_file)
            self.cursor = self.connection.cursor()
            print(f"Connected to {self.db_file}")
        except sqlite3.Error as e:
            print(f"Error connecting to the database: {e}")

    def db_exist(self):
        return os.path.exists(self.db_file) and os.stat(self.db_file).st_size > 0

    def create_and_save_database(self):
        if self.db_exist():
            return "La base de données existe déjà!"
        else:
            with open(self.json_db_path, "r") as file:
                data = json.load(file)
            self.connect()
            conn = self.connection
            self.cursor.execute(
                """
            CREATE TABLE IF NOT EXISTS joueurs (
                player_id INTEGER PRIMARY KEY,
                name TEXT,
                position TEXT,
                height TEXT,
                weight TEXT,
                current_team TEXT,
                birth_date TEXT,
                draft_position TEXT,
                current_salary TEXT
            )
            """
            )

            self.cursor.execute("SELECT COUNT(*) FROM joueurs")
            data_exists = self.cursor.fetchone()[0] > 0

            if not data_exists:
                for entry in data:
                    self.cursor.execute(
                        """
                    INSERT INTO joueurs (
                        player_id,
                        name,
                        position,
                        height,
                        weight,
                        current_team,
                        birth_date,
                        draft_position,
                        current_salary
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                        (
                            entry["player_id"],
                            entry["name"],
                            entry["position"],
                            entry["height"],
                            entry["weight"],
                            entry["current_team"],
                            entry["birth_date"],
                            entry["draft_position"],
                            entry["current_salary"],
                        ),
                    )

            conn.commit()

            conn.close()
            return "La base de données a été téléchargée avec succès!"

    def delete_database(self):
        if self.db_exist():
            os.remove(self.db_file)
            return "Base de données supprimée avec succès!"
        else:
            return "La base de données n'existe pas!"

    def calculate_salary_stats(self):
        self.connect()
        conn = self.connection
        self.cursor.execute(
            "SELECT current_salary FROM joueurs WHERE current_salary IS NOT NULL"
        )
        salaries = [float(row[0].replace(",", "")) for row in self.cursor.fetchall()]

        total_salary = sum(salaries)
        average_salary = total_salary / len(salaries) if len(salaries) > 0 else 0
        min_salary = min(salaries) if len(salaries) > 0 else 0
        max_salary = max(salaries) if len(salaries) > 0 else 0
        conn.close()
        return average_salary, min_salary, max_salary

    def display_salary_stats(self):
        average, minimum, maximum = self.calculate_salary_stats()
        return f"Salaire moyen: {average}, Salaire minimal: {minimum}, Salaire maximal: {maximum}"

    def display_salary_chart(self):
        average, minimum, maximum = self.calculate_salary_stats()

        labels = ["Salaire moyen", "Salaire minimal", "Salaire maximal"]
        values = [average, minimum, maximum]
        fig, ax = plt.subplots(figsize=(10, 8))
        bars = ax.bar(labels, values, color=["orange", "red", "green"])

        plt.xlabel("Statistique sur les salaires")
        plt.ylabel("Valeur (en dollars)")
        plt.title("Statistiques sur les salaires")
        plt.ylim(bottom=0)
        plt.grid(True)
        for bar, value in zip(bars, values):
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                height,
                f"{value:.2f}",
                ha="center",
                va="bottom",
            )
        plt.show()

    def display_salary_pie_chart(self):
        average, minimum, maximum = self.scalculate_salary_stats()

        labels = ["Moyenne", "Salaire minimal", "Salaire maximal"]
        values = [average, minimum, maximum]

        plt.figure(figsize=(8, 8))
        plt.pie(
            values,
            labels=labels,
            autopct="%1.1f%%",
            colors=["orange", "green", "red"],
            startangle=140,
        )
        plt.title("Statistiques sur les salaires")
        plt.show()

    def count_players_by_position(self):
        self.connect()
        conn = self.connection
        self.cursor.execute(f"SELECT position, COUNT(*) from joueurs GROUP BY position")
        count = self.cursor.fetchall()
        conn.close()
        conn.close()

        return count

    def minmax_players_by_position(self):
        dict_positions = self.count_players_by_position()
        max_position = max(dict_positions, key=lambda x: x[1])
        min_position = min(dict_positions, key=lambda x: x[1])

        return f"La position occupé par le minimum de joueur est {min_position[0]} à {min_position[1]} joueurs. La plus populaire est {max_position[0]}, avec {max_position[1]}"

    def player_by_height(self):
        position = "DB"
        self.connect()
        conn = self.connection

        self.cursor.execute(
            "SELECT height, COUNT(*) FROM joueurs WHERE position = ? AND height IS NOT NULL GROUP BY height",
            (position,),
        )
        data = self.cursor.fetchall()

        return data

    def player_by_height_chat(self):
        heights = [entry[0] for entry in self.player_by_height()]
        counts = [entry[1] for entry in self.player_by_height()]

        plt.figure(figsize=(8, 5))
        plt.bar(heights, counts, color="purple")
        plt.xlabel("taille des joueurs DB")
        plt.ylabel("Nombre de joueurs")
        plt.title("Nombre de joueurs DB par taille")
        plt.grid(True)
        plt.show()

    def display_player_by_height(self):
        data = self.player_by_height()

        if not data:
            return "Aucun résultat trouvé pour les joueurs DB par taille."

        result_text = "Tailles des joueurs DB (Defensive end):\n"
        for entry in data:
            result_text += f"Taille: {entry[0]}, Nombre de joueurs: {entry[1]}\n"

        return result_text

    def close_connection(self):
        if self.connection:
            self.connection.close()
            print("Connection closed")
