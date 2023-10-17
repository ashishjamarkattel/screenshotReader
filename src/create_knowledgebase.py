"Create a knowledge base from title and description"

import os
import numpy as np

def check_faiss_import():
    """Import faiss if available, otherwise raise error."""
    try:
        import faiss
    except ImportError:
        raise ValueError(
            "Could not import faiss python package. "
            "Please it install it with `pip install faiss` "
            "or `pip install faiss-cpu` (depending on Python version)."
        )
    return faiss


def check_sentencepiece_import(embedding_model_name: str = 'all-MiniLM-L6-v2'):
    """
    Import sentencepiece and download the model if available,
    otherwise, raise import error
    """
    try:
        from sentence_transformers import SentenceTransformer

        embedding_model = SentenceTransformer(embedding_model_name)
    except ImportError:
        raise ImportError(
            "Could not import sentence_transformer python package. "
            "Please it install it with `pip install sentence-transformers`(depending on Python version)."
        )
    return embedding_model



class FAISS:
    """Construct Faiss wrapper for the title and description

        This class contain following functionality:

                1. store the title and description
                2. Search for the relevant tilte and description
                3. Save the title and description corresponding to user

    """
    def __init__(
            self,
            title_desc_json,
            title_desc_vector,
            title_desc
    ):
        self.title_desc_json = title_desc_json
        self.title_dec_vector = title_desc_vector
        self.title_desc = title_desc
        self.faiss_idx_store_folder = "../faiss_idx"

    @classmethod
    def embed_document(
            cls,
            title_desc_json,
            **kwargs
    ):
        """"Method embedded the title and description"""

        embedding_model = check_sentencepiece_import()

        title = title_desc_json["title"]
        description = title_desc_json["description"]
        title_desc = title + "##description" + description
        title_desc_vector = embedding_model.encode(title_desc)

        return cls(title_desc_json, title_desc_vector.tolist(), title_desc)
    
    def add_vector_to_faiss(
            self,
            unique_user_id
    ):
        """Add vector of title and description to Faiss"""

        try:
            import pandas as pd
        except ImportError:
            raise ImportError(
                "Pandas not found as module,"
                "Please install it with `pip install pandas`"
            )


        faiss = check_faiss_import()
        user_faiss_index_file_name = f"../faiss_idx/{unique_user_id}.idx"
        user_csv_file_name = f"../faiss_idx/{unique_user_id}.csv"

        if not os.path.isfile(user_faiss_index_file_name):
            index = faiss.IndexFlatL2(384) 
            index = faiss.IndexIDMap(index)
            embeddings = np.array([self.title_dec_vector]).astype('float32')
            ids = np.array([1], dtype='int64')
            index.add_with_ids(embeddings, ids)
            new_text_desc_row = {
                "text": self.title_desc
            }
            user_df = pd.DataFrame(columns=["text"])  ##create a new panda dataframe
            user_df.loc[len(user_df)] = new_text_desc_row

            user_df.to_csv(user_csv_file_name, index=False)  ##save the dataframe
            faiss.write_index(index, user_faiss_index_file_name)    ##save the faiss index file


        else:
            index = faiss.read_index(user_faiss_index_file_name)
            embeddings = np.array([self.title_dec_vector]).astype('float32')
            ids = index.ntotal + 1
            new_text_desc_row = {
                "text": self.title_desc
            }
            user_df = pd.read_csv(user_csv_file_name)
            user_df.loc[len(user_df)] = new_text_desc_row

            user_df.to_csv(user_csv_file_name, index=False)
            index.add_with_ids(embeddings, ids)

    @staticmethod
    def similarity_search(
            query: str,
            unique_user_id: str,
            k: int = 1    
    ):
        "Search for tile, description most similar to query."


        try:
            import pandas as pd
        except ImportError:
            raise ImportError(
                "Pandas not found as module,"
                "Please install it with `pip install pandas`"
            )
        

        embedding_model = check_sentencepiece_import()
        faiss = check_faiss_import()

        query_vector = embedding_model.encode(query)
        embedding = np.array([query_vector]).astype('float32')

        ##load the faiss and dataframe
        user_faiss_index_file_name = f"../faiss_idx/{unique_user_id}.idx"
        user_csv_file_name = f"../faiss_idx/{unique_user_id}.csv"
        user_index = faiss.read_index(user_faiss_index_file_name)
        user_csv = pd.read_csv(user_csv_file_name)

        ## search the query in the faiss index
        distances, index = user_index.search(embedding, k)
        value_stored = user_csv.iloc[index[0][0]]["text"]
        return value_stored
        



## usages        
if __name__ == "__main__":

#     json = {
#     "title":"Adding two Numbers",
#     "description": "This function, add2number(a,b), takes three numbers as input and returns their sum."
# }
#     emb = CreateKnowledgeBase.embed_document(json)
#     emb.add_vector_to_faiss("1231")
      CreateKnowledgeBase.similarity_search(
          "add 2 number",
          "1231"
      )

    

    


    



