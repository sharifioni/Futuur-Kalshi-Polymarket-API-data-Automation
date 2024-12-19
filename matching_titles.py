import pandas as pd
from sentence_transformers import SentenceTransformer, util

# Function to find at least two similar titles using Sentence Transformers
def find_similar_titles(df1, df2, df3, threshold=0.75):
    # Load the pre-trained model
    model = SentenceTransformer('all-MiniLM-L6-v2')  # You can use other models as well

    # Extract titles from the three dataframes
    titles_1 = df1['title'].dropna().tolist()
    titles_2 = df2['title'].dropna().tolist()
    titles_3 = df3['title'].dropna().tolist()

    # Encode the titles into sentence embeddings
    embeddings_1 = model.encode(titles_1, convert_to_tensor=True)
    embeddings_2 = model.encode(titles_2, convert_to_tensor=True)
    embeddings_3 = model.encode(titles_3, convert_to_tensor=True)

    matched_data = []

    # Compare embeddings between Polymarket, Futuur, and Kalshi
    for i, embedding_1 in enumerate(embeddings_1):
        for j, embedding_2 in enumerate(embeddings_2):
            sim_1_2 = util.pytorch_cos_sim(embedding_1, embedding_2).item()
            if sim_1_2 >= threshold:
                # Match between df1 and df2, leave df3 optional
                best_match = {'Polymarket': titles_1[i], 'Futuur': titles_2[j], 'Kalshi': ''}
                for k, embedding_3 in enumerate(embeddings_3):
                    sim_1_3 = util.pytorch_cos_sim(embedding_1, embedding_3).item()
                    sim_2_3 = util.pytorch_cos_sim(embedding_2, embedding_3).item()
                    if sim_1_3 >= threshold or sim_2_3 >= threshold:
                        # All three match
                        best_match['Kalshi'] = titles_3[k]
                        break
                matched_data.append(best_match)

    # Handle case where there's a match between df1 and df3, but not df2
    for i, embedding_1 in enumerate(embeddings_1):
        for k, embedding_3 in enumerate(embeddings_3):
            sim_1_3 = util.pytorch_cos_sim(embedding_1, embedding_3).item()
            if sim_1_3 >= threshold:
                # Match between df1 and df3, leave df2 empty if not already matched
                if not any(match['Polymarket'] == titles_1[i] and match['Kalshi'] == titles_3[k] for match in matched_data):
                    matched_data.append({'Polymarket': titles_1[i], 'Futuur': '', 'Kalshi': titles_3[k]})

    # Handle case where there's a match between df2 and df3, but not df1
    for j, embedding_2 in enumerate(embeddings_2):
        for k, embedding_3 in enumerate(embeddings_3):
            sim_2_3 = util.pytorch_cos_sim(embedding_2, embedding_3).item()
            if sim_2_3 >= threshold:
                # Match between df2 and df3, leave df1 empty if not already matched
                if not any(match['Futuur'] == titles_2[j] and match['Kalshi'] == titles_3[k] for match in matched_data):
                    matched_data.append({'Polymarket': '', 'Futuur': titles_2[j], 'Kalshi': titles_3[k]})

    # Convert the matched data into a DataFrame
    matched_df = pd.DataFrame(matched_data)

    return matched_df


