import psycopg2

def get_db_connection():
    """Manages connection details dynamically for the Docker network environment."""
    return psycopg2.connect(
        dbname="facedb",        # Matches your teammate's Docker Compose config
        user="user",            # Matches your teammate's Docker Compose config
        password="password",    # Matches your teammate's Docker Compose config
        host="postgres",        # Routes to the postgres container inside the Docker network
        port="5432"
    )

def register_new_face(name, raw_512d_vector):
    """Inserts a new identity and their 512D face vector into the database."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Step 1: Insert the name and get the auto-generated person_id
        cursor.execute(
            "INSERT INTO public.persons (name) VALUES (%s) RETURNING person_id;", 
            (name,)
        )
        person_id = cursor.fetchone()[0]

        # Step 2: Insert the vector linking it to that person_id
        cursor.execute(
            "INSERT INTO public.face_embeddings (person_id, embedding) VALUES (%s, %s::vector);",
            (person_id, raw_512d_vector)
        )

        conn.commit()
        cursor.close()
        conn.close()
        return f"✅ Successfully registered {name} (ID: {person_id})"
    except Exception as e:
        return f"❌ Registration Error: {e}"

def identify_face(live_embedding, threshold=0.4):
    """Compares a live 512D camera vector against stored vectors using HNSW Cosine Distance."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # SQL query with explicit typecast to resolve the operator error
        query = """
            SELECT p.name, (f.embedding <=> %s::vector) AS distance
            FROM public.face_embeddings f
            JOIN public.persons p ON f.person_id = p.person_id
            ORDER BY distance ASC
            LIMIT 1;
        """
        
        cursor.execute(query, (live_embedding,))
        result = cursor.fetchone()
        
        cursor.close()
        conn.close()

        if result:
            name, distance = result
            if distance < threshold:
                return f"✅ Match: {name} (Distance: {distance:.4f})"
            else:
                return f"❌ Unknown Person (Closest guess: {name} with distance {distance:.4f})"
        else:
            return "⚠️ Database is currently empty."
    except Exception as e:
        return f"❌ Database Query Error: {e}"