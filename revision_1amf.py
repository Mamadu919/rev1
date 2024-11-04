import pandas as pd
import streamlit as st

# Titre de l'application
st.title("Révision pour le Certificat AMF")

# Charger les données via un téléversement
uploaded_file = st.file_uploader("Choisissez un fichier Excel", type="xlsx")

# Si un fichier est téléversé, chargez-le
if uploaded_file is not None:
    data = pd.read_excel(uploaded_file)
    
    # Filtrer les questions par catégorie en utilisant l'index de colonne pour 'Categorie'
    category_a = data[data.iloc[:, 3] == 'A']  # Colonne d'index 3 pour la catégorie
    category_c = data[data.iloc[:, 3] == 'C']

    # Liste pour garder en mémoire les questions posées
    asked_questions = []

    # Fonction pour sélectionner des questions aléatoires
    def select_questions(category, num_questions):
        available_questions = category[~category.iloc[:, 0].isin(asked_questions)]  # Colonne d'index 0 pour 'ID question'
        if len(available_questions) < num_questions:
            st.warning("Pas assez de questions disponibles.")
            return available_questions.sample(n=len(available_questions), random_state=1)
        return available_questions.sample(n=num_questions, random_state=1)

    # Fonction pour poser les questions à l'utilisateur
    def ask_questions(questions):
        correct_count = 0
        for index, row in questions.iterrows():
            st.write(f"Question {index + 1}: {row.iloc[4]}")  # Colonne d'index 4 pour 'Question'
            st.write(f"A) {row.iloc[5]}")
            st.write(f"B) {row.iloc[6]}")
            st.write(f"C) {row.iloc[7]}")
            answer = st.radio("Votre réponse :", ["A", "B", "C"], key=f"question_{index}")
            if answer == row.iloc[8]:  # Colonne d'index 8 pour 'Bonne réponse'
                correct_count += 1
            # Ajouter l'ID de la question à la liste des questions posées
            asked_questions.append(row.iloc[0])  # Colonne d'index 0 pour 'ID question'
        return correct_count

    # Boucle principale pour réviser
    if st.button("Commencer la révision"):
        # Sélectionner les questions
        selected_a = select_questions(category_a, 33)  # 33 questions de catégorie A
        selected_c = select_questions(category_c, 87)  # 87 questions de catégorie C

        # Poser les questions à l'utilisateur
        correct_answers_a = ask_questions(selected_a)
        correct_answers_c = ask_questions(selected_c)

        # Fonction pour évaluer les résultats
        def evaluate_results(correct_a, correct_c):
            total_a = 33
            total_c = 87
            score_a = (correct_a / total_a) * 100
            score_c = (correct_c / total_c) * 100
            return score_a >= 80 and score_c >= 80

        # Afficher le résultat
        if evaluate_results(correct_answers_a, correct_answers_c):
            st.success("Vous avez réussi !")
        else:
            st.error("Vous n'avez pas réussi. Continuez à réviser.")
else:
    st.warning("Veuillez téléverser un fichier Excel pour commencer.")
