import psycopg2
import numpy as np

def identify_face(live_embedding, threshold=0.4):
    try:
        # Connect to your verified database
        conn = psycopg2.connect(
            dbname="face_recognition",
            user="postgres",
            password="x@ditix00",
            host="localhost",
            port="5432"
        )
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
            # If the vector distance is close enough, recognize them
            if distance < threshold:
                return f"✅ Match: {name} (Distance: {distance:.4f})"
            else:
                return f"❌ Unknown Person (Closest guess: {name} with distance {distance:.4f})"
        else:
            return "⚠️ Database is currently empty."

    except Exception as e:
        return f"❌ Database Query Error: {e}"

# --- Test Area ---
if __name__ == "__main__":
    print("🔄 Simulating a live camera vector search...")
    # Generate a random 512D vector to simulate a live face frame
    test_camera_vector = np.random.rand(512).tolist()
    
    match_result = identify_face(test_camera_vector)
    print(match_result)