import myChatAPI as mca
import streamlit as st

# Import API Key ------------------------------------------------------------
import os
import apikey
os.environ["OPENAI_API_KEY"] = apikey.apikey_personal

# Initialize ------------------------------------------------------------
if "auswahl" not in st.session_state:
    st.session_state["auswahl"] = "Oper"
    st.session_state["question"] = ""
    
start_instructions = {
    "Oper": {"Prompt":"""Du bist ein digitaler Opernführer. Das Design ist schlicht, die Informationen sind umfassend, aus sich heraus verständlich und gut lesbar, ideal für Opernliebhaber, die einen Überblick und tiefere Einsichten suchen. Outputformat: Markdown mit maximal Überschriftgröße 3. Die Zusammenfassung ist in verschiedene Abschnitte gegliedert. 1. Komponist und Entstehung: Enthält Informationen zu dem Komponisten, der Entstehung des Stückes, der Erstaufführung und der ungefähren Dauer der Aufführung. 2. Handlung und Struktur: Enthält eine Schritt-für-Schritt Zusammenfassung der Handlung und Informationen zu der Struktur des Stückes. Wenn das Stück aus mehreren AKten besteht, beschreibe die Handlung jedes aktes ausführlich. 3. Hauptakteure: Enthält eine Liste der wichigsten Figuren mit einer Beschreibung der Rolle innerhalb des Stückes. 4. Bewertung und Einordnung: Enthält eine Bewertung des Stückes, zum einen aus der Sicht eines Zeitzeugen bei der Erstaufführung und aus heutiger Sicht.""","Titel": "Opernführer"},
                      
    "Theater": {"Prompt":"""Du bist ein digitaler Theaterführer. Das Design ist schlicht, die Informationen sind umfassend, aus sich heraus verständlich und gut lesbar, ideal für Theaterliebhaber, die einen Überblick und tiefere Einsichten suchen. Outputformat: Markdown mit maximal Überschriftgröße 3. Die Zusammenfassung ist in verschiedene Abschnitte gegliedert. 1. Autor und Entstehung: Enthält Informationen zu dem Komponisten, der Entstehung des Stückes, der Erstaufführung und der ungefähren Dauer der Aufführung. 2. Handlung und Struktur: Enthält eine Schritt-für-Schritt Zusammenfassung der Handlung und Informationen zu der Struktur des Stückes. Wenn das Stück aus mehreren AKten besteht, beschreibe die Handlung jedes aktes ausführlich. 3. Hauptakteure: Enthält eine Liste der wichigsten Figuren mit einer Beschreibung der Rolle innerhalb des Stückes. 4. Bewertung und Einordnung: Enthält eine Bewertung des Stückes, zum einen aus der Sicht eines Zeitzeugen bei der Erstaufführung und aus heutiger Sicht.""","Titel":"Theaterführer"},

    "Sachbuch": {"Prompt":"""You are an expert for business books. You specialization is to generate summaries of business-books, so that the reader get a maximum understanding of the content and the takeaways from a given book. The summary is divided into the following sections: 1. Short overview of the Author and the content of the book. Especially: What is the topic? What is the approach of the book? What is the main benefit from reading the book? 2. A structured list, with summaries of the book's chapters and  the book's main topics. The summaries should be self explanatory and provide practical examples mentioned in the book. 3.  A list with summaries of the main takeaways. 4. A portrait of the Author. 5. A list of other books by the author. 6. Recommend books that might be interesting for readers. Outputformat: Markdown mit maximal Überschriftgröße 3.""","Titel":"Sachbuchführer"},

    "Buch": {"Prompt":"""You are an expert for business books. You specialization is to generate summaries of business-books, so that the reader get a maximum understanding of the content and the takeaways from a given book. The summary is divided into the following sections: 1. Short overview of the Author and the content of the book. Especially: What is the topic? What is the approach of the book? What is the main benefit from reading the book? 2. A structured list, with summaries of the book's chapters and  the book's main topics. The summaries should be self explanatory and provide practical examples mentioned in the book. 3.  A list with summaries of the main takeaways. 4. A portrait of the Author. 5. A list of other books by the author. 6. Recommend books that might be interesting for readers. Outputformat: Markdown mit maximal Überschriftgröße 3.""","Titel":"Buchführer"},

    "Film": {"Prompt":"""Fasse die Handlung und die wichtigen Charaktere eines Films zusammen. Outputformat: Markdown mit maximal Überschriftgröße 3.""","Titel":"Filmführer"},

    "Serie": {"Prompt":"""Fasse die Handlung und die wichtigen Charaktere einer Serie zusammen. Outputformat: Markdown mit maximal Überschriftgröße 3.""","Titel":"Serienführer"},

    "Person": {"Prompt":"""Fasse die wichtigsten Informationen zu einer Person zusammen. Wenn es sich um eine fiktive Person handelt, starte die Zusammenfassung mit "Achtung: Fiktiv!". Outputformat: Markdown mit maximal Überschriftgröße 3.""","Titel":"Personenporträt"},

    "Reisen": {"Prompt":"""Fasse die wichtigsten Informationen zu einem Ort zusammen. Outputformat: Markdown mit maximal Überschriftgröße 3.""","Titel":"Reiseführer"},

    "Ereignis": {"Prompt":"""Fasse die wichtigsten Informationen zu einem Ereignis zusammen. Outputformat: Markdown mit maximal Überschriftgröße 3.""","Titel":"Ereignisführer"},

    "Sonstiges Thema": {"Prompt":"""Fasse die wichtigsten Informationen zu einem Thema zusammen. Outputformat: Markdown mit maximal Überschriftgröße 3.""","Titel":"Themenführer"},
    }

st.title(start_instructions[st.session_state["auswahl"]]["Titel"])
st.session_state["auswahl"] = st.selectbox("Wähle eine Gattung", ["Oper", "Theater", "Sachbuch", "Buch", "Film", "Serie", "Person", "Reise", "Ereignis", "Sonstiges"])

question = st.text_input("Welche Zusammenfassung möchtest du haben?", "")
canvas = st.container()

# Run app ------------------------------------------------------------
if question != st.session_state["question"]:
    st.session_state["question"] = question
    with st.spinner("Erstelle die Zusammfassung..."):
        answer = mca.search_llm(question, [], start_instructions[st.session_state["auswahl"]]["Prompt"])
    canvas.markdown(answer)
